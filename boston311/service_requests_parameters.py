"""Data model for handling logic in parameters of a 'service requests' request."""

from datetime import datetime, timezone
from typing import Optional

from .datamodels import Status
from .formatting import format_in_utc


class ServiceRequestsParameters:
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
        """Create a ServiceRequestParameters object.

        Args:
            service_code (Optional[str]): Service code.
            start_date (Optional[datetime]): Start date.
            end_date (Optional[datetime]): End date.
            status (Optional[Status]): Status.
        """
        self.service_code = service_code
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def get_params(self) -> dict[str, str]:
        """Get a dictionary of the parameters for the request.

        Returns:
            dict[str, str]: Dictionary of parameters to be used in GET.
        """
        if self.end_date is None and self.start_date is not None:
            self.end_date = datetime.now(tz=timezone.utc)

        params: dict[str, str] = {}

        if self.service_code is not None:
            params["service_code"] = self.service_code
        if self.start_date is not None:
            params["start_date"] = format_in_utc(self.start_date)
        if self.end_date is not None:
            params["end_date"] = format_in_utc(self.end_date)
        if self.status is not None:
            params["status"] = self.status

        return params
