from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)
from dagster_airbyte import airbyte_resource
# from dagster_gcp import bigquery_resource
from dagster_dbt import dbt_cli_resource

from . import assets
from .utils.constants import AIRBYTE_CONFIG, DBT_CONFIG

defs = Definitions(
    assets=load_assets_from_package_module(assets),
    resources={
        "airbyte": airbyte_resource.configured(AIRBYTE_CONFIG),
        "dbt": dbt_cli_resource.configured(DBT_CONFIG),
        #TODO: bigquery resource
    },
    schedules=[
        # update all assets once a day
        ScheduleDefinition(
            job=define_asset_job("all_assets", selection="*"), cron_schedule="@daily"
        ),
    ],
)