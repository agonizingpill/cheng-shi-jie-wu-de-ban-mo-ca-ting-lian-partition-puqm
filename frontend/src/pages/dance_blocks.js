        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "分区调课与开课登记",
  "module": "课程与调区回执",
  "caption": "课程与调区回执",
  "detail": "原分区停练后可改派同舞室其他区块，并校验可用时段与容量。开课前再次防止进入围挡。",
  "path": "/dance_blocks",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "course",
      "label": "课目"
    },
    {
      "name": "shift",
      "label": "开课时段"
    },
    {
      "name": "headcount",
      "label": "参与人数"
    },
    {
      "name": "home_panel",
      "label": "原分区"
    },
    {
      "name": "live_panel",
      "label": "当前分区"
    },
    {
      "name": "move_note",
      "label": "调区原因"
    },
    {
      "name": "state",
      "label": "课程状态"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "move_class",
      "label": "改派停练区课程",
      "path": "/dance_blocks/move-class",
      "fields": [
        {
          "name": "course",
          "label": "课程号",
          "kind": "text",
          "initial": "CLASS-POP"
        },
        {
          "name": "to_panel",
          "label": "改派分区",
          "kind": "text",
          "initial": "ZONE-B"
        },
        {
          "name": "reason",
          "label": "调区回执备注",
          "kind": "text",
          "initial": "A 区围挡，改窗侧蓝胶带"
        }
      ],
      "help": "保留原课程分区，改派后写入新分区及回执备注。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "open_class",
      "label": "确认当前区开课",
      "path": "/dance_blocks/open-class",
      "fields": [
        {
          "name": "course",
          "label": "课程号",
          "kind": "text",
          "initial": "CLASS-POP"
        }
      ],
      "help": "围挡撤销或改派后可以确认。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "dance_blocks";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
