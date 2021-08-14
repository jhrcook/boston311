from datetime import datetime, timedelta

import pytest
from requests import HTTPError

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
def test_get_service_request_fails():
    fake_service_code = "A!"
    with pytest.raises(HTTPError):
        api.get_service_request(fake_service_code)


@pytest.mark.network
def test_get_service_request():
    my_service_request_id = "101003914012"
    service_req = api.get_service_request(my_service_request_id)
    assert service_req is not None
    assert service_req.service_request_id == my_service_request_id
    assert service_req.address == "335 Gallivan Blvd, 1, Dorchester"
    assert service_req.service_name == "Dead Animal Pick-up"
    assert service_req.address_id is None
    assert service_req.media_url is None


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
        [datetime.now() - timedelta(days=5), True],
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
        [datetime.now() - timedelta(days=6), False],
        [datetime.now(), True],
    ),
)
def test_get_service_requests_with_end(end_date: datetime, more_than_zero: bool):
    start_date = datetime.now() - timedelta(days=5)
    services_req = api.get_service_requests(start_date=start_date, end_date=end_date)
    assert (len(services_req.service_requests) > 0) == more_than_zero


@pytest.mark.network
@pytest.mark.parametrize("status", Status)
def test_get_service_requests_with_status(status: Status):
    services_req = api.get_service_requests(status=status)
    assert len(services_req.service_requests) > 0
