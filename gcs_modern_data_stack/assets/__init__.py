from dagster_airbyte import build_airbyte_assets
from dagster_dbt import load_assets_from_dbt_project

from ..utils.constants import AIRBYTE_CONNECTION_IDS, DBT_PROJECT_DIR, DBT_PROFILES_DIR

customers_assets = build_airbyte_assets(
    connection_id=AIRBYTE_CONNECTION_IDS["JAFFLE_SHOP_CUSTOMERS_CONNECTION_ID"],
    asset_key_prefix=["jaffle_shop"],
    destination_tables=["jaffle_shop_customers"]
)

orders_assets = build_airbyte_assets(
    connection_id=AIRBYTE_CONNECTION_IDS["JAFFLE_SHOP_ORDERS_CONNECTION_ID"],
    asset_key_prefix=["jaffle_shop"],
    destination_tables=["jaffle_shop_orders"]
)

payment_assets = build_airbyte_assets(
    connection_id=AIRBYTE_CONNECTION_IDS["STRIPE_PAYMENTS_CONNECTION_ID"],
    asset_key_prefix=["stripe"],
    destination_tables=["stripe_payments"]
)

dbt_assets = load_assets_from_dbt_project(
    project_dir=DBT_PROJECT_DIR, profiles_dir=DBT_PROFILES_DIR
)
