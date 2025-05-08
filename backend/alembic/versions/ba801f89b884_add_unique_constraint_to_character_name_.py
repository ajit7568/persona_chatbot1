"""Add unique constraint to character name and movie

Revision ID: ba801f89b884
Revises: 22905a4a3dae
Create Date: 2025-04-15 03:14:28.862665

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = 'ba801f89b884'
down_revision: Union[str, None] = '22905a4a3dae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Get database connection
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    has_constraint = any(
        constraint['name'] == 'uq_character_name_movie'
        for constraint in inspector.get_unique_constraints('characters')
    )

    if not has_constraint:
        with op.batch_alter_table('characters') as batch_op:
            batch_op.create_unique_constraint(
                'uq_character_name_movie',
                ['name', 'movie']
            )

def downgrade() -> None:
    with op.batch_alter_table('characters') as batch_op:
        batch_op.drop_constraint('uq_character_name_movie', type_='unique')
