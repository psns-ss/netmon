import logging
from typing import Any, List

import structlog

from app import crud, models, schemas
from app.api import deps
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

logger = structlog.get_logger()

router = APIRouter()


@router.get("/", response_model=List[schemas.Machine])
def read_machines(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve machines.
    """
    machines = crud.machine.get_multi(db, skip=skip, limit=limit)
    return machines


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
    logger.info("updating machine")
    machine = crud.machine.update(db=db, db_obj=machine, obj_in=machine_in)
    return machine


@router.get("/{id}", response_model=schemas.Machine)
def read_machine(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get machine by ID.
    """
    machine = crud.machine.get(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")
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
    response_model=List[schemas.ActiveProcess],
    dependencies=[Depends(deps.get_current_active_user)],
)
def get_machine_active_processes(*, id: int, db: Session = Depends(deps.get_db)):
    """
    Get machine active processes
    """
    machine = crud.machine.get(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")

    return [schemas.ActiveProcess(hash="nkaflfaknl", name="test")]


@router.get(
    "/{id}/interfaces",
    response_model=List[schemas.Interface],
    dependencies=[Depends(deps.get_current_active_user)],
)
def get_machine_interfaces(*, id: int, db: Session = Depends(deps.get_db)):
    """
    Get machine interfaces
    """
    machine = crud.machine.get(db=db, id=id)
    if not machine:
        raise HTTPException(status_code=404, detail="machine not found")

    return [schemas.Interface(name="test")]
