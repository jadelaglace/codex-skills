# 四技能吸收计划（仓库正式执行计划）

状态：`S0-completed / S1-completed / S2-completed / S3-completed / S4-completed / S5-completed / S6-completed / S7-completed`
版本：`2026-10-24.plan.1`
最后更新：2026-10-25
当前范围：把截图来源中的可迁移判据吸收到现有 `architecture`、`code-quality`、
`design-standards`；`product-docs` 本轮只保护、不修改。
执行授权：用户于 2026-10-24 明确启动 S3，随后明确“继续下一步，严谨并自测”；本次执行 S6，范围为三个专业 Skill 的跨技能校验与版本升级。
当前动作：S0（冻结基线、来源与工作区边界）、S1（持久备份和隔离）、S2（不落盘
diff 预览和 66 项唯一映射）、S3（吸收 architecture 判据）、S4（吸收 code-quality
判据与调试方法）、S5（吸收 design-standards 视觉判据）与 S6（跨技能校验并升级到
1.1.0）、S7（本地 review 与精确 commit）已完成；S8–S9 未启动。
S4 临时子计划（2026-10-25）：只修改本计划已授权的三个 code-quality 文件，保留
product-docs、architecture、design-standards、安装副本和既有工作区改动；独立 review
发现预览 C12 的字面替换会删除既有幂等性、版本、事务和恢复语义，因此保留该既有
bullet，仅追加失败路径和长操作判据；完成后以
预览编号 C01–C13、A12、K07、G02、G06 的唯一落点、行数预算、链接、敏感扫描和
保护哈希作为验收入口。S4 不改版本、不安装同步、不 commit、不 push、不打标签。
S5 临时子计划（2026-10-25）：只修改本计划已授权的两个 design-standards 文件，保留
product-docs、architecture、code-quality、安装副本和既有工作区改动；完成后以视觉判据
唯一落点、入口与 reference 行数预算、链接、敏感扫描、`git diff --check` 和保护哈希作为
验收入口。S5 不改版本、不安装同步、不 commit、不 push、不打标签。
S6 临时子计划（2026-10-25）：仅将三个目标入口的 `metadata.version` 从 `1.0.0`
改为 `1.1.0`，随后重跑 YAML/front matter、链接、敏感绑定、单一真源、预算、
`product-docs` 保护哈希和 `git diff --check`；不修改其它 Skill、不安装同步、不 commit、
不 push、不打标签。
S0 授权来源：用户明确“开始第一个”，对应 GitHub issue #6；不等于授权后续吸收、commit、安装或 push。

S0 终态证据（2026-10-24）：仓库四个基线文件的完整 SHA256 均符合计划前缀；
计划参考行数与 PowerShell `Get-Content` 行数各差 1，是末尾换行/读取口径差异，
不是内容漂移。外部计划仍为 906 行、状态“未执行”；来源归档存在 README、整理正文、
manifest 和 34 张原图。三个 `.agents\skills` 目录均存在，逐文件核对仅发现计划已知的
入口 `metadata.version` 缺失，未发现其它文件或内容差异。工作区既有未提交改动保持原样。
S0 不修改任何 Skill、安装副本或外部素材；S1 仅建立备份与验证清单，未修改目标内容。

