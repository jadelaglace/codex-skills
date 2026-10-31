# 用 1028 新素材加固上一轮四技能吸收计划

日期：2026-10-31
计划版：`2026-10-31.four-skills-hardening.1`
状态：`plan-ready / implementation-requires-explicit-start`

## 0. 范围与结论

本计划只处理 1028 对上一轮四个已吸收技能的加固：

- `product-docs`
- `architecture`
- `design-standards`
- `code-quality`

1028 其他技能、其他 Agent 的复刻/去留计划、恢复机制 #16、安装、版本、commit、push、tag、Release 均排除在外。本文是计划和验收设计，不是运行队列，也不授权开始修改。本轮尚未修改 Skill、安装副本或 GitHub。

上一轮终态以[四技能吸收计划](skill-absorption-plan.md)为准：`product-docs` 1.0.4；其余三个技能 1.1.0。本轮不重做上一轮已完成的吸收、测试、安装或发布；只有新证据证明旧结论失效时才登记重新打开。

## 1. 1028 来源和证据边界

原图只读根目录：

`C:\\Users\\Aiano\\Desktop\\research_reports\\reports\\technology\\外部Skill翻新_1028版\\`

已知事实：

1. 归档含 33 张图，覆盖 28 个外部技能档案。
2. 本轮只读取四技能对应页面及跨页衔接；不把其余页面转成任务。
3. 临时逐页文本为 32/33，缺 `page_07.md`；缺页对应 `git-workflow`，不在本轮范围。不能把 32/33 说成完整逐字归档。
4. `docs/reference-transcripts/` 是 2026-10-23 旧批次，不能冒充 1028。
5. 原图中的内部路径、账号、凭据、项目名、固定地址和实例数字仅用于核对，不复制进公开 Skill。

四技能的 1028 原图切口按印刷页定位为：25/36 页承接 `product-docs` 开头，26/36 页承接 `product-docs` 结尾并进入 `design-standards` 与 `architecture`，27/36 页承接 `architecture` 结尾并进入 `code-quality`。页码只用于定位；跨页内容仍须以原图边界和来源哈希复核。

实施前对每条候选内容做四类裁决：`已有覆盖`、`确认新增`、`冲突不采纳`、`无法判定`。只有确认新增且能抽象为通用合同，才可进入补丁。字迹不清、项目特例和外部建议不能升级为规则。

## 2. 四技能裁决

### 2.1 `product-docs`：先对照，不改

1028 与现有合同的交集已被上一轮覆盖。本轮只核对并登记以下落点：

- 需求、产品行为和最终验收标准分开；
- 需求、架构、实现、测试和用户验收不互相冒充；
- 外部材料保持外部来源，明确采用后才进入当前合同；
- specialist 通过不能代替 product 层整体验收。

四点均有落点则记为 `已有覆盖 / 不改`。如发现真实缺口，单独记录来源、风险和最小修复候选，停止扩散，不复制其他技能规则。

### 2.2 `architecture`：先对照，不改

本轮核对：

- 选型说明为什么选、拒绝了什么、失败怎么办；
- 接口、数据所有权、输入输出和错误语义可检查；
- 功能单元完成不等于集成完成，架构层保留集成回收；
- 试验路径不会未经采用变成稳定技术栈。

当前无确认补丁。只有 1028 原句与现有合同存在可复现语义缺口时才另起最小补丁；不把设计验收或代码细节塞进架构入口。

### 2.3 `design-standards`：H01、H02

#### H01：分开参考图用途和成品图复用政策

上一轮 `One Image, One Job` 约束参考图各自承担的验证用途；1028 的“一图一用”可能是产品对成品图跨板块复用的政策。两者不等义。

候选落点：`skills/design-standards/references/visual-verification.md`，保留原参考图解释并在该节补入：

```text
### Reference Purpose And Delivered-Asset Reuse

Each reference image serves one purpose: a layout reference does not fix colour,
and a material reference does not fix typography. Mixing them is unfalsifiable.

Reference purpose and delivered-asset reuse are separate constraints. When the
adopted design requires distinct imagery across sections, check each finished
image against its intended placement and flag reuse that breaks that rule.
Do not invent a site-wide single-use policy when none was adopted. Logos,
icons, and intentionally recurring brand assets follow their own adopted rules.
```

