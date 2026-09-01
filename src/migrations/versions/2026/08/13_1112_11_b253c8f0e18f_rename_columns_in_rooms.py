from collections.abc import Sequence

from alembic import op

revision: str = "b253c8f0e18f"
down_revision: str | Sequence[str] | None = "fa9aafc6c4b9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("rooms", "quantit", new_column_name="quantity")


def downgrade() -> None:
    # op.alter_column("rooms", "name", new_column_name="title")
    ...
