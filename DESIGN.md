## Multi-cloud architecture

To support GCP and Azure in the future, I would separate the Janitor into:

- A shared core engine responsible for:
  - orphan detection rules
  - report generation
  - cost estimation
  - deletion safety checks

This separation keeps the code modular and prevents the Janitor from becoming one large file containing all provider logic and cleanup rules.

- Cloud-specific provider modules:
  - providers/aws/
  - providers/gcp/
  - providers/azure/

Each provider module would manage its own cloud resources separately so the main Janitor system would not need major changes when adding new cloud providers.

This structure improves maintainability because provider SDK logic stays isolated from the main application logic. It also makes testing easier since each provider can be tested independently.

## Permissions

The Janitor should use separate IAM roles for --dry-run mode and --delete mode.

In --dry-run mode, the Janitor only needs read-only permissions to scan resources and check tags. It should not have permission to modify or delete anything.

In --delete mode, additional delete permissions would be required for resources such as EBS volumes and unused Elastic IPs.

Using separate roles follows the principle of least privilege and reduces the risk of accidental deletions.

Example minimal read-only IAM policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:DescribeAddresses",
        "ec2:DescribeSnapshots",
        "tag:GetResources"
      ],
      "Resource": "*"
    }
  ]
}
```

## Safety net

One possible failure mode is deleting an unattached EBS volume that still contains important backup or recovery data. Even though the volume is unused, deleting it immediately could result in permanent data loss.

To reduce this risk, I would:
- skip resources tagged Protected=true
- require a minimum age threshold before deletion
- use approval-based deletion for critical environments
- send alerts before destructive actions using SNS or CloudWatch notifications

Another failure mode is deleting stopped EC2 instances that are intentionally kept for disaster recovery, testing, or scheduled workloads.

To prevent accidental outages, I would:
- skip resources tagged Protected=true
- only delete resources after multiple scans confirm they are unused
- require --dry-run review before running deletion mode
- use configurable age thresholds before deletion

## Observability

I would publish Janitor metrics to CloudWatch so the FinOps team can monitor cost hygiene trends and detect failures early.

| Metric | Source | Alert Threshold |
|---|---|---|
| orphan_resources_detected_total | Janitor scan results | Alert if orphan count suddenly increases |
| estimated_monthly_waste_usd | Generated report.json | Alert if waste exceeds a defined budget |
| janitor_scan_failures_total | GitHub Actions / Janitor logs | Alert if multiple scans fail consecutively |
| resources_deleted_total | Janitor deletion logs | Alert if deletion count spikes unexpectedly |
| scan_duration_seconds | Janitor execution metrics | Alert if scans become unusually slow |

CloudWatch alarms and SNS notifications could be used to notify engineers when thresholds are exceeded.