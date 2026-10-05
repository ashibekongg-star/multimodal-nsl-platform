"""Add user account status

Revision ID: f8155b9f792e
Revises: 05bbba29f7ba
Create Date: 2026-08-16 17:00:34.396585

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f8155b9f792e"
down_revision = "05bbba29f7ba"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("users", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "status",
                sa.String(length=20),
                nullable=False,
                server_default="active"
            )
        )


def downgrade():

    with op.batch_alter_table("users", schema=None) as batch_op:

        batch_op.drop_column("status")