#Reference:
#https://spacelift.io/blog/terraform-locals
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "5.49.0" }
  }
}

provider "aws" {
  profile = "default"
  region  = "eu-west-3"
}

# --- VPC ---

data "aws_availability_zones" "available" { state = "available" }

locals {
  azs_count = 2
  azs_names = data.aws_availability_zones.available.names
  bucket_name = "mytest"
  env         = "dev"
}


resource "aws_s3_bucket" "my_test_bucket" {
    count = locals.azs_count
    bucket = local.bucket_name
 
    tags = {
        Name        = local.bucket_name
        Environment = local.env
    }
}