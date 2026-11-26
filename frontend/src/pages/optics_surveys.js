        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "局部密度、离群踏点和分析簿",
  "module": "OPTICS 走向与离群观察",
  "caption": "OPTICS 走向与离群观察",
  "detail": "在同分区和同轮次内用 OPTICS 划分空间与读数的密度簇。低于试调关注线的踏点先单列保留，其余踏点再归入密度组；试算不动现行关注线，排课照常，确认时才一次性切换关注线与签认分析。",
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
    },
    {
      "name": "control_band",
      "label": "签认关注线"
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
        },
        {
          "name": "control_band",
          "label": "试调关注线 / 演练关注线（留空用现行线）",
          "kind": "float",
          "initial": "",
          "optional": true
        }
      ],
      "help": "复核员可在本页试调关注线：低读数踏点先单列，其余点再分组。试调只生成试算，不改动现行关注线，也不影响排课；确认签认后才生效。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "sign_scan",
      "label": "确认并保存密度分析簿（签认）",
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
      "help": "确认时关注线与签认分析一次性切换，旧分析不得再新设围挡；同凭证重试不会重复签认。补录踏点一经复核，原试算过期须重新分析。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入并确认签认"
    }
  ]
};

        export const {title} = page;
        export const key = "optics_surveys";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
