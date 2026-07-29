from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Note:
    title: str
    content: str
    id: Optional[int] = None
    tags: Optional[str] = None
    is_encrypted: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now
