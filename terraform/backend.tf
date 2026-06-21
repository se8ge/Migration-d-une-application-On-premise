terraform {
  backend "s3" {
    bucket         = "stocklive-tfstate-443628962197"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    # dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}
