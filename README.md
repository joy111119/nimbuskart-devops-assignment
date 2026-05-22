## Overview

This project aims to automate cloud infrastructure management for NimbusKart by helping detect inefficient or wasteful AWS resources.

The project helps optimize cloud costs by detecting orphaned resources, identifying missing tags, and finding resources that may unnecessarily increase monthly cloud bills. Terraform and LocalStack are used to provision the infrastructure locally. 

The solution provisions a staging infrastructure environment locally using Terraform and LocalStack. 


---

## How to run locally

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Start LocalStack

```bash
docker run --rm -d -p 4566:4566 --name localstack localstack/localstack
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
```4

## Architecture



---

## Decisions & deviations

- SSH access is set to `0.0.0.0/0` because it was required in the assignment, but in a real setup it should be restricted to specific IPs or a VPN.

- S3 lifecycle configuration was removed because LocalStack kept timing out even though the Terraform syntax was correct.

- A static AMI ID was used since LocalStack does not require a real EC2 image.

- As assigned, common tags were added to all supported resources to make resource tracking and cost monitoring easier.

- Variables were used for region, environment, subnet CIDRs, and project names instead of hardcoding values to make the setup easier to reuse across environments.

---

## Trade-offs


---

## AI usage disclosure

AI tools used:
- ChatGPT was used for understanding what is being done (for example code and real world examples of this project), Code generation for terraform, Terraform debugging, LocalStack troubleshooting,. 
