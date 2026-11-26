        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "落点测读与踏点复核",
  "module": "按踏点录入走向测值",
  "caption": "按踏点录入走向测值",
  "detail": "测值必须对应胶带区内的厘米坐标，同一轮次同点只记录一次。后台分析仅使用审核记录。",
  "path": "/floor_readings",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "panel",
      "label": "地板块"
    },
    {
      "name": "survey",
      "label": "走测轮次"
    },
    {
      "name": "x_cm",
      "label": "点位 X cm"
    },
    {
      "name": "y_cm",
      "label": "点位 Y cm"
    },
    {
      "name": "slide",
      "label": "模拟滑步读数"
    },
    {
      "name": "capture_key",
      "label": "轮次点位凭证"
    },
    {
      "name": "checked",
      "label": "已复核"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "record_step",
      "label": "登记走向踏点",
      "path": "/floor_readings/record-step",
      "fields": [
        {
          "name": "code",
          "label": "踏点号",
          "kind": "text",
          "initial": "STEP-A-QA"
        },
        {
          "name": "panel",
          "label": "地板块",
          "kind": "text",
          "initial": "ZONE-A"
        },
        {
          "name": "survey",
          "label": "走测轮次",
          "kind": "text",
          "initial": "SUR-E-01"
        },
        {
          "name": "x_cm",
          "label": "点 X cm",
          "kind": "int",
          "initial": 95
        },
        {
          "name": "y_cm",
          "label": "点 Y cm",
          "kind": "int",
          "initial": 90
        },
        {
          "name": "slide",
          "label": "模拟滑步读数",
          "kind": "float",
          "initial": 0.21
        }
      ],
      "help": "用厘米坐标和相对模拟读数复现测点。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "verify_step",
      "label": "复核踏点量测",
      "path": "/floor_readings/verify-step",
      "fields": [
        {
          "name": "point",
          "label": "踏点号",
          "kind": "text",
          "initial": "STEP-A-QA"
        }
      ],
      "help": "复核员对照纸质走测记录后确认。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "floor_readings";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
