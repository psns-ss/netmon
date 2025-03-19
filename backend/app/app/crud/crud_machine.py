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
                ping_url = f"{db_obj.host}/ping"
                async with session.get(ping_url) as resp:
                    if resp.status == 200:
                        db_obj.last_online_timestamp = int(time.time())
                        db.add(db_obj)
                        db.commit()
                        db.refresh(db_obj)
                        logger.debug(
                            f"ping success",
                            status=resp.status,
                            machine_id=db_obj.id,
                            machine_host=db_obj.host,
                            ping_url=ping_url,
                        )
                    else:
                        logger.debug(
                            f"ping failed",
                            status=resp.status,
                            machine_id=db_obj.id,
                            machine_host=db_obj.host,
                            ping_url=ping_url,
                        )
        except Exception as e:
            logger.debug(
                f"{e}: ping failed",
                machine_id=db_obj.id,
                machine_host=db_obj.host,
                ping_url=ping_url,
            )

        return db_obj


machine = CRUDMachine(Machine)
