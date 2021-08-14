from datetime import datetime, timedelta

import pytest

from boston311 import api
from boston311.datamodels import Status


@pytest.mark.network
def test_get_services():
    services = api.get_services()
    assert len(services.services) > 1


@pytest.mark.network
def test_get_service_requests():
    services_req = api.get_service_requests()
    assert len(services_req.service_requests) > 1


@pytest.mark.network
@pytest.mark.parametrize(
    "service_code, more_than_zero", (["AAA", False], ["4f389210e75084437f0001ce", True])
)
def test_get_service_requests_with_code(service_code: str, more_than_zero: bool):
    services_req = api.get_service_requests(service_code=service_code)
    assert (len(services_req.service_requests) > 0) == more_than_zero


@pytest.mark.network
@pytest.mark.parametrize(
    "start_date, more_than_zero",
    (
        [datetime.now() - timedelta(days=10), True],
        [datetime.now() + timedelta(days=3), False],
    ),
)
def test_get_service_requests_with_start(start_date: datetime, more_than_zero: bool):
    services_req = api.get_service_requests(start_date=start_date)
    assert (len(services_req.service_requests) > 0) == more_than_zero


@pytest.mark.network
@pytest.mark.parametrize(
    "end_date, more_than_zero",
    (
        [datetime.now() - timedelta(days=11), False],
        [datetime.now(), True],
    ),
)
def test_get_service_requests_with_end(end_date: datetime, more_than_zero: bool):
    start_date = datetime.now() - timedelta(days=10)
    services_req = api.get_service_requests(start_date=start_date, end_date=end_date)
    assert (len(services_req.service_requests) > 0) == more_than_zero


@pytest.mark.network
@pytest.mark.parametrize("status", Status)
def test_get_service_requests_with_status(status: Status):
    services_req = api.get_service_requests(status=status)
    assert len(services_req.service_requests) > 0
