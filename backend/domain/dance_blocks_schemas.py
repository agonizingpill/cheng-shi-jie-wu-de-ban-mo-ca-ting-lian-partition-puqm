from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class MoveClass(BaseModel):
    model_config = ConfigDict(extra="forbid")
    course: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    to_panel: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class OpenClass(BaseModel):
    model_config = ConfigDict(extra="forbid")
    course: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
