
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  # Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  #  credentials = 
  project = var.project
  region  = var.region
}



resource "google_storage_bucket" "demo-bucket" {
  name     = var.gcs_project-name
  location = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1 // days
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }

}


resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}



# terraform fmt
# terraform init
# terraform plan
# terraform apply //to creat a bucket
# terraform destroy // to delect a bucket