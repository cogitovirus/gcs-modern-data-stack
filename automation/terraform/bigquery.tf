resource "google_bigquery_dataset" "dataset_landing" {
  dataset_id                  = "mds_test_dataset" # reference this in .env
  friendly_name               = "mds test dataset"
  description                 = "This is a test dataset"
  location                    = "US"
  delete_contents_on_destroy  = true
}

resource "google_bigquery_dataset" "dataset_raw" {
  dataset_id                  = "mds_test_dataset_raw"
  friendly_name               = "mds test dataset raw"
  description                 = "data warehouse - raw"
  location                    = "US"
  delete_contents_on_destroy  = true
}

resource "google_bigquery_dataset" "dataset_trusted" {
  dataset_id                  = "mds_test_dataset_trusted"
  friendly_name               = "mds test dataset"
  description                 = "data warehouse - trusted"
  location                    = "US"
  delete_contents_on_destroy  = true
}