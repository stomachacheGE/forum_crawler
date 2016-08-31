"""add subforum column for user

Revision ID: df52ada9307c
Revises: 
Create Date: 2016-08-27 16:26:39.905334

"""

# revision identifiers, used by Alembic.
revision = 'df52ada9307c'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('subforum', sa.String()))


def downgrade():
    pass
