#REMINDER: The variables.tfvars file is used to define variables and the *.tf file declare that the variable exists. It is a fine distinction but important. Let me clarify.
#Refrence: https://amazic.com/difference-between-variable-tf-and-variable-tfvars-in-terraform/

#As these are automatically loaded, you can have your orchestration Automator dynamically create a tfvars file to define defaults such as Region, environment (dev, test, stage or prod) cidr_blocks, subnet ranges, etc.

variable "bucket_name" {
  type        = string
  description = "the name of our data lake bucket"
  #Use "python3 generate_random_string.py" if the bucket name isn't available anymore
  default = "irfziqsepanz"
}