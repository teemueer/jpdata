"""empty message

Revision ID: 16ac4c4560c3
Revises: ccf19812f563
Create Date: 2024-06-05 17:10:39.015702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16ac4c4560c3'
down_revision = 'ccf19812f563'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kanji', sa.String(length=32), nullable=False),
    sa.Column('kana', sa.String(length=32), nullable=False),
    sa.Column('meaning', sa.String(length=256), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.DateTime(), nullable=False),
    sa.Column('time_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('kanji', 'kana', 'user_id', name='uq_kanji_kana_user')
    )
    with op.batch_alter_table('words', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_words_time_created'), ['time_created'], unique=False)
        batch_op.create_index(batch_op.f('ix_words_time_updated'), ['time_updated'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('words', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_words_time_updated'))
        batch_op.drop_index(batch_op.f('ix_words_time_created'))

    op.drop_table('words')
    # ### end Alembic commands ###
