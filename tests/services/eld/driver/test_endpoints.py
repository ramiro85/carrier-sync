import pytest
from fastapi import HTTPException

from app.services.eld.driver.endpoints import (
    activate_driver,
    create_driver,
    deactivate_driver,
    delete_driver,
    get_driver,
    list_drivers,
    update_driver,
)
from app.services.eld.driver.schemas import DriverCreateRequest, DriverUpdateRequest


class FakeELDController:
    def create_driver(self, driver_id, driver_data):
        return {"ok": True, "driver_id": driver_id, "email": driver_data.email}

    def get_driver(self, driver_id):
        return {"ok": True, "driver_id": driver_id}

    def update_driver(self, driver_id, driver_data, rev=None):
        return {
            "ok": True,
            "driver_id": driver_id,
            "rev": rev,
            "active": driver_data.active,
        }

    def delete_driver(self, driver_id, rev=None):
        return {"ok": True, "driver_id": driver_id, "rev": rev}

    def list_drivers(self, company_id, limit, skip):
        return {"ok": True, "company_id": company_id, "limit": limit, "skip": skip}

    def activate_driver(self, driver_id, rev=None):
        return {"ok": True, "driver_id": driver_id, "active": True, "rev": rev}

    def deactivate_driver(self, driver_id, rev=None):
        return {"ok": True, "driver_id": driver_id, "active": False, "rev": rev}


class FailingController(FakeELDController):
    def create_driver(self, driver_id, driver_data):
        raise RuntimeError("boom")


def _driver_payload() -> dict:
    return {
        "companyId": "company-1",
        "createdBy": "system",
        "email": "driver@example.com",
        "firstName": "First",
        "lastName": "Last",
        "active": True,
        "driverInfo": {
            "companyDriverId": "DRV-1",
            "licenseNumber": "L123",
            "licenseState": {"id": "TX"},
            "homeTerminal": {"id": "TERM-1"},
            "hosSettings": {
                "cycle": {"id": "USA 70 hour / 8 day"},
                "cargoType": {"id": "CARGO"},
                "restartHours": {"id": "34 Hour Restart"},
                "restBreak": {"id": "30 Minute Rest Break Required"},
            },
            "avi": [],
        },
        "ou": {"id": "TX"},
    }


@pytest.mark.asyncio
async def test_create_driver_endpoint():
    result = await create_driver(
        driver_id="User:abc",
        driver_data=DriverCreateRequest.model_validate(_driver_payload()),
        controller=FakeELDController(),
    )

    assert result["driver_id"] == "User:abc"


@pytest.mark.asyncio
async def test_get_driver_endpoint():
    result = await get_driver("User:abc", FakeELDController())
    assert result["driver_id"] == "User:abc"


@pytest.mark.asyncio
async def test_update_driver_endpoint():
    result = await update_driver(
        driver_id="User:abc",
        driver_data=DriverUpdateRequest(active=False),
        rev="1-a",
        controller=FakeELDController(),
    )

    assert result["rev"] == "1-a"
    assert result["active"] is False


@pytest.mark.asyncio
async def test_delete_driver_endpoint():
    result = await delete_driver("User:abc", "1-a", FakeELDController())
    assert result["rev"] == "1-a"


@pytest.mark.asyncio
async def test_list_drivers_endpoint():
    result = await list_drivers("company-1", 10, 5, FakeELDController())
    assert result["limit"] == 10
    assert result["skip"] == 5


@pytest.mark.asyncio
async def test_activate_driver_endpoint():
    result = await activate_driver("User:abc", "2-a", FakeELDController())
    assert result["active"] is True


@pytest.mark.asyncio
async def test_deactivate_driver_endpoint():
    result = await deactivate_driver("User:abc", "3-a", FakeELDController())
    assert result["active"] is False


@pytest.mark.asyncio
async def test_create_driver_raises_http_400_on_exception():
    with pytest.raises(HTTPException) as exc:
        await create_driver(
            driver_id="User:abc",
            driver_data=DriverCreateRequest.model_validate(_driver_payload()),
            controller=FailingController(),
        )

    assert exc.value.status_code == 400
