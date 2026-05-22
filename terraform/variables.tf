variable "project" {
  type    = string
  default = "NimbusKart"
}

variable "environment" {
  type    = string
  default = "staging"
}

variable "owner" {
  type    = string
  default = "Harsh"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "public_subnet_1_cidr" {
  type    = string
  default = "10.20.1.0/24"
}

variable "public_subnet_2_cidr" {
  type    = string
  default = "10.20.2.0/24"
}

variable "ssh_cidr" {
  type    = string
  default = "0.0.0.0/0"
}