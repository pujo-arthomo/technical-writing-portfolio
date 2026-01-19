from typing import Dict, List
from datetime import datetime


class ValidationError(Exception):
    pass


class Request:
    def __init__(self, payload: Dict[str, str]):
        self.payload = payload
        self.created_at = datetime.utcnow()
        self.status = "submitted"


def validate_client_side(payload: Dict[str, str]) -> None:
    required_fields = ["title", "description", "priority"]

    for field in required_fields:
        if field not in payload or not payload[field].strip():
            raise ValidationError(f"Missing required field: {field}")


def validate_server_side(payload: Dict[str, str]) -> None:
    if payload.get("priority") not in ["low", "medium", "high"]:
        raise ValidationError("Invalid priority value")


def store_request(request: Request, database: List[Request]) -> None:
    database.append(request)


def process_request(payload: Dict[str, str], database: List[Request]) -> Request:
    validate_client_side(payload)
    validate_server_side(payload)

    request = Request(payload)
    store_request(request, database)

    return request


# Example usage
if __name__ == "__main__":
    database = []

    incoming_payload = {
        "title": "Update access permissions",
        "description": "Requesting access for a new team member",
        "priority": "medium"
    }

    try:
        request = process_request(incoming_payload, database)
        print(f"Request stored with status: {request.status}")
    except ValidationError as error:
        print(f"Request rejected: {error}")
