"""update for krebs.de

Revision ID: 0cc72fc056ec
Revises: 6079c6bc1dcb
Create Date: 2016-08-29 00:38:16.992754

"""

# revision identifiers, used by Alembic.
revision = '0cc72fc056ec'
down_revision = '6079c6bc1dcb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('threads', sa.Column('subforum', sa.String()))
    op.add_column('threads', sa.Column('subforum_url', sa.String()))
    op.add_column('posts', sa.Column('subforum', sa.String()))
    op.add_column('posts', sa.Column('subforum_url', sa.String()))
    op.drop_column('users', 'subforum')


def downgrade():
    pass
