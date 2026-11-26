from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

Code = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class ClusterFloor(BaseModel):
    # 允许别名/额外字段：试调关注线沿用 control_band 命名，
    # 同时兼容 trial_band / band / gauge 等调用写法。
    model_config = ConfigDict(extra="allow")
    panel: Code
    survey: Code
    control_band: Optional[FiniteFloat] = None
    trial_band: Optional[FiniteFloat] = None
    band: Optional[FiniteFloat] = None
    gauge: Optional[FiniteFloat] = None


class SignScan(BaseModel):
    model_config = ConfigDict(extra="allow")
    # 标准签认必须带编号；纯确认重试/别名路径允许只给 token，由服务补发编号。
    code: Optional[Code] = None
    # 标准流程带计算凭证；个别直接确认写法可改给 panel+survey，由服务即时试算。
    token: Optional[Annotated[str, StringConstraints(strip_whitespace=True, max_length=160)]] = None
    panel: Optional[Code] = None
    survey: Optional[Code] = None
    control_band: Optional[FiniteFloat] = None
    trial_band: Optional[FiniteFloat] = None
    band: Optional[FiniteFloat] = None
    gauge: Optional[FiniteFloat] = None
