# 截图复刻与安装证据

## 当前发布状态（2026-10-25）

本轮总体收口已将 `product-docs` 的 L1 D1/D2 变更升级为 `1.0.4`，并同步到
`C:\Users\Aiano\.agents\skills`；仓库与安装副本逐文件回读一致。以下“未执行”记录均
属于先前 R1/验证轮的当时边界，不覆盖当前主计划的发布状态。运行时搜索、渲染和用户接受
仍保持未证明，不因安装或 GitHub 发布自动升级。

记录日期：2026-10-24。本文保存来源、清理边界和具体验证证据；当前进度只由
[当前计划](skill-replication-plan.md)管理，全会话背景见[工作区记录](workspace-history-and-rules.md)。
正式行为入口：[report-render](../skills/report-render/SKILL.md)、[research-report](../skills/research-report/SKILL.md)。

## 来源和授权

用户明确优先两个技能、清理特定环境内容，随后要求自测和“安装到本机 .agents”。
安装使用本地已验证源，不从过时 GitHub 副本拉取，不用默认 `.codex/skills` 替代用户目标。
来源为本机桌面 `research_reports/reports/technology/近期AgentSkill构建/`：

- 原图 `originals/page_01.png`—`page_34.png`：本轮只读确认 34 张。
- report-render 对应原图 22–24 页，research-report 对应 24–26 页。
- README、整理正文、manifest 本轮核对存在，仅是报告辅助归档，不是原技能源码。
- 用户明确技能内容只有截图，没有原始 Skill、脚本和模板；原图权威，整理正文只是索引。
- 页码及内容判读沿用前轮已完成分析，本轮没有重新 OCR 或逐页核读。
- 原图和私有归档未改、未删、未复制进仓库候选文件。

## 清理和交付边界

复刻可迁移的职责、路由、输入输出、停止条件和验收，不移植特定环境实现。
清理/参数化用户名、本机路径、个人项目路径、内网 URL/服务/端口、Cookie、token、API key、
文档 ID、组织/客户/样例和原环境验证数字。
`diworker`、`vision-recognition`、`web-search`、飞书/Lark、私有 Node 模块不作为默认依赖。
外部能力经当前可用路线接入，缺失时明确状态和回退，不伪称已部署。

```text
skills/report-render/                         # 1.0.0
  SKILL.md
  agents/openai.yaml
  references/render-qc.md
skills/research-report/                       # 1.1.0
  SKILL.md
  agents/openai.yaml
  references/evidence-register.md
```

report-render 接收已有 HTML、明确输出目录及 long/paged 模式，约束资源检查、分页和视觉 QC，
不负责调研或改写/认证事实。research-report 编排问题、来源、冲突口径、草稿、对抗性发布前审查、
渲染和归档，不自带搜索供应商。Markdown 到 HTML 仍需实际转换路线，不能把 Markdown 当已有 HTML 输入。
当前无可执行渲染脚本、HTML 模板或已绑定浏览器。
两份 reference 存在但尚未从各自 SKILL.md 显式链接；已记录可发现性缺口，本轮不改合同。

## 验证记录与证明边界

| 检查 | 结果 | 能证明什么 / 不能证明什么 |
| --- | --- | --- |
| 源/安装技能官方 quick_validate | 本轮 4/4 通过（仓库与本机各 2/2） | 格式及校验器覆盖字段，不证明运行行为 |
| UI YAML | 前轮实际解析通过 | 元数据语法，不代表实际 UI 交互实测 |
| 敏感环境绑定扫描 | 前轮通过 | 扫描范围内的检查，不授权公开原件 |
| git diff --check | 前轮通过 | 已跟踪 diff 空白，未跟踪文件需另检查 |
| 目标目录冲突 | 安装前两目标均不存在 | 当次无同名覆盖 |
| 安装与回读 | 每个 3 文件，共 6 个 | 已安装，没有额外隐藏脚本/模板 |
| 相对清单与 SHA256 | report-render 全一致；research-report 仓库已吸收清理后的 1.1.0 | 身份/变更边界可回读，不证明实际搜索/渲染效果 |
| 安装副本 quick_validate | 安装当轮 2/2 `Skill is valid!` | 临时 PyYAML 环境完成，不改官方校验器 |
| 搜索、Markdown→HTML、PNG、视觉 | 未完成真实流程验证 | 不得宣称端到端可用 |
| 用户实战接受 | pending_user_acceptance | 安装授权不等于效果验收 |
| commit/push/tag/Release | 本轮未执行 | 仓库吸收不代表 GitHub 已发布 |

