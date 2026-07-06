from ninja import Schema
from pydantic import Field


class AnimeListOut(Schema):
    slug: str
    name: str


class AnimeDetailOut(Schema):
    slug: str
    name: str
    season: str
    type: str
    genres: str
    description: str
    avg_rating: float | None
    total_views: int
    user_rating: int | None


class RatingIn(Schema):
    rating: int = Field(ge=1, le=5)


class RatingOut(Schema):
    avg_rating: float
    user_rating: int
