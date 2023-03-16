# Remove all airbyte source, destination and connection definitions from the Airbyte instance
from typing import Any, Dict, Mapping

from dagster_airbyte import AirbyteResource

from .constants import AIRBYTE_CONFIG

def _safe_request(
    client: AirbyteResource, endpoint: str, data: Dict[str, object]
) -> Mapping[str, Any]:
    response = client.make_request(endpoint, data)
    return response

def teardown_airbyte():
    client = AirbyteResource(
        host=AIRBYTE_CONFIG["host"],
        port=AIRBYTE_CONFIG["port"],
        username=AIRBYTE_CONFIG["username"],
        password=AIRBYTE_CONFIG["password"],
        use_https=False
    )

    # get the workspace id
    workspace_id = _safe_request(client, "/workspaces/list", data={})["workspaces"][0][
        "workspaceId"
    ]

    # get all connections
    connections = _safe_request(client, "/web_backend/connections/list", data={"workspaceId": workspace_id})["connections"]

    # for each connection
    for connection in connections:
        # get the source id
        source_id = connection["source"]["sourceId"]
        #  delete the source
        print(f"Deleting Airbyte Source: {source_id}")
        _safe_request(client, "/sources/delete", data={"sourceId": source_id})
        # get the destination id
        destination_id = connection["destination"]["destinationId"]
        # delete the destination
        print(f"Deleting Airbyte Destination: {destination_id}")
        _safe_request(client, "/destinations/delete", data={"destinationId": destination_id})
        # delete the connection
        print(f"Deleting Airbyte Connection: {connection['connectionId']}")
        _safe_request(client, "/connections/delete", data={"connectionId": connection["connectionId"]})

teardown_airbyte()