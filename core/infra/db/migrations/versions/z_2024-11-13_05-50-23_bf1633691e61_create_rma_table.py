"""create RMA table

Revision ID: bf1633691e61
Revises: e99058b3e85c
Create Date: 2024-11-13 05:50:23.729377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf1633691e61'
down_revision = 'e99058b3e85c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rmas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('defect_description', sa.Text(), nullable=False),
    sa.Column('defect', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rma_user_association',
    sa.Column('rma_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rma_id'], ['rmas.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('rma_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rma_user_association')
    op.drop_table('rmas')
    # ### end Alembic commands ###