S1 终态证据（2026-10-24）：备份根目录为
`C:\Users\Aiano\codex-skills-replicas\screenshot-lineage\absorb-backups\20261024-211750\`，
清单为 `backup-manifest.csv`。清单共 17 项：15 个已存在文件均已复制并逐项回读大小与
SHA256，2 个计划新 reference 明确记录为 `absent-before`，未伪造旧文件或哈希。备份包含
三个待改入口、两个待追加 reference、`product-docs/SKILL.md` 保护副本，以及三个
`.agents\skills` 目录的完整当前文件集（共 9 个文件）。自测通过：备份与源文件哈希一致，
`product-docs` 保持 `F08AC541A3A19B4B1AE68BA1A52A3BD4E07EAF3B57052F8B950CBDFF9CD1E608`，
外部计划保持原始哈希；仓库既有 `README.md`、`skills/report-render`、`skills/research-report`
改动保持不动。S1 未生成 diff、未改 Skill 或安装副本、未改版本、未 commit、未 push、未打标签。

S2 终态证据（2026-10-24）：仓库外初版预览目录为
`C:\Users\Aiano\codex-skills-replicas\screenshot-lineage\absorb-diffs\20261024-212614\`，
包含 `S2-DIFF-PREVIEW.md` 和 `S2-DIFF-MANIFEST.json`。预览绑定外部
`ABSORB-PLAN.md` SHA256
`FD3FA969109774EB0A81905864DA763E68905DDDE0EC85EAA5B3CD6C31D73F22`、仓库 HEAD
`e43c0cbe33a038ea1e94c563066546eb57b9a6e9`，覆盖 7 个且仅 7 个拟改文件，并将
G/K/C/A/V/P/E 组按 6/8/13/13/11/7/8 计为 66 个唯一 ID。初版自测通过：manifest
JSON 可解析，66 个 ID 各出现一次，7 个目标标题存在，公开文本无用户目录/私有
URL/凭证/临时目录，五个既有目标哈希及 `product-docs` 保护哈希仍与 S1 一致，
两个新 reference 仍不存在，工作区既有 `README.md`、`docs/`、`report-render`、
`research-report` 改动未被改写。初版 S2 发现一个必须在 S3 前解决的行数预算风险：
按逐点终稿原换行展开，三个入口 Skill 的拟增非空行约为 32/33/22，前两个超过
外部计划估算及 `+25` 上限。初版未压缩或改写终稿，也未写入 Skill、安装副本、
版本号或 Git 状态。

S2 预算修订证据（2026-10-24）：保留初版目录不变，新增仓库外修订目录为
`C:\Users\Aiano\codex-skills-replicas\screenshot-lineage\absorb-diffs\20261024-213900\`。
修订只压缩三个入口 `SKILL.md` 的英文表达并明确真实锚点替换；复核公开来源注释时发现三处
误指向仓库外暂存目录，现已改为稳定的无路径来源说明；66 个 ID、7 个目标、两个长 reference
的内容和独立预算均保持不变。按冻结目标文件的非空物理行、逐锚点
“插入行 - 替换掉的旧行”计算：architecture `25 - 5 = +20`、code-quality
`29 - 8 = +21`、design-standards `20 - 0 = +20`，均低于 `+25`。manifest 可解析，
66 个 ID 各一次，目标基线与 `product-docs` 哈希不变，新 reference 仍 absent-before，
初版预览哈希仍保持不变；敏感扫描无用户路径、凭证、私有地址或外部暂存路径命中。此修订仍是
S2 preview-only，不授权 S3、源码写入、版本变更、安装、commit、push 或发布。

## 0. 一页结论

这是一项“四技能吸收任务”的首轮：目标总体包含四个同宗技能，但本轮只落地
三个专业层（L2–L4），不改 L1 `product-docs`。完成三个专业层后，只能报告
“L2–L4 首轮吸收完成”；不能报告“四个技能全部完成”。L1 的延后项要单独形成
下一轮计划并重新取得用户授权。

基本策略：以仓库现有技能为骨架，吸收截图技能里可迁移的“怎么做对、怎么发现错”
判据；不替换现有恢复、授权、状态、证据和比例原则，不引入截图环境的强制路由、
固定文档目录或项目专属实现。

本轮计划默认结果：

- 仓库修改 7 个文件：3 个 `SKILL.md`、2 个新 references、2 个现有 references 追加；
- 三个技能的 `metadata.version` 从 `1.0.0` 升为 `1.1.0`；
- `product-docs` 保持 `1.0.3`，内容和 SHA256 不得变化；
- 不创建新 Skill，不修改截图原件，不修改外部计划，不自动安装、不 push、不打标签、不创建 GitHub Release；
- 阶段 2 先生成不落盘 diff；只有用户明确确认 diff 后才允许写入；
- 本地 commit 与本机安装同步是两个独立动作，均需单独回读证据。


## 子 issue 拆分（GitHub）

父 issue：#5（https://github.com/jadelaglace/codex-skills/issues/5）
- [x] S0：#6 [吸收 S0：冻结基线、来源与工作区边界](https://github.com/jadelaglace/codex-skills/issues/6)
- [x] S1：#7 [吸收 S1：建立持久仓库与安装副本备份](https://github.com/jadelaglace/codex-skills/issues/7)
- [x] S2：#8 [吸收 S2：生成不落盘 diff 与 66 项唯一落点映射](https://github.com/jadelaglace/codex-skills/issues/8)
- [x] S3：#9 [吸收 S3：吸收 architecture 判据](https://github.com/jadelaglace/codex-skills/issues/9)
- [x] S4：#10 [吸收 S4：吸收 code-quality 判据与调试方法](https://github.com/jadelaglace/codex-skills/issues/10)
- [x] S5：#11 [吸收 S5：吸收 design-standards 视觉判据](https://github.com/jadelaglace/codex-skills/issues/11)
- [x] S6：#12 [吸收 S6：跨技能校验并升级到 1.1.0](https://github.com/jadelaglace/codex-skills/issues/12)
- [x] S7：#13 [吸收 S7：本地 review 与精确 commit](https://github.com/jadelaglace/codex-skills/issues/13)
- [ ] S8：#14 [吸收 S8：同步三个 Skill 到本机 .agents](https://github.com/jadelaglace/codex-skills/issues/14)
- [ ] S9：#15 [吸收 S9：建立 product-docs L1 延后轮计划](https://github.com/jadelaglace/codex-skills/issues/15)

## 1. 权威、状态和不可混淆的文件

### 1.1 本计划的权威地位

本文件是目标仓库对本轮吸收任务的唯一执行计划。它记录当前范围、门禁、
执行顺序和终态，不复制每条稳定 Skill 规则。写入本文件不等于执行吸收。

### 1.2 外部计划只读参考

外部文件：

```text
C:\Users\Aiano\codex-skills-replicas\screenshot-lineage\ABSORB-PLAN.md
```

它保留外部整理出的 66 项裁决、逐点终稿和素材索引，本轮不再勘误、不修改、不把它
当作仓库执行状态。外部计划中的路径、脚本、备份命令和安装命令必须经过本计划的
本机路径、授权和安全门禁重写后才可执行。

外部计划已恢复为“状态：未执行”的原始版本。此前的审核意见只作为本计划设计输入，
不作为外部文件中的追加内容。

### 1.3 目标仓库和安装副本

仓库：

```text
C:\Users\Aiano\codex-skills
```

目标安装根（用户明确指定）：

```text
C:\Users\Aiano\.agents\skills
```

不得把 PowerShell 的 `~`、`$HOME` 或工具默认的 `.codex\skills` 当作本轮目标。
任何同步前都要解析并打印实际目标路径，确认它等于上面的绝对路径。

### 1.4 当前工作区状态快照

基线提交：`e43c0cbe33a038ea1e94c563066546eb57b9a6e9`（`main`）。
远端配置：`git@github.com:jadelaglace/codex-skills.git`。
本地 `origin/main` 当前缓存与 HEAD 一致；未据此声称 GitHub 实时无更新。

与本轮无关、必须保留的已有工作区改动：

```text
 M README.md
