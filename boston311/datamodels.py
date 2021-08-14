"""Data models."""

import pprint
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, HttpUrl


def _pprint_format(d: dict[Any, Any], indent: int = 4) -> str:
    pp = pprint.PrettyPrinter(indent=4)
    return pp.pformat(d)


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
        """String representation."""
        return _pprint_format(self.dict())

    def __hash__(self) -> int:
        """Hash of a service based on its service code."""
        return hash(self.service_code)


class Services(BaseModel):
    """Servies available from Boston 311."""

    version: int = 1
    services: list[Service]

    def __repr__(self) -> str:
        """String representation."""
        return f"{len(self)} available services"

    def __str__(self) -> str:
        """String representation."""
        return self.__repr__()

    def __len__(self) -> int:
        """Get number of services."""
        return len(self.services)

    def __getitem__(self, indices):
        """Get a service by index."""
        return self.services[indices]

    def list_service_names(self) -> list[str]:
        """List all of the unique service names.

        Returns:
            list[str]: List of service names (all unique).
        """
        return list(set([s.service_name for s in self.services]))

    def get_service_code(self, service_name: str) -> Optional[str]:
        """Get the service code by its name.

        Args:
            service_name (str): Service name.

        Returns:
            Optional[str]: Corresponding service code if found.
        """
        for service in self.services:
            if service.service_name == service_name:
                return service.service_code
        return None

    def get_service_name(self, service_code: str) -> Optional[str]:
        """Get the service name by its code.

        Args:
            service_code (str): Service code.

        Returns:
            Optional[str]: Corresponding service name.
        """
        for service in self.services:
            if service.service_code == service_code:
                return service.service_name
        return None


class Status(str, Enum):
    """Possible statuses of service requests."""

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

    def __str__(self) -> str:
        """String representation."""
        return _pprint_format(self.dict())

    def __hash__(self) -> int:
        """Hash of a service request based on its service ID."""
        return hash(self.service_request_id)


class ServiceRequests(BaseModel):
    """Service requests."""

    version: int = 1
    service_requests: list[ServiceRequest]

    def __repr__(self) -> str:
        """String representation."""
        return f"{len(self)} service requests"

    def __str__(self) -> str:
        """String representation."""
        return self.__repr__()

    def __len__(self) -> int:
        """Number of service request objects."""
        return len(self.service_requests)

    def __getitem__(self, indices):
        """Get a service request by index."""
        return self.service_requests[indices]
