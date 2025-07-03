"""api usage table

Revision ID: f49a1ace9951
Revises: 9a584f75e3ab
Create Date: 2025-07-03 12:41:42.031934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f49a1ace9951'
down_revision: Union[str, None] = '9a584f75e3ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create api_usage table
    op.create_table(
        'api_usage',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        
        # Date tracking (we track usage per day)
        sa.Column('usage_date', sa.Date(), nullable=False),
        
        # Usage counters
        sa.Column('api_calls_count', sa.Integer(), nullable=False, default=0),
        
        # Breakdown by endpoint type (optional - helps with analytics)
        sa.Column('chat_calls', sa.Integer(), nullable=False, default=0),
        sa.Column('pdf_processing_calls', sa.Integer(), nullable=False, default=0),
        sa.Column('ats_analysis_calls', sa.Integer(), nullable=False, default=0),
        sa.Column('suggestion_calls', sa.Integer(), nullable=False, default=0),
        
        # Metadata
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        
        # Ensure one record per user per day
        sa.UniqueConstraint('user_id', 'usage_date', name='unique_user_daily_usage')
    )
    
    # Create indexes for better performance
    op.create_index('idx_api_usage_user_id', 'api_usage', ['user_id'])
    op.create_index('idx_api_usage_date', 'api_usage', ['usage_date'])
    op.create_index('idx_api_usage_user_date', 'api_usage', ['user_id', 'usage_date'])
    
    # Note: We removed the partial index for "today" because CURRENT_DATE is not immutable
    # The composite index on user_id + usage_date will be sufficient for our queries


def downgrade():
    # Drop indexes first
    op.drop_index('idx_api_usage_user_date', table_name='api_usage')
    op.drop_index('idx_api_usage_date', table_name='api_usage')
    op.drop_index('idx_api_usage_user_id', table_name='api_usage')
    
    # Drop the table
    op.drop_table('api_usage')