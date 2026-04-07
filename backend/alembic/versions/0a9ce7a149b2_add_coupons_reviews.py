"""add_coupons_reviews

Revision ID: 0a9ce7a149b2
Revises: 001_initial
Create Date: 2026-04-06 23:25:46.111896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0a9ce7a149b2'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('coupons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=False),
    sa.Column('discount_type', sa.Enum('percentage', 'fixed', name='coupontype'), nullable=False),
    sa.Column('discount_value', sa.Float(), nullable=False),
    sa.Column('min_order_amount', sa.Float(), nullable=False),
    sa.Column('max_discount_amount', sa.Float(), nullable=True),
    sa.Column('usage_limit', sa.Integer(), nullable=True),
    sa.Column('used_count', sa.Integer(), nullable=False),
    sa.Column('starts_at', sa.DateTime(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint("(discount_type = 'percentage' AND discount_value <= 100) OR (discount_type = 'fixed')", name='ck_coupons_percentage_max_100'),
    sa.CheckConstraint('discount_value > 0', name='ck_coupons_discount_value_positive'),
    sa.CheckConstraint('expires_at > starts_at', name='ck_coupons_expiry_after_start'),
    sa.CheckConstraint('min_order_amount >= 0', name='ck_coupons_min_order_non_negative'),
    sa.CheckConstraint('usage_limit IS NULL OR usage_limit >= 0', name='ck_coupons_usage_limit_non_negative'),
    sa.CheckConstraint('used_count >= 0', name='ck_coupons_used_count_non_negative'),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('coupons', schema=None) as batch_op:
        batch_op.create_index('ix_coupons_active_expiry', ['is_active', 'expires_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_coupons_code'), ['code'], unique=True)
        batch_op.create_index(batch_op.f('ix_coupons_id'), ['id'], unique=False)

    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.Column('menu_item_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint('rating >= 1 AND rating <= 5', name='ck_reviews_rating_range'),
    sa.ForeignKeyConstraint(['menu_item_id'], ['menu_items.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id', 'menu_item_id', name='uq_reviews_order_item')
    )
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_reviews_id'), ['id'], unique=False)
        batch_op.create_index('ix_reviews_menu_item_rating', ['menu_item_id', 'rating'], unique=False)

    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_order_items_order_menu_item', ['order_id', 'menu_item_id'])


def downgrade() -> None:
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.drop_constraint('uq_order_items_order_menu_item', type_='unique')

    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_index('ix_reviews_menu_item_rating')
        batch_op.drop_index(batch_op.f('ix_reviews_id'))

    op.drop_table('reviews')
    with op.batch_alter_table('coupons', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_coupons_id'))
        batch_op.drop_index(batch_op.f('ix_coupons_code'))
        batch_op.drop_index('ix_coupons_active_expiry')

    op.drop_table('coupons')