from dataclasses import dataclass, field

@dataclass(frozen=True)
class NetworkDTO:
    success: bool = False
    data: list = field(default_factory=list)
    error: str | None = None
    #is_last_page: bool = False # no longer in use, usecase should decide if over using total_count
    total_count: int | None = None
