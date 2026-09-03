# AI 生成手册 · 官方图锚点版（AI 只补官方缺口）

> ⚠️ **主线是「官方海报 + 官方图优先」，AI 生成只补缺失部分**（后期境界、UI 专属构图）。
> 官方动画已更新至 153 集（约化神期），优先按 `workers\官方海报收集任务书.md` 扒官方海报；
> 官方没有的（如碎涅以后、UI 专属构图、王林后期形态）才用本手册让 AI 生成。
> 生成时用手上的官方王林 figure-01 + 境界 bg-01 当 Anchor，AI 照原片风格扩产。
> 依据：Kimi K3 + GPT-5.6 两轮问诊 + 版权放开（D-20260815-01）。用户决定 2026-08-15。

---

## 一、手上已有的官方锚点（workers\collected\）

| 境界 | figure-01 王林 | bg-01 背景 | 其他锚点 |
|---|---|---|---|
| ningqi 凝气 | ✅ 少年杂役/灰蓝弟子服 | ✅ 石崖云雾 | enemy-01 / treasure-01 |
| zhuji 筑基 | ✅ | ✅ | companion / skill-01 |
| jiedan 结丹 | ✅ | ✅（另有 scene-02） | treasure-01 |
| **yuanying 元婴** | ✅ 白发黑袍/红衣煞星 | ✅ | enemy-01 / treasure-01 |
| **huashen 化神** | ✅ 青衫木雕师/青衫胜雪 | ✅ | skill-01 / treasure-01 |
| yingbian 婴变 | ✅ | ✅ | enemy-01 / treasure-01 |
| wending 问鼎 | ✅ | ✅ | skill-01 / treasure-01 |
| yinyang 阴虚阳实 | ✅ | ✅ | companion / weapon-01 |
| nie 窥涅净涅 | ✅ | ✅ | skill-01 / treasure-01 |
| suinie 碎涅 | ✅ | ✅ | treasure-01 |
| kongnie 空涅 | ✅ | ✅（仅此） | — |
| tatian 踏天 | ✅ | ✅（仅此） | — |

> 所有境界都有 figure-01 + bg-01，这是生成一切的基础。

---

## 二、核心方法（怎么保证像原片）

### 1. 王林别用「自由发挥」，用官方图锁脸 —— 三选一
- **首选（最省事）**：生成王林立绘/海报时，把该境界 `figure-01.jpg` 当 Reference：
  - Midjourney：`--cref [figure-01路径/URL] --cw 100`（锁脸 + 特征）
  - SD WebUI：`IP-Adapter / Reference Only` 挂 figure-01
- **进阶（一致性最强）**：用全部 12 境 figure-01 训一个王林 LoRA（触发词 `wanglin_xianni`，rank 16~32），之后所有图带 `<lora:wanglin_xianni:0.8>`，跨境界永不串脸
- **保底**：直接「图生图」从 figure-01 改构图（Denoising 0.3~0.5），不换脸只换场景/服装细部

### 2. 风格统一靠「境界锚点图」—— 生成一套境界内资产时
- 每境界把 `bg-01.jpg` 当**风格参考**：MJ `--sref [bg-01]`；SD 用 IP-Adapter style reference
- 同一境界固定 seed + 色调词，保证背景/立绘/敌人/法宝同属一套视觉

### 3. 王林核心特征词（跨境界必须保留，中英都给）
```
中文：丹凤眼，黑发，身姿挺拔，气质冷峻，自带一缕煞气，动漫CG渲染，官方动画角色画风
English: phoenix eyes, black hair, upright bearing, cold sharp aura, subtle killing intent, 
  anime CG character render, official animation style
```
> 各境界只改「时代/服饰/气质」增量词，核心词不动。

---

## 三、MVP 三境界提示词（凝气 / 元婴 / 化神）

> 每境给「背景海报 + 王林立绘」两条；敌人/法宝套用第四节通用模板。

### 凝气期 ningqi（恒岳杂役，初心起步）
形象增量：`青涩农家少年，粗布麻衣`/`恒岳宗灰蓝弟子服，眼神狠辣`
色调：冷青 + 山岩灰 + 玄墨；氛围：朴素、山林、初入修真
```
【凝气·背景海报】中文：恒岳山后山悬崖，云雾缭绕，陡峭石崖，少年王林满身伤痛触碰天逆珠，冷青色山雾，史诗电影构图，体积光，动漫CG，官方仙逆画风，--ar 16:9
English: Hengyue Mountain rear cliff, misty clouds, steep rocky crag, wounded teenage Wang Lin touching Tianni pearl, cool cyan mountain fog, epic cinematic composition, volumetric light, anime CG, official Xian Ni style, --ar 16:9
【凝气·王林立绘】中文：王林，青涩农家少年，粗布麻衣，丹凤眼，黑发，冷峻，全身立绘，纯白背景，动漫CG官方画风，--ar 3:4 --cref [ningqi/figure-01] --cw 100
English: Wang Lin, youthful farmer boy, rough linen robe, phoenix eyes, black hair, cold, full body character stand, pure white background, anime CG official style, --ar 3:4 --cref [ningqi/figure-01] --cw 100
```

