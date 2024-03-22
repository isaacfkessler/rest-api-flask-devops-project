module "kubernetes" {
  source       = "git@github.com:isaacfkessler/terraform-eks-devops-mm.git?ref=master"
  cidr_block   = "10.34.0.0/16"
  project_name = "restapi"
  region       = "us-west-2"
  tags = {
    Department = "DevOps"
  }
}