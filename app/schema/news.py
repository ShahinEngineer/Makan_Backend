from pydantic import BaseModel

class NewsCreate(BaseModel):
    title: str
    subtitle: str | None = None
    description: str
    hash_tags: list[str] | None = None
    img_url: str | None = None
    photo_links: list[str] | None = None