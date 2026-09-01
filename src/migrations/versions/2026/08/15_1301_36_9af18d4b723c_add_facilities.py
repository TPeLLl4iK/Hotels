
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9af18d4b723c"
down_revision: str | Sequence[str] | None = "8a6faa9a79e3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facility_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.alter_column(
        "users",
        "login",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=20),
        existing_nullable=False,
    )

def downgrade() -> None:
    op.alter_column(
        "users",
        "login",
        existing_type=sa.String(length=20),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )
    op.drop_table("rooms_facilities")
    op.drop_table("facilities")
