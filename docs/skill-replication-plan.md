# 工作区当前计划与状态

## 当前公开发布收口（2026-10-25）

吸收计划已完成内容实施；本轮发布证据与 GitHub 状态回读已完成。`product-docs`
已升级为 `1.0.4` 并同步到 `C:\Users\Aiano\.agents\skills`；三个专业技能保持 `1.1.0`。
旧的未发布/待授权描述均为历史记录，不能覆盖当前主计划状态。运行时搜索、渲染、真实用户
接受仍保持证据缺口，不因 GitHub 发布自动升级。公开提交为 `ea254d2`，日期标签为
`repo-2026.10.25.2`；吸收父 issue #5 与阶段 issue #9–#15 已关闭。

本文件沿用原文件名，是本轮复刻/安装历史的入口；四技能吸收任务的正式执行计划已经独立写入
[四技能吸收计划](skill-absorption-plan.md)，后者是该任务唯一执行权威。
全会话背景、规则与坑见[工作区记录](workspace-history-and-rules.md)，
具体来源和校验证据见[复刻及安装证据](replication-evidence.md)。
它们是依据与快照，不是第二套活动队列；Skill 正式合同仍由各自入口拥有。

## 当前用户目标

最新指令（2026-10-25，原话）：“本机的 汇报调研技能更新了 分析下收进来”。
当前槽：`none`（R1 已闭环）；来源：`user-explicit-goal-start`；
user-explicit-goal-start：比较本机 `.agents/skills/report-render` 与
`.agents/skills/research-report` 的最新内容和仓库对应版本，审查可迁移性、环境绑定、
版本边界与现有职责合同；安全时吸收到仓库并完成格式、链接、敏感边界和差异自测，
不覆盖本机副本、不自动 push/tag/Release。若发现语义冲突、私有环境绑定或无法安全迁移，
停在分析并汇报具体问题。
Agent 临时子计划：先读取本机与仓库文件清单及哈希，再做逐文件 diff；仅将可证明是
通用工作流合同的更新带回仓库，保留本机路径、浏览器、账号、服务和项目事实在本地；
同步后回读版本、链接、格式和保护边界，最后关闭本项。

R1 结论（2026-10-25）：`report-render` 本机与仓库逐文件、逐哈希一致，无需吸收；
`research-report` 仅新增可迁移的发布前对抗性审查与交互图表检查，已在仓库吸收为
`1.1.0`。领域专用单位表述已泛化为单位/基准/时间口径；外部 issue 要求已改为优先使用
项目既有缺陷记录、无机制时保留在运行证据。本机副本已在本轮同步；GitHub 发布状态以主计划
与最终回读证据为准。
R1 验收：两项官方 quick_validate、Markdown 本地链接、敏感环境绑定、差异和保护边界检查通过；
真实搜索、Markdown→HTML、渲染、视觉和用户接受仍未证明。

R1 已闭环：当前槽回到 `none`；后续本机同步、commit、push、tag、Release 或真实实战均需
新的明确指令，不从历史“收进来”重复执行。

最新指令（2026-10-25，原话）：“开始下一步吧 仔细严谨 闭环掉”。
当前槽：`none`；来源：`user-explicit-goal-start`；
user-explicit-goal-start：用户在 S8 终态之后重新明确开始下一步，现执行 S9 的 L1 计划制定与自检。
S9 L1 已完成；本轮正在完成 product-docs 1.0.4 安装同步、精确提交、push、日期标签和 issue 回读。
唯一执行进度见[吸收计划](skill-absorption-plan.md)顶部；本入口仅转达当前项。
上一执行终态：`S8-completed`。三个专业 Skill 已按仓库提交
`70c18bd9df346e0e3cd555f95c75350eb644e649` 发布到本机 `.agents/skills`，均为
`1.1.0`；11 个文件清单、大小和 SHA256 回读一致，格式及 5 个链接校验通过。
恢复时只补缺失的终态文档，不重复同步或自测。完整备份、动作和保护证据由
[吸收计划的 S8 终态](skill-absorption-plan.md)维护，本入口只保留摘要。
S9 的实施授权已由后续“推进到闭环 严谨仔细 做好自测”明确给出；发布动作以实际 Git 回读为准。
检查报告见[product-docs L1 计划检查](validation/2026-10-25-product-docs-l1/REVIEW.md)。
Goal API 返回 `goal: null`，未创建 Goal。以下验证和文档任务均为历史终态，不是当前项。

