"""
The discovery to start simple.

The static discovery strategy is a good start when you don't need a strategy.

For instance, a short list of services with static endpoint.
"""
from typing import Mapping

from aioli.domain.exceptions import UnregisteredServiceException
from aioli.typing import Service, ServiceName, Version

from ..base import AbtractServiceDiscovery, Url

Endpoints = Mapping[Service, Url]


class StaticDiscovery(AbtractServiceDiscovery):
    """
    A discovery instance based on a static dictionary.
    """

    endpoints: Endpoints

    def __init__(self, endpoints: Endpoints) -> None:
        self.endpoints = endpoints

    async def get_endpoint(self, service: ServiceName, version: Version) -> Url:
        """
        Retrieve endpoint using the given parameters from `endpoints`.
        """
        try:
            return self.endpoints[(service, version)]
        except KeyError:
            raise UnregisteredServiceException(service, version)
