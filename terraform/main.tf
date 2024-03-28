module "kubernetes" {
  source       = "/home/isaac/estudos/terraform/terraform-eks/terraform"
  cidr_block   = "10.34.0.0/16"
  project_name = "restapi"
  region       = "us-west-2"
  tags = {
    Department = "DevOps"
  }
}