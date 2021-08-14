"""Interacting with the Boston 311 API."""
from datetime import datetime
from typing import Optional

import requests

from .constants import BOSTON_API_ENDPOINT
from .datamodels import ServiceRequest, ServiceRequests, Services, Status
from .exceptions import UnexpectedNumberOfResultsError
from .service_requests_parameters import ServiceRequestsParameters


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


def get_service_request(service_request_id: str) -> Optional[ServiceRequest]:
    """Query the current status of an individual request.

    Args:
        service_request_id (str): Service request ID.

    Returns:
        ServiceRequest: The service request information.
    """
    res = requests.get(BOSTON_API_ENDPOINT + f"requests/{service_request_id}.json")
    if res.status_code != 200:
        raise requests.HTTPError(res)
    results = res.json()
    if len(results) == 0:
        return None
    elif len(results) > 1:
        raise UnexpectedNumberOfResultsError(n_expected=1, n_received=len(results))
    return ServiceRequest(**results[0])


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
    params = ServiceRequestsParameters(
        service_code=service_code,
        start_date=start_date,
        end_date=end_date,
        status=status,
    ).get_params()

    res = requests.get(BOSTON_API_ENDPOINT + "requests.json", params=params)
    if res.status_code != 200:
        raise requests.HTTPError(res)
    return ServiceRequests(service_requests=res.json())