?? docs/
?? skills/report-render/
?? skills/research-report/
```

执行吸收时不得用宽泛的 `git add .`、`git checkout -- <目录>` 或目录级删除，
以免带入或破坏这些改动。

## 2. 用户目标、来源和边界

### 2.1 用户目标

用户要求把外部同宗技能中有价值的判据吸收到现有四技能体系，同时保持现有治理资产。
当前明确的外部材料只有截图复刻和整理文件；不是一个可以直接复制的原始 Skill 仓库。

用户已裁定采用外部建议，但“采用建议”只决定计划内容，不绕过本轮执行前的 diff 确认。

### 2.2 来源证据链

```text
桌面 34 张原图
  -> screenshot-lineage/project-arch / project-design / project-dev / project-docs
  -> COMPARISON.md
  -> answer-sheet.html（66 项）
  -> 外部 ABSORB-PLAN.md（逐点执行草案）
  -> 本仓库 skill-absorption-plan.md（本机安全执行计划）
```

原始素材目录：

```text
C:\Users\Aiano\Desktop\research_reports\reports\technology\近期AgentSkill构建
```

规则：原图只读；不修改、删除、重命名或覆盖来源。`README.md`、`整理正文.md`、
`manifest.json` 仅作页序和归档索引，原图是内容权威。OCR 是辅助，不能覆盖图像中
可见的结构、标记和用户裁决。

截图页码：

| 还原件 | 对应层 | 页码 |
|---|---|---|
| `project-arch` | L3 架构 | p17–p18 |
| `project-design` | L2 设计 | p18–p19 |
| `project-dev` | L4 开发测试 | p19–p20 |
| `project-docs` | L1 产品 | p20–p21 |

`report-render` / `research-report` 在 p22–p26，已经另行复刻安装，不属于本轮吸收目标。

### 2.3 必须清理的环境绑定

不得把以下内容写入公开 Skill 合同：用户名、本机绝对路径、个人仓库路径、内网地址、
服务名、端口、Cookie、Bearer token、API key、文档/表格 ID、客户/组织名称、真实样例、
截图中的历史验证数字、私有 Node 模块和特定环境脚本名。

可迁移的是职责、判据、失败处理、证据要求和方法。项目化例子要改成泛化表达；如果
一个例子无法去项目化，就留在外部还原件，不进入目标 Skill。

### 2.4 不吸收的冲突资产

本轮明确不引入：

- 四层强制路由；保留现有“按需专业化”和比例原则；
- `01`–`07` 固定文档目录；
- Round-Close 作为所有任务的强制流程；
- 截图版本历史 `v1`–`v5` 与 SemVer 并存；
- 截图环境的 `interchange` 协议、项目目录和私有工具；
- 新的状态词汇；继续使用仓库既有 `passed`、`failed`、`partial`、`skipped`、`blocked` 等状态；
- 任何“review 通过即授权实现”“路由即授权”“一张截图代表全部页面”等越权解释。

## 3. 基线和目标变更清单

### 3.1 阶段 0 基线哈希

执行前必须重新计算，以下只是计划生成时的参考快照：

| 文件 | 参考行数 | SHA256 前 16 位 | 版本 |
|---|---:|---|---|
| `skills/architecture/SKILL.md` | 122 | `12F9EC85B6DD10B4` | 1.0.0 |
| `skills/code-quality/SKILL.md` | 130 | `C19231B25795F792` | 1.0.0 |
| `skills/design-standards/SKILL.md` | 120 | `B8A27D0D35595921` | 1.0.0 |
| `skills/product-docs/SKILL.md` | 536 | `F08AC541A3A19B4B` | 1.0.3 |

任一基线不一致都停止，不尝试“顺手合并当前变化”。先汇报漂移并重新建立计划。

### 3.2 计划修改文件（共 7 个）

| # | 文件 | 动作 | 主要内容 |
|---:|---|---|---|
| 1 | `skills/architecture/SKILL.md` | 修改 | 选型三问、失败回落链、显式收尾、宿主解耦、任务单字段、回收沉淀、五态映射、指针和来源标记 |
| 2 | `skills/architecture/references/structure-and-topology.md` | 新建 | 存储、运行真源、跨服务参数命名、仓库拓扑、位置前缀可选实践 |
| 3 | `skills/code-quality/SKILL.md` | 修改 | 先读后写、标识符占用、最小 diff、case 断言化、边界三件套、证据三样、基线核算、最低证据门、指针和来源标记 |
| 4 | `skills/code-quality/references/debugging.md` | 新建 | 现象分类、逼真探针、变式矩阵、测量先验；每步带错误反例 |
| 5 | `skills/code-quality/references/review-and-tests.md` | 追加 | 断言形式和最小边界集合示例 |
| 6 | `skills/design-standards/SKILL.md` | 修改 | 气质词、A/B 候选、可判定规范、特征锁、提亮复核、点检不扩权、指针和来源标记 |
| 7 | `skills/design-standards/references/visual-verification.md` | 追加 | 逐屏比较、一图一用途、提示词约束、放大验字、单变量收敛 |

`skills/product-docs/SKILL.md` 和它的所有 references 本轮不得修改。

### 3.3 版本目标

三个实际改动的 Skill：`1.0.0 -> 1.1.0`。理由是新增可执行能力和 references，
属于向后兼容的功能增量，不是单纯修错。`product-docs` 保持 `1.0.3`。

版本改动必须在内容校验通过后单独完成，并在版本改动后重跑完整校验；不能让版本门禁
出现在版本尚未变更的阶段而造成自相矛盾。

## 4. 66 项裁决的闭合分配

### 4.1 数量闭合

66 项按下列互斥类别闭合：

| 类别 | 编号 | 数量 | 处理 |
|---|---|---:|---|
| 全篇原则 | G01、G03、G05、K01、K05、K06、K08 | 7 | 作为边界，不重复写成新规则 |
| G04 反例原则 | G04 | 1 | 只在调试和视觉 references 的对应段落落地 |
| 内容型插入 | C01–C13、A01–A13、V01–V11 | 37 | 第 4 节逐点执行 |
| 冲突裁决落地 | K04、K07 | 2 | 分别落在 architecture、code-quality |
| 机制型决定 | G02、G06 | 2 | 指针和来源标记，按目标文件落地 |
| 本轮延后 | P01–P07、K02、K03 | 9 | L1 专项轮或独立协议评估 |
| 执行协议 | E01–E08 | 8 | 本计划阶段和门禁 |
| **合计** |  | **66** | 互斥统计 |

G04 不能继续作为“未列入分类的 1 项”；它有对应落点但不新增通用正文规则。

### 4.2 延后项的准确归属

本轮延后不等于放弃，也不等于自动排队执行：

- `P01`、`P02`、`P03`、`P04`、`P06`、`P07`：落点候选为 `product-docs`，需 L1 专项授权；
- `K02`、`K03`：与 L1 文档链和收尾治理绑定，随 L1 专项重新决策；
- `P05`：独立 interchange 协议候选，不能简单归入 `product-docs`，需另行确认是否真的需要多会话通信协议。

L1 专项轮开始前必须重新评估“强制四层路由 vs 按需专业化”，不能把本轮 K01 的结论
机械带入不同范围。所有延后项保持 `requires-explicit-resume`，不得因本轮完成自动提升。

## 5. 逐文件内容计划

本节规定目标和落点；具体英文终稿以外部 `ABSORB-PLAN.md` 第 4 节为素材，执行阶段 2
必须把每一条编号展开为不落盘 diff，并由用户确认后才落盘。不能凭摘要自行重写终稿。

### 5.1 architecture

内联高频判据：

- A01：选型必须回答为什么选、放弃什么及理由、失败后怎么办；
- A03/A02：外部依赖写出失败顺序、回落链和穷尽后的确定性行为；自终止路径必须显式收尾；
- A09：领域规则与承载表面解耦；换宿主不重开契约；
- A10/A11：任务单固定目标、范围/非目标、验收 case、依赖/契约版本、返回/阻断条件；一单一功能单元；
- A13：跨返回单元重复出现的问题沉淀为架构权威记录，原 ticket 保留为证据；
- K04：只使用仓库既有五态；失败带相对原始验收的差异清单，blocked 指明缺依赖，原单不改写；
- G02：只在存储、跨服务参数或仓库拓扑场景指向新 reference；
- G06：只能使用稳定、不含本机路径的来源标记。

新建 `structure-and-topology.md`，定义：存储/持久化显式决策、运行数据单一手写真源、
跨服务参数统一命名、仓库拓扑关系；位置前缀只能作为 Optional Practice，不能变成普遍规则。

### 5.2 code-quality

内联高频判据：

- C01/C02：写前读取文件、调用方和周边命名；新标识符先检查符号、路由、查询键和存储键冲突；
- C03：重命名/格式化与行为改动分开；
- C12：在 happy path 同步接上依赖不可用、上下文丢失、重试耗尽等失败路径；长操作可观察，错误可读；
- C04/C05：不能写成可执行断言的 case 退回上游；最小边界集合是空输入、极值/边界、失败路径；
- C06/C11：证据包含可观察产物、无未解释警告/错误的干净运行和量化变化；退役断言必须同批补回不少于原数；
- K07/A12：批次或发布至少有构建身份、实际执行的必需 case 和结果；跨进程改动重跑 E2E，但时间压力只改变时机不取消必需门；
- C13：契约无法实现或互相矛盾时，作为具体 finding 返回上游，不私自改需求；
- G02/G06：按需指向 `debugging.md` 并使用稳定来源标记。

新建 `debugging.md`，四步必须保持顺序，每步附一个“看似合理但错”的反例：
现象分类先于归因、探针必须逼真、变式矩阵定位差异、先验证测量手段可信度。
现有 `review-and-tests.md` 追加断言形式和最小边界集合示例，不复制 `debugging.md` 的定义。

### 5.3 design-standards

内联高频判据：

- V01/V03：先从需求提取 3–5 个气质词；候选 A/B 由用户拍板，设计层不代替用户定稿；
- V04/V06：规范必须可判定；特征锁和禁令清单要能约束实际输出；
- V08/V11：暗图先提亮复核；点检只证明适用范围，不扩大为产品级验收；
- G02/G06：按需指向 `visual-verification.md`，来源标记不含本机路径。

现有 `visual-verification.md` 追加：逐屏比较、一图一用途、提示词写需求/约束/禁令而非
不可控技法、逐字放大检查生成文本、每轮只调一个变量族且参数收敛后再动结构。

### 5.4 单一真源和来源标记

每条新增规则必须有唯一“定义落点”；其它文件只使用短指针、引用或验收映射。
编号、原因、验收说明不是第二份规则定义。关键词 grep 仅作辅助，最终要做语义对读。
来源 HTML 注释不能指向外部暂存区路径、用户目录或不存在的仓库文件；只写稳定的泛化来源标签。

## 6. 执行阶段与硬门禁

任何阶段失败都停止并报告；不能为了完成下一阶段而自动降低门禁。

### 阶段 0：恢复与漂移确认

1. 查询 Goal/task-state；若无 Goal，记录 `goal: null`，若查询失败记 `unknown`。
2. 读取本计划和外部只读计划，确认外部仍为未执行状态。
3. 读取目标仓库 `git status --short`、分支、HEAD、远端配置，不修改任何文件。
4. 计算 4 个仓库基线文件的完整 SHA256、行数；检查 `product-docs` 安装与仓库差异。
5. 对三个目标安装目录建立相对清单、入口版本字段和完整 SHA256 快照。

门禁：任一仓库目标文件、外部计划状态、安装副本或既有未提交文件与预期不符，停止汇报；
不把漂移自动吸收到本轮。

### 阶段 1：持久备份和隔离

在一个可恢复的计划专用目录建立备份，例如：

```text
C:\Users\Aiano\codex-skills-replicas\screenshot-lineage\absorb-backups\<timestamp>\
```

备份范围必须完整：

- 仓库 3 个待改 `SKILL.md`；
- 仓库 2 个待新建 reference（记录 `absent-before`，不得伪造旧哈希）；
- 仓库 2 个待追加的现有 reference；
- `product-docs/SKILL.md` 及其哈希作为保护证据；
- `.agents\skills\architecture`、`.agents\skills\code-quality`、`.agents\skills\design-standards` 的当前完整目录、清单和哈希。

备份可另外复制到 `%TEMP%` 做工作缓存，但 `%TEMP%` 不是唯一恢复权威。备份清单必须包含
时间、源路径、目标路径、相对文件、大小、SHA256、原先是否存在。

门禁：备份目录存在、清单可读、每个已存在文件哈希回读一致；否则停。

### 阶段 2：不落盘 diff 草案

只生成文本 diff 和编号映射，不写入仓库，不改版本，不改安装副本。每个 diff 项必须标出：

```text
decision id -> target file -> exact anchor -> proposed text -> reason -> acceptance check
```

检查 66 项数量闭合、7 个文件覆盖、唯一落点和不碰 `product-docs`。用户明确确认该 diff
后才能进入阶段 3；没有确认就保持等待，不把“全部按建议”解释为“跳过 diff 审阅”。

### 阶段 3：写入 references，再写 SKILL.md

按顺序：

1. 新建 `structure-and-topology.md`；
2. 新建 `debugging.md`；
3. 追加 `review-and-tests.md`；
4. 追加 `visual-verification.md`；
5. 修改三个 `SKILL.md`，让指针只指向已经存在的 reference；
6. 写入稳定来源标记，不能出现用户目录、外部暂存区路径、项目名或私有 URL。

写入范围只允许第 3 节列出的 7 个文件。任何相邻“顺手优化”、换行大规模重排、
语言改写或目录整理都属于越界，需撤回并报告。

### 阶段 4：内容校验（不含版本目标门）

在版本仍为 `1.0.0` 时检查：YAML 结构、`name` 与目录匹配、Markdown 语法/本地链接、
新增 reference 存在、无环境绑定、唯一落点、行数预算、`product-docs` 哈希不变、
目标文件 diff 只含授权编号。

版本字段此阶段暂不要求 `1.1.0`，避免与阶段 5 顺序冲突；但必须确认三个目标的
版本字段仍可被明确、局部地改为 `1.1.0`。

### 阶段 5：版本变更并重跑完整校验

仅修改三个目标 `SKILL.md` 的 `metadata.version: "1.0.0"` 为 `"1.1.0"`；不改
`product-docs`，不改其它技能版本。然后重新执行完整校验：YAML、链接、敏感绑定、
单一真源、行数预算、`product-docs` 完整哈希、编号映射和公开路径检查。

门禁：完整校验必须看到三个 `1.1.0`，且 `product-docs` 仍为参考完整 SHA256。

### 阶段 6：本地 review 和 commit（不 push、不打标签）

逐文件 review：内容、编号、边界、英文表达、链接、来源和无关 diff。执行适用的
官方 Skill 校验、YAML 解析、链接检查、敏感扫描和 `git diff --check`；未跟踪文件要单独检查。

只精确暂存 7 个目标文件及用户明确要求纳入的计划/证据文件；不得用宽泛 `git add .`。
提交前报告拟提交清单和未纳入清单。commit 信息须包含 `#absorb` 和编号范围。
本阶段只做本地 commit，不 push、不创建 Release、不打标签。

