"""update portfolios defense component column type

Revision ID: 02ac8bdcf16f
Revises: 08f2a640e9c2
Create Date: 2019-12-26 16:10:54.366461

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '02ac8bdcf16f' # pragma: allowlist secret
down_revision = '08f2a640e9c2' # pragma: allowlist secret
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('portfolios', 'defense_component',
               type_=postgresql.ARRAY(sa.VARCHAR()),
               existing_type=sa.VARCHAR(),
               postgresql_using="string_to_array(defense_component, ',')::character varying[]",
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('portfolios', 'defense_component',
               type_=sa.VARCHAR(),
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               postgresql_using="defense_component[1]::character varying",
               nullable=False)
    # ### end Alembic commands ###
