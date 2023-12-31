"""Add archived to classes

Revision ID: cf2b4eaa320d
Revises: 335928f166cb
Create Date: 2023-10-22 00:49:21.382757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf2b4eaa320d'
down_revision: Union[str, None] = '335928f166cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classes', sa.Column('archived', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('classes', 'archived')
    # ### end Alembic commands ###
