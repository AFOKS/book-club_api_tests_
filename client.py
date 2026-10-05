import requests

from config import BASE_URL, TIMEOUT


class ApiClient(requests.Session):
    """Session с базовым URL, таймаутом по умолчанию и заголовком Accept."""

    def __init__(self, base_url: str = BASE_URL):
        super().__init__()
        self.base_url = base_url
        self.headers["Accept"] = "application/json"

    def request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", TIMEOUT)
        return super().request(method, f"{self.base_url}{url}", **kwargs)