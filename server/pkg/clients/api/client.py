from typing import Dict, Any, Literal, Tuple

import pydantic
from aiohttp import ClientSession
from pydantic import PositiveInt

from server.pkg.models.exceptions.api import UnexpectedStatus

__all__ = ["ChatApiClient"]


class ChatApiClient:
    """Client for chat api."""

    def __init__(
        self,
        base_url: pydantic.AnyUrl,
    ):
        self._client = ClientSession(base_url=base_url)

    @staticmethod
    def __set_auth(kwargs: Dict[str, Any]) -> Dict[str, Any]:
        if auth := kwargs.pop("auth", None):
            headers = kwargs.get("headers", {})
            headers['Authorization'] = f"Bearer {auth}"
            kwargs.setdefault("headers", headers)
        return kwargs

    async def make_request(
        self,
        path: str,
        method: Literal["POST", "GET", "PUT", "DELETE"],
        valid_status: Tuple[PositiveInt] = (200, 201, 204),
        **kwargs
    ) -> Dict[str, Any]:
        """Make request to chat api."""
        async with self._client.request(method, path, **self.__set_auth(kwargs)) as response:
            if response.status not in valid_status:
                raise UnexpectedStatus(
                    message=f"Unexpected status code: {response.status} {response.reason}"
                )
            return await response.json()

    def __del__(self):
        self._client.close()

    async def __aenter__(self) -> "ChatApiClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._client.close()
