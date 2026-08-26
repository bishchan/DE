variable "location"{
  description = "Project Location"
  default     = "US"
}

variable "gcs_bucket_name"{
  description = "Name of the BigQuery dataset"
  default     = "project-22d3f624-2ead-491d-b43-demo-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "bq_dataset_name" {
  description = "Name of the BigQuery dataset"
  default     = "demo_dataset"
}

variable "project" {
  description = "Project"
  default     = "project-22d3f624-2ead-491d-b43"
}

variable "region" {
  description = "Project Region"
  default     = "us-central1"
}

variable "credentials" {
  description = "Path to the service account key file"
  default     = "./key/my-creds.json"
}