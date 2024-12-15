"""add user table

Revision ID: 4c89811ab5ce
Revises: 620c979e1a48
Create Date: 2024-10-05 19:30:08.796025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c89811ab5ce'
down_revision: Union[str, None] = '620c979e1a48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column("id",sa.Integer(),nullable=False),
                    sa.Column("email",sa.String(),nullable=False),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("now()"),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
