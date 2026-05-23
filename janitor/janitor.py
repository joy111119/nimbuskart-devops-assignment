import argparse
import json
from datetime import datetime, timezone

import boto3

from constants import (
    REQUIRED_TAGS,
    EBS_GP3_PRICE_PER_GB,
    ELASTIC_IP_MONTHLY_COST
)


def get_ec2_client():

    return boto3.client(
        "ec2",
        region_name="us-east-1",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )


def get_tags_dict(tag_list):

    if not tag_list:
        return {}

    return {
        tag["Key"]: tag["Value"]
        for tag in tag_list
    }


def has_required_tags(tags):

    for required_tag in REQUIRED_TAGS:

        if required_tag not in tags:
            return False

    return True


def is_protected(tags):

    return (
        tags.get("Protected", "").lower()
        == "true"
    )


def scan_unattached_volumes(ec2):

    findings = []

    response = ec2.describe_volumes()

    for volume in response["Volumes"]:

        if volume["State"] == "available":

            size = volume["Size"]

            tags = get_tags_dict(
                volume.get("Tags", [])
            )

            findings.append({
                "resource_id": volume["VolumeId"],

                "resource_type": "ebs_volume",

                "reason": "unattached",

                "age_days": 0,

                "estimated_monthly_cost_usd": round(
                    size * EBS_GP3_PRICE_PER_GB,
                    2
                ),

                "tags": tags,

                "suggested_action": "delete",

                "safe_to_auto_delete": (
                    not is_protected(tags)
                )
            })

    return findings


def scan_unused_elastic_ips(ec2):

    findings = []

    response = ec2.describe_addresses()

    for address in response["Addresses"]:

        if "InstanceId" not in address:

            tags = get_tags_dict(
                address.get("Tags", [])
            )

            findings.append({
                "resource_id": address.get(
                    "AllocationId",
                    address.get("PublicIp")
                ),

                "resource_type": "elastic_ip",

                "reason": "unassociated",

                "age_days": 0,

                "estimated_monthly_cost_usd": (
                    ELASTIC_IP_MONTHLY_COST
                ),

                "tags": tags,

                "suggested_action": "release",

                "safe_to_auto_delete": (
                    not is_protected(tags)
                )
            })

    return findings


def scan_missing_tags(ec2):

    findings = []

    response = ec2.describe_volumes()

    for volume in response["Volumes"]:

        tags = get_tags_dict(
            volume.get("Tags", [])
        )

        if not has_required_tags(tags):

            findings.append({
                "resource_id": volume["VolumeId"],

                "resource_type": "ebs_volume",

                "reason": "missing_required_tags",

                "age_days": 0,

                "estimated_monthly_cost_usd": 0,

                "tags": tags,

                "suggested_action": "add_tags",

                "safe_to_auto_delete": False
            })

    return findings


def delete_resources(ec2, findings):

    for item in findings:

        if not item["safe_to_auto_delete"]:
            continue

        if item["resource_type"] == "ebs_volume":

            ec2.delete_volume(
                VolumeId=item["resource_id"]
            )

            print(
                f"Deleted volume: "
                f"{item['resource_id']}"
            )

        elif item["resource_type"] == "elastic_ip":

            ec2.release_address(
                AllocationId=item["resource_id"]
            )

            print(
                f"Released Elastic IP: "
                f"{item['resource_id']}"
            )


def generate_markdown_summary(findings):

    lines = [
        "# Cost Janitor Summary",
        ""
    ]

    if not findings:

        lines.append(
            "No orphaned resources found."
        )

        return "\n".join(lines)

    for item in findings:

        lines.extend([
            f"## {item['resource_id']}",
            f"- Type: {item['resource_type']}",
            f"- Reason: {item['reason']}",
            f"- Estimated Monthly Cost: "
            f"${item['estimated_monthly_cost_usd']}",
            f"- Suggested Action: "
            f"{item['suggested_action']}",
            ""
        ])

    return "\n".join(lines)


def generate_report(findings):

    report = {
        "scan_timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "account_id": "000000000000",

        "region": "us-east-1",

        "summary": {

            "total_orphans": len(findings),

            "estimated_monthly_waste_usd": round(
                sum(
                    item[
                        "estimated_monthly_cost_usd"
                    ]
                    for item in findings
                ),
                2
            )
        },

        "findings": findings
    }

    return report


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Scan resources without deleting"
    )

    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete orphaned resources"
    )

    args = parser.parse_args()

    if args.delete:
        args.dry_run = False

    ec2 = get_ec2_client()

    findings = []

    findings.extend(
        scan_unattached_volumes(ec2)
    )

    findings.extend(
        scan_unused_elastic_ips(ec2)
    )

    findings.extend(
        scan_missing_tags(ec2)
    )

    if args.delete:

        delete_resources(
            ec2,
            findings
        )

    report = generate_report(findings)

    markdown_summary = (
        generate_markdown_summary(
            findings
        )
    )

    with open("report.json", "w") as file:

        json.dump(
            report,
            file,
            indent=2
        )

    with open("summary.md", "w") as file:

        file.write(markdown_summary)

    print(json.dumps(report, indent=2))

    print("\n")
    print(markdown_summary)

    if findings and args.dry_run:
        exit(1)


if __name__ == "__main__":
    main()