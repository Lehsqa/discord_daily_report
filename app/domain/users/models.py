from datetime import datetime

from app.infrastructure.models import PublicModel


# Public models
# ------------------------------------------------------
class UserUncommited(PublicModel):
    name: str
    department: str
    report: str
    update_date: datetime


class User(UserUncommited):
    id: int