验收：采用分板块成品图政策时能发现违规复用；未采用时不自创全站禁复用；logo、icon 和有意重复品牌资产按自身规则处理；参考图复用仍按用途区分。

#### H02：量化检查和聚焦视觉检查成对

1028 的实例数字不是全局门槛。可量化属性应记录阈值、方法、条件、实测结果；结构或感知属性应提出具体、可反驳的问题并检查实际输出；验收同时依赖两者时，两类证据都要满足。

候选落点：同一文件的 `## Self-Check And Refinement Record` 之前：

```text
## Pair Measurements With Focused Visual Inspection

For requirements that can be measured, record the adopted threshold, method,
conditions, and actual result. For structural or perceptual checks, ask a
specific question tied to an expected property or suspected defect, then
inspect the actual output; do not ask only whether it looks good. Keep the
question open to counterevidence rather than leading the reviewer to a pass.

When acceptance depends on both measurable and visual properties, require both:
a passing measurement does not prove visual quality, and a plausible image does
not prove a threshold. Use the applicable method for each property, not two
methods for every check. Report missing required evidence as unverified.
Keep check -> expected property -> measured result and/or visual observation
-> evidence in the existing refinement record. Project-specific brightness,
exposure, or size values are not universal gates.
```

验收：量化通过但文字被裁切不能整体通过；画面可读但阈值未测保持 `unverified`；只有尺寸要求时不强制视觉模型；不把 `<100`、`2.6x` 等实例数值固化。

### 2.4 `code-quality`：H03

1028 的有效增量是环境敏感证据边界：渲染后端、硬件、时钟/调度、大资产和配置会改变结果；单环境成功只能证明该环境。它应补进忠实探针和变化矩阵，不应变成所有测试强制双环境。

候选落点：`skills/code-quality/references/debugging.md`，现有 `## 3. Bisect With A Variation Matrix` 之前：

```text
### Qualify Environment-Sensitive Evidence

Record the runtime, relevant configuration, rendering backend, and clock or
scheduler mode when they can affect the result. Hardware and software
rendering, or real and virtual time, are different evidence conditions, not
interchangeable proof of the same path.

For environment-sensitive rendering, timing, or large-asset behavior, compare
the relevant execution paths while holding other inputs constant. State which
path reproduces the symptom and which supported environments the evidence
covers. Do not require duplicate environments for unrelated checks.

If a comparison path is unavailable, report the untested path and limit the
conclusion to the observed environment. An unmet required environment gate
remains blocked or unverified; this limitation does not turn it into a pass.
```

验收：记录运行时、配置、后端和时钟语义；固定其他输入比较；缺少必需环境为 `blocked`/`unverified`；无环境敏感性的纯函数不翻倍。

## 3. 实施范围和硬边界

| 对象 | 允许动作 | 明确不做 |
| --- | --- | --- |
| `product-docs` | 对照并记录已有覆盖 | 无确认缺口不改 |
| `architecture` | 对照并记录已有覆盖 | 无确认缺口不改 |
| `design-standards` | 仅 H01/H02 两个 reference 落点 | 不改入口、不禁所有复用、不固化实例数字、不固定模型 |
| `code-quality` | 仅 H03 一个 debugging reference 落点 | 不改四步、不强制双环境、不宣称未测环境通过 |
| 原图/转写 | 只读定位 | 不改名、覆盖、清理或补造缺页 |
| 他 Agent 工作 | 保留并避让 | 不接手、不回滚、不合并其他路线 |
| Git/安装 | 本轮不操作 | 不改版本、不安装、不 commit/push/tag/Release |

预算：design reference 净增不超过 35 行；debugging reference 净增不超过 20 行。出现第四处实质落点、并发重叠或合同冲突，立即停止并汇报。

## 4. 阶段计划和门禁

### P0：范围冻结（只读）

读取四技能入口、相关 reference、上一轮终态、本计划和 1028 对应原图；重新采集 HEAD、dirty 状态、目标文件清单与哈希；读取多 Agent 协调清单。目标重叠则停。

门禁：四技能页码和跨页可回读；保护边界清楚；未知项未被当成无差异。

### P1：四层差异裁决

逐条对照上一轮合同、reference、验收记录和保护边界，生成四类裁决表。`product-docs` 与 `architecture` 必须先完成对照，不能因为设计和代码有候选就默认它们也改。

