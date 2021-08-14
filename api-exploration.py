#!/usr/bin/env python3

from datetime import datetime
from enum import Enum
from typing import Optional

import requests
from pydantic import BaseModel, HttpUrl

BOSTON_API_ENDPOINT = "https://mayors24.cityofboston.gov/open311/v2/"


class Service(BaseModel):
    """Available service from Boston 311."""

    version: int = 1
    description: Optional[str] = None
    group: str
    metadata: str
    service_code: str
    service_name: str
    type: str


class Services(BaseModel):
    """Servies available from Boston 311."""

    version: int = 1
    services: list[Service]


class Status(Enum):
    OPEN = "open"
    CLOSED = "closed"


class ServiceRequest(BaseModel):
    """Individual service request."""

    version: int = 1
    address: str
    address_id: Optional[str]
    zipcode: Optional[str]
    description: Optional[str]
    lat: float
    long: float
    media_url: Optional[HttpUrl]
    requested_datetime: datetime
    service_code: str
    service_name: str
    service_request_id: str
    status: Status
    updated_datetime: Optional[datetime]
    status_notes: Optional[str]
    agency_responsible: Optional[str]
    service_notice: Optional[str]
    expected_datetime: Optional[datetime]


class ServiceRequests(BaseModel):
    """Service requests."""

    version: int = 1
    service_requests: list[ServiceRequest]


def get_services() -> Services:
    res = requests.get(BOSTON_API_ENDPOINT + "services.json")
    if res.status_code != 200:
        print(f"Failed request - status code {res.status_code}")
        raise requests.HTTPError(res)
    services = Services(services=res.json())
    print(f"Number of services: {len(services.services)}")
    groups = set([s.group for s in services.services])
    print(f"Number of groups: {len(groups)}")
    print(groups)
    print(services.services[:5])
    return services


def get_services_requests() -> ServiceRequests:
    params: dict[str, str] = {
        "end_date": "2021-08-12T00:00:00Z",
        "service_code": "4f38920fe75084437f0001a0",
        "status": "open",
    }
    res = requests.get(BOSTON_API_ENDPOINT + "requests.json", params=params)
    if res.status_code != 200:
        print(f"Failed request - status code {res.status_code}")
        raise requests.HTTPError(res)
    service_requests = ServiceRequests(service_requests=res.json())
    print(f"Number of service requests: {len(service_requests.service_requests)}")
    return service_requests


if __name__ == "__main__":
    get_services()
