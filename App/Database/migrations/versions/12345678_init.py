"""add_chat_member_table

Revision ID: <новый_ID>
Revises: <предыдущий_ID>
Create Date: <дата_и_время>

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12345678'
down_revision = '5378cdc164a8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('telegram_chat_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('is_premium', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('telegram_chat_members')
