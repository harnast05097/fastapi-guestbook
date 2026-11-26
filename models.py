from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Review(Base):
    __tablename__ = "review"
    __table_args__ = (
        CheckConstraint(
            "length(author) BETWEEN 1 AND 80",
            name="review_author_length",
        ),
        CheckConstraint(
            "length(text) BETWEEN 1 AND 1000",
            name="review_text_length",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(80))
    text: Mapped[str] = mapped_column(String(1000))
