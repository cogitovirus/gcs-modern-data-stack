"""
A script that will create tables in the source postgres database, then automatically
create an Airbyte Connection between the source database and destination database.
"""

from typing import Any, Dict, Mapping
from pathlib import Path
from dotenv import set_key

import dagster._check as check
from dagster_airbyte import AirbyteResource

from .constants import AIRBYTE_CONFIG, S3_SOURCE_CONFIG, BQ_TARGET_CONFIG

env_file_path = Path("../.env")


def _safe_request(
    client: AirbyteResource, endpoint: str, data: Dict[str, object]
) -> Mapping[str, Any]:
    response = client.make_request(endpoint, data)
    assert response, "Request returned null response"
    return response


def _create_ab_sources(client: AirbyteResource, workspace_id: str) -> str:
    source_defs = _safe_request(
        client, "/source_definitions/list_latest", data={"workspaceId": workspace_id}
    )

    s3_definitions = [
        sd for sd in source_defs["sourceDefinitions"] if sd["name"] == "S3"
    ]
    if not s3_definitions:
        raise check.CheckError("Expected at least one S3 source definition.")
    source_definition_id = s3_definitions[0]["sourceDefinitionId"]

    # define three distinct sources (jaffle_shop_customers, jaffle_shop_orders, stripe_payments)
    sources_data = [
        {
            "name": "JAFFLE_SHOP_CUSTOMERS",
            "sourceDefinitionId": source_definition_id,
            "workspaceId": workspace_id,
            "connectionConfiguration": {
                "path_pattern": "**/jaffle_shop_customers*.csv",
                "provider": {
                    "aws_secret_access_key": S3_SOURCE_CONFIG["aws_secret_access_key"],
                    "aws_access_key_id": S3_SOURCE_CONFIG["aws_access_key_id"],
                    "path_prefix": "",
                    "endpoint": "",
                    "bucket": "wzolni-test-bucket"
                },
                "dataset": "jaffle_shop_customers",
                "schema": "{}",
                "format": {
                    "filetype": "csv",
                    "newlines_in_values": False,
                    "infer_datatypes": True,
                    "double_quote": True,
                    "quote_char": "\"",
                    "block_size": 10000,
                    "delimiter": ",",
                    "encoding": "utf8"
                }
            }
        },
        {
            "name": "JAFFLE_SHOP_ORDERS",
            "sourceDefinitionId": source_definition_id,
            "workspaceId": workspace_id,
            "connectionConfiguration": {
                "path_pattern": "**/jaffle_shop_orders*.csv",
                "provider": {
                    "aws_secret_access_key": S3_SOURCE_CONFIG["aws_secret_access_key"],
                    "aws_access_key_id": S3_SOURCE_CONFIG["aws_access_key_id"],
                    "path_prefix": "",
                    "endpoint": "",
                    "bucket": "wzolni-test-bucket"
                },
                "dataset": "jaffle_shop_orders",
                "schema": "{}",
                "format": {
                    "filetype": "csv",
                    "newlines_in_values": False,
                    "infer_datatypes": True,
                    "double_quote": True,
                    "quote_char": "\"",
                    "block_size": 10000,
                    "delimiter": ",",
                    "encoding": "utf8"
                }
            }
        },
        {
            "name": "STRIPE_PAYMENTS",
            "sourceDefinitionId": source_definition_id,
            "workspaceId": workspace_id,
            "connectionConfiguration": {
                "path_pattern": "**/stripe_payments*.csv",
                "provider": {
                    "aws_secret_access_key": S3_SOURCE_CONFIG["aws_secret_access_key"],
                    "aws_access_key_id": S3_SOURCE_CONFIG["aws_access_key_id"],
                    "path_prefix": "",
                    "endpoint": "",
                    "bucket": "wzolni-test-bucket"
                },
                "dataset": "stripe_payments",
                "schema": "{}",
                "format": {
                    "filetype": "csv",
                    "newlines_in_values": False,
                    "infer_datatypes": True,
                    "double_quote": True,
                    "quote_char": "\"",
                    "block_size": 10000,
                    "delimiter": ",",
                    "encoding": "utf8"
                }
            }
        }

    ]

    sources_id_name_array = []

    for source_data in sources_data:
        source_id = _safe_request(client, "/sources/create", data=source_data)["sourceId"]
        sources_id_name_array.append([source_id, source_data["name"]])

        print(f"Created Airbyte Source: {source_id}")

    return sources_id_name_array


def _create_ab_destination(client: AirbyteResource, workspace_id: str) -> str:
    # get the latest available BigQuery destination definition
    destination_defs = _safe_request(
        client, "/destination_definitions/list_latest", data={"workspaceId": workspace_id}
    )
    bigquery_definitions = [
        dd for dd in destination_defs["destinationDefinitions"] if dd["name"] == "BigQuery"
    ]
    if not bigquery_definitions:
        raise check.CheckError(
            "Expected at least one BigQuery destination definition.")
    destination_definition_id = bigquery_definitions[0]["destinationDefinitionId"]

    # create BigQuery destination
    destination_id = _safe_request(
        client,
        "/destinations/create",
        data={
            "name": "mds_bigquery",
            "destinationDefinitionId": destination_definition_id,
            "workspaceId": workspace_id,
            "connectionConfiguration": {
                    "loading_method": {
                        "method": "Standard"
                    },
                "transformation_priority": "interactive",
                "big_query_client_buffer_size_mb": 15,
                "project_id": BQ_TARGET_CONFIG["project_id"],
                "dataset_id": BQ_TARGET_CONFIG["dataset_id"],
                "dataset_location": "US"
            }
        },
    )["destinationId"]
    print(f"Created Airbyte Destination: {destination_id}")
    return destination_id


def setup_airbyte():
    client = AirbyteResource(
        host=AIRBYTE_CONFIG["host"],
        port=AIRBYTE_CONFIG["port"],
        username=AIRBYTE_CONFIG["username"],
        password=AIRBYTE_CONFIG["password"],
        use_https=False
    )

    workspace_id = _safe_request(client, "/workspaces/list", data={})["workspaces"][0][
        "workspaceId"
    ]

    sources_id_name_array = _create_ab_sources(client, workspace_id)
    destination_id = _create_ab_destination(client, workspace_id)

    # for each source, discover the catalog and create a connection
    for source_id_name in sources_id_name_array:
        source_id = source_id_name[0]
        source_name = source_id_name[1]
        # discover the catalog for the new source
        source_catalog = _safe_request(
            client, "/sources/discover_schema", data={"sourceId": source_id}
        )["catalog"]

        # create a connection between the new source and destination
        connection_id = _safe_request(
            client,
            "/connections/create",
            data={
                "name": source_name,
                "sourceId": source_id,
                "destinationId": destination_id,
                "syncCatalog": source_catalog,
                "status": "active",
            },
        )["connectionId"]

        # patch the connection to set the normalization operation
        _safe_request(client,
                    "/web_backend/connections/update",
                    data={
                        "connectionId": connection_id,
                        "operations": [
                            {
                                "name": "Normalization",
                                "workspaceId": workspace_id,
                                "operatorConfiguration": {
                                    "operatorType": "normalization",
                                    "normalization": {
                                        "option": "basic"
                                    }
                                }
                            }
                        ]
                    }
                    )

        print(f"Created Airbyte Connection: {connection_id}")
        # set the source id in the .env file
        print(f"Setting {source_name}_CONNECTION_ID in .env file")
        set_key(dotenv_path=f"{Path.cwd()}/.env", key_to_set=f"{source_name}_CONNECTION_ID", value_to_set=connection_id)

setup_airbyte()
