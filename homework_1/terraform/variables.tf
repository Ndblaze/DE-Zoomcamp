variable "location" {
  description = "This is the location"
  default = "US"
}

variable "region" {
  description = "This is the region"
  default = "us-central1"
}

variable "project" {
  description = "This is the project"
  default = "terraform-demo-448802"
}

variable "gcs_project-name" {
  description = "This is the project name"
  default = "terraform-demo-448802-terra-bucket"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default = "demo_dataset"
}