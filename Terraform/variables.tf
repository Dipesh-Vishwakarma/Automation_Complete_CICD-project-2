variable "aws_region" {
description = "AWS region to deploy into"
type = string
}
variable "vpc_cidr" {
description = "VPC CIDR block"
type = string
}
variable "public_subnet_cidr" {
description = "Public subnet CIDR"
type = string
}
variable "private_subnet_cidr" {
description = "Private subnet CIDR"
type = string
}
variable "AppVM" {
description = "EC2 instance type for Jenkins master"
type = string
}
variable "MonitorVM" {
description = "EC2 instance type for Jenkins master"
type = string
}
variable "ami" {
description = "AMI ID for both instances (Ubuntu 22.04 or Amazon Linux)"
type = string
}
variable "key_name" {
description = "Existing EC2 Key Pair name for SSH"
type = string
}
variable "ssh_cidr" {
description = "CIDR block allowed to SSH to instances"
type = string
}
variable "availability_zone_1a" {
  description = "Select the Availability zone eu-north-1a"
  type = string
}
variable "availability_zone_1b" {
  description = "Select the Availability zone eu-north-1b"
  type = string
}
variable "availability_zone_1c" {
  description = "Select the Availability zone eu-north-1c"
}