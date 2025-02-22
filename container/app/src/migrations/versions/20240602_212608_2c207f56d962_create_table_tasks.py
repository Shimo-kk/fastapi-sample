"""create_table_tasks

Revision ID: 2c207f56d962
Revises: cec4f297f9e6
Create Date: 2024-06-02 21:26:08.209404+09:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2c207f56d962'
down_revision: Union[str, None] = 'cec4f297f9e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('user_id', sa.INTEGER(), nullable=False, comment='ユーザーID'),
    sa.Column('title', sa.VARCHAR(length=50), nullable=False, comment='タイトル'),
    sa.Column('detail', sa.TEXT(), nullable=True, comment='詳細'),
    sa.Column('priority_id', sa.INTEGER(), nullable=False, comment='優先度ID'),
    sa.Column('category_id', sa.INTEGER(), nullable=False, comment='カテゴリID'),
    sa.Column('start_date', sa.DATE(), nullable=True, comment='開始日'),
    sa.Column('is_done', sa.BOOLEAN(), nullable=False, comment='完了フラグ'),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False, comment='登録日時'),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新日時'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('categories', 'user_id',
               existing_type=sa.INTEGER(),
               comment='ユーザーID',
               existing_nullable=False)
    op.create_foreign_key(None, 'categories', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'categories', type_='foreignkey')
    op.alter_column('categories', 'user_id',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='ユーザーID',
               existing_nullable=False)
    op.drop_table('tasks')
    # ### end Alembic commands ###
