"""initial

Revision ID: 445749daa0cd
Revises: 92014f49cc00
Create Date: 2023-08-18 13:59:34.078097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "445749daa0cd"
down_revision: Union[str, None] = "92014f49cc00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
