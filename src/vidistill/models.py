from typing import Optional
from pydantic import BaseModel


class VideoMetadata(BaseModel):
    model_config = {"frozen": True}

    video_id: str
    title: str
    duration: Optional[int] = None
    channel: Optional[str] = None
