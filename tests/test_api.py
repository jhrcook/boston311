import pytest

from boston311 import api


@pytest.mark.network
def test_get_services():
    services = api.get_services()
    assert len(services.services) > 1


@pytest.mark.network
def test_get_service_requests():
    services_req = api.get_service_requests()
    assert len(services_req.service_requests) > 1
