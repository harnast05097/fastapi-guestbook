from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.String(length=80), nullable=False),
    sa.Column('text', sa.String(length=1000), nullable=False),
    sa.CheckConstraint('length(author) BETWEEN 1 AND 80', name='review_author_length'),
    sa.CheckConstraint('length(text) BETWEEN 1 AND 1000', name='review_text_length'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('review')
