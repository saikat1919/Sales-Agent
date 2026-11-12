
"""add role to users

Revision ID: be15ea49f6ea
Revises: 9c578c1df4d3
Create Date: 2026-11-12 21:07:24.269151
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'be15ea49f6ea'
down_revision: Union[str, Sequence[str], None] = '9c578c1df4d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.Enum(
                'customer',
                'admin',
                name='role',
                native_enum=False,
                length=20,
            ),
            server_default='customer',
            nullable=False,
        ),
        schema='sales_agent',
    )


def downgrade() -> None:
    op.drop_column(
        'users',
        'role',
        schema='sales_agent',
    )
