resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "mds_test_dataset" # reference this in .env
  friendly_name               = "mds test dataset"
  description                 = "This is a test dataset"
  location                    = "US"
  delete_contents_on_destroy  = true
}