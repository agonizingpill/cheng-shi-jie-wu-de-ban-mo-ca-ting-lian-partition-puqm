from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class PostHold(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    review: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    point: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    shift: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class ClearHold(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hold: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    retest: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
