# 逆天主题（仙逆）游戏

## 这是什么

《仙逆》原著深度联动的修仙养成网页游戏：完整境界体系（炼气→筑基→结丹→元婴→化神→问鼎）、双风格（动漫/真人）资产、行路叙事层。由本地 Agent（Qoder）+ GPT 美术总监协作生产资产，人类拍板方向。

## 当前状态（As of 2026-09-03）

- 阶段：形态矩阵铺量期（6 系统 27 项变体，24/27 目检合格）
- 当前重点：收尾 3 张变体；4 大境界 real 风格背景视频待验收
- 最近重大变化：知识管理迁至本地 Obsidian vault + GitHub 多仓 SSOT（本仓 + handbook + workspace-index）
- 详细任务状态：docs/01-任务看板.md

## Source of Truth

- 项目总览：docs/00-项目总览.md
- 任务状态：docs/01-任务看板.md
- 资产状态：docs/02-资产清单.md
- 项目规格：docs/03-规格与规范.md

## 依赖规范

- handbook v1.0：https://github.com/201650545/handbook
- 项目 override：docs/03-规格与规范.md

## 项目结构

- `docs/` 知识库（本仓事实源）
- `workers/` 资产生产与校验脚本
- `assets/` 游戏内引用资产（成品图/视频/GLB 不入库）
- `preview/` 形态矩阵成品（不入库）
- `dsh-plugin/` DSH 插件

## 给 AI / Agent 的读取顺序

1. 本 README → 2. docs/00 总览 → 3. tasks / assets / spec → 4. 需要时查 handbook v1.0

## 不要假设

- 成品图 / 视频 / GLB 均不进本仓；资产清单之外的文件不视为正式资产
- GitHub 可能落后本地，以文档内时间戳为准
