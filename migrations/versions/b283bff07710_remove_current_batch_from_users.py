"""remove current_batch from users

Revision ID: b283bff07710
Revises: 27192f0beafa
Create Date: 2025-07-25 01:11:39.079851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b283bff07710'
down_revision = '27192f0beafa'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('current_batch')

def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_batch', sa.Integer(), nullable=True))