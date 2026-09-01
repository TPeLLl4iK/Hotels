from collections.abc import Sequence

from alembic import op

revision: str = "8a6faa9a79e3"
down_revision: str | Sequence[str] | None = "b253c8f0e18f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("bookings", "date_to1", new_column_name="date_from")


def downgrade() -> None:
    op.alter_column()
