import pytest

from converter.api.main import create_app


@pytest.fixture()
async def api_client(aiohttp_client):
    app = create_app()
    client = await aiohttp_client(app)

    try:
        yield client
    finally:
        await client.close()
