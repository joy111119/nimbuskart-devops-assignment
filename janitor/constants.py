# Approximate monthly costs
# Sources:
# gp3 EBS pricing:
# https://aws.amazon.com/ebs/pricing/

EBS_GP3_PRICE_PER_GB = 0.08

# Small approximation for unused Elastic IP
ELASTIC_IP_MONTHLY_COST = 3.60

# Approximation for stopped t3.micro storage + attached infra
STOPPED_T3_MICRO_MONTHLY_COST = 8.00

REQUIRED_TAGS = [
    "Project",
    "Environment",
    "Owner"
]