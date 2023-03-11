terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_project_service" "api_services" {
  project = var.project
  for_each = toset(
    [
      "iam.googleapis.com",
      "compute.googleapis.com",
      "cloudresourcemanager.googleapis.com",
    ]
  )
  service                    = each.key
  disable_on_destroy         = false
  disable_dependent_services = true
}

resource "google_service_account" "airbyte" {
  account_id   = "airbyte"
  display_name = "airbyte"
  description  = "Authorisation to use with Airbyte and Compute Engine VM"
  depends_on   = [google_project_service.api_services]
}

resource "google_project_iam_member" "airbyte-service-account-iam" {
  for_each = toset([
    "roles/iam.serviceAccountUser",
    "roles/run.admin",
    "roles/logging.admin",
    "roles/bigquery.jobUser",
    "roles/bigquery.user",
    "roles/bigquery.dataEditor"
  ])
  role       = each.value
  project    = var.project
  member     = "serviceAccount:${google_service_account.airbyte.email}"
  depends_on = [google_project_service.api_services]
}

resource "google_compute_instance" "vm_instance" {
  name                    = "data-stack-vm"
  machine_type            = "e2-medium"
  tags                    = [
    "${var.network}-firewall-ssh"
     ]
  metadata_startup_script = file("./sh_scripts/airbyte.sh")

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 30
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.mds_network_subnetwork.id
    access_config {
      # Ephemeral IP
    }
  }

  service_account {
    scopes = [
      "cloud-platform",
    ]
    email = google_service_account.airbyte.email
  }

  depends_on = [google_project_service.api_services]
}
