# product-docs L1 吸收专项计划

日期：2026-10-25。计划版本：`2026-10-25.l1-plan.1`。
性质：S9 的实施与发布收口计划及证据入口；D1/D2 已实施，后续发布动作受本文件门禁约束。
唯一执行进度由[四技能吸收计划](skill-absorption-plan.md)维护。
关联：[GitHub #15](https://github.com/jadelaglace/codex-skills/issues/15)。

## 1. 要达到的结果与本次边界

用户最新原话：“开始下一步吧 仔细严谨 闭环掉”。
该指令在 S8 本机同步完成后启动 S9 L1 实施：复核实时基线、建立独立备份，
按已审阅 D1/D2 精确 diff 修改仓库 reference，并完成验证与终态回写。用户已明确
“ok继续吧 L1 闭环掉”，因此本轮实施范围已授权；不扩展到安装、版本或发布。

目标是补足真正改变文档维护决策的缺口，同时保护现有用户意图、恢复防重放、
按需专业化及整体交付回收责任。外部截图复刻是比较材料，不能直接替换现役技能。

本轮后续修改范围为仓库 `product-docs` patch 版本、安装副本和实施证据/进度记录；不改外部材料。
公开 GitHub 写操作仅在自测与精确提交完成后进行；不创建 GitHub Release，除非后续明确要求。
S0–S8 和已有 Babata 验证均保持终态，不重复安装、自测或启动真实项目任务。

## 2. 来源、基线与证据限制

### 2.1 来源地位

外部只读根为本机 `codex-skills-replicas/screenshot-lineage`：

| 材料 | 本轮使用方式 | 限制 |
| --- | --- | --- |
| `ABSORB-PLAN.md` §5 | 恢复 P01–P07、K02、K03 九项及 K01 复评要求 | 旧计划的“延后”不是当前仍有缺口的证明 |
| `project-docs/SKILL.md` | 对照两区、路由、任务链、模板与收尾具体表述 | 截图 OCR 后复刻，属于解释层；不是原始源码 |
| 原截图 p20–p21 | 来源位置索引 | 本轮未重新逐像素核对；不把复刻中的推断升级为用户新决定 |
| [现役入口](../skills/product-docs/SKILL.md)及相关 references | 判断已有覆盖与不可破坏合同 | 仓库与安装入口有已知 metadata 差异，分别保护 |
| [专业化记录](../skills/product-docs/references/quality-specialization-plan.md) | 核对用户要求的各层下发、回收、本层验收与整体交付 | 历史计划不是第二个运行合同；专业规则以实际 Skill 为准 |

复刻文件自身标注了路由单元格不可辨认后的推断、版本头 v4/历史 v5 差异及路径统一。
因此不能因为它写了“铁律”就复制强制路由，不能依其路径创建本机通信设施。
本轮没有执行新的外部研究，也没有重新审计原始项目。

### 2.2 冻结身份

规划基线 HEAD：`70c18bd9df346e0e3cd555f95c75350eb644e649`。
发布前基线为 `product-docs` `1.0.3`；本轮目标版本为兼容 patch `1.0.4`，三个专业技能
仓库/安装版本均为 `1.1.0`。

| 对象 | SHA256 |
| --- | --- |
| 仓库 `product-docs/SKILL.md` | `F08AC541A3A19B4B1AE68BA1A52A3BD4E07EAF3B57052F8B950CBDFF9CD1E608` |
| 安装 `product-docs/SKILL.md` | `327EF8944E170A1C15BCDF192205C5103BF90584E0CF93F947E041E6B6F080BD` |
| 外部 `ABSORB-PLAN.md` | `FD3FA969109774EB0A81905864DA763E68905DDDE0EC85EAA5B3CD6C31D73F22` |
| 外部 `project-docs/SKILL.md` | `4AEFEA3A75559F4C1BA58A04E6D3E20CD32D1A8AA0C38880291A09FDC24271CB` |

保护清单见[本轮基线](validation/2026-10-25-product-docs-l1/baseline.json)：
仓库 skills 全树 27 文件、四个安装技能 19 文件、README 与两个外部文件，共 49 文件；
摘要保存清单范围、关键文件大小与哈希，不包含凭据或原图正文。该文件是校验快照，
**不是可还原内容备份**。
实施前必须重核基线并建立独立内容备份；不能把 S1/S8 备份当作 L1 的备份。

## 3. 全项裁决与唯一落点

下表逐项区分现役覆盖和本轮建议。九项延后候选，加一项 K01 前置复评，共十项。
“已有”不表示刚刚实施；“拒绝”针对冲突机制；“延后”保留明确的重新评估条件。

| ID | 当前覆盖、差异与风险 | 本轮建议 | 唯一合同落点 / 后续触发 |
| --- | --- | --- | --- |
| P01 | 入口已有 current truth 优先，lifecycle 已分开当前意图与原话证据；尚未明确禁止用连续勘误维持过期解释正文 | 仅补“已采用决定落到当前正文”这一句组；拒绝强制所有文档两区、50 条压缩原话及多份引文副本 | `document-chain.md` → One Primary Authority And Honest Status；预览 D1 |
| P02 | Persist New Governing Input First + lifecycle First Capture 已要求先落盘后分析，并区分产品原话、通用协议、执行事实 | 已有，不再加一条 docs-first；保留恢复时先核 Goal/当前项，不能被“先写原话”越过 | 现有入口与 `intent-plan-lifecycle.md`；零增量 |
| P03 | 入口、document-chain 和 governance 已区分权威、派生、状态与证据；PRD/设计/测试也可能各自拥有实际合同 | 按角色保留单一权威；拒绝固定 01/04/05/07 永远控制、02/03/06 永远次级的划分 | `document-chain.md` Authority Roles、governance 既有所有权；零增量 |
| P04 | 单一当前项、阶段终态、禁止重放、下发/回收已有；一项可有多个合法子阶段 | 已有，不强制每事建 issue、不另造派单状态机；跨会话先核当前项，完成记录禁止重复派发 | `intent-plan-lifecycle.md` + 入口专业回收段；零增量 |
| P05 | 现役已规定只有真实 caller/生命周期边界需要时才建协议；当前任务无多会话协作需要 | 继续延后独立 interchange 协议；不创建角色信箱、目录、花名册或自动发信 | 触发：用户明确协作需求且现有可用通道不能满足；另立协议范围与验收，不塞入产品入口 |
| P06 | document-chain 已以权威、读者、节奏和独立契约判断拆合，入口要求 purpose/exclusions 可发现 | 保留职责内聚；拒绝“出现和就拆”和“不写边界声明”；不拆已有有效文档 | `document-chain.md` Make The Contract Discoverable、Split Or Combine Deliberately；零增量 |
| P07 | 改名/移动已有旧路径搜索；对未改名的语义、状态变更，受影响引用检查尚可更明确 | 增补有界 stale-reference 检查；拒绝每次全文扫描、全量数字对账及自动 bump 所有版本 | `document-chain.md` → Stable Navigation And Renames；预览 D2 |
| K02 | greenfield 已有按角色最小建链，明确不造空壳；未发现编号缺失导致的实际故障 | 不新增 01–07 reference、不改名、不铺七文件；可选编号建议也须有具体使用需要再评估 | 现有 `greenfield-init.md`；触发：真实新项目明确需要该模板，且不重复现有角色表 |
| K03 | 入口已有轻重相称的 Coherent Rounds、terminal maintenance、按实际影响传播与报告 | 已有；D2 补引用核对后不另建 Round-Close 清单；不强制每回合 bump/版本史/commit | 既有入口与 lifecycle；零增量 |
| K01 | 用户要求各参与层下发、收回、验证，但现役允许直接专业调用、按需设计和复用证据 | 重新评估后保留按需专业化，拒绝强制逐层中转和固定写权层级；不改变用户整体交付验收权 | 入口 Connect Specialist Quality Work Conditionally；零增量 |

明确不吸收不等于取消原有要求。例如拒绝机械“数字对账”，不取消真实运行声明必须回读系统、
状态声明必须有匹配证据的现役规则；不新建 Round-Close，不免除既有阶段终态回写。

## 4. 两处可审阅候选改法

目标只有 [document-chain.md](../skills/product-docs/references/document-chain.md)。
独立预览与实施身份见[L1 patch evidence](validation/2026-10-25-product-docs-l1/PATCH-EVIDENCE.md)。
它未应用到 Skill；候选只增加 10 个非空物理行，不删除、替换或迁移现有正文。
不改入口/description/UI，不增加 reference 文件，不复制规则到别处。预算上限为该 reference
净增 16 个非空物理行；预算是本次约束，不是以后所有 Skill 的通用上限。

### D1：P01，当前正文与历史证据分开维护

锚点为 `One Primary Authority And Honest Status` 中以下两行之后：

```text
- Reference or summarize these facts elsewhere without competing editable
  copies, and make the update direction clear.
```

新增英文候选全文：

```text
- When an adopted decision changes interpreted current truth, update the owning
  body in place instead of stacking corrective addenda. Preserve exact user
  wording, adopted-decision history, and completion evidence in their existing
  authorities; do not rewrite historical or still-effective material.
```

只对已经采用的决定更新当前解释正文；一个问题、外部建议或候选不能触发覆盖。
不删除原话、已采用历史、失败记录和完成证据。若原项目规定独立修订记录，保留其记录，
但当前正文不能要求读者自行叠加多轮勘误才能判断现状。

### D2：P07，按影响检查陈旧引用

锚点为 `Stable Navigation And Renames` 中本段之后、`When renaming or moving...` 之前：

```text
Prefer the repository's existing stable document identifiers, authority index,
and registry when filenames or ordering may change. Introduce an identifier,
glossary, relationship diagram, or grouped naming convention only when it makes
authority or navigation materially clearer. Follow a locally adopted numbering
scheme; do not impose a universal numeric or alphabetic pattern.
```

新增英文候选全文：

```text
After changing document meaning, status, or navigation, inspect the affected
live references for stale paths, section targets, and conflicting current
claims. Repair actual drift; unchanged references need no edit. Preserve old
names and claims in exact quotations and historical evidence with their source
context; do not make them current by proximity. This check does not require a
whole-repository audit, mechanical version bumps, or rewriting history.
```

按语义依赖检查当前可执行引用，目标可以是路径、节锚点或仍指向旧结论的当前声明。
不把引用出现次数当真源冲突证据：带来源的历史引用合法。保留原改名四步及其精确引文保护，
以通用段规定适用范围、原四步规定改名场景，不复制成第二份清单。

## 5. 后续实施步骤与门禁

本节是待批准的实施路线；S9 规划完成不自动启动其中任何阶段。

| 阶段 | 工作 | 必须满足的退出条件 |
| --- | --- | --- |
| L1-A：复核 | 先按恢复链核新指令，再核 HEAD、dirty 状态、目标/reference/安装清单与基线 | 当前内容与预览绑定；若外部或本地已更新，先评估具体漂移，旧补丁不得盲套；本轮已通过 |
| L1-B：独立备份与预览确认 | 在独立持久本地目录保存仓库 product-docs 和安装 product-docs 完整文件树，标记各自身份、文件集、大小、SHA256；回读复制内容；重核 D1/D2 精确 diff | 内容可还原、无遗漏；备份不混进公开 Skill；本轮已通过 |
| L1-C：最小实施 | 只向仓库目标 reference 应用经确认的 D1/D2；先检查锚点唯一、不能重复插入 | 除已批准目标外的保护文件逐一不变；规则仅定义一处；无目录迁移/原话清理/路由改变；本轮已通过 |
| L1-D：自检与修复 | 做范围/链接/锚点/负例与情境审查、官方格式检查，检查新文本环境绑定和预算 | 每项结果及限制可回读；本轮已通过；实际 diff 与候选一致 |
| L1-E：交付决策 | 升级兼容 patch 版本，备份并同步安装副本，精确提交后 push/日期标签，回读 GitHub 状态 | 仓库、安装、Git、GitHub 四层身份一致；运行时实战与用户接受仍单独标为 pending |

独立备份只针对新轮事实，不改写 S1/S8 备份；既有 Git 版本是历史，备份用于未提交内容与安装态恢复，
二者不能互相冒充。首次预检 product-docs 仓库/安装共 16 文件，未来以实际清单为准；
对新增文件必须记录 absent-before，对任何已有额外文件先判断所有权，不能镜像删除。

Git 留痕沿用精确路径/逐项 diff 审阅，不 `git add .`，不夹带 README、research/report 技能、验证生成物。
本机“发布”仅指同步到用户指定 `.agents/skills`，GitHub “gh/上传”指 push，两者独立回读。
若只改本计划与检查记录，不能为此升级任何 Skill。候选若最终作为兼容修正实施，可按既有规则
考虑 product-docs 的 patch 版本；本计划不预定新版本号，不推断 minor/major 授权。
安装入口已知缺 metadata 的差异必须明确处理和验收，不能本轮顺手修复。

## 6. 验收方案：证明行为，不靠关键词宣称通过

### 6.1 静态与保护检查

1. 检查十项 ID 各有唯一裁决行，D1/D2 各有唯一合同落点，延后项有触发条件。
2. 候选补丁对基线 dry-run 适用，改变的文件集恰为一文件；实际实施时另核实际 diff。
3. 原有 Goal 优先/三层恢复/终态防重放/阶段冻结/证据等级/条件路由不变。
4. 本地链接存在，受影响节目标真实可定位；历史原话引用不被改写。
5. 无凭据、私有服务、通信花名、特定项目/桌面/主机路径进入候选 Skill 新文本。
6. 保护清单文件集、大小及 SHA256 不变；实施时只豁免明确批准的目标文件。
7. 实施后运行官方 `quick_validate.py`，实际解析 frontmatter 与 UI（若涉及），保留失败与结果。
   本次未改 Skill，不重复格式验证；预览 dry-run 不等于行为测试或实际修改成功。
8. 检查修订文档的空白和 `git diff --check`；新建未跟踪文档也独立检查，不能只查 tracked diff。

### 6.2 情境审查与反例

| Case | 输入/故障 | 正确结果 | 必须拒绝的结果 |
| --- | --- | --- | --- |
| T01 | 用户已采用 B，当前解释正文仍 A，尾部另有“改为 B” | 更新当前正文为 B；原话、决定历史仍可回读 | 只追加第三条勘误，或删去 A 的历史证据 |
| T02 | 外部仅推荐 B，用户尚未决定 | 候选带来源，当前决定仍 A | 因 D1 把正文改为 B |
| T03 | 通用过程纠正与产品需求混合输入 | 分别落进度/原话角色，再分析；恢复先核当前项 | 一股脑写进 PRD，或先搜旧史 |
| T04 | 同一阶段已在对话汇报完成，docs 未回写 | 只补终态回写；不重复执行/测试/发布 | 借 P04 重新派单或重跑 |
| T05 | 一个文档有同权威同节奏的需求与约束，句子含“和” | 内聚保留，必要职责边界可写 | 机械拆成多文件，禁止写 exclusions |
| T06 | 用户只修一条文字，或直接请求 code-quality | 按影响使用现有入口；不强制四层串行 | 为“闭环”启动设计/架构全审 |
| T07 | 纯后端任务无界面 | 条件跳过设计，保留适用专业验收 | 虚构界面和设计产物 |
| T08 | 改验收结论但不改路径，当前计划仍引旧结论 | 查受影响引用并修正，未受影响文档不改 | 只检查文件是否存在就宣布无陈旧引用 |
| T09 | 历史引文含旧文件名，当前入口已正确 | 保留引文与日期来源；当前入口可导航 | 全局替换引文或把合法历史报错 |
| T10 | 大检查表有所有数字但真实运行未回读 | 维持证据缺口，不能宣布真实完成 | 用拒绝数字对账为由免除真实证据核验 |
| T11 | 新项目简单，无人要求 01–07 编号 | 依 greenfield 建最小链，不铺空壳 | 因 K02 建七份文件 |
| T12 | 只有本会话，没有协作需求 | P05 延后，不建协议/角色目录/发信 | 根据截图路径建立通信设施 |
| T13 | 文档状态 changed，正文引用未受影响 | 有界检查后保持未变；记录需要的证据 | 每回合 bump 所有版本并强制 commit |
| T14 | 上游收到单测通过，缺真实集成或视觉证据 | 各层收回本层核验，保留未验证和用户接受缺口 | 将局部工程证据升级为整体交付 |

本轮对这些 Case 做的是候选方案的人工情境审查；结果记录在独立检查报告。
将来实施后的真实前向验证须使用隔离 fixture/镜像并记录实际行为；不能把本表、
dry-run、关键词检查或旧 Babata 测试当成新 Skill 行为已验证。

## 7. 停止条件与回滚

下列情况停止对应阶段，保持已完成的无关工作，并报告具体对象/证据：
目标哈希漂移未解释、预览锚点不唯一、备份不可回读、原话/终态保护受损、
出现无授权的安装/外部写需求、验证失败无法在批准范围内修复。

本次只生成计划和预览，没有 Skill 回滚需求。后续若实施失败：

- 先核实际 diff 与独立备份，仅恢复自己本轮修改的文件/片段；保留用户并发修改。
- 若并发修改重叠，先停止该文件恢复，报告冲突；不整树覆盖，不 reset hard，不清理工作区。
- 未安装时不触碰安装副本；已获安装授权并执行后，只用该轮安装前备份恢复受影响文件。
- Git 已提交或已 push 的历史不能用 force push 重写来伪装无事发生，按新授权选择修复提交。
- 删除新增文件前核 absent-before 与所有权；不要删其他会话或用户新建内容。

## 8. S9 收口与恢复入口

规划终态及实际检查结果见[检查报告](validation/2026-10-25-product-docs-l1/REVIEW.md)。
完成发布收口后，主计划当前项应回写为 `S9-publication-terminal-with-limits`；GitHub #15、
阶段 issue #9–#15 应按实际执行证据关闭，不能先行勾选。安装与 GitHub 身份必须逐文件回读；
运行时实战、外部搜索/渲染、真实用户接受仍不能因发布成功而自动完成。

下次若要运行时实战或用户验收，必须有新的明确指令；恢复时先 Goal/task API → README 浅入口 →
主计划当前项，本文件提供本轮方案与证据；旧 S8、旧编号基线与截图待办都不能重开。
