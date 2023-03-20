# gcs-modern-data-stack
Demo of a "modern" open source data stack. Airbyte + Dagster + dbt + BigQuery.
Overview of this project is posted [on my website](https://cogitovirus/posts/20230320-open-source-data-stack-poc/).

![Alt text](Global_Asset_Lineage.svg)

## Running it semi-locally

### Install the dependencies
```sh
pip install -e ".[dev]"
```

### Env variables
In `.env_template` you will find the enviroment variables that you need to set. Rename this file to `.env`.

### Google Cloud
This setup uses Google BigQuery as a data warehouse. That means that you should have an accound and ideally a seperate Google Cloud Project to run it. Switching to Databricks, Snowflake or Postgres shouldn't be that diffucult if you want to try it out, you would just need to manually setup up the Airbyte connectors and make sure dbt is pointing at the right schema.

### S3
Since Airbyte does not have a working source GCS connector, S3 is used as a source. That means that you will need an S3 bucket with it's secret and access key. Bucket contect is structured as follows:
```
jaffle_shop/
  jaffle_shop_customers.csv
  jaffle_shop_orders.csv
  stripe_payments.csv
```
With source files available [here](https://github.com/dbt-labs/jaffle_shop/tree/main/seeds)

### dbt
Dagster points at the dbt profile located under dbt_project/config/profiles.yml . By default it authorizes via gcloud cli, but you will most likely need to run
```
gcloud auth application-default login
```
to first obtain [access credentials](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login).


### Airbyte
Follow the instructions in the [Airbyte repo](https://docs.airbyte.com/deploying-airbyte/local-deployment/) to start Airbyte locally.

Alternatively you can use the terraform scripts in the `automation/terraform` folder to create the resources in GCP (along with the BigQuery dataset). Then you will need to run the following command to create an SSH tunnel to the Airbyte server:
```sh
# In your workstation terminal
SSH_KEY=~/Downloads/dataline-key-airbyte.pem
ssh -i $SSH_KEY -L 8000:localhost:8000 -N -f ec2-user@$INSTANCE_IP
```
or using gcloud
```sh
gcloud compute ssh --zone=us-central1-a --ssh-key-file=$SSH_KEY --project=$PROJECT_ID $INSTANCE_NAME -- -L 8000:localhost:8000 -N -f
```

You should now be able to access Airbyte under `http://localhost:8000/`using username and password specified in the `.env` file

### Create the S3 to BigQuery connectors
Run:

```sh
python3 -m gcs_modern_data_stack.utils.setup_airbyte
```
This will seed airbyte with 3 source connectors, bigQuery destination and the connections between sources and destination. After running it, you can inspect the AirByte UI.

**Hint:** Make sure that the ids that were set up, did indeed made it to .env file. I stumbled upon an issue where i had .env file opened in my IDE which was preventing automation from writing to the file properly.

### Dagster
Run the dagster server
```sh
dagster dev
```
And materialize all the assets. If you've done everything correctly you should be able to push the test data through and play around some more!


## Terraform
If you were not able/don't want to setup Airbyte locally, here's how you would do it with terraform:
```sh
cd automation/terraform
```
create a `terraform.tfvars` file with the following content:
```hcl
project          = "your-project-id"
credentials_file = "path/to/your/credentials.json"
```
In order to run:
```sh
terraform init
terraform plan
terraform apply
```
Remember to destroy the resources when you are done
```sh
terraform destroy
```
