# Boston's 311 Service API

**Python package for interfacing with Boston 311 API.**

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=FFFF9A)](https://www.python.org)
[![pytest](https://github.com/jhrcook/boston311/actions/workflows/test.yaml/badge.svg)](https://github.com/jhrcook/boston311/actions/workflows/test.yaml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

I recently made a request to have some graffiti removed by the city of Boston and used their 311 service for reporting non-emergency crimes.
I found it an interesting service and  decided to look closer into it.
They provide an free API for the service, so I decided to make this Python package to interface with the API.

## Quick start

### Installation

Install the `boston311` package through PyPI.

```bash
pip install boston311
```

### Features

Below are features of this package:

1. Get a collection of all services offered by Boston 311.
2. Get a collection of all service requests with some useful filters.
3. Get information for a specific service request.

All underlying data models were **parsed and validated with ['pydantic'](https://pydantic-docs.helpmanual.io)** so there is increased type safety and helpful hints for your IDE.

### Examples

#### Collection of available services

Use the `get_services()` function to get a collection of all of the available services offered through the 311 service.
The returned object contains a field `services` which is a list of the services.

In the example below, I make the request, show how many services are available, and print out the third service in the list.
Finally, I demonstrate a convenience method I added to make a list of the names of the services.

```python
import boston311

available_services = boston311.get_services()

print(available_services)
#> 22 available services
type(available_services)
#> <class 'boston311.datamodels.Services'>
len(available_services)
#> 22
print(available_services[2])
#> {
#>      'description': 'Graffiti Removal Request',
#>      'group': 'Illegal Graffiti',
#>      'metadata': 'True',
#>      'service_code': '4f38920fe75084437f0001b3',
#>      'service_name': 'Illegal Graffiti',
#>      'type': 'batch',
#>      'version': 1
#> }
print(available_services.list_service_names())
#> ['Residential Trash out Illegally', 'Broken Sidewalk', ..., 'Abandoned Vehicle']
```

#### Collection of service requests

It is easy to get a collection of all service requests made in the last 90 days (the default date range).
There are also some useful [filters](https://jhrcook.github.io/boston311/api.html#boston311.api.get_service_requests) for indicating types of service requests, date ranges, and the status of the request.

```python
import boston311

service_requests = boston311.get_service_requests()
print(service_requests)
#> 50 service requests
```

#### Information for a known service request

Finally, it is very fast to get the information for a single known service request.
Below is an example of a random request I found on the website.

```python
import boston311

service_request = boston311.get_service_request("101003914012")
print(service_request)
#> {
#>    'address': '335 Gallivan Blvd, 1, Dorchester',
#>    'address_id': None,
#>    'agency_responsible': None,
#>    'description': 'Dead cat',
#>    'expected_datetime': None,
#>    'lat': 42.28033447265625,
#>    'long': -71.06434967989543,
#>    'media_url': None,
#>    'requested_datetime': datetime.datetime(2021, 8, 14, 12, 19, 13, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000))),
#>    'service_code': '4f389210e75084437f0001c4',
#>    'service_name': 'Dead Animal Pick-up',
#>    'service_notice': None,
#>    'service_request_id': '101003914012',
#>    'status': <Status.OPEN: 'open'>,
#>    'status_notes': None,
#>    'updated_datetime': datetime.datetime(2021, 8, 14, 12, 19, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000))),
#>    'version': 1,
#>    'zipcode': None
#>}
```

### Limitations

There are some parts of the API that I have not included in this package (e.g. the ability to make a new service request submission) because I do not currently need them.
However, they are likely simple enough to add, so if you want them, either implement them yourself and submit a PR or open and [Issue](https://github.com/jhrcook/boston311/issues) and I will eventually take care of it.

## API Documentation

Below are links to the documentation for the original API.

- [API website](https://mayors24.cityofboston.gov/open311)
- [API docs](http://wiki.open311.org/GeoReport_v2/)
