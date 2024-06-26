"""empty message

Revision ID: 3e463d64d63b
Revises: 125c089f9f62
Create Date: 2024-06-05 17:55:35.272260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e463d64d63b'
down_revision = '125c089f9f62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dictionaries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=16), nullable=False))
        batch_op.drop_index('ix_dictionaries_dic')
        batch_op.drop_constraint('uq_dic_page', type_='unique')
        batch_op.create_index(batch_op.f('ix_dictionaries_name'), ['name'], unique=False)
        batch_op.create_unique_constraint('uq_name_page', ['name', 'page'])
        batch_op.drop_column('dic')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dictionaries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dic', sa.VARCHAR(length=16), autoincrement=False, nullable=False))
        batch_op.drop_constraint('uq_name_page', type_='unique')
        batch_op.drop_index(batch_op.f('ix_dictionaries_name'))
        batch_op.create_unique_constraint('uq_dic_page', ['dic', 'page'])
        batch_op.create_index('ix_dictionaries_dic', ['dic'], unique=False)
        batch_op.drop_column('name')

    # ### end Alembic commands ###
