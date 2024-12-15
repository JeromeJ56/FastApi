"""add content column to posts table

Revision ID: 620c979e1a48
Revises: c2d0d0ca37d4
Create Date: 2024-10-05 19:25:20.162643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '620c979e1a48'
down_revision: Union[str, None] = 'c2d0d0ca37d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
