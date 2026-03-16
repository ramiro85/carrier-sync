from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.services.eld.dependencies import get_eld_controller
from app.services.eld.driver.schemas import DriverCreateRequest, DriverUpdateRequest, DriverResponse
from app.services.eld.driver.controller import ELDDriverController

router = APIRouter(
    prefix="/api/eld/drivers",
    tags=["ELD Drivers"]
)


@router.post("/{driver_id}", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_driver(
        driver_id: str,
        driver_data: DriverCreateRequest,
        controller: ELDDriverController = Depends(get_eld_controller)
):
    """
    Create a new driver in the ELD system.

    - **driver_id**: Unique identifier for the driver (e.g., "User:ebIdZ-83s")
    - **driver_data**: Complete driver information including driverInfo, hosSettings, etc.
    """
    try:
        result = controller.create_driver(driver_id, driver_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create driver: {str(e)}"
        )


@router.get("/{driver_id}", response_model=Dict[str, Any])
async def get_driver(
        driver_id: str,
        controller: ELDDriverController = Depends(get_eld_controller)
):
    """
    Retrieve driver information by ID.

    - **driver_id**: Unique identifier for the driver
    """
    try:
        result = controller.get_driver(driver_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver not found: {str(e)}"
        )


@router.put("/{driver_id}", response_model=Dict[str, Any])
async def update_driver(
        driver_id: str,
        driver_data: DriverUpdateRequest,
        rev: str = None,
        controller: ELDDriverController = Depends(get_eld_controller)
):
    """
    Update an existing driver.

    - **driver_id**: Unique identifier for the driver
    - **driver_data**: Updated driver information (only include fields to update)
    - **rev**: Optional document revision
    """
    try:
        result = controller.update_driver(driver_id, driver_data, rev)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update driver: {str(e)}"
        )


@router.delete("/{driver_id}", response_model=Dict[str, Any])
async def delete_driver(
        driver_id: str,
        rev: str = None,
        controller: ELDDriverController = Depends(get_eld_controller)
):
    """
    Delete (deactivate) a driver.

    - **driver_id**: Unique identifier for the driver
    - **rev**: Optional document revision
    """
    try:
        result = controller.delete_driver(driver_id, rev)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete driver: {str(e)}"
        )


@router.get("/company/{company_id}", response_model=Dict[str, Any])
async def list_drivers(
        company_id: str,
        limit: int = 100,
        skip: int = 0,
        controller: ELDDriverController = Depends(get_eld_controller)
):
    """
    List all drivers for a company.

    - **company_id**: Company identifier
    - **limit**: Maximum number of drivers to return (default: 100)
    - **skip**: Number of drivers to skip for pagination (default: 0)
    """
    try:
        result = controller.list_drivers(company_id, limit, skip)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to list drivers: {str(e)}"
        )


@router.patch("/{driver_id}/activate", response_model=Dict[str, Any])
async def activate_driver(
        driver_id: str,
        rev: str = None,
        controller: ELDDriverController = Depends(get_eld_controller)
):
    """
    Activate a driver.

    - **driver_id**: Unique identifier for the driver
    - **rev**: Optional document revision
    """
    try:
        result = controller.activate_driver(driver_id, rev)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to activate driver: {str(e)}"
        )


@router.patch("/{driver_id}/deactivate", response_model=Dict[str, Any])
async def deactivate_driver(
        driver_id: str,
        rev: str = None,
        controller: ELDDriverController = Depends(get_eld_controller)
):
    """
    Deactivate a driver.

    - **driver_id**: Unique identifier for the driver
    - **rev**: Optional document revision
    """
    try:
        result = controller.deactivate_driver(driver_id, rev)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to deactivate driver: {str(e)}"
        )
