        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "局部密度、离群踏点和分析簿",
  "module": "OPTICS 走向与离群观察",
  "caption": "OPTICS 走向与离群观察",
  "detail": "在同分区和同轮次内用 OPTICS 划分空间与读数的密度簇。低于演练关注线的踏点保持独立条目。",
  "path": "/optics_surveys",
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
      "name": "low_points",
      "label": "单列点位"
    },
    {
      "name": "members",
      "label": "分区点位"
    },
    {
      "name": "clusters",
      "label": "密度簇数"
    },
    {
      "name": "noise",
      "label": "未分组数"
    },
    {
      "name": "token",
      "label": "分析凭证"
    }
  ],
  "layout": "flip",
  "view": "grid",
  "actions": [
    {
      "name": "cluster_floor",
      "label": "计算踏点的密度分区",
      "path": "/optics_surveys/cluster-floor",
      "fields": [
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
        }
      ],
      "help": "将厘米点位和模拟读数映射到同一特征空间。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "sign_scan",
      "label": "保存密度分析簿",
      "path": "/optics_surveys/sign-scan",
      "fields": [
        {
          "name": "code",
          "label": "分析簿编号",
          "kind": "text",
          "initial": "SCAN-QA"
        },
        {
          "name": "token",
          "label": "计算凭证",
          "kind": "token",
          "initial": ""
        }
      ],
      "help": "签认簿保留密度组与独立踏点列表。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "optics_surveys";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
