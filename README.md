## Overview

This project automates cloud cost hygiene for NimbusKart by provisioning a local AWS-like staging environment using Terraform and LocalStack and detecting potentially wasteful resources through a Cost Janitor automation script. The solution identifies orphaned resources, missing required tags, stopped EC2 instances, and unused Elastic IPs that may unnecessarily increase cloud costs, while also supporting safe dry-run and delete workflows integrated into CI/CD using GitHub Actions.


---

## How to run locally

### 1. Clone the repository

```bash
git clone https://github.com/joy111119/nimbuskart-devops-assignment
cd nimbuskart-devops-assignment
```

### 2. Start LocalStack

```bash
docker run --rm -d -p 4566:4566 --name localstack localstack/localstack:3.5
```

### 3. Install Terraform Local wrapper

```bash
pip install terraform-local
```

### 4. Initialize Terraform

```bash
cd terraform
tflocal init
```

### 5. Apply infrastructure

```bash
tflocal apply -auto-approve
```

### 6. Validate Terraform

```bash
terraform fmt
tflocal validate
```

### 7. Run the Cost Janitor in dry-run mode

```bash
cd ../janitor
python janitor.py --dry-run
```

### 8. Run the Cost Janitor in delete mode

```bash
python janitor.py --delete
```

### 9. View generated reports

The Janitor generates:

```text
report.json
report.md
```

inside the `janitor/` directory.

### 10. Run the GitHub Actions workflow


The workflow will:

- Start LocalStack
- Apply Terraform infrastructure
- Run the Cost Janitor in `--dry-run` mode
- Upload reports as workflow artifacts
- Comment findings on pull requests
- Fail the workflow if orphaned resources are detected

## Architecture

```text
                +----------------------+
                |   GitHub Actions     |
                |  cost-janitor.yml    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |      LocalStack      |
                |  Simulated AWS APIs  |
                +----------+-----------+
                           |
        -----------------------------------------
        |                    |                  |
        v                    v                  v
+---------------+   +----------------+   +----------------+
| Terraform IaC |   |  AWS Resources |   | Cost Janitor   |
| VPC/Subnets   |   | EC2 / EBS / S3 |   | Python Script  |
+---------------+   +----------------+   +----------------+
                                                |
                                                v
                                   +------------------------+
                                   | report.json + summary |
                                   +------------------------+

---

## Decisions & deviations

- SSH access was restricted to a configurable CIDR instead of `0.0.0.0/0` because unrestricted SSH access is insecure in production environments.

- Since LocalStack has limited support for stopped EC2 instance and unattached Elastic IP simulation, the Janitor currently focuses primarily on detecting unattached EBS volumes and missing required tags.

- S3 lifecycle configuration was removed because LocalStack kept timing out even though the Terraform syntax was correct.

- A static AMI ID was used since LocalStack does not require a real EC2 image.

- As assigned, common tags were added to all supported resources to make resource tracking and cost monitoring easier.

- - For testing delete-safety logic, an additional unattached EBS volume was added with the tag `Protected=true` so the Janitor could verify that protected resources are skipped in `--delete` mode.

---

## Trade-offs
Given more time, I would improve the project by adding real CloudWatch metrics, SNS notifications, approval workflows before deletion, and support for additional orphan resource types. I would also improve testing coverage and add support for more cloud providers in the future instead of keeping the project limited to AWS resources only.
---

## AI usage disclosure

AI tools used:
- ChatGPT was used for understanding what is being done (for example code and real world examples of this project), Code generation for terraform, Terraform debugging, LocalStack troubleshooting, assisting and giving ideas in README.md and DESIGN.md, and generating the ASCII diagram. I continuously asked my doubts to ChatGPT about anything related to this project to keep myself on track as I progressed in the project.  

- I wrote the Janitor scanning logic and deletion safeguards manually because I wanted to carefully control the detection behavior and understand exactly why each resource was being flagged.

- - AI initially suggested that naming a Terraform resource `stopped_instance` would make the EC2 instance start in a stopped state. While testing the Janitor, I noticed the instance was still reported as `running` by LocalStack/AWS APIs using `describe-instances`. It then became clear to me that Terraform resource names do not affect EC2 state, and that instances must be explicitly stopped after creation.
