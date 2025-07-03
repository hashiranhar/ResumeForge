"""Adding Payment schemas

Revision ID: 32595032404a
Revises: f2ecf32b61e9
Create Date: 2025-07-03 12:27:39.452184

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '32595032404a'
down_revision: Union[str, None] = 'f2ecf32b61e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create subscription_plans table
    op.create_table(
        'subscription_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('display_name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        
        # Pricing information (in pennies to avoid floating point issues)
        sa.Column('monthly_price_pennies', sa.Integer(), nullable=False, default=0),
        sa.Column('yearly_price_pennies', sa.Integer(), nullable=False, default=0),
        
        # Usage limits (same daily limits regardless of billing cycle)
        sa.Column('api_calls_per_day', sa.Integer(), nullable=False, default=0),
        sa.Column('max_cvs', sa.Integer(), nullable=False, default=0),
        
        # Stripe integration fields (will be populated later)
        sa.Column('stripe_monthly_price_id', sa.String(255), nullable=True),
        sa.Column('stripe_yearly_price_id', sa.String(255), nullable=True),
        
        # Metadata
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create indexes for better performance
    op.create_index('idx_subscription_plans_name', 'subscription_plans', ['name'])
    op.create_index('idx_subscription_plans_active', 'subscription_plans', ['is_active'])
    
    # Insert the three subscription tiers
    connection = op.get_bind()
    connection.execute(text("""
        INSERT INTO subscription_plans (
            name, display_name, description, 
            monthly_price_pennies, yearly_price_pennies,
            api_calls_per_day, max_cvs
        ) VALUES 
            ('free', 'Free', 'Basic resume building features', 0, 0, 5, 3),
            ('basic', 'Basic', 'Enhanced features with more API calls', 350, 2940, 25, 10),
            ('pro', 'Pro', 'Full access with maximum limits', 550, 4620, 50, 50)
    """))


def downgrade():
    # Drop indexes first
    op.drop_index('idx_subscription_plans_active', table_name='subscription_plans')
    op.drop_index('idx_subscription_plans_name', table_name='subscription_plans')
    
    # Drop the table
    op.drop_table('subscription_plans')
