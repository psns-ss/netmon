from app import crud, models
from app.schemas.machine import MachineCreate
from app.tests.utils.utils import random_lower_string
from sqlalchemy.orm import Session


def create_random_machine(db: Session) -> models.Machine:
    host = "localhost:3000"
    name = random_lower_string()
    machine_in = MachineCreate(host=host, name=name, id=id)
    return crud.machine.create(db=db, obj_in=machine_in)
