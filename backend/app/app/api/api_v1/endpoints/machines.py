import time
from pathlib import Path
from typing import Any, List

import aiohttp
import app.schemas.machine_interface
import app.schemas.machine_process
import structlog
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_email
from fastapi import APIRouter, Depends, HTTPException, requests
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
    response_model=List[app.schemas.machine_process.MachineProcess],
    dependencies=[Depends(deps.get_current_active_user)],
)
async def get_machine_active_processes(*, id: int, db: Session = Depends(deps.get_db)):
    """
    Get machine active processes
    """
    machine = crud.machine.get(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")

    return await crud.machine_process.get_multi_with_poll(db, machine.id)


@router.put(
    "/{machine_id}/active-processes/{id}",
    response_model=app.schemas.machine_process.MachineProcess,
    dependencies=[Depends(deps.get_current_active_user)],
)
async def update_machine_process(
    *,
    machine_id: int,
    id: int,
    machine_process_in: schemas.MachineProcessUpdate,
    db: Session = Depends(deps.get_db),
):
    """
    Update machine active process
    """
    machine_process = crud.machine_process.get_by_machine(
        db=db, id=id, machine_id=machine_id
    )
    if not machine_process:
        raise HTTPException(status_code=404, detail="machine process not found")

    machine_process = crud.machine_process.update(
        db=db, db_obj=machine_process, obj_in=machine_process_in
    )
    return machine_process


@router.get(
    "/{id}/interfaces",
    response_model=List[schemas.MachineInterface],
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
                client_machine_interfaces = await resp.json()
                logger.debug(
                    f"get machine active processes success",
                    status=resp.status,
                    machine_id=machine.id,
                    machine_host=machine.host,
                    url=url,
                    machine_interfaces=client_machine_interfaces,
                )
                return [
                    schemas.MachineInterfaceFromClient(**mi).dict()
                    for mi in client_machine_interfaces
                ]

        except Exception as e:
            logger.debug(
                f"{e}: get machine interfaces failed",
                machine_id=machine.id,
                machine_host=machine.host,
                url=url,
            )
            raise HTTPException(status_code=400, detail="host is not available")


@router.get("/{id}/ping", dependencies=[Depends(deps.get_current_active_user)])
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


@router.post("/new-adapter")
async def detected_new_adapter(
    new_adapter: schemas.NewAdapter, request: requests.Request
):
    client_host = request.client.host

    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New Adapter"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_adapter.html") as f:
        template_str = f.read()
    email_to = settings.FIRST_SUPERUSER
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": project_name,
            "new_adapter": new_adapter.new_adapter,
            "client_host": client_host,
        },
    )
