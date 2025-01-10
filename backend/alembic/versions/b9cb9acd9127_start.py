"""Start

Revision ID: b9cb9acd9127
Revises: 
Create Date: 2024-12-27 00:47:23.414402

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b9cb9acd9127'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('surname', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=False),
                    sa.Column('registered_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"),
                              nullable=False),
                    sa.Column('role', sa.Enum('ADMIN', 'ANALYST', 'SCIENTIST', name='role'), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
    op.execute('DROP TYPE IF EXISTS role;')