### 阶段 7：本机安装同步（明确路径，独立于 Git）

只有本地 commit 成功且用户授权本地发布后才执行。目标固定为：

```text
C:\Users\Aiano\.agents\skills
```

只同步三个改过的 Skill。同步前重新比较仓库与安装副本的相对文件清单、版本字段和 SHA256。
若发现任何非本轮差异（包括此前版本字段缺失之外的新差异），停止，不覆盖并汇报。
同步后逐文件回读清单、大小、SHA256 和 `metadata.version=1.1.0`。

“本机安装成功”只证明安装副本一致，不代表 GitHub 已 push，也不代表用户实战验收完成。

### 阶段 8：终态回写

把实际执行结果、commit、安装路径、文件清单、哈希、校验结果、未完成项和用户待决事项写回
本计划或对应证据文档。若本轮失败/阻塞/中断，保留原因和恢复入口；不能把半成品标为完成。
只有在所有声明都有对应证据后，才能把本轮标记为 `completed`；否则保持 `blocked` 或 `partial`。

## 7. 校验矩阵

| 编号 | 检查 | 通过标准 |
|---|---|---|
| Q1 | 基线 | 4 个仓库参考文件完整 SHA256/行数符合阶段 0 |
| Q2 | YAML | 三个 Skill `name` 正确，阶段 5 后版本均为 1.1.0 |
| Q3 | 链接 | 所有 `references/*.md` 指针指向真实文件，锚点可解析 |
| Q4 | 来源/隐私 | 无用户目录、凭证、私有 URL、项目专名、暂存区路径 |
| Q5 | 单一真源 | 66 项编号都有唯一落点；指针不重复定义正文规则 |
| Q6 | 状态 | 只使用既有状态词，不生成第二套三态词表 |
| Q7 | 范围 | 只有 7 个授权目标文件发生改动；`product-docs` 完整哈希不变 |
| Q8 | 预算 | 三个 `SKILL.md` 各不超过 +25 行；`structure-and-topology.md` ≤60 行；`debugging.md` ≤60 行；`review-and-tests.md` 追加 ≤18 行；`visual-verification.md` 追加 ≤28 行 |
| Q9 | 证据 | 每个改动编号有 diff、原因和验收记录；G04 有两个指定 reference 落点 |
| Q10 | 安装 | 三个安装目录与仓库逐文件清单/哈希一致，绝对路径正确 |
| Q11 | Git | 只精确暂存计划授权文件；commit 可回读；无 push/tag/Release 误操作 |

