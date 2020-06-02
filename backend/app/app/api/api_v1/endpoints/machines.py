import time
from typing import Any, List

import aiohttp
import structlog
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

logger = structlog.get_logger()

router = APIRouter()


@router.get("/", response_model=List[schemas.MachineWithOnlineStatus])
async def read_machines(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve machines.
    """
    machines = await crud.machine.get_multi_with_check_online(
        db, skip=skip, limit=limit
    )
    return [
        schemas.MachineWithOnlineStatus(
            **schemas.MachineInDB.from_orm(machine).dict(),
            was_recently_online=was_recently_online(machine),
        )
        for machine in machines
    ]


@router.post("/", response_model=schemas.Machine)
def create_machine(
    *,
    db: Session = Depends(deps.get_db),
    machine_in: schemas.MachineCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new machine.
    """
    machine = crud.machine.create(db=db, obj_in=machine_in)
    return machine


@router.get("/{id}", response_model=schemas.MachineWithOnlineStatus)
async def read_machine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get machine by ID.
    """
    machine = await crud.machine.get_with_check_online(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")

    return schemas.MachineWithOnlineStatus(
        **schemas.MachineInDB.from_orm(machine).dict(),
        was_recently_online=was_recently_online(machine),
    )


def was_recently_online(machine: models.Machine) -> bool:
    if not machine.last_online_timestamp:
        return False

    delta_between_last_online = int(time.time()) - machine.last_online_timestamp
    return delta_between_last_online <= settings.WAS_RECENTLY_ONLINE_TIMEDELTA


@router.put("/{id}", response_model=schemas.Machine)
def update_machine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    machine_in: schemas.MachineUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an machine.
    """
    machine = crud.machine.get(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")
    logger.info("updating machine", machine_in=machine_in)
    machine = crud.machine.update(db=db, db_obj=machine, obj_in=machine_in)
    return machine


@router.delete("/{id}", response_model=schemas.Machine)
def delete_machine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an machine.
    """
    machine = crud.machine.get(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")
    machine = crud.machine.remove(db=db, id=id)
    return machine


@router.get(
    "/{id}/active-processes",
    response_model=List[schemas.MachineActiveProcess],
    response_model_by_alias=False,
    dependencies=[Depends(deps.get_current_active_user)],
)
async def get_machine_active_processes(*, id: int, db: Session = Depends(deps.get_db)):
    """
    Get machine active processes
    """
    machine = crud.machine.get(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")

    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout, raise_for_status=True) as session:
        url = f"{machine.host}/active-processes"
        try:
            async with session.get(url) as resp:
                machine.last_online_timestamp = int(time.time())
                machine_active_processes = await resp.json()
                logger.debug(
                    f"get machine active processes success",
                    status=resp.status,
                    machine_id=machine.id,
                    machine_host=machine.host,
                    url=url,
                    machine_active_processes=machine_active_processes,
                )
                return machine_active_processes

        except Exception as e:
            logger.debug(
                f"{e}: get machine active processes failed",
                machine_id=machine.id,
                machine_host=machine.host,
                url=url,
            )
            raise HTTPException(status_code=400, detail="host is not available")


@router.get(
    "/{id}/interfaces",
    response_model=List[schemas.MachineInterface],
    response_model_by_alias=False,
    dependencies=[Depends(deps.get_current_active_user)],
)
async def get_machine_interfaces(*, id: int, db: Session = Depends(deps.get_db)):
    """
    Get machine interfaces
    """
    machine = crud.machine.get(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")

    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout, raise_for_status=True) as session:
        url = f"{machine.host}/interfaces"
        try:
            async with session.get(url) as resp:
                machine.last_online_timestamp = int(time.time())
                machine_interfaces = await resp.json()
                logger.debug(
                    f"get machine active processes success",
                    status=resp.status,
                    machine_id=machine.id,
                    machine_host=machine.host,
                    url=url,
                    machine_interfaces=machine_interfaces,
                )
                return machine_interfaces

        except Exception as e:
            logger.debug(
                f"{e}: get machine interfaces failed",
                machine_id=machine.id,
                machine_host=machine.host,
                url=url,
            )
            raise HTTPException(status_code=400, detail="host is not available")


@router.get("/{id}/ping")
async def ping_machine(*, id: int, db: Session = Depends(deps.get_db)):
    machine = crud.machine.get(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")

    timeout = aiohttp.ClientTimeout(total=5)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{machine.host}/ping") as resp:
                resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
