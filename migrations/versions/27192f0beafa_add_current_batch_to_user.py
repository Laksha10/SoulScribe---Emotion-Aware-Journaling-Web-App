"""Add current_batch to User

Revision ID: 27192f0beafa
Revises: 742739cef9a9
Create Date: 2025-07-25 00:29:12.125520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27192f0beafa'
down_revision = '742739cef9a9'
branch_labels = None
depends_on = None


def upgrade():
    # Add with default = 1 for all existing rows
    op.add_column('users', sa.Column('current_batch', sa.Integer(), nullable=False, server_default='1'))
    # Remove the default after initialization so future inserts must set it explicitly in the model
    op.alter_column('users', 'current_batch', server_default=None)


def downgrade():
    op.drop_column('users', 'current_batch')

    # ### end Alembic commands ###
