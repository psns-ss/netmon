import time
from typing import List, cast

import aiohttp
import structlog
from app.crud.base import CRUDBase
from app.models.machine import Machine
from app.schemas.machine import MachineCreate, MachineUpdate
from sqlalchemy.orm import Session

logger = structlog.get_logger()


class CRUDMachine(CRUDBase[Machine, MachineCreate, MachineUpdate]):
    async def get_with_check_online(self, db: Session, id: int) -> Machine:
        db_obj = cast(Machine, super().get(db, id))
        db_obj = await self.update_last_online_timestamp(db=db, db_obj=db_obj)
        return db_obj

    async def get_multi_with_check_online(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Machine]:
        machines = cast(List[Machine], super().get_multi(db, skip=skip, limit=limit))
        for i, db_obj in enumerate(machines):
            machines[i] = await self.update_last_online_timestamp(db=db, db_obj=db_obj)
        return machines

    @staticmethod
    async def update_last_online_timestamp(db: Session, db_obj: Machine) -> Machine:
        timeout = aiohttp.ClientTimeout(total=2)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{db_obj.host}/ping") as resp:
                    if resp.status == 200:
                        db_obj.last_online_timestamp = int(time.time())
                        db.add(db_obj)
                        db.commit()
                        db.refresh(db_obj)
                    else:
                        logger.debug(
                            f"{db_obj.host} ping failed",
                            status=resp.status,
                            machine=db_obj,
                        )
        except Exception as e:
            logger.debug(f"{e}: {db_obj.host} ping failed", machine=db_obj)

        return db_obj


machine = CRUDMachine(Machine)
