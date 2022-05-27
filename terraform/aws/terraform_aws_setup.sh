sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

sudo aptitude -ry install python3 python3-pip
sudo pip3 install awscli

#Go to aws & create a role called s3admin in a group called S3Admins with the associated strategy S3FullAccess
aws configure

export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="eu-west-3"

#<TO BE CHANGED>
git clone https://github.com/Ibrahimous/Miscellaneous
cd Miscellaneous/aws
#</TO BE CHANGED>

terraform init
#should get "Terraform has been successfully initialized!"

terraform fmt
#should get nothing

terraform validate
#should get "Success! The configuration is valid."

terraform apply
#should get:
#aws_s3_bucket.b: Creating...
#aws_s3_bucket.b: Creation complete after 2s [id=irfziqsepanz]
#aws_s3_bucket_acl.s3acl: Creating...
#aws_s3_bucket_acl.s3acl: Creation complete after 1s [id=irfziqsepanz,private]
#Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

terraform destroy
#should get:
#Destroy complete! Resources: 2 destroyed.