### 元婴期 yuanying（罗天星域，纵横一方）
形象增量：`白发黑袍，眉心古神星点`/`白发狂舞，红衣煞气，绝世煞星`
色调：星蓝 + 血红暗红；锚点名场面：**百万人头塔**
```
【元婴·背景海报】中文：赵国藤家城前百万人头塔，阴森血腥震撼苍穹，白发红衣煞气王林立于塔前，暗红血色、星蓝微光，史诗电影构图，动漫CG官方画风，--ar 16:9
English: Million Souls Tower before Teng Family city, grim bloody monumental, white-haired red-robed fierce Wang Lin standing before, dark crimson + star-blue glow, epic cinematic composition, anime CG official style, --ar 16:9
【元婴·王林立绘】中文：王林，白发狂舞，黑袍红衣，眉心两颗古神星点，丹凤眼冷峻，全身立绘，纯白背景，动漫CG官方画风，--ar 3:4 --cref [yuanying/figure-01] --cw 100
English: Wang Lin, wild white hair, black robe crimson sash, two ancient-god star marks on brow, phoenix eyes cold, full body stand, pure white background, anime CG official style, --ar 3:4 --cref [yuanying/figure-01] --cw 100
```

### 化神期 huashen（神游太虚）
形象增量：`朴素青衫木雕师，眼神深邃沧桑`/`青衫胜雪，道韵环绕，超凡脱俗`
色调：清冷青 + 银白；氛围：出尘、太虚、生死意境
```
【化神·背景海报】中文：雨之仙界仙玉祭坛，飞瀑流云，青衫胜雪道韵环绕的王林渡化神劫融入生死意境，清冷青色、银白辉光，空灵史诗构图，动漫CG官方画风，--ar 16:9
English: Rain Immortal Realm jade altar, waterfall and drifting clouds, cyan-robed snow-white Wang Lin merging life-and-death dao resonance through tribulation, cool cyan + silver glow, ethereal epic composition, anime CG official style, --ar 16:9
【化神·王林立绘】中文：王林，朴素青衫，眼神深邃沧桑，青衫胜雪道韵环绕，超凡脱俗，全身立绘，纯白背景，动漫CG官方画风，--ar 3:4 --cref [huashen/figure-01] --cw 100
English: Wang Lin, plain cyan robe, deep weary gaze, snow-pale robe with dao resonance, transcendent, full body stand, pure white background, anime CG official style, --ar 3:4 --cref [huashen/figure-01] --cw 100
```

---

## 四、通用模板（敌人 / 法宝 / 印章，全境界可套用）

```text
【敌人】中文：仙逆风格的<境界>强敌<名字>，<一句外形描述>，煞气逼人，头像/半身，暗色调，动漫CG官方画风，--ar 1:1
【法宝】中文：<法宝名>，<外形描述：半透明/符文/光芒>，纯白背景，道具设计，3D渲染风格，超精细，--ar 1:1  （可用 treasure-01 当 cref）
【境界印章/图标】中文：仙侠风格<境界名>印章/纹章，<境界专属元素+配色>，SVG线条风格，--ar 1:1
```

---

## 五、一致性工程要点

- **王林 LoRA 优先**：用 12 境 figure-01 + 你已有的 states/ 五态图全部喂训练，触发词统一
- **Identity Board**：把 凝气/元婴/化神 三张 figure-01 挑精华合成一张「王林演变板」，全局故事气泡里展示、也当 cref 增强一致性
- **每境界建 `style-guide.md`**：记色值（`#D4AF37` 结丹金 / `星蓝`元婴等）+ 专属元素 + 光照方向，后续补资产照抄
- **Master 保留**：每张生成图存 MASTER PNG → 处理成 RUNTIME WEBP + THUMB JPG，永不覆盖原图

---

## 六、生成后进入 runtime（接 asset-manifest）

- 生成图按 `assets\realms\<id>\` 归档命名（参考 `workers\asset-manifest.schema.json`）
- 背景/立绘/海报直填 manifest 的 `assets.bg / character / hero_poster`
- 敌人/法宝先只做 MVP 三境必需，缺失的让引擎 fallback 到前境

---

## 七、无片源下「声音」怎么办（接决策5）
- 不依赖动画音频：用**原创/本人声线**训 GPT-SoVITS 配「王林式冷静克制」判词（决策 5）
- 对白/BGM 不取自动画（无片源），改用免费古风音效库（若日后有片源再换官方 OST 属于锦上添花）
