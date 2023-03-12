"""
A basic script that will create tables in the source postgres database, then automatically
create an Airbyte Connection between the source database and destination database.
"""

from typing import Any, Dict, Mapping

import dagster._check as check
from dagster_airbyte import AirbyteResource

def _safe_request(
    client: AirbyteResource, endpoint: str, data: Dict[str, object]
) -> Mapping[str, Any]:
    response = client.make_request(endpoint, data)
    assert response, "Request returned null response"
    return response


def _create_ab_source(client: AirbyteResource) -> str:
    workspace_id = _safe_request(client, "/workspaces/list", data={})["workspaces"][0][
        "workspaceId"
    ]

    # get latest available BigQuery source definition
    source_defs = _safe_request(
        client, "/source_definitions/list_latest", data={"workspaceId": workspace_id}
    )
    bigquery_definitions = [
        sd for sd in source_defs["sourceDefinitions"] if sd["name"] == "BigQuery"
    ]
    if not bigquery_definitions:
        raise check.CheckError("Expected at least one BigQuery source definition.")
    source_definition_id = bigquery_definitions[0]["sourceDefinitionId"]

    # create BigQuery source
    source_id = _safe_request(
        client,
        "/sources/create",
        data={
            "sourceDefinitionId": source_definition_id,
            # TODO: set BQ_SOURCE_CONFIG in constants.py
            # "connectionConfiguration": dict(**BQ_SOURCE_CONFIG, ssl=False),
            "workspaceId": workspace_id,
            "name": "Source Database",
        },
    )["sourceId"]
    print(f"Created Airbyte Source: {source_id}")
    return source_id


def _create_ab_destination(client: AirbyteResource) -> str:
    workspace_id = _safe_request(client, "/workspaces/list", data={})["workspaces"][0][
        "workspaceId"
    ]

    # get the latest available BigQuery destination definition
    destination_defs = _safe_request(
        client, "/destination_definitions/list_latest", data={"workspaceId": workspace_id}
    )
    postgres_definitions = [
        dd for dd in destination_defs["destinationDefinitions"] if dd["name"] == "BigQuery"
    ]
    if not postgres_definitions:
        raise check.CheckError("Expected at least one Postgres destination definition.")
    destination_definition_id = postgres_definitions[0]["destinationDefinitionId"]

    # create Postgres destination
    destination_id = _safe_request(
        client,
        "/destinations/create",
        data={
            "destinationDefinitionId": destination_definition_id,
            # TODO: set BQ_DESTINATION_CONFIG in constants.py
            # "connectionConfiguration": dict(**BQ_DESTINATION_CONFIG, schema="public", ssl=False),
            "workspaceId": workspace_id,
            "name": "Destination Database",
        },
    )["destinationId"]
    print(f"Created Airbyte Destination: {destination_id}")
    return destination_id


def setup_airbyte():
    # TODO: should use environment variables for this
    client = AirbyteResource(host="localhost", port="8000", use_https=False)
    source_id = _create_ab_source(client)
    destination_id = _create_ab_destination(client)

    source_catalog = _safe_request(
        client, "/sources/discover_schema", data={"sourceId": source_id}
    )["catalog"]

    # create a connection between the new source and destination
    connection_id = _safe_request(
        client,
        "/connections/create",
        data={
            "name": "Example Connection",
            "sourceId": source_id,
            "destinationId": destination_id,
            "syncCatalog": source_catalog,
            "prefix": "",
            "status": "active",
        },
    )["connectionId"]

    print(f"Created Airbyte Connection: {connection_id}")

setup_airbyte()
