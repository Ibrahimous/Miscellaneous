#Reference:
#https://medium.com/@vladkens/aws-ecs-cluster-on-ec2-with-terraform-2023-fdb9f6b7db07
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
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags                 = { Name = "demo-vpc" }
}

resource "aws_subnet" "public" {
  count                   = locals.azs_count
  vpc_id                  = aws_vpc.main.id
  availability_zone       = locals.azs_names[count.index]
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, 10 + count.index)
  map_public_ip_on_launch = true
  tags                    = { Name = "demo-public-${locals.azs_names[count.index]}" }
}

# --- Internet Gateway ---

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "demo-igw" }
}

resource "aws_eip" "main" {
  count      = locals.azs_count
  depends_on = [aws_internet_gateway]
  tags       = { Name = "demo-eip-${locals.azs_names[count.index]}" }
}

# --- Public route table ---

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "demo-rt-public" }
  route = {
    cidr_block = "0.0.0.0"
    gateway_id = aws_eip.main.id
  }
}

resource "aws_route_table_association" "public" {
  count          = locals.azs_count
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}