from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class RecordStep(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    panel: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    survey: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    x_cm: int
    y_cm: int
    slide: FiniteFloat


class VerifyStep(BaseModel):
    model_config = ConfigDict(extra="forbid")
    point: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
