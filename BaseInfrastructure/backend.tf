terraform {
required_version = ">= 1.0"

 backend "s3" {
  bucket = "project-2-baseinfra-state-files" # CHANGE
  key = "BaseInfra/Jenkins.tfstate" # CHANGE
  region = "eu-north-1" # CHANGE
  }
 }
