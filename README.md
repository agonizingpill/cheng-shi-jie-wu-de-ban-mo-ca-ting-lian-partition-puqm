# 城市街舞地板摩擦与停练分区

雨燕街舞教学社的地面走测和改课工作席。分区保存测点、密度结构、围挡和其解除凭证，课程保留原分区及改派记录。

## 现场工作与联系人

模拟客户为雨燕街舞教学社。踏点摩擦、密度簇、无练区围挡、开课跨区调整；低摩擦离群点不可被正常簇吸收。

- 舞室地板分块 `studio_panels`，字段为 `room`（舞室）、`label`（胶带区名）、`x1`（起点 X cm）、`y1`（起点 Y cm）、`x2`（终点 X cm）、`y2`（终点 Y cm）、`people`（小班人数上限）、`control_band`（演练关注线）。模型约束位于 `backend/domain/studio_panels_model.py`，规则位于 `studio_panels_service.py`。
- 按踏点录入走向测值 `floor_readings`，字段为 `panel`（地板块）、`survey`（走测轮次）、`x_cm`（点位 X cm）、`y_cm`（点位 Y cm）、`slide`（模拟滑步读数）、`capture_key`（轮次点位凭证）、`checked`（已复核）。模型约束位于 `backend/domain/floor_readings_model.py`，规则位于 `floor_readings_service.py`。
- OPTICS 走向与离群观察 `optics_surveys`，字段为 `panel`（地板块）、`survey`（走测轮次）、`low_points`（单列点位）、`members`（分区点位）、`clusters`（密度簇数）、`noise`（未分组数）、`token`（分析凭证）。模型约束位于 `backend/domain/optics_surveys_model.py`，规则位于 `optics_surveys_service.py`。
- 停练带与复测解封 `practice_holds`，字段为 `panel`（停练区）、`point`（触发踏点）、`review`（分析簿）、`shift`（课程时段）、`scope_key`（分区时段钥匙）、`reason`（围挡原因）、`status`（围挡状态）、`retest`（复测踏点）。模型约束位于 `backend/domain/practice_holds_model.py`，规则位于 `practice_holds_service.py`。
- 课程与调区回执 `dance_blocks`，字段为 `course`（课目）、`shift`（开课时段）、`headcount`（参与人数）、`home_panel`（原分区）、`live_panel`（当前分区）、`move_note`（调区原因）、`state`（课程状态）。模型约束位于 `backend/domain/dance_blocks_model.py`，规则位于 `dance_blocks_service.py`。

### 一天的业务操作

1. 16:00 朱青核对东侧舞室的粉 A、蓝 B、白 C 胶带范围。
2. 16:20 录入 SUR-E-01 踏点，(95,90) 读数为 0.21，复核人过单。
3. 16:45 运行 OPTICS 并保存 SCAN-QA，将两个低读数点留在密度组之外。
4. 17:00 对 EV-02 课程时段设置 HOLD-QA。原 A 区开课被拦。
5. 17:05 白 C 只能容纳 7 人，9 人的小班改派蓝 B。
6. 18:00 在蓝 B 开课，之后对粉 A 的同坐标做 SUR-E-02 复测。
7. 19:10 审核复测，保留原围挡历史与当前解封状态。

## 启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

打开 `http://127.0.0.1:18322`。FastAPI OpenAPI 在 `http://127.0.0.1:19322/docs`。
Compose 运行 Nginx、Python FastAPI、独立 Redis 消费进程、SQL 数据库和 Redis，SQL 与 Redis 使用命名卷。
使用 compose 的 bind mount 或在 Python 3.11 环境安装 `backend/requirements.txt` 后从 backend 目录运行 `uvicorn core.app:app`。须提供 `DATABASE_URL`、`REDIS_URL`、`JWT_SECRET`，`SEED_DEMO` 控制演示初始化。

| 演示账号 | 权限 |
|---|---|
| operator@demo.test | 提交领域记录和计算请求 |
| reviewer@demo.test | 提交记录并执行有业务约束的复核操作 |
| viewer@demo.test | 浏览业务台账 |

三个本地演示账号均使用 `DemoC0de!2026`。角色在 `backend/core/roles.py` 和 `frontend/src/store.js` 中声明。计算状态在 worker、queueing、API 和同一前端 store 中使用。

## 页面与接口

| 业务任务 | FastAPI 路由 | 页面 |
|---|---|---|
| 舞室地板分块 | `/studio_panels` /studio_panels/set-gauge | `frontend/src/pages/studio_panels.js` |
| 按踏点录入走向测值 | `/floor_readings` /floor_readings/record-step，/floor_readings/verify-step | `frontend/src/pages/floor_readings.js` |
| OPTICS 走向与离群观察 | `/optics_surveys` /optics_surveys/cluster-floor，/optics_surveys/sign-scan | `frontend/src/pages/optics_surveys.js` |
| 停练带与复测解封 | `/practice_holds` /practice_holds/post-hold，/practice_holds/clear-hold | `frontend/src/pages/practice_holds.js` |
| 课程与调区回执 | `/dance_blocks` /dance_blocks/move-class，/dance_blocks/open-class | `frontend/src/pages/dance_blocks.js` |

SQL 实体与约束在 `backend/domain` 下维护。前端使用原生 ES modules。核心算子为 OPTICS。将 x 和 y 除以 55 cm、相对读数除以 .18，实际运行 OPTICS 计算可达距离和簇。独立点位单列，无限可达距离记录为 null。按同批已复核踏点固定顺序运算。

读数来源为虚拟场地巡查，关注线只服务演练闭环。项目不提供现实场地安全阈值、材料处理措施或开课安全认证。当前场景只支持同一个舞室内改派。

[MIT](LICENSE)
