"""add recipe cache storage.

Revision ID: 34380bfec0ce
Revises: 329a19a0136c
Create Date: 2014-10-11 17:28:16.871284

"""

# revision identifiers, used by Alembic.
revision = '34380bfec0ce'
down_revision = '329a19a0136c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'recipes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('yummly_id', sa.String(length=30), nullable=True),
        sa.Column('json', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('recipes')
