"""add suforum columns

Revision ID: 0311359c3043
Revises: 0cc72fc056ec
Create Date: 2016-08-31 18:18:33.737695

"""

# revision identifiers, used by Alembic.
revision = '0311359c3043'
down_revision = '0cc72fc056ec'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('threads', sa.Column('subforum', sa.String()))
    op.add_column('threads', sa.Column('subforum_url', sa.String()))
    op.add_column('posts', sa.Column('subforum', sa.String()))
    op.add_column('posts', sa.Column('subforum_url', sa.String()))


def downgrade():
    pass
