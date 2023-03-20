from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)
from dagster_airbyte import airbyte_resource
from dagster_dbt import dbt_cli_resource
from dagster_dbt import load_assets_from_dbt_project

from gcs_modern_data_stack.assets import airbyte

from .utils.constants import AIRBYTE_CONFIG, DBT_CONFIG, DBT_PROJECT_DIR, DBT_PROFILES_DIR

dbt_assets = load_assets_from_dbt_project(
    project_dir=DBT_PROJECT_DIR, profiles_dir=DBT_PROFILES_DIR
)

airbyty_assets = load_assets_from_package_module(airbyte, group_name="landing")

defs = Definitions(
    assets=[*airbyty_assets, *dbt_assets],
    resources={
        "airbyte": airbyte_resource.configured(AIRBYTE_CONFIG),
        "dbt": dbt_cli_resource.configured(DBT_CONFIG)
    },
    schedules=[
        # update all assets once a day
        ScheduleDefinition(
            job=define_asset_job("all_assets", selection="*"), cron_schedule="@daily"
        ),
    ],
)
