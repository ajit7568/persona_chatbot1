"""add_character_id_to_chat

Revision ID: 383df366afae
Revises: b2194c962f6b
Create Date: 2025-04-15 11:45:23.512219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic.operations import ops


# revision identifiers, used by Alembic.
revision: str = '383df366afae'
down_revision: Union[str, None] = 'b2194c962f6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.add_column(sa.Column('character_id', sa.Integer(), nullable=True))
        batch_op.create_index(op.f('ix_chats_character_id'), ['character_id'], unique=False)
        batch_op.create_foreign_key('fk_chats_character_id', 'characters', ['character_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('chats', schema=None) as batch_op:
        batch_op.drop_constraint('fk_chats_character_id', type_='foreignkey')
        batch_op.drop_index(op.f('ix_chats_character_id'))
        batch_op.drop_column('character_id')
