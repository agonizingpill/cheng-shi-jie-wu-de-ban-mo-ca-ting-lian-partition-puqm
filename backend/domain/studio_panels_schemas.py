from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class SetGauge(BaseModel):
    model_config = ConfigDict(extra="ignore")
    panel: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    control_band: Optional[FiniteFloat] = None
    # 兼容别名写法。
    band: Optional[FiniteFloat] = None
    trial_band: Optional[FiniteFloat] = None
    gauge: Optional[FiniteFloat] = None

    def resolved_band(self):
        for value in (self.control_band, self.band, self.trial_band, self.gauge):
            if value is not None:
                return float(value)
        return None
