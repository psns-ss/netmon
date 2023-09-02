import time
from typing import List, Optional

import aiohttp
import structlog
from app import crud, schemas
from app.crud.base import CRUDBase
from app.models import MachineProcess
from app.schemas import MachineProcessCreate, MachineProcessUpdate
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

logger = structlog.get_logger()


class CRUDMachineProcess(
    CRUDBase[MachineProcess, MachineProcessCreate, MachineProcessUpdate]
):
    def create_with_machine(
        self, db: Session, *, obj_in: MachineProcessCreate, machine_id: int
    ) -> MachineProcess:

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, machine_id=machine_id)  # noqa type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_machine(
        self, db: Session, *, id: int, machine_id: int
    ) -> Optional[MachineProcess]:
        return (
            db.query(self.model)
            .filter(self.model.id == id)
            .filter(self.model.machine_id == machine_id)
            .first()
        )

    async def get_multi_with_poll(
        self, db: Session, machine_id: int
    ) -> List[MachineProcess]:
        machine = crud.machine.get(db, machine_id)
        if not machine:
            raise ValueError(machine_id)

        try:
            client_processes = await poll_machine_interfaces(host=machine.host)
        except Exception as e:
            logger.warning(f"failed to poll machine: {e}")
            return []

        machine.last_online_timestamp = int(time.time())
        db.add(machine)
        db.refresh(machine)

        for client_process in client_processes:
            db_obj = self.get_by_machine(
                db, id=client_process.id, machine_id=machine_id
            )
            if db_obj:
                logger.debug("updating existing process")
                if not db_obj.is_hash_same:
                    is_hash_same = False
                else:
                    is_hash_same = client_process.hash == db_obj.hash

                self.update(
                    db,
                    db_obj=db_obj,
                    obj_in=MachineProcessUpdate(
                        id=client_process.id,
                        name=client_process.name,
                        path=client_process.path,
                        hash=client_process.hash,
                        is_hash_same=is_hash_same,
                    ),
                )
            else:
                logger.debug("creating machine process")
                self.create_with_machine(
                    db,
                    obj_in=MachineProcessCreate(
                        id=client_process.id,
                        name=client_process.name,
                        path=client_process.path,
                        hash=client_process.hash,
                    ),
                    machine_id=machine_id,
                )

        db.commit()
        db.refresh(machine)

        return machine.processes


async def poll_machine_interfaces(host: str) -> List[schemas.MachineProcessFromClient]:
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout, raise_for_status=True) as session:
        url = f"{host}/active-processes"
        async with session.get(url) as resp:
            logger.debug(f"polled machine processes", host=host)
            return [
                schemas.MachineProcessFromClient(**process)
                for process in await resp.json()
            ]


machine_process = CRUDMachineProcess(MachineProcess)