“规则只准写一处”不能只靠关键词 grep。Q5 必须使用编号→唯一落点→指针表，
再由人工语义复核定义、原因、示例和验收是否重复或互相矛盾。

## 8. 回滚和中断处理

### 8.1 写入前中断

不改仓库，保留阶段 0 快照和阶段 1 备份；当前项标为 `interrupted`，等待明确恢复。

### 8.2 未 commit 的部分写入

优先使用阶段 1 的逐文件备份恢复；恢复前保存当前 diff 和哈希，恢复后逐文件回读。
禁止使用会覆盖整目录的 `git checkout -- <directory>`，因为会损坏无关用户改动。

### 8.3 已 commit、未 push

保留 commit 和工作区证据。只有用户明确要求回滚时，才对精确 commit 执行 `git revert`；
不使用 reset、force push 或移动标签作为默认恢复手段。

### 8.4 安装同步中断

安装前必须有三个安装副本备份。只恢复受影响文件，逐文件比对原备份哈希；发现非本轮差异时
不覆盖，先汇报。仓库 commit 与本机安装状态分开记录。

### 8.5 外部计划或来源发生变化

如果外部 `ABSORB-PLAN.md`、截图、还原件或用户裁决变化，暂停当前执行；重新建立来源哈希、
决策映射和 diff，不把旧计划当作仍然有效。原始截图始终只读。

