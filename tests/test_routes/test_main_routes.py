import pytest
import httpx
from httpx import ASGITransport
from app.main import app # Import your FastHTML app instance

@pytest.mark.asyncio
async def test_home_page_full_load():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_change_page_htmx_fragment():
    htmx_headers = {
        "HX-Request": "true",
        "HX-Target": "main-content",
    }

    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/change", headers=htmx_headers)

    assert response.status_code == 200
    # Assertions for FRAGMENT structure
    assert "<!DOCTYPE html>" not in response.text # Should NOT be a full page
    assert "<title>" not in response.text
    assert "<body" not in response.text
    assert "<header" not in response.text # HeaderBar should NOT be in the fragment
    