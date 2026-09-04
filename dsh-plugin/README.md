# dsh-plugin · DSH 插件（运行时代码）

> 这是**唯一「碰了会中断运行」的目录**。改这里要重启 DSH 插件。
- `pkg\` — 折叠插件包：`src\index.ts`（服务/路由）、`lib\client.js`（浏览器测采集）。

## 别在这改的
素材本身（去 `assets\`）、文档（去 `docs\`）。这里只管插件怎么跑。
资产装订按 `workers/asset-manifest.schema.json` 契约，也不在这。