### 已完成历史任务（不恢复执行）

历史验证指令（2026-10-25，已完成）：用户明确要求“从babata里拿一些东西只读拿出来一份 然后在这个镜像里测”，并随后纠正为“四个技能都测”。
本项范围是用 Babata 只读样本建立隔离镜像，真实调用四个已安装技能
`product-docs`、`architecture`、`code-quality`、`design-standards`，分别记录其能证明的结果和证据缺口。
执行边界：只读 Babata；只复制最小文档、代码、测试和可渲染素材到镜像；不修改 Babata 原目录、运行数据、凭证、四个 Skill、`.agents` 安装副本、Git 发布状态或外部服务。
当前验证项：`completed`；来源：`user-explicit-goal-start`；临时子计划：选取
`Babata-2.0-frozen/compass-output/docs/00–05` 作为产品/架构文档链，选取
`Babata/08_adapters/01_browser_extension/{manifest.json,popup.html,popup.css,src/capture.ts,src/capture.test.ts,package.json}`
作为代码与实际界面样本；在隔离镜像中完成四层检查，逐层区分通过、失败、部分、跳过和未验证。
验收：镜像清单与源哈希可回读；四个 Skill 各有明确输入、动作、结果和证据；任何真实缺口不升级为整体验收；完成后回写本项终态并清理仅为本次验证建立的临时锚点/保留必要证据。
结果：`passed with limits`。四个技能均已在同一只读 Babata 样本镜像中实际走过对应环节；详见
[四技能真实任务验证报告](validation/2026-10-25-four-skills/VALIDATION-REPORT.md)。产品文档与架构
为文档链/边界范围通过，代码质量在补齐镜像遗漏的 `src/popup.ts`、`src/index.ts` 后通过
check、4 个单测和 build，设计规范完成初始静态渲染与源级检查但未覆盖 Chrome API、配对、
交互、响应式和用户验收。Babata 原目录、技能、安装副本、Git 发布状态均未修改；镜像源清单
与 SHA-256 已保存。临时工作目录保留为可回读验证证据，不作为产品运行数据。

最新验证指令（2026-10-25）：先拿一个真实、简单的任务验证已安装技能的工作链路。
历史验证项：`completed`；来源：`user-explicit-goal-start`；保护边界：只读审阅
`docs/replication-evidence.md` 的验证记录与证明边界，核对其与仓库文件、安装身份和
已声明限制是否一致；不修改技能、安装副本、外部来源、Git 状态或发布状态。
验收：给出可回读的检查命令、实际结果、通过/失败/部分/阻塞状态及剩余证据缺口；完成后
将本项标记为 `completed`，不把文档导航检查升级为 report-render/research-report 的
端到端真实能力证明。结果：`passed`（只读验证通过）。第一次校验因 PowerShell 将
绝对路径再次拼接为相对路径而失败，属于校验器脚本错误；修正路径计算后重跑通过，未将
该工具错误归因于技能。两个安装技能各 3 个文件，源/安装清单和 SHA256 一致；证据文档
本地链接、`未完成真实流程验证`、`pending_user_acceptance` 和“不升级搜索/渲染证据层级”
边界声明均存在。无源文件、安装副本或 Git 发布状态变更。

最新指令（2026-10-24）：审核外部 `ABSORB-PLAN.md` 后，按审核修正另写一份完整正式计划；本轮只写计划，不执行吸收。
当前项：`completed`；来源：`user-explicit-goal-start`；保护边界：不修改目标技能、不安装、不提交、不 push、不打标签。

最新指令（2026-10-24，进度管控原话）：
“详细点 坑 注意的 规则之类 再详细 保证不出错 docs 也全面更新 然后最新完整交接发我”。
随后明确范围（原话）：“整个会话 整个工作区的坑 简史”。

