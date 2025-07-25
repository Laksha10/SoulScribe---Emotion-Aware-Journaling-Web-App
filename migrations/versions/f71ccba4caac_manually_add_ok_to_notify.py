"""Manually add ok_to_notify

Revision ID: f71ccba4caac
Revises: 064ff9e40fef
Create Date: 2025-07-21 20:17:19.771866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f71ccba4caac'
down_revision = '064ff9e40fef'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('ok_to_notify', sa.Boolean(), server_default='false'))

def downgrade():
    op.drop_column('users', 'ok_to_notify')