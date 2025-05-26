"""add status to events

Revision ID: add_status_to_events
Revises: 
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_status_to_events'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Thêm cột status vào bảng events
    op.add_column('events', sa.Column('status', sa.String(20), nullable=False, server_default='active'))


def downgrade():
    # Xóa cột status khỏi bảng events
    op.drop_column('events', 'status') 