`CURRENT-ACTIVE: none`；本轮状态：`completed`。
当前项已完成：审核外部四技能吸收计划，并在仓库写入独立的完整正式计划；不执行吸收。此前已完成的整个会话与工作区简史、
恢复规则、踩坑记录、证据与完整交接仍保持终态，
不限于两个新技能。历史用户纠正、当前磁盘事实和 Git 证据分开记录，不能凭历史指令重做操作。
变更来源：`user-explicit-goal-start`；user-explicit-goal-start：用户明确要求更新 docs 并输出完整交接。
Goal API 本轮返回 `goal: null`，无运行中 Goal。这里记录文档任务，不创建 Goal 对象。
此前文档交接结论：已固化恢复入口和单一进度权威，补充全会话简史、规则、证据与条件式后续；
该项已收口；审核细节见[吸收计划审核](absorb-plan-review.md)，正式执行方案见[四技能吸收计划](skill-absorption-plan.md)。
保护边界：不改 Skill 合同、不重装、不提交、不 push、不打标签，不自动启动实战验证。

已完成授权（2026-10-24）：将已验证的两个 `1.0.0` 安装到本机 `.agents/skills`。
安装已完成：目标原无同名目录，安装副本与仓库的文件清单、SHA256 一致，格式校验通过。

优先复刻桌面截图报告中记录的两个技能：`report-render` 与
`research-report`。截图是唯一来源；报告中的代码、路径、服务、账号、token、
验证数字和项目约定不是本机现状，也不是公开仓库内容。

来源、清理边界、职责及文件身份详见[复刻及安装证据](replication-evidence.md)，
不在恢复热路径重复维护。原有五个技能的版本、分工和 Git 简史见[工作区记录](workspace-history-and-rules.md)。

## 当前实施状态

- [x] 已确认两个目标及截图页码。
- [x] 已建立本记录，锁定截图来源与清理边界。
- [x] 创建仓库内隔离复刻：`skills/report-render`、`skills/research-report`。
- [x] 运行 Skill 格式校验并扫描私密环境绑定。
- [x] 同步到本机 `.agents/skills`，不覆盖现有 Skill。
- [x] Git 发布已进入本轮收口；实战与用户接受仍为 `requires-explicit-resume`，不自动提升。
- [x] 已完成一次真实只读验证：回读两个安装技能的 6 个文件清单/SHA256，并检查复刻证据
  的本地链接及能力边界声明；结果 `passed`，未升级端到端能力证明。

## 限制与候选后续

以下均不自动启动；当前交接结束后当前槽为空，等待新明确指令。

| 项目 | 当前结论 | 启动条件 |
| --- | --- | --- |
| product-docs 安装版本字段 | 已补为 `1.0.4` 并完成仓库/安装同步回读 | 后续若再改动需重新比对目标 |
| L1 延后轮计划 S9 | 已实施 D1/D2；发布回读后标记终态，运行时验收仍独立 | 新的 product-docs 需求 |
| 新技能实战 | 未附渲染脚本/HTML 模板，无真实搜索/渲染证据 | 用户明确实际任务或实战验证 |
| reference 导航 | 两参考文档存在，入口未显式链接 | 用户要求完善技能时再处理 |
| Git 入库 | 本轮正在精确提交、tag、push 并回读 | 后续变更另起发布轮 |
| 其他截图技能 | 未完成全量盘点/复刻 | 用户明确范围和优先级 |

## 恢复约束

1. 新会话/压缩/中断先查 Goal/task-state，再读本文件当前项；null 与查询失败/unknown 分开。
2. 先排除同一指令实例的完成终态，再选择最新未完成用户指令、started Goal、当前可执行文档项。
3. held、paused、requires-explicit-resume 不自动提升；历史命令不是新授权。
4. 对话已证明完成但 docs 落后，仅补终态回写，不重做执行、测试、安装、push 或发布。
5. 同步命令明确失败且上下文完整时局部处理；不为普通报错重启历史恢复。
6. 只读临时锚点完成后保存必要证据，再删除或标记终态。

## 变更说明

