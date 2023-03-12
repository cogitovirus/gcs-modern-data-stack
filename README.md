# gcs-modern-data-stack
Demo of a modern data stack. Airbyte + Dagster + dbt + BigQuery.

## Running it locally
You need to have environment variables set up for the following:
```
AIRBYTE_CONNECTION_ID=
AIRBYTE_HOST=
AIRBYTE_PORT=
DBT_PROFILES_DIR=
```
those can be put in a `.env` file.

Then you can install the dependencies
```sh
pip install -e ".[dev]"
```

Now you can run the dagster server
```sh
dagster dev
```



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
