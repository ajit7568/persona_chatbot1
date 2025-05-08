"""add_chat_session_to_chat

Revision ID: cc9aa6945363
Revises: b7a4dd782851
Create Date: 2025-04-16 19:16:03.386625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cc9aa6945363'
down_revision: Union[str, None] = 'b7a4dd782851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create new table with desired schema
    op.create_table('chats_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('character_id', sa.Integer(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('is_bot', sa.Boolean(), nullable=True, server_default=sa.text('false')),
        sa.Column('timestamp', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('chat_session', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from old table to new table
    op.execute('INSERT INTO chats_new SELECT id, user_id, character_id, message, is_bot, timestamp, NULL FROM chats')
    
    # Drop old table and rename new table
    op.drop_table('chats')
    op.rename_table('chats_new', 'chats')

    # Create indexes
    op.create_index(op.f('ix_chats_chat_session'), 'chats', ['chat_session'], unique=False)
    op.create_index(op.f('ix_chats_character_id'), 'chats', ['character_id'], unique=False)
    op.create_index(op.f('ix_chats_user_id'), 'chats', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Create table with old schema
    op.create_table('chats_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('character_id', sa.Integer(), nullable=True),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('is_bot', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('timestamp', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from new table to old table
    op.execute('INSERT INTO chats_old SELECT id, user_id, character_id, message, is_bot, timestamp FROM chats')
    
    # Drop new table and rename old table
    op.drop_table('chats')
    op.rename_table('chats_old', 'chats')

    # Recreate original indexes
    op.create_index('ix_chats_character_id', 'chats', ['character_id'], unique=False)
    op.create_index('ix_chats_user_id', 'chats', ['user_id'], unique=False)
