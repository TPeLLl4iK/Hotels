from collections.abc import Sequence

from alembic import op

revision: str = "1e8d41ef01f8"
down_revision: str | Sequence[str] | None = "f3e6b702dab0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["login"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
