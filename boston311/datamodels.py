"""Data models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl


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
