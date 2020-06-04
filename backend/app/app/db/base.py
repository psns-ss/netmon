# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.machine import Machine  # noqa
from app.models.machine_process import MachineProcess  # noqa
from app.models.user import User  # noqa
