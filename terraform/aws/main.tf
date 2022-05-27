terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "eu-west-3"
}

#Reference: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket
resource "aws_s3_bucket" "b" {
  bucket = var.bucket_name

  tags = {
    Name        = "My Data Lake bucket"
    Environment = "Dev"
  }
}

#/!\Objects can be public
#TODO: Activate versionning, encryption, storage class (for instance intelligent tiering), configure cloudtrail, perhaps transfer acceleration
resource "aws_s3_bucket_acl" "s3acl" {
  bucket = aws_s3_bucket.b.id
  acl    = "private"
}