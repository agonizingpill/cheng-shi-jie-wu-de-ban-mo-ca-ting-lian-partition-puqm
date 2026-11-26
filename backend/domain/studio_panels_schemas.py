from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class SetGauge(BaseModel):
    model_config = ConfigDict(extra="forbid")
    panel: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    control_band: FiniteFloat
