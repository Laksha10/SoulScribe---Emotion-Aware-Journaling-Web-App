"""Add batch_id to user_red_zone_logs

Revision ID: 742739cef9a9
Revises: f71ccba4caac
Create Date: 2025-07-24 20:26:35.322902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '742739cef9a9'
down_revision = 'f71ccba4caac'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add column with default 1 to backfill existing rows
    with op.batch_alter_table('user_red_zone_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('batch_id', sa.Integer(), nullable=False, server_default='1'))

    # Step 2: Remove the default for future inserts (ORM will handle)
    op.alter_column('user_red_zone_logs', 'batch_id', server_default=None)


def downgrade():
    with op.batch_alter_table('user_red_zone_logs', schema=None) as batch_op:
        batch_op.drop_column('batch_id')
