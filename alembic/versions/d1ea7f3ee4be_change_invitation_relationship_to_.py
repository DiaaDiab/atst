"""change invitation relationship to workspace role

Revision ID: d1ea7f3ee4be
Revises: 5284ac1ac77c
Create Date: 2018-10-30 14:09:42.277467

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd1ea7f3ee4be'
down_revision = '5284ac1ac77c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invitations', sa.Column('workspace_role_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_index(op.f('ix_invitations_workspace_role_id'), 'invitations', ['workspace_role_id'], unique=False)
    op.drop_index('ix_invitations_token', table_name='invitations')
    op.create_index(op.f('ix_invitations_token'), 'invitations', ['token'], unique=False)
    op.drop_index('ix_invitations_workspace_id', table_name='invitations')
    op.drop_constraint('invitations_workspace_id_fkey', 'invitations', type_='foreignkey')
    op.create_foreign_key(None, 'invitations', 'workspace_roles', ['workspace_role_id'], ['id'])
    op.drop_column('invitations', 'workspace_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invitations', sa.Column('workspace_id', postgresql.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'invitations', type_='foreignkey')
    op.create_foreign_key('invitations_workspace_id_fkey', 'invitations', 'workspaces', ['workspace_id'], ['id'])
    op.create_index('ix_invitations_workspace_id', 'invitations', ['workspace_id'], unique=False)
    op.drop_index(op.f('ix_invitations_token'), table_name='invitations')
    op.create_index('ix_invitations_token', 'invitations', ['token'], unique=True)
    op.drop_index(op.f('ix_invitations_workspace_role_id'), table_name='invitations')
    op.drop_column('invitations', 'workspace_role_id')
    # ### end Alembic commands ###
