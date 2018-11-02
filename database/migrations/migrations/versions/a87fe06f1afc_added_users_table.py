"""Added users table

Revision ID: a87fe06f1afc
Revises:
Create Date: 2018-11-02 08:51:38.385612

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'a87fe06f1afc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###