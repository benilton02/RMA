"""create product table

Revision ID: 65e385880ee9
Revises: 766e69e9a76d
Create Date: 2024-11-16 18:12:20.341259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65e385880ee9'
down_revision = '766e69e9a76d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('model', sa.String(length=255), nullable=False),
    sa.Column('color', sa.String(length=255), nullable=False),
    sa.Column('serial_number', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('serial_number')
    )
    op.drop_column('rmas', 'product_name')
    op.drop_column('rmas', 'color')
    op.drop_column('rmas', 'model')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rmas', sa.Column('model', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('rmas', sa.Column('color', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('rmas', sa.Column('product_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_table('products')
    # ### end Alembic commands ###