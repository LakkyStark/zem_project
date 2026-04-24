"""document pipeline tables

Revision ID: c3e48d547507
Revises: 0001_initial
Create Date: 2026-04-24 10:34:57.860979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c3e48d547507'
down_revision: Union[str, None] = '0001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1) Add new columns to documents
    op.add_column("documents", sa.Column("type", sa.String(length=64), nullable=False, server_default="other"))
    op.add_column("documents", sa.Column("pages_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("documents", sa.Column("error_message", sa.Text(), nullable=True))

    # 2) Update document_status enum (MVP-friendly migration)
    # Rename old enum, create new one, cast column, drop old.
    op.execute("ALTER TYPE document_status RENAME TO document_status_old")
    op.execute(
        "CREATE TYPE document_status AS ENUM ("
        "'pending_upload','uploaded','queued','ocr_done','parsed','analyzed','failed'"
        ")"
    )
    op.execute(
        "ALTER TABLE documents ALTER COLUMN status TYPE document_status "
        "USING status::text::document_status"
    )
    op.execute("DROP TYPE document_status_old")

    # 3) Create document_pages
    op.create_table(
        "document_pages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("document_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=False),
        sa.Column("ocr_text", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0"),
        sa.Column("provider", sa.String(length=64), nullable=False, server_default="mock"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("organization_id", "document_id", "page_number", name="uq_doc_page"),
    )
    op.create_index("ix_document_pages_organization_id", "document_pages", ["organization_id"])
    op.create_index("ix_document_pages_document_id", "document_pages", ["document_id"])

    # cleanup server_defaults for new columns
    op.alter_column("documents", "type", server_default=None)
    op.alter_column("documents", "pages_count", server_default=None)


def downgrade() -> None:
    op.drop_index("ix_document_pages_document_id", table_name="document_pages")
    op.drop_index("ix_document_pages_organization_id", table_name="document_pages")
    op.drop_table("document_pages")

    op.execute("ALTER TYPE document_status RENAME TO document_status_new")
    op.execute(
        "CREATE TYPE document_status AS ENUM ("
        "'pending_upload','uploaded','processing','ready','failed'"
        ")"
    )
    op.execute(
        "ALTER TABLE documents ALTER COLUMN status TYPE document_status "
        "USING status::text::document_status"
    )
    op.execute("DROP TYPE document_status_new")

    op.drop_column("documents", "error_message")
    op.drop_column("documents", "pages_count")
    op.drop_column("documents", "type")
