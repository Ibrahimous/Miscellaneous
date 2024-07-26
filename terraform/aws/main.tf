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

#TIERING - redundant with lifecycle policy?
#https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_intelligent_tiering_configuration
#resource "aws_s3_bucket_intelligent_tiering_configuration" "s3Tieringconfig" {
#  bucket = aws_s3_bucket.b.bucket
#  name   = "EntireBucket S3 Tiering configuration"

#  tiering {
#    access_tier = "DEEP_ARCHIVE_ACCESS"
#    days        = 180
#  }
#  tiering {
#    access_tier = "ARCHIVE_ACCESS"
#    days        = 125
#  }
#}

#TODO: Activate versionning, MFA delete, encryption, storage class (for instance intelligent tiering), configure cloudtrail, perhaps transfer acceleration
#https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket

#/!\ACL:private - Objects can be public, though
resource "aws_s3_bucket_acl" "s3acl" {
  bucket = aws_s3_bucket.b.id
  acl    = "private"
}

#versioning
resource "aws_s3_bucket_versioning" "s3versioning" {
  bucket = aws_s3_bucket.b.id
  versioning_configuration {
    status = "Enabled"
  }
}

#bucket acceleration
#Transfer Acceleration is currently not supported for buckets in eu-north-1
#https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html#transfer-acceleration-requirements
resource "aws_s3_bucket_accelerate_configuration" "s3acceleration" {
  bucket = aws_s3_bucket.b.bucket
  status = "Enabled"
}

#lifecycle - you may filter on tags or directories
#https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_lifecycle_configuration
resource "aws_s3_bucket_lifecycle_configuration" "s3lifecycle" {
  bucket = aws_s3_bucket.b.id

  #Error: error creating S3 Lifecycle Configuration for bucket (irfziqsepanz): InvalidRequest: At least one action needs to be specified in a rule
  rule {
    id = "log-rule"

    filter {
      prefix = "logs/"
    }
    
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 60
      storage_class = "GLACIER"
    }

  }
}

# AWS key creation
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_key
# /!\ Requires kms:CreateKey action
# TODO: restric rights according to https://docs.aws.amazon.com/kms/latest/developerguide/iam-policies-best-practices.html
resource "aws_kms_key" "s3key" {
  description              = "KMS key for the s3 bucket"
  deletion_window_in_days  = 10 #default = 30
  key_usage                = "ENCRYPT_DECRYPT"
  customer_master_key_spec = "SYMMETRIC_DEFAULT"

  #policy - All KMS keys must have a key policy.
  #If a key policy is not specified, AWS gives the KMS key a default key policy that gives all principals in the owning account unlimited access to all KMS operations for the key.
  #This default key policy effectively delegates all access control to IAM policies and KMS grants.

  bypass_policy_lockout_safety_check = false

  is_enabled          = true
  enable_key_rotation = false
  multi_region        = false

  #tags - A map of tags to assign to the object.

}

# Encryption
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration
resource "aws_s3_bucket_server_side_encryption_configuration" "s3encryption" {
  bucket = aws_s3_bucket.b.bucket

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.s3key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}
