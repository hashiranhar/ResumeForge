"""user payment history

Revision ID: 9a584f75e3ab
Revises: 32595032404a
Create Date: 2025-07-03 12:37:45.713405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '9a584f75e3ab'
down_revision: Union[str, None] = '32595032404a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create user_subscriptions table
    op.create_table(
        'user_subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        
        # Billing information
        sa.Column('billing_cycle', sa.String(20), nullable=False, default='monthly'),  # 'monthly' or 'yearly'
        sa.Column('status', sa.String(20), nullable=False, default='active'),  # 'active', 'cancelled', 'past_due', 'unpaid'
        
        # Subscription period tracking
        sa.Column('current_period_start', sa.DateTime(), nullable=True),
        sa.Column('current_period_end', sa.DateTime(), nullable=True),
        
        # Stripe integration fields
        sa.Column('stripe_customer_id', sa.String(255), nullable=True),
        sa.Column('stripe_subscription_id', sa.String(255), nullable=True),
        
        # Cancellation tracking
        sa.Column('cancel_at_period_end', sa.Boolean(), default=False),
        sa.Column('cancelled_at', sa.DateTime(), nullable=True),
        
        # Metadata
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['plan_id'], ['subscription_plans.id'], ondelete='RESTRICT')
    )
    
    # Create indexes for better performance
    op.create_index('idx_user_subscriptions_user_id', 'user_subscriptions', ['user_id'])
    op.create_index('idx_user_subscriptions_status', 'user_subscriptions', ['status'])
    op.create_index('idx_user_subscriptions_stripe_customer', 'user_subscriptions', ['stripe_customer_id'])
    op.create_index('idx_user_subscriptions_stripe_subscription', 'user_subscriptions', ['stripe_subscription_id'])
    
    # Add unique constraint to ensure one active subscription per user
    op.create_index('idx_user_subscriptions_unique_active', 'user_subscriptions', ['user_id'], 
                   unique=True, postgresql_where=sa.text("status = 'active'"))
    
    # Create default free subscriptions for existing users
    connection = op.get_bind()
    
    # First, get the free plan ID
    result = connection.execute(text("SELECT id FROM subscription_plans WHERE name = 'free'"))
    free_plan_id = result.scalar()
    
    # Create free subscriptions for all existing users
    connection.execute(text(f"""
        INSERT INTO user_subscriptions (user_id, plan_id, billing_cycle, status)
        SELECT id, {free_plan_id}, 'monthly', 'active'
        FROM users
        WHERE NOT EXISTS (
            SELECT 1 FROM user_subscriptions WHERE user_subscriptions.user_id = users.id
        )
    """))


def downgrade():
    # Drop indexes first
    op.drop_index('idx_user_subscriptions_unique_active', table_name='user_subscriptions')
    op.drop_index('idx_user_subscriptions_stripe_subscription', table_name='user_subscriptions')
    op.drop_index('idx_user_subscriptions_stripe_customer', table_name='user_subscriptions')
    op.drop_index('idx_user_subscriptions_status', table_name='user_subscriptions')
    op.drop_index('idx_user_subscriptions_user_id', table_name='user_subscriptions')
    
    # Drop the table
    op.drop_table('user_subscriptions')