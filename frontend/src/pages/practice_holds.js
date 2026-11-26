        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "独立踏点停练与复测解封",
  "module": "停练带与复测解封",
  "caption": "停练带与复测解封",
  "detail": "审核人用独立踏点作依据，在选定课程时段设置围挡。解封需后续轮次的同坐标点，并经复核。",
  "path": "/practice_holds",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "panel",
      "label": "停练区"
    },
    {
      "name": "point",
      "label": "触发踏点"
    },
    {
      "name": "review",
      "label": "分析簿"
    },
    {
      "name": "shift",
      "label": "课程时段"
    },
    {
      "name": "scope_key",
      "label": "分区时段钥匙"
    },
    {
      "name": "reason",
      "label": "围挡原因"
    },
    {
      "name": "status",
      "label": "围挡状态"
    },
    {
      "name": "retest",
      "label": "复测踏点"
    }
  ],
  "layout": "split",
  "view": "table",
  "actions": [
    {
      "name": "post_hold",
      "label": "登记停练围挡",
      "path": "/practice_holds/post-hold",
      "fields": [
        {
          "name": "code",
          "label": "停练带编号",
          "kind": "text",
          "initial": "HOLD-QA"
        },
        {
          "name": "review",
          "label": "分析簿",
          "kind": "text",
          "initial": "SCAN-QA"
        },
        {
          "name": "point",
          "label": "独立踏点",
          "kind": "text",
          "initial": "STEP-A-QA"
        },
        {
          "name": "shift",
          "label": "开课时段",
          "kind": "text",
          "initial": "EV-02"
        },
        {
          "name": "reason",
          "label": "围挡缘由",
          "kind": "text",
          "initial": "巡场读数复核前暂停使用"
        }
      ],
      "help": "保持相关课程待开，不允许停练区签入。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "clear_hold",
      "label": "核对复测并解封",
      "path": "/practice_holds/clear-hold",
      "fields": [
        {
          "name": "hold",
          "label": "停练带号",
          "kind": "text",
          "initial": "HOLD-QA"
        },
        {
          "name": "retest",
          "label": "复测踏点",
          "kind": "text",
          "initial": "STEP-A-RETEST"
        }
      ],
      "help": "围挡历史和复测点均保留。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "practice_holds";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
