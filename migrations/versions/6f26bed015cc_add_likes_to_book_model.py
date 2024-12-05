"""Add likes to Book model

Revision ID: 6f26bed015cc
Revises: 4d463c912bcd
Create Date: 2024-12-05 00:03:16.189002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f26bed015cc'
down_revision = '4d463c912bcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.String(length=120), nullable=False))
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.drop_column('likes')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes', sa.INTEGER(), nullable=True))
        batch_op.alter_column('title',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.drop_column('author')

    # ### end Alembic commands ###
