"""Data models."""

import pprint
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl


class Service(BaseModel):
    """Available service from Boston 311."""

    version: int = 1
    description: Optional[str] = None
    group: str
    metadata: bool
    service_code: str
    service_name: str
    type: str

    def __str__(self) -> str:
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(self.dict())

    def __hash__(self) -> int:
        return hash(self.service_code)


class Services(BaseModel):
    """Servies available from Boston 311."""

    version: int = 1
    services: list[Service]

    def __repr__(self) -> str:
        return f"{len(self)} available services"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        return len(self.services)

    def __getitem__(self, indices):
        return self.services[indices]

    def list_service_names(self) -> list[str]:
        return list(set([s.service_name for s in self.services]))

    def get_service_code(self, service_name: str) -> Optional[str]:
        for service in self.services:
            if service.service_name == service_name:
                return service.service_code
        return None

    def get_service_name(self, service_code: str) -> Optional[str]:
        for service in self.services:
            if service.service_code == service_code:
                return service.service_name
        return None


class Status(str, Enum):
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

    def __hash__(self) -> int:
        return hash(self.service_request_id)


class ServiceRequests(BaseModel):
    """Service requests."""

    version: int = 1
    service_requests: list[ServiceRequest]

    def __repr__(self) -> str:
        return f"{len(self)} available services"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        return len(self.service_requests)

    def __getitem__(self, indices):
        return self.service_requests[indices]
