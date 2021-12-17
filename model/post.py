from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
import json
from typing import List, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ExtractedData:
    author: Optional[str] = None
    text: Optional[str] = None
    region: Optional[str] = None
    root: List[str] = field(default_factory=list)
    department: List[str] = field(default_factory=list)
    actors: List[str] = field(default_factory=list)


@dataclass_json
@dataclass
class Post:
    source: str
    url: str
    date: Decimal
    title: str = ""
    is_downloaded: bool = False

    extracted_data: Optional[ExtractedData] = None

    pk: str = None
    sk: str = None

    def __post_init__(self):
        cleaned_title = self.title.lower().replace(" ", "-").replace("--", "-")

        self.sk = json.dumps({
            "title": cleaned_title,
            "date": int(self.date)
        })

        self.pk = Post.build_key(self.source, self.is_downloaded)

    def __str__(self) -> str:
        return self.to_dict().__str__()

    @staticmethod
    def build_key(source: str, is_downloaded: bool):
        return json.dumps({
            "source": source,
            "is_downloaded": str(is_downloaded)
        })

    def set_extracted_data(self, extracted_data: ExtractedData):
        self.extracted_data = extracted_data
        self.is_downloaded = True
        self.pk = Post.build_key(
            self.source,
            self.is_downloaded
        )


def build_post_obj(source: str, title: str, url: str, date: datetime) -> Post:
    return Post(
        source=source,
        title=title,
        url=url,
        date=Decimal(date.timestamp())
    )


def build_extracted_data_obj(author: str = "", text: str = "") -> ExtractedData:
    return ExtractedData(
        author=author,
        text=text
    )