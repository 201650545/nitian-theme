# workers · 资产生产工作区

> **定位：只负责生产，不保存正式成果。**
> 正式成果分两处：运行代码 → `dsh-plugin/`，运行资产 → `assets/`；给人看的展示 → `preview/`。凡未验收的生成物、缓存、日志，一律留在这里或进下面的归档子目录。

## 分层（按职责，不是按文件类型堆）

| 层 | 位置 | 入 Git？ |
|---|---|---|
| **生产 / 采集 / 校验 / 修补脚本** | 按文件名前缀约定（见下表）平铺在 `workers/` 根 | ✅ 可复现生产 / 核查的脚本属于源码，**应入 Git** |
| **契约真源** | `workers/asset-manifest.schema.json` | ✅ **必须**（引擎怎么取资产的唯一真源，怎么摆 `assets/` 都以它为准） |
| **输入资料** | `T1-境界考证.json` `T2-编年史底稿.json` 等人工整理、可复现所需的源数据 | ✅ 必要部分入 Git |
| **缓存** | `workers/缓存/`（爬取缓存 / 采集原始结果） | ❌ 不入 |
| **待验收** | `workers/待验收/`（刚生成、尚未成为正式成果，含 `char_gen/`、`运行截图/`） | ❌ 不入 |
| **运行日志** | `workers/运行日志/`（task id / status / log / 运行截图） | ❌ 不入 |
| 历史遗留数据目录 | `collected/` `officials/` `states/` `treasures/` `ui/` `enemies/` | 按 .gitignore 边界走 |

### 脚本文件名前缀 → 类别（人看层快速归类，勿据此物理搬动）

| 前缀 | 类别 | 示例 |
|---|---|---|
| `gen_` `probe_` `mk_` | 生产：画资产 / 做背景 / 装配运行时 / 探测能力 | `gen_bt_batch.py`、`mk_bodycollect.py`、`probe_agnes_i2v.py` |
| `crawl_` `collect` `_merge_` `extract` `dump_` `find_` | 采集：爬取 / 提取 / 盘点 | `crawl_chronicle.py`、`extract_gpt.py`、`find_niyi.py` |
| `verify_` `check_` `dedup_` | 校验：核查 / 去重 | `verify_realms.py`、`check_realms.py`、`dedup_three.py` |
| `patch_` `fix_` `remap_` `rescale_` `split_` `rebuild_` | 修补：给已生成产物打补丁 / 修 bug | `patch_3d_viewer.py`、`fix_yuetianzhu.py`、`rescale_ladder.py` |

> **为什么脚本保持平铺不拆子目录**：文档与任务书里大量以 `python workers/xxx.py` 记录调用路径，物理搬动会全部断链，且这些是单次/可再生成的开发脚本，不值得为目录美学冒破坏风险。分层意图已由「前缀→类别 + 上表」固化；深入制作需求见 `docs/10-制作需求/`。

## 注意

- 这里是过程产物，不是给人看的成品。成品预览去 `preview/`，游戏资产去 `assets/`。
- 契约为真源：`asset-manifest.schema.json` 怎么说，`assets/` 就怎么摆；**缓存和生成结果可以丢，契约不能丢**。
- 新产生的未验收物 → `待验收/`；缓存 → `缓存/`；日志 → `运行日志/`。三者不入 Git（见 `.gitignore`）。