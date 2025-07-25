"""Add ok_to_notify manually

Revision ID: 064ff9e40fef
Revises: a3f9780a5845
Create Date: 2025-07-21 19:55:34.475504

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Boolean


# revision identifiers, used by Alembic.
revision = '064ff9e40fef'
down_revision = 'a3f9780a5845'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', Column('ok_to_notify', Boolean(), server_default='false'))



def downgrade():
    op.drop_column('users', 'ok_to_notify')
