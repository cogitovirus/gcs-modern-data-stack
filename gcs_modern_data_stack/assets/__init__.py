from dagster_airbyte import build_airbyte_assets
from dagster_dbt import load_assets_from_dbt_project

from ..utils.constants import AIRBYTE_CONNECTION_ID, DBT_PROJECT_DIR, DBT_PROFILES_DIR

airbyte_assets = build_airbyte_assets(
    connection_id=AIRBYTE_CONNECTION_ID,
    asset_key_prefix=["jaffle_shop"],
    destination_tables=["jaffle_shop_customers"]
)

dbt_assets = load_assets_from_dbt_project(
    project_dir=DBT_PROJECT_DIR, profiles_dir=DBT_PROFILES_DIR
)
