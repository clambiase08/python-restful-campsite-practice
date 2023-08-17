"""created reservation model

Revision ID: 44e734f6d9d1
Revises: 9bbb93b77789
Create Date: 2023-08-17 11:53:05.263463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44e734f6d9d1'
down_revision = '9bbb93b77789'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('campsite_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['campsite_id'], ['campsites.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservation')
    # ### end Alembic commands ###
