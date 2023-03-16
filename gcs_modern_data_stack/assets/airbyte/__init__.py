from dagster_airbyte import build_airbyte_assets

from ...utils.constants import AIRBYTE_CONNECTION_IDS

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