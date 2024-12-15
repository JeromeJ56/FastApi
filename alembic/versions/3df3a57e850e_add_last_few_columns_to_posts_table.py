"""add last few columns to posts table

Revision ID: 3df3a57e850e
Revises: 572791095c10
Create Date: 2024-12-15 11:18:45.364959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3df3a57e850e'
down_revision: Union[str, None] = '572791095c10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False,server_default="True"),)
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
