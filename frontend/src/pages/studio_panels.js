        import {workspace} from '../workspace.js';
        import {floorPlan} from '../floor-plan.js';

        const page = {
  "title": "舞室分区和课堂容量",
  "module": "舞室地板分块",
  "caption": "舞室地板分块",
  "detail": "为每块地面布置独立胶带边界，保留最大课堂人数。本地演练关注线由现有场地记录输入。",
  "path": "/studio_panels",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "room",
      "label": "舞室"
    },
    {
      "name": "label",
      "label": "胶带区名"
    },
    {
      "name": "x1",
      "label": "起点 X cm"
    },
    {
      "name": "y1",
      "label": "起点 Y cm"
    },
    {
      "name": "x2",
      "label": "终点 X cm"
    },
    {
      "name": "y2",
      "label": "终点 Y cm"
    },
    {
      "name": "people",
      "label": "小班人数上限"
    },
    {
      "name": "control_band",
      "label": "演练关注线"
    }
  ],
  "layout": "split",
  "view": "grid",
  "actions": [
    {
      "name": "set_gauge",
      "label": "调整演练关注线",
      "path": "/studio_panels/set-gauge",
      "fields": [
        {
          "name": "panel",
          "label": "分区号",
          "kind": "text",
          "initial": "ZONE-A"
        },
        {
          "name": "control_band",
          "label": "演练关注线",
          "kind": "float",
          "initial": 0.34
        }
      ],
      "help": "内部实验参考参数；对既有分析签认需重新校核。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "studio_panels";
        export async function render(root, role) {
          await workspace(root, role, page);
          await floorPlan(root);

        }
