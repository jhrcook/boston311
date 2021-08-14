"""Custom error types."""


class UnexpectedNumberOfResultsError(BaseException):
    """Unexpected number of results error."""

    def __init__(self, n_expected: int, n_received: int) -> None:
        """Initialize an UnexpectedNumberOfResultsError error.

        Args:
            n_expected (int): Number of expected results.
            n_received (int): Number of received results.
        """
        self.n_expected = n_expected
        self.n_received = n_received
        self.message = f"Expected {n_expected} but received {n_received}"
        super().__init__(self.message)
