"""merging modification on User model from trevor with video models from het-tale

Revision ID: d1b72a7a0346
Revises: 19a325b461e9, d992892557ec
Create Date: 2026-02-04 23:09:47.410380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1b72a7a0346'
down_revision: Union[str, None] = ('19a325b461e9', 'd992892557ec')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