门禁：每条候选有来源、语义、影响、证据等级和处理结论；外部建议未冒充用户决定；实例数字未变通用门槛。

### P2：候选预览

在内存副本或独立临时目录套用 H01–H03，只生成两个 reference 的预览 diff；确认旧规则、入口、链接和边界仍在，不写正式 Skill。

门禁：H01/H02/H03 各一个落点；敏感信息、标题、链接、行数预算通过；两项只读对照结论已落盘。

### P3：获得明确启动授权后实施

先写 design 的 H01/H02，回读 diff；再写 code 的 H03，回读 debugging 四步上下文。不改四个入口、不改版本、不同步 `.agents`。并发变化、锚点不唯一、删旧合同或需要第四处改动时停。

### P4：有界自测

先做文本语义情境审查；没有真实前向试用只能称静态/语义验证，不能称实战验证。

设计必须覆盖：成品复用政策的有/无、logo/icon 例外、量化绿但视觉失败、视觉可读但量化缺失、只有尺寸要求、实例数字不升级。

代码必须覆盖：真 GPU/软件渲染差异、真实/虚拟时间差异、必需环境缺失、纯函数不双跑、比较时只变一个因素。

每个 case 记录输入、采用约束、预期、实际、证据指针和 `pass/fail/unverified/blocked/not-run`。

### P5：终态回写

记录实际 diff、检查命令、失败和未执行项。只读规划成功且无义务时删除临时锚点；失败、阻塞、来源缺口和后续义务保留并标终态。只完成规划不得写成 Skill 已加固。

## 5. 自测矩阵

| ID | 场景 | 结论 |
| --- | --- | --- |
| D01 | 参考图多处复用但用途标注不同 | 允许参考复用，仍分用途 |
| D02 | 已采用分板块成品图却跨板块复用 | 报违反采用政策 |
| D03 | 未采用单次使用政策 | 不自创禁令 |
| D04 | logo/nav icon 多页重复 | 按采用规则判断 |
| D05 | 阈值通过但文字裁切 | 视觉失败，不整体通过 |
| D06 | 看着清楚但阈值未测 | `unverified` |
| D07 | 只有像素尺寸要求 | 只验尺寸 |
| D08 | 外部给出亮度/提亮实例数字 | 不变全局门槛 |
| C01 | GPU 成功、软件渲染失败 | 结论限于环境 |
| C02 | 虚拟时间超时、真实时间成功 | 分开时钟语义 |
| C03 | 必需环境不可用 | `blocked`/`unverified` |
| C04 | 纯函数无环境敏感性 | 不要求双跑 |
| C05 | 同时换后端和大资产 | 标记混杂，重做比较 |
| G01 | 1028 已被上一轮覆盖 | 记录已有覆盖，不补丁 |
| G02 | 来源模糊或项目特例 | 冲突/无法判定，停止升级 |
| G03 | 目标被其他 Agent 占用 | 停目标，保留对方改动 |

## 6. 静态检查、版本和交付

实施后至少运行：

```powershell
git status --short
git rev-parse HEAD
git diff -- skills/design-standards/references/visual-verification.md skills/code-quality/references/debugging.md
git diff --check
Get-FileHash skills/design-standards/references/visual-verification.md,skills/code-quality/references/debugging.md -Algorithm SHA256
```

还需检查：实际 diff 只含授权目标；三处落点唯一；旧参考用途规则和调试四步仍在；新文本无内部信息、固定模型或实例阈值；Markdown 链接/标题/围栏/尾空白/编码通过；原图、转写、保护树和他 Agent dirty 文件集不变。静态绿灯不等于运行时或用户验收。

本轮不改版本。将来若实施并获得明确发布授权，才考虑 design-standards 1.1.1、code-quality 1.1.1；product-docs/architecture 无实际改动不升级。仓库日期标签和 Skill 版本号继续分开。GitHub push、本地 `.agents` 发布、tag、Release 和用户接受分别授权、分别回读。

## 7. 当前终态

范围已收束到四技能；1028 其他技能和另一 Agent 计划已排除。`product-docs`、`architecture` 暂定只读对照；design 的 H01/H02、code 的 H03 是最小候选。本轮只修正计划并做文档自检，未实施、未安装、未改版本、未提交、未 push、未发布。

下一步只有用户明确启动实施时才按 P0→P5 走；仅要求评审计划时停在这里。