## 9. 明确的失败停止条件

遇到以下任一项立即停止并汇报，不自行补救或扩大授权：

- 基线哈希不符，无法证明当前文件仍是计划假定版本；
- `product-docs` 或其 reference 被意外修改；
- 外部计划状态不再是未执行；
- 目标安装副本出现未解释的额外差异；
- 无法把某条规则放在唯一权威位置；
- 发现凭证、私有地址、用户目录或项目专名进入公开 Skill；
- YAML、链接、敏感扫描、行数预算或必要测试失败；
- 版本号不是明确的 `1.1.0`，或误改其它 Skill 版本；
- 用户未确认阶段 2 diff 却要求继续落盘；
- commit、安装或任何外部写操作结果不明确；
- 需要 push、tag、Release、force push、删除标签或覆盖无关改动才能继续。

## 10. 版本、Git 和发布边界

本轮计划中的 `1.1.0` 是三个 Skill 的合同版本，不是仓库整体版本。
仓库整体标签沿用日期式 `repo-YYYY.MM.DD`，但本轮默认不打标签。

本地 commit 是留痕；GitHub push 是远端同步；本机安装是运行时同步；GitHub Release 是独立动作。
它们必须分别授权、分别执行、分别验证。外部计划默认只要求本地 commit 和本机同步，
不自动 push、不自动创建 Release、不自动移动或删除旧标签。

