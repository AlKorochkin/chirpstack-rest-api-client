from typing import Any, AsyncGenerator
from pydantic import HttpUrl, computed_field
from pydantic_core import Url
import pytest
from pydantic_settings import BaseSettings
from chirpstack_rest_api_client.schemas.applications import (
    Application,
    CreateApplicationRequest,
)
from chirpstack_rest_api_client.schemas.device_profiles import (
    CreateDeviceProfileRequest,
    DeviceProfile,
)
from chirpstack_rest_api_client.services.devices import DeviceClient
from chirpstack_rest_api_client.services.gateways import GatewayClient
from chirpstack_rest_api_client.services.tenants import TenantClient
from chirpstack_rest_api_client.services.applications import ApplicationClient
from chirpstack_rest_api_client.services.device_profiles import DeviceProfileClient

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    CHIRPSTACK_BASEURL: str = "http://localhost:8090"
    API_KEY: str = "api_key_secret"
    HTTP_INTEGRATION_HEADER: str = "X-API-KEY"
    HTTP_INTEGRATION_KEY: str = "api_key_secret"

    @computed_field
    @property
    def HTTP_INTEGRATION_HEADERS(self) -> dict:
        return {self.HTTP_INTEGRATION_HEADER: self.HTTP_INTEGRATION_KEY}


settings = Settings()


@pytest.fixture
def get_settings() -> Settings:
    return Settings()


@pytest.fixture(scope="function")
async def tenant_client(get_settings) -> AsyncGenerator[TenantClient, Any]:
    async with TenantClient(
        get_settings.CHIRPSTACK_BASEURL, get_settings.API_KEY
    ) as cli:
        yield cli


@pytest.fixture(scope="function")
async def application_client(get_settings) -> AsyncGenerator[ApplicationClient, Any]:
    async with ApplicationClient(
        get_settings.CHIRPSTACK_BASEURL, get_settings.API_KEY
    ) as cli:
        yield cli


@pytest.fixture(scope="function")
async def device_profile_client(
    get_settings,
) -> AsyncGenerator[DeviceProfileClient, Any]:
    async with DeviceProfileClient(
        get_settings.CHIRPSTACK_BASEURL, get_settings.API_KEY
    ) as cli:
        yield cli


@pytest.fixture(scope="function")
async def gateway_client(get_settings) -> AsyncGenerator[GatewayClient, Any]:
    async with GatewayClient(
        get_settings.CHIRPSTACK_BASEURL, get_settings.API_KEY
    ) as cli:
        yield cli


@pytest.fixture(scope="function")
async def device_client(get_settings) -> AsyncGenerator[DeviceClient, Any]:
    async with DeviceClient(
        get_settings.CHIRPSTACK_BASEURL, get_settings.API_KEY
    ) as cli:
        yield cli


@pytest.fixture(scope="function")
async def get_default_tenant_id(tenant_client: TenantClient):
    response_get_tenants = await tenant_client.get_tenants(search="ChirpStack")
    tenant_id = (
        response_get_tenants.result[0].id if response_get_tenants.result else None
    )
    return tenant_id


@pytest.fixture(scope="function")
async def create_application(
    application_client: ApplicationClient,
    get_default_tenant_id,
):
    tenant_id = get_default_tenant_id
    create_application_request = CreateApplicationRequest(
        application=Application(
            name="TestApplication",
            tenantId=tenant_id,
        )
    )
    create_application_response = await application_client.create_application(
        create_application_request
    )
    return create_application_response.id


@pytest.fixture(scope="function")
async def create_device_profile(
    device_profile_client: DeviceProfileClient,
    get_default_tenant_id,
):
    tenant_id = get_default_tenant_id
    create_device_profile_request = CreateDeviceProfileRequest(
        deviceProfile=DeviceProfile(
            name="TestDeviceProfile",
            tenantId=tenant_id,
        )
    )
    create_device_profile_response = await device_profile_client.create_device_profile(
        create_device_profile_request
    )
    return create_device_profile_response.id
