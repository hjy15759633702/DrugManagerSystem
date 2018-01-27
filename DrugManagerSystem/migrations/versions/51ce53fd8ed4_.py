"""empty message

Revision ID: 51ce53fd8ed4
Revises: 
Create Date: 2018-01-27 11:43:45.075000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51ce53fd8ed4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('drugType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('drug',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('desc', sa.String(length=500), nullable=False),
    sa.Column('isSale', sa.Boolean(), nullable=False),
    sa.Column('stockDate', sa.DateTime(), nullable=True),
    sa.Column('saleDate', sa.DateTime(), nullable=True),
    sa.Column('stockPrice', sa.REAL(), nullable=True),
    sa.Column('salePice', sa.REAL(), nullable=True),
    sa.Column('drugTypeId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['drugTypeId'], ['drugType.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drug')
    op.drop_table('drugType')
    # ### end Alembic commands ###