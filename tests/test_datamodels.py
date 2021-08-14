import factory
import faker

import boston311.datamodels as dm

fake = faker.Faker()


class ServiceFactory(factory.Factory):
    class Meta:
        model = dm.Service

    version = 1
    description = factory.Sequence(lambda n: fake.paragraph())
    group = factory.Sequence(lambda n: fake.company())
    metadata = fake.pybool()
    service_code = factory.Sequence(lambda n: fake.iban())
    service_name = factory.Sequence(lambda n: fake.bs() + f" ({n})")
    type = factory.Sequence(lambda n: fake.bs() + f" ({n})")


class ServicesFactory(factory.Factory):
    class Meta:
        model = dm.Services

    version = fake.pyint()
    services = [ServiceFactory() for _ in range(11)]


#### ---- Service model ---- ####


def test_service_str():
    service = ServiceFactory()
    assert isinstance(service, dm.Service)
    service_str = str(service)
    assert isinstance(service_str, str)


def test_service_hash():
    service = ServiceFactory()
    assert isinstance(service, dm.Service)
    service_hash = hash(service)
    assert service_hash != service.service_code
    assert isinstance(service_hash, int)


#### ---- Services model ---- ####


def test_services_len():
    services = ServicesFactory()
    assert isinstance(services, dm.Services)
    assert len(services) == len(services.services)


def test_services_getitem():
    services = ServicesFactory()
    assert isinstance(services, dm.Services)
    for i in range(len(services)):
        assert services[i] == services.services[i]


def test_list_service_names():
    services = ServicesFactory()
    assert isinstance(services, dm.Services)
    names_list = services.list_service_names()
    assert len(names_list) == len(services)
    assert all([isinstance(n, str) for n in names_list])


def test_get_service_code():
    services = ServicesFactory()
    fake_service = ServiceFactory()
    assert isinstance(services, dm.Services) and isinstance(fake_service, dm.Service)
    fake_service.service_code = "123"
    fake_service.service_name = "Josh"
    services.services.append(fake_service)
    assert services.get_service_code("Josh") == "123"


def test_get_service_id():
    services = ServicesFactory()
    fake_service = ServiceFactory()
    assert isinstance(services, dm.Services) and isinstance(fake_service, dm.Service)
    fake_service.service_code = "123"
    fake_service.service_name = "Josh"
    services.services.append(fake_service)
    assert services.get_service_name("123") == "Josh"
