"""new task order table

Revision ID: a4cb6444eb4a
Revises: c457386dac86
Create Date: 2018-12-13 09:17:25.406453

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a4cb6444eb4a'
down_revision = 'c457386dac86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_orders',
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('number', sa.String(), nullable=True),
    sa.Column('clin_0001', sa.Integer(), nullable=True),
    sa.Column('clin_0003', sa.Integer(), nullable=True),
    sa.Column('clin_1001', sa.Integer(), nullable=True),
    sa.Column('clin_1003', sa.Integer(), nullable=True),
    sa.Column('clin_2001', sa.Integer(), nullable=True),
    sa.Column('clin_2003', sa.Integer(), nullable=True),
    sa.Column('expiration_date', sa.Date(), nullable=True),
    sa.Column('workspace_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_orders')
    # ### end Alembic commands ###
