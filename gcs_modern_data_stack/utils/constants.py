from dagster._utils import file_relative_path

# =========================================================================
# To get this value, run `python -m assets_modern_data_stack.setup_airbyte`
# and grab the connection id that it prints at the end
AIRBYTE_CONNECTION_ID = {"env": "AIRBYTE_CONNECTION_ID"}
# =========================================================================
AIRBYTE_CONFIG = {"host": "localhost", "port": "8000"}

DBT_PROJECT_DIR = file_relative_path(__file__, "../../dbt_project")
DBT_PROFILES_DIR = {"env": "DBT_PROFILES_DIR"}
DBT_CONFIG = {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}
