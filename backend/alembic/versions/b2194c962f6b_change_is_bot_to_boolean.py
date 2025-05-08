"""change_is_bot_to_boolean

Revision ID: b2194c962f6b
Revises: a6a78f93597c
Create Date: 2025-04-15 11:38:27.202469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2194c962f6b'
down_revision: Union[str, None] = 'a6a78f93597c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # First drop the default
    op.alter_column('chats', 'is_bot',
                    server_default=None)

    # Update any NULL values to false string
    op.execute("UPDATE chats SET is_bot = 'false' WHERE is_bot IS NULL")
    
    # Convert existing string values to proper boolean values
    op.execute("UPDATE chats SET is_bot = CASE WHEN LOWER(is_bot::text) IN ('true', 't', '1', 'yes', 'y') THEN 'true' ELSE 'false' END")
    
    # Now alter the column type to boolean
    op.execute('ALTER TABLE chats ALTER COLUMN is_bot TYPE boolean USING CASE WHEN is_bot::text = \'true\' THEN true ELSE false END')
    
    # Add back the default constraint
    op.alter_column('chats', 'is_bot',
                    server_default=sa.text('false'))


def downgrade() -> None:
    """Downgrade schema."""
    # First drop the default
    op.alter_column('chats', 'is_bot',
                    server_default=None)
    
    # Convert boolean back to string
    op.execute('ALTER TABLE chats ALTER COLUMN is_bot TYPE text USING CASE WHEN is_bot THEN \'true\' ELSE \'false\' END')
    
    # Add back string default
    op.alter_column('chats', 'is_bot',
                    server_default=sa.text("'false'"))
