"""payment history

Revision ID: ed5fae598524
Revises: f49a1ace9951
Create Date: 2025-07-03 12:46:04.474547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed5fae598524'
down_revision: Union[str, None] = 'f49a1ace9951'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create payment_history table
    op.create_table(
        'payment_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('subscription_id', sa.Integer(), nullable=False),
        
        # Stripe payment information
        sa.Column('stripe_invoice_id', sa.String(255), nullable=True),
        sa.Column('stripe_payment_intent_id', sa.String(255), nullable=True),
        sa.Column('stripe_charge_id', sa.String(255), nullable=True),
        
        # Payment details
        sa.Column('amount_pennies', sa.Integer(), nullable=False),  # Amount in pennies
        sa.Column('currency', sa.String(3), nullable=False, default='GBP'),
        sa.Column('billing_cycle', sa.String(20), nullable=False),  # 'monthly' or 'yearly'
        
        # Payment status and timing
        sa.Column('status', sa.String(20), nullable=False),  # 'pending', 'paid', 'failed', 'refunded'
        sa.Column('payment_date', sa.DateTime(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        
        # Billing period covered by this payment
        sa.Column('period_start', sa.DateTime(), nullable=True),
        sa.Column('period_end', sa.DateTime(), nullable=True),
        
        # Additional details
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('failure_reason', sa.Text(), nullable=True),
        
        # Metadata
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subscription_id'], ['user_subscriptions.id'], ondelete='CASCADE')
    )
    
    # Create indexes for better performance
    op.create_index('idx_payment_history_user_id', 'payment_history', ['user_id'])
    op.create_index('idx_payment_history_subscription_id', 'payment_history', ['subscription_id'])
    op.create_index('idx_payment_history_status', 'payment_history', ['status'])
    op.create_index('idx_payment_history_stripe_invoice', 'payment_history', ['stripe_invoice_id'])
    op.create_index('idx_payment_history_payment_date', 'payment_history', ['payment_date'])


def downgrade():
    # Drop indexes first
    op.drop_index('idx_payment_history_payment_date', table_name='payment_history')
    op.drop_index('idx_payment_history_stripe_invoice', table_name='payment_history')
    op.drop_index('idx_payment_history_status', table_name='payment_history')
    op.drop_index('idx_payment_history_subscription_id', table_name='payment_history')
    op.drop_index('idx_payment_history_user_id', table_name='payment_history')
    
    # Drop the table
    op.drop_table('payment_history')
