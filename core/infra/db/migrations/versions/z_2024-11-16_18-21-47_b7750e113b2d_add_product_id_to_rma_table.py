"""add product_id to rma table

Revision ID: b7750e113b2d
Revises: 65e385880ee9
Create Date: 2024-11-16 18:21:47.537279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7750e113b2d'
down_revision = '65e385880ee9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rmas', sa.Column('product_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'rmas', 'products', ['product_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rmas', type_='foreignkey')
    op.drop_column('rmas', 'product_id')
    # ### end Alembic commands ###
