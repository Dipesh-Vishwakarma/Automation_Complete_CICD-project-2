terraform {
required_version = ">= 1.0"

 backend "s3" {
  bucket = "dipeshdevops4stroage" # CHANGE
  key = "JenkinsBaseInfra/Jenkins.tfstate" # CHANGE
  region = "eu-north-1" # CHANGE
  }
 }
