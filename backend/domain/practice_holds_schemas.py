from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class PostHold(BaseModel):
    # 忽略额外字段：立挡关注线等快照由服务端按立挡时刻生成，不接受客户端指定。
    model_config = ConfigDict(extra="ignore")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    review: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    point: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    shift: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class ClearHold(BaseModel):
    model_config = ConfigDict(extra="ignore")
    hold: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    retest: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