安装证据已移至[验证记录](replication-evidence.md#验证记录与证明边界)，仍保留完成终态。
本次文档交接检查：README 与 3 份 docs 共 4 个 Markdown 文件、18 个本地链接/锚点通过；
包括未跟踪文档的末尾空白检查通过。恢复钩子顺序、普通失败边界及内存负例通过，LF/CRLF 均通过。
`git diff --check` 通过，只有 README 换行提示。完整记录见[文档检查证据](replication-evidence.md#本次文档交接检查)。
没有升级 Skill、创建标签、提交、push、重装或启动实战。没有自动提升的下一项。

2026-10-24 吸收计划：外部 `ABSORB-PLAN.md` 恢复为原始未执行参考；本仓库新增
`docs/skill-absorption-plan.md` 作为四技能吸收的正式唯一执行计划。该计划已覆盖审核发现的
路径、版本顺序、备份、安装差异、来源标记、回滚、66 项闭合和 L2–L4/L1 边界；静态检查通过。
当时计划状态为 `plan-ready / not-executing`；此后 S0–S8 已依阶段授权完成，当前状态以本文顶部和吸收计划为准，不重放历史门禁。

## 2026-10-31 终局：28 个技能全部去向已定

本节为当前唯一执行结论，取代此前所有分批计划。证据在各自 Issue 的评论里，这里只记去向。

### 一、已复刻并验证（10 个，均可本地复跑）

| 技能 | Issue | 验证 |
| --- | --- | --- |
| vision-recognition | #20 | 格式校验、CV 度量、真实截图转写、多图对比、负路径 |
| vision-matting | #44 | 五个子命令实测；合成 MAD 4.546；参数按 1028 版对齐 |
| vision-qc | #45 | 四类夹具判定（pass / 光晕 / 杂点 / 空 alpha） |
| comfyui-generate | #23 | 本地 stub 全链路 27/27，八类退出码 |
| powershell | #34 | PS7 26 PASS / PS5.1 29 PASS |
| git-workflow | #26 | 13/13，临时仓库真提交 |
| llm-api | #29 | 38/38，reasoning 空回复与截断分类 |
| gitea | #27 | 20/20 本地 stub，api 直通 + squash 合并 |
| course-docs | #24 | 11/11 结构检查 |
| server-ops | #42 | 16/16 探针（重复 header / 缺 charset / 5xx / HTML 套 JSON） |

### 二、已吸收，不再单开技能（7 个）

handoff-note(#28) → handoff-context；project-docs(#38) → product-docs；report-render(#40)；research-report(#41)；project-arch(#35) / project-design(#36) / project-dev(#37) → 方法论已在 product-docs / architecture / design-standards / code-quality，截图转写存 `docs/reference-transcripts/`。

### 三、只识别不复刻、不注册（11 个）

| 技能 | 原因 |
| --- | --- |
| q3-logger(#39) / ta-mgr(#43) / zijian-mgr(#47) / pet-vl(#33) | 科室内部流程与表结构 |
| bug-filler(#22) | 飞书缺陷表 + 内网 CODING 链接 |
| diworker(#25) | aic.byd.com 平台客户端 |
| ops-release(#31) | 算力卡发布 runbook |
| pet-pack(#32) | 卓宠资源表与产物格式 |
| web-search(#46) | DiWorker API + byd-opensearch 两条内部通道 |
| archive-vault(#21) | 用户指示不注册；转写存 `docs/reference-transcripts/archive-vault.md` |
| lovart-gen(#30) | 无凭据且原文未给 HMAC 待签串规范；转写存 `docs/reference-transcripts/lovart-gen.md` |

### 四、可迁移的五条结论

1. 索引/配置是唯一真源，脚本不自带规则副本，换库只改索引。
2. 干跑优先：入库、去重、批量改写默认只报告，显式 `--apply` 才动手。
3. 去重三重保障：授权 + 同名同大小 + SHA256，产物进回收站而非删除。
4. 内容相同但名字不同通常是两份合法副本，不合并。
5. 签名/加密规范未知时不写客户端：猜出来的实现第一次真调就失败，属于假实现。

### 五、证据边界（不夸大）

- 所有复刻项的断言都在本地跑（stub 服务器或临时目录），**没有一个对真实内网服务验证过**；
- gitea 证明的是协议正确，不证明 token 的 scope；
- server-ops 的运维建议是知识，不是测试证明；
- lovart-gen 与 archive-vault 只有文本转写，没有代码。

### 六、未做的事（明确边界）

- 未提交、未推送、未打 tag；
- 未安装任何技能到 `.agents`（除 `llm-api` 外均为仓库内文件）；
- `docs/reference-transcripts/` 下的 5 份转写是机器 OCR，含识别噪声，只作追溯。
