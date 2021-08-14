"""Interacting with the Boston 311 API."""

import requests

from .constants import BOSTON_API_ENDPOINT
from .datamodels import ServiceRequests, Services


def get_services() -> Services:
    res = requests.get(BOSTON_API_ENDPOINT + "services.json")
    if res.status_code != 200:
        raise requests.HTTPError(res)
    return Services(services=res.json())


def get_service_requests() -> ServiceRequests:
    params: dict[str, str] = {
        "end_date": "2021-08-12T00:00:00Z",
        "service_code": "4f38920fe75084437f0001a0",
        "status": "open",
    }
    res = requests.get(BOSTON_API_ENDPOINT + "requests.json", params=params)
    if res.status_code != 200:
        print(f"Failed request - status code {res.status_code}")
        raise requests.HTTPError(res)
    return ServiceRequests(service_requests=res.json())