## 11. 后续 L1 专项轮

只有用户重新明确启动，才可建立第二份针对 `product-docs` 的计划。那一轮必须先评估：

1. docs-first 的增强是否已被现有恢复规则覆盖，避免重复定义；
2. 两区模型、控制面/派生档和 01–07 模板是否适合本仓库的比例原则；
3. Round-Close 是否应成为可选检查，而不是所有小改动的强制流程；
4. interchange 是否真的需要独立协议文档；
5. 强制四层路由是否与按需专业化、Goal 和授权机制冲突。

L1 轮不能因为本轮 L2–L4 成功而自动开始，也不能把外部 `project-docs` 直接覆盖现有
`product-docs`。任何吸收都必须先有不落盘 diff、用户确认、备份和独立验收。

## 12. 执行完成定义

本轮只有同时满足以下条件才可标记完成：

- 阶段 0–8 的实际状态有记录；
- 7 个计划文件的 diff 与 66 项映射闭合；
- 三个技能内容和版本 `1.1.0` 通过全部 Q 检查；
- `product-docs` 完整 SHA256 未变；
- 目标安装副本（若已获本地发布授权）逐文件与仓库一致；
- 本地 commit 身份可回读；
- 未发生未授权 push、tag、Release、force push、删除标签或覆盖无关改动；
- 未完成的 L1 项、真实项目验收和用户接受明确标记为 `pending_user_acceptance` 或 `requires-explicit-resume`。

如果只完成了 diff、只完成了仓库写入、只完成了 commit 或只完成了安装，都必须使用
相应阶段状态，不能用“吸收完成”概括全部生命周期。

## 13. 接手顺序

新 Agent 进入本任务时按以下顺序，不得直接执行：

1. 查询 Goal/task-state；
2. 读取本文件第 0、1、6、9、12 节；
3. 读取外部计划第 0–3 节和对应目标文件的逐点终稿；
4. 核对阶段 0 基线和当前 Git 状态；
5. 如果没有用户对阶段 2 diff 的明确确认，停在 `plan-ready / not-executing`；
6. 只有用户明确启动后，才建立备份并生成不落盘 diff。

## 14. 当前计划终态

- 外部 `ABSORB-PLAN.md`：已恢复为原始未执行参考，未再修改。
- 本仓库 S3 已落地：`skills/architecture/SKILL.md` 吸收 architecture 判据，新增
  `skills/architecture/references/structure-and-topology.md`；S3 最终入口 SHA256 为
  `DE9E98BD4B13D6FDC87144DBE82EE37A4E516BFEE87B8F8F27633AE68143A520`，新 reference
  SHA256 为 `97D0C42BD0A184CE79A7CD7C4E13130EDD9BBCEE472BCA10E12B736732ADDA6B`。
- S3 自测通过：入口 diff 非空物理行 `25 added / 5 removed / +20 net`；reference 40 行；
  revision 3 预览 SHA256 `01F2B9E68C6C90889AB0C84EA5BF099AF7C6BB4962C6D5C61B69BB8F2E75F89E`
  与 manifest 绑定哈希 `D0CCBC71CA3BA651619A08275E5B1158CF077B2D639841CB60E5E4AE90952983`
  回读一致；manifest JSON、66 项唯一映射、7 个目标文件、链接和敏感扫描均通过。
- S3 保护哈希：`product-docs/SKILL.md` 为
  `F08AC541A3A19B4B1AE68BA1A52A3BD4E07EAF3B57052F8B950CBDFF9CD1E608`，
  `design-standards/SKILL.md` 为
  `B8A27D0D355959211938A9BF9A46369F578586988F79FCE46D20E60E555DB354`；
  `code-quality/SKILL.md` 的 S4 变更及最终哈希见下方 S4 证据。
- 本机 `C:\Users\Aiano\.agents\skills`：未修改；S1 快照中的 9 个安装文件逐一回读哈希一致，
  新 reference 仍按 `absent-before` 保持未同步。
