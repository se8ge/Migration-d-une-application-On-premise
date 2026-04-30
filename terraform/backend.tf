terraform {
  backend "s3" {
    bucket         = "stocklive-terraform-state"
    key            = "terraform.tfstate"
    region         = "eu-west-3"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}
