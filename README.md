# chirpstack-rest-api-client

Клиент для обращения к REST API Chirpstack на основе httpx и pydantic.

Содержит готовые клиенты с реализованными методами и pydantic-схемы для следующих сервисов:
- TenantService
- GatewayService
- DeviceService
- DeviceProfileService
- ApplicationService

Установка:

```
pip install chirpstack-rest-api-client
```

Пример использования:

```python
from chirpstack_rest_api_client.services.tenants import TenantClient


api_key = "chirpstack_global_api_key"
base_url = "http://localhost:8090"

async def run():
    async with TenantClient(base_url, api_key) as cli:
        tenants_list = await cli.get_tenants(limit=10)
        if tenants_list.totalCount > 0:
            print(f"Tenants: {tenants_list.result}")

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())        
```