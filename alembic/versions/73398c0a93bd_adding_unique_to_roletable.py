"""adding unique to roletable

Revision ID: 73398c0a93bd
Revises: 0e078e183fd1
Create Date: 2024-11-26 14:40:48.519898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73398c0a93bd'
down_revision: Union[str, None] = '0e078e183fd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'roles', ['role_name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'roles', type_='unique')
    # ### end Alembic commands ###
