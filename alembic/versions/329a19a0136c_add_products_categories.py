"""add products & categories.

Revision ID: 329a19a0136c
Revises: None
Create Date: 2014-10-11 10:27:22.382911

"""

# revision identifiers, used by Alembic.
revision = '329a19a0136c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('migros_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parent_category_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['parent_category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('migros_id', sa.Integer(), nullable=True),
        sa.Column('ean', sa.String(length=13), nullable=True),
        sa.Column('subtitle', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('products')
    op.drop_table('categories')
