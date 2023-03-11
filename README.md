# gcs-modern-data-stack
Demo of a modern data stack. Airbyte + Dagster + dbt + BigQuery.

## Terraform
```sh
cd automation/terraform
```
create a `terraform.tfvars` file with the following content:
```hcl
project          = "your-project-id"
credentials_file = "path/to/your/credentials.json"
```
In order to run
```sh
terraform init
terraform plan
terraform apply
```
Remember to destroy the resources when you are done
```sh
terraform destroy
```
