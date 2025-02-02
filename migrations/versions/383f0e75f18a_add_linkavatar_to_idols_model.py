"""Add linkAvatar to Idols model

Revision ID: 383f0e75f18a
Revises: 
Create Date: 2024-07-19 17:39:01.065659

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '383f0e75f18a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('album', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['name'])

    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.alter_column('link',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['link'])

    with op.batch_alter_table('models', schema=None) as batch_op:
        batch_op.add_column(sa.Column('linkAvatar', sa.String(length=250), nullable=True))
        batch_op.alter_column('name',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('models', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.String(length=80),
               type_=mysql.TEXT(),
               existing_nullable=False)
        batch_op.drop_column('linkAvatar')

    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('link',
               existing_type=sa.String(length=250),
               type_=mysql.TEXT(),
               existing_nullable=False)

    with op.batch_alter_table('album', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.String(length=80),
               type_=mysql.TEXT(),
               existing_nullable=False)

    # ### end Alembic commands ###
