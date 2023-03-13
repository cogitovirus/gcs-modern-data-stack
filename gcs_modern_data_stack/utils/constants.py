import os
from dagster._utils import file_relative_path
from dotenv import load_dotenv

load_dotenv()


# =========================================================================
# To get this value, run `python -m assets_modern_data_stack.setup_airbyte`
# and grab the connection id that it prints at the end
AIRBYTE_CONNECTION_ID = os.getenv("AIRBYTE_CONNECTION_ID")
# =========================================================================
AIRBYTE_CONFIG = {
    "host": os.getenv("AIRBYTE_HOST"),
    "port": os.getenv("AIRBYTE_PORT"),
    "username": os.getenv("AIRBYTE_USER"),
    "password": os.getenv("AIRBYTE_PASS")
    }

S3_SOURCE_CONFIG = {
    "aws_secret_access_key": os.getenv("S3_SOURCE_AWS_SECRET_ACCESS_KEY"),
    "aws_access_key_id": os.getenv("S3_SOURCE_AWS_ACCESS_KEY_ID"),
}

BQ_TARGET_CONFIG= {
    "project_id": os.getenv("BQ_TARGET_PROJECT_ID"),
    "dataset_id": os.getenv("BQ_TARGET_DATASET_ID"),
}


DBT_PROJECT_DIR = file_relative_path(__file__, "../../dbt_project")
# Seems kind of stupid to have it here instead of the ~/.dbt/profiles.yml
DBT_PROFILES_DIR = file_relative_path(__file__, "../../dbt_project/config")
DBT_CONFIG = {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}
