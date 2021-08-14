"""Interacting with the Boston 311 API."""
from datetime import datetime, timezone
from typing import Optional

import requests

from .constants import BOSTON_API_ENDPOINT
from .datamodels import ServiceRequests, Services, Status


def get_services() -> Services:
    """Retrieve the acceptable 311 service request types and their service codes.

    Raises:
        requests.HTTPError: Raised if the API request is unsuccessful.

    Returns:
        Services: Collection of all available services.
    """
    res = requests.get(BOSTON_API_ENDPOINT + "services.json")
    if res.status_code != 200:
        raise requests.HTTPError(res)
    return Services(services=res.json())


# Query the current status of an individual request
# def get_service_request(service_request_id: str) -> ServiceRequest:
#     pass


def _format_in_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt.replace(tzinfo=timezone.utc)
    elif dt.tzinfo is not timezone.utc:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + "Z"


class ServiceRequestParameters:
    """Parameters for a GET request for service requests."""

    service_code: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: Optional[Status]

    def __init__(
        self,
        service_code: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        status: Optional[Status],
    ) -> None:
        self.service_code = service_code
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def get_params(self) -> dict[str, str]:
        """Get a dictionary of the parameters for the request."""
        if self.end_date is None and self.start_date is not None:
            self.end_date = datetime.now(tz=timezone.utc)

        params: dict[str, str] = {}

        if self.service_code is not None:
            params["service_code"] = self.service_code
        if self.start_date is not None:
            params["start_date"] = _format_in_utc(self.start_date)
        if self.end_date is not None:
            params["end_date"] = _format_in_utc(self.end_date)
        if self.status is not None:
            params["status"] = self.status

        return params


def get_service_requests(
    service_code: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    status: Optional[Status] = None,
) -> ServiceRequests:
    """Query the current status of multiple requests.

    All dates should be supplied with timezone information or they will be assumed to be
    in UTC.

    Args:
        service_code (Optional[str], optional): Specify the service type by calling the
        unique ID of the service_code. Defaults to `None` to request all service codes.
        start_date (Optional[datetime], optional): Earliest datetime to include in
        search. When not specified, the range defaults to most recent 90 days.
        Defaults to `None`.
        end_date (Optional[datetime], optional): Latest datetime to include in search.
        When not specified (`None`), the current date time is used. Defaults to `None`.
        status (Optional[Status], optional): Search for requests which have a specific
        status. Defaults to `None` to include all statuses.

    Raises:
        requests.HTTPError: Raised if the API request is unsuccessful.

    Returns:
        ServiceRequests: Collection of all service requests based on any provided
        criteria.
    """
    params = ServiceRequestParameters(
        service_code=service_code,
        start_date=start_date,
        end_date=end_date,
        status=status,
    ).get_params()

    res = requests.get(BOSTON_API_ENDPOINT + "requests.json", params=params)
    if res.status_code != 200:
        print(f"Failed request - status code {res.status_code}")
        raise requests.HTTPError(res)
    return ServiceRequests(service_requests=res.json())
