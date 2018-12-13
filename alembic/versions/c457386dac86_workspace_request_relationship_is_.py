"""workspace request relationship is nullable

Revision ID: c457386dac86
Revises: 1c1394e496a7
Create Date: 2018-12-13 08:57:09.319288

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c457386dac86'
down_revision = '1c1394e496a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('workspaces', 'request_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('workspaces', 'request_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###
