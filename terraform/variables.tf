variable "project" {
  description = "Project name"
  type        = string
  default     = "NimbusKart"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "staging"
}

variable "owner" {
  description = "Resource owner"
  type        = string
  default     = "Saharsh"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "availability_zone" {
  description = "Availability zone for EBS volumes"
  type        = string
  default     = "us-east-1a"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.20.0.0/16"
}

variable "public_subnet_1_cidr" {
  description = "CIDR block for public subnet 1"
  type        = string
  default     = "10.20.1.0/24"
}

variable "public_subnet_2_cidr" {
  description = "CIDR block for public subnet 2"
  type        = string
  default     = "10.20.2.0/24"
}

variable "ssh_cidr" {
  description = "Allowed SSH CIDR block"
  type        = string
  default     = "0.0.0.0/0"
}