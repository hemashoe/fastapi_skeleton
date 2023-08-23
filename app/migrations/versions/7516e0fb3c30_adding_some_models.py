"""adding some models

Revision ID: 7516e0fb3c30
Revises: e1c671c6bbca
Create Date: 2023-08-22 16:05:11.543901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7516e0fb3c30'
down_revision: Union[str, None] = 'e1c671c6bbca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faculty',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('faculty_name', sa.String(), nullable=False),
    sa.Column('faculty_dean', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('professions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('profession_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('study_year',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('year', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('change',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('change_name', sa.String(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=True),
    sa.Column('end_time', sa.Time(), nullable=True),
    sa.Column('change_year', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['change_year'], ['study_year.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('group_name', sa.String(), nullable=False),
    sa.Column('group_year', sa.String(), nullable=False),
    sa.Column('group_change_id', sa.Integer(), nullable=True),
    sa.Column('study_year_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_change_id'], ['change.id'], ),
    sa.ForeignKeyConstraint(['study_year_id'], ['study_year.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('groups')
    op.drop_table('change')
    op.drop_table('study_year')
    op.drop_table('professions')
    op.drop_table('faculty')
    # ### end Alembic commands ###
