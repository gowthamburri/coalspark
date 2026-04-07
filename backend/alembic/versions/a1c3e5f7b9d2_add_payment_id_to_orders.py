"""add payment_id to orders

Revision ID: a1c3e5f7b9d2
Revises: 0a9ce7a149b2
Create Date: 2026-04-07 01:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = 'a1c3e5f7b9d2'
down_revision: Union[str, None] = '0a9ce7a149b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add `payment_id` column to orders table
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_id', sa.String(length=128), nullable=True))


def downgrade() -> None:
    # Remove `payment_id` column
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('payment_id')