环境踩坑：前轮 Windows 默认编码读取失败，用 `-X utf8`；安装当轮默认 Python 的连接器 venv
缺 `yaml`，明确报 `ModuleNotFoundError`。用 `uv run --with pyyaml` 临时依赖完成，
不改连接器/全局 Python 或官方校验器。一次应用依赖路径发现工具返回无效响应，未视为成功。

以下仅供确有变更且需重校验时使用，不授权恢复后重复测试；路径占位应换成本机实际位置：

```powershell
uv run --with pyyaml python -X utf8 '<系统技能根>/skill-creator/scripts/quick_validate.py' '<本机技能根>/report-render'
uv run --with pyyaml python -X utf8 '<系统技能根>/skill-creator/scripts/quick_validate.py' '<本机技能根>/research-report'
```

当次系统技能根是用户目录下 `.codex/skills/.system`，本机技能根是 `.agents/skills`。
uv 缓存缺包时可能联网；这里不是要求将这些机器路径写入两个技能的合同。

## 安装身份记录

源为仓库 `skills/<name>`，目标为本机 `.agents/skills/<name>`。
本轮已对仓库与本机各运行 quick_validate；report-render 保持字节一致，research-report
保留本机新内容但仓库版本经过公开边界清理，未覆盖本机副本。仓库当前清单哈希为：

```text
report-render/agents/openai.yaml
A6B2C7A7B597E0FE5524F98BC83C55C9B9821710FC40FBE7CBAF25899A685EA7
report-render/references/render-qc.md
A312B8E11ED90BE9ED48665D984350A046A5D0A03114B1550E05184B90589404
report-render/SKILL.md
4F0E8A2AA9B80B841208DECB2B98A25DB83DFFAD77B8414D97B587EF5BA7CC20
research-report/agents/openai.yaml
28C1DBB7C5A59F3D10FBBA98F2DD80CC9BAB9AA37B33E74526FE8D91BD40FD20
research-report/references/evidence-register.md
D562ADA905466A3444D9B5E65E01F99B9FBDEBA6C2A3581E7DF5FADA11F1C84B
research-report/SKILL.md
A5A7E0F0417D80893258203F76260F5CB44508F477AF9A13C5B4E512D0017932
```

## 实战验收依据（明确启动后适用）

1. 隔离小环境、非敏感输入，固定输入身份、输出目录与阶段终态，不污染原报告或旧 PNG。
2. 分别看长图/分页、字体/图片加载、表格/卡片完整性、连续编号、空白带、裁切与可读性。
3. 缺输入、必需资源/渲染器或关键检查失败，返回明确状态，不伪造文件或把缺项算 pass。
4. 回读尺寸、数量、内容及视觉区域；命令返回 0 不能独立证明视觉通过。
5. 研究分开记录问题、来源、声明核验、草稿、转换、渲染、视觉、归档、用户接受，保留冲突和推断标记。
6. 用户只要求一阶段就停在该阶段；不自动发布、push 或向外分享。

## 本次文档交接检查

本轮已完成：

- README 与 3 份 docs 共 4 个 Markdown 文件，检查时的 18 个本地文件链接/锚点全部解析通过；终态补充增加的证据链接随后回读检查。
- 包含未跟踪文档的末尾空白检查通过；`git diff --check` 通过，README 的 LF/CRLF 提示不构成失败。
- README 恢复钩子边界标记唯一，Goal/task-state API 在当前计划链接之前，普通同步失败保持局部处理。
- 内存负例：顺序倒置、普通失败边界被改写、结束标记缺失、开始标记重复，全部被检查拒绝；没有修改磁盘文件来制造负例。
- LF 和 CRLF 两种钩子输入均通过。
- 本轮核对了七个仓库技能与本机同名副本，四个旧入口缺少版本字段的差异见工作区记录；没有修复安装目录。

这些只验证文档导航与状态约束，不升级搜索/渲染证据层级，也没有重跑已完成技能校验或安装。
