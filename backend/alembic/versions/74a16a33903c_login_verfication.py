"""login verfication

Revision ID: 74a16a33903c
Revises: ed5fae598524
Create Date: 2025-07-05 19:01:38.978102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74a16a33903c'
down_revision: Union[str, None] = 'ed5fae598524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add email verification fields to users table
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('verification_code', sa.String(length=6), nullable=True))
    op.add_column('users', sa.Column('verification_code_expires', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('verification_attempts', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('users', 'verification_attempts')
    op.drop_column('users', 'verification_code_expires')
    op.drop_column('users', 'verification_code')
    op.drop_column('users', 'email_verified')