- Git：S7 已创建本地 commit `ab20612efb633792d8c182cd49cafcd184580ee5`（`docs: absorb layered skill criteria #absorb S7`）；未 push、未打标签。
- S4 已完成：`skills/code-quality/SKILL.md` 吸收 C01–C13、A12、K07、G02、G06 判据，
  新增 `skills/code-quality/references/debugging.md`，并向
  `skills/code-quality/references/review-and-tests.md` 追加断言形式和最小边界集。
  S4 入口最终 SHA256 为 `29C6D6D639DF72298378E76F14E987DFA82E85B049C90059B6A0FD8D857F98FA`，
  debugging reference SHA256 为 `58E2D05487FCD7E44C923AC772C193187B8F414BB5050A01BC972AECDA3DD6E2`，
  review-and-tests 最终 SHA256 为 `4D2A23E22894AB47D4C114D66FE3D97BB7581EA029B43ED50AAFA0D9E76B41FA`。
- S4 自测通过：入口 diff 非空物理行 `28 added / 5 removed / +23 net`；debugging 41 行；
  review-and-tests 追加 15 行；四步调试顺序和四个反例、两个本地链接、敏感扫描、
  `git diff --check`、保护哈希及 9 个安装快照文件回读均通过。独立 review 发现预览 C12
  若按字面替换会删除既有幂等性、版本、事务和恢复语义，已保留原 bullet，仅追加失败路径
  与长操作判据；这不扩大文件范围且入口仍低于 +25 行预算。
- S5 已完成：`skills/design-standards/SKILL.md` 吸收 V01/V03/V04/V06/V08/V11/G02/G06
  视觉判据，`skills/design-standards/references/visual-verification.md` 追加逐屏比较、
  一图一用途、提示词约束、放大验字和单变量收敛规则。入口最终 SHA256 为
  `3C476B13B53018348988DCD09643CFC74DCD51DB14ED09AB21880ACC54BC3E0A`，reference
  最终 SHA256 为 `D119D44C8BEA0FF90E16A27CF456C810DE0B18A0A8AEF293BC5936392C6C3F98`。
- S5 自测通过：入口 diff 非空物理行 `26 added / 2 removed / +24 net`，低于 `+25`；
  `visual-verification.md` 追加 `28` 行，达到但未超过 `+28` 上限；`git diff --check`、
  视觉 reference 本地链接、敏感信息扫描和 `product-docs/SKILL.md` 保护哈希均通过。
  本次未发现用户路径、凭证、私有 URL 或项目绑定；全量扫描命中的既有
  `product-docs` 历史路径文本未归因于 S5 新增。
- S6 已完成：三个目标入口 `metadata.version` 已由 `1.0.0` 升为 `1.1.0`，未改
  `product-docs` 或其它 Skill。三项官方 `quick_validate.py` 均通过；`design-standards`
  在 Windows 默认编码下首次读取失败，改用 `PYTHONUTF8=1` 后通过，属于校验环境编码
  问题而非 Skill 内容失败。跨技能门禁通过：三个 front matter 的 `name`/版本正确，
  本地链接存在，敏感绑定扫描无命中，入口非空净增为 architecture `+20`、
  code-quality `+23`、design-standards `+20`，两个新 reference 分别 29/28 行，
  两个现有 reference 追加分别 11/17 行，均在预算内；`product-docs/SKILL.md`
  SHA256 仍为 `F08AC541A3A19B4B1AE68BA1A52A3BD4E07EAF3B57052F8B950CBDFF9CD1E608`，
  `git diff --check` 通过。一次全量脚本误把现有 reference 全文行数当追加预算，已修正为
  diff 追加行数后重跑通过，未改内容。
- S7 已完成：精确暂存并提交 8 个文件（本计划、三个入口、两个新增 reference、两个现有
  reference）；未纳入 README、`docs/absorb-plan-review.md`、`docs/replication-evidence.md`、
  `docs/skill-replication-plan.md`、`docs/workspace-history-and-rules.md`、
  `skills/report-render/`、`skills/research-report/` 等既有或无关工作区改动。提交前后通过
  `git diff --cached --check`、三个官方 `quick_validate.py`、本地链接、名称/版本、敏感扫描、
  staged 文件集合和 `product-docs` 保护哈希校验。提交后工作区仅保留上述未纳入文件的既有改动。
- 本计划：S0–S7 已完成；S8–S9 未启动，后续阶段仍需单独授权并按门禁执行。
- 版本号与 Git commit 已完成；安装同步、push、打标签和发布均未执行。

初版预览 SHA256 为
`05D4FE6CD7D965E7FD38504408F781170D1A3002D67685ABB1F1D1EE3CEB2A46`，初版
manifest SHA256 为 `72FB06EA07921291C4B5F8C1DB8F71E59EA08DE3380057C860CA0F5FE8BF12DD`。
修订预览 SHA256 为
`A8D8BAE88FF9E5F4C2BB8AAD184E78D8E6955685F3C0CA7846C284437AD63F76`，修订 manifest
SHA256 为 `F90E451FB9B2A032411AB05D1DB91FFF1B923DB4BC8DE4758749B87F100A0BDB`；manifest
中的预览哈希已与预览文件回读一致。revision 3 预览和 manifest 见
`C:\Users\Aiano\codex-skills-replicas\screenshot-lineage\absorb-diffs\20261024-230719\`。
