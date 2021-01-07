"""create users table

Revision ID: d9dd29a29266
Revises:
Create Date: 2021-01-07 05:57:19.945200

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = 'd9dd29a29266'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('firebase_id', sa.String(), nullable=True),
        sa.Column('search_vector', sqlalchemy_utils.types.ts_vector.TSVectorType(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'ix_user_search_vector', 'user', ['search_vector'], unique=False, postgresql_using='gin'
    )


def downgrade():
    op.drop_index('ix_user_search_vector', table_name='user')
    op.drop_table('user')
