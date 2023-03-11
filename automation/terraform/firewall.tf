resource "google_compute_firewall" "ssh" {
  name    = "${var.network}-firewall-ssh"
  network = google_compute_network.mds_vpc_network.id

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags   = ["${var.network}-firewall-ssh"]
  source_ranges = ["0.0.0.0/0"]
  direction     = "INGRESS"
  priority      = 1000
}

# remember to add tags to the instance if order for the rule to work
# resource "google_compute_firewall" "http" {
#   name    = "${var.network}-firewall-http"
#   network = "${google_compute_network.mds_vpc_network.name}"

#   allow {
#     protocol = "tcp"
#     ports    = ["80", "8080", "8000"]
#   }

#   target_tags   = ["${var.network}-firewall-http"]
# #   source_ranges = ["0.0.0.0/0"]
#   source_ranges = ["83.8.45.199"]
# }

# resource "google_compute_firewall" "https" {
#   name    = "${var.network}-firewall-https"
#   network = "${google_compute_network.mds_vpc_network.name}"

#   allow {
#     protocol = "tcp"
#     ports    = ["443"]
#   }

#   target_tags   = ["${var.network}-firewall-https"]
#   source_ranges = ["0.0.0.0/0"]
# }