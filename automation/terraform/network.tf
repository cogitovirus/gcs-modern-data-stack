resource "google_compute_network" "mds_vpc_network" {
  name = var.network
}

resource "google_compute_subnetwork" "mds_network_subnetwork" {
  name          = "${var.network}-subnetwork-${var.region}"
  region        = var.region
  network       = "${google_compute_network.mds_vpc_network.self_link}"
  ip_cidr_range = "10.0.0.0/16"
}