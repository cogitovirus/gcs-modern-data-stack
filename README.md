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
### Airbyte
Follow the instructions in the [Airbyte repo](https://docs.airbyte.com/deploying-airbyte/local-deployment/) to start Airbyte locally. Alternatively you can use the terraform scripts in the `automation/terraform` folder to create the resources in GCP, then you can run the following command to create an SSH tunnel to the Airbyte server:
```sh
# In your workstation terminal
SSH_KEY=~/Downloads/dataline-key-airbyte.pem
ssh -i $SSH_KEY -L 8000:localhost:8000 -N -f ec2-user@$INSTANCE_IP
```
or using gcloud
```sh
gcloud compute ssh --zone=us-central1-a --ssh-key-file=$SSH_KEY --project=$PROJECT_ID $INSTANCE_NAME -- -L 8000:localhost:8000 -N -f
```
### Setup a sample s3<>bigquery connector

```sh
python -m gcs_modern_data_stack.utils.setup_airbyte
```

## dbt BigQuery
### option 1 - gcloud authentification
Your profile should look like this:
```yml
jaffle_shop_bq:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: [GCP project id]
      dataset: [the name of your dbt dataset] # You can also use "schema" here
      threads: [1 or more]
      <optional_config>: <value>
```
### option 2 - service account
<!-- TODO: service account terraform -->
```yml
my-bigquery-db:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth-secrets
      project: [GCP project id]
      dataset: [the name of your dbt dataset] # You can also use "schema" here
      threads: [1 or more]
      refresh_token: [token]
      client_id: [client id]
      client_secret: [client secret]
      token_uri: [redirect URI]
      <optional_config>: <value>
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
