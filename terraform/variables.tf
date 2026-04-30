variable "project_name" {
  description = "Name of the project used for tagging and naming resources"
  type        = string
  default     = "stocklive"
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-west-3"
}
