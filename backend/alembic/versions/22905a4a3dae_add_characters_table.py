"""Add characters table

Revision ID: 22905a4a3dae
Revises: 6781c0885257
Create Date: 2025-04-13 16:04:42.862665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '22905a4a3dae'
down_revision: Union[str, None] = '6781c0885257'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('movie', sa.String(), nullable=False),
    sa.Column('chat_style', sa.String(), nullable=False),
    sa.Column('example_responses', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_characters_movie'), 'characters', ['movie'], unique=False)
    op.create_index(op.f('ix_characters_name'), 'characters', ['name'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_characters_name'), table_name='characters')
    op.drop_index(op.f('ix_characters_movie'), table_name='characters')
    op.drop_table('characters')
