# project-arch — 截图转写（仅供追溯）

- 来源：2026-10-23 截图批次（桌面 research_reports 研究报告目录），第 17 页
- 方式：机器转写（Qwen-VL），保留原文顺序与命令，未做改写；识别噪声以 [?] 或错字形式存在
- 状态：**不做复刻**。方法论已吸收进 `product-docs` / `architecture` / `design-standards`；本文件只作为追溯材料
- 边界：文中出现的内部地址、人员、表格 ID 仅为原文残留，不得复制进任何技能或脚本

---
- No space before `{` in `if — if($x){` works but `if ($x) {` preferred  
- `=` is assignment in conditions — use `-eq` for comparison  
- Function return array unrolls — `return ,$(@Sarr)` to keep array  
- `Get-Content` returns lines array — `-Raw` for single string  
- `Select-Object` creates new object — properties are copies, not references  

**Windows PowerShell 5.1 Traps（内网实测 2026-10-16）**

- 中文 .ps1 必须 UTF-8 带 BOM：无 BOM 时 5.1 按 GBK 解析，中文注释变 [?] 糊贴纹揽[?] 乱码并引发大量诡异 parse error。DSH 的 edit/write 工具改写文件会剥掉 BOM——每次工具级编辑后重补： `$c=[IO.File]::ReadAllText($p,[Text.Encoding]::UTF8); [IO.File]::WriteAllText($p,$c,(New-Object Text.UTF8Encoding $true))`  
- IWR 一律 `-UseBasicParsing`：5.1 下 `Invoke-WebRequest` 不加它时 POST 可能直接抛 `NullReferenceException`（IE COM 解析路径损坏；GET 却正常，极具迷惑性，症状无 Response 对象、无堆栈）  
- 含中文 JSON body 发 UTF-8 字节： `-ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($json))`；纯字符串 body 按拉丁-1 发送，中文全变 `???`（且不可逆）  
- EAP=`$ps1 Stop` 下别重定向原生命令 `stderr`：`-Content-Type ... 2>&1` 会把 `stderr` 包成 `ErrorRecord` 直接炸 `NativeCommandError`，不重定向（原生 `stderr` 直进控制台不受 EAP 影响），用 `$LASTEXITCODE` 判错  
- `'[ ]' | ConvertFrom-Json` 返回 `$null` 而非空数组，`@($null)` 计数为 1 → 空列表被数出“1 条空数据”。收敛用 `if ($null -eq $r) { ,@() } else { @($r) }`  
- 变量名不区分大小写：`$base` 与 `$Base` 是同一个变量——局部变量会静默覆盖脚本级配置（实例①：`$base` 分支名覆盖 `$Base` API 地址，URI 变 `main/repos/...`，报 DNS 解析 `'main'` 失败；实例② P57 下 `$repo = Invoke-RestMethod ...` 覆盖 `$REPO` 路径串，整个仓库对象 dump 进 URL 连环 404——非 5.1 专属，7.x 一样咬），URL 类故障先打印实际请求 URI 再归因  
- DSH 宿主 `pwsh -Command` 实为 PS 5.1：`-SkipHttpErrorCheck` 参数不识别即征光；嵌套 `pwsh -NoProfile -File <脚本>` 跑的才是 7.x——本书陷阱对命令行直跑的调用全部适用，想用 7.x 特性就落 `.ps1` 再嵌套跑  
- `Invoke-RestMethod` 长上下文抛 URI 解析异常：无淡泊 URI：未能分析主机名（UriFormatException）——同一 URI 短命令能通，数 KB 长内联命令 / 复杂 .ps1 里时好时坏（2026-10-16 office_utils 折痕实测；换 Node fetch 一次跑通）。批量 web API 活用 IRM，改 Node 脚本 + fetch（node ≥18 自带，UTF-8/JSON 原生；实战模板见 gitea skill）  
- `curl` 在 PS 里是 `Invoke-WebRequest` 的别名：调真 curl 必须写 `curl.exe`——内网 API 快验 `curl.exe -s -u user:pass <url>` 很稳  

**Cross-Platform**

- `pwsh` is PowerShell 7+ — `powershell` is Windows PowerShell 5.1  
- Paths use `/` or `\` — `Join-Path` for portable  
- Environment vars: `$env:VAR` — works on all platforms  
- Aliases differ across platforms — `ls`, `cat` may not exist, use full cmdlet names  

---

**AGENT SKILL · 逐字渲染**  
**project-arch**  
skills/project-arch/SKILL.md · 4,241 字符  

---  

name: project-arch  
description: 'L3 架构层 skill（周层流水线第三层）：接到 L1 产品层（project-docs）下发的需求（含 L2 设计定案：规范/token），拆解技术方案、架构、接口设计，拆分成原子开发任务单下发 L4（project-dev）；回收 L4 集件后梳理整合，把跨层疏漏好的整个交付模块回馈 L1。Bug/点检率由本层定位+拆任务。方法论：选型三问、单一职责、契约先行、容错御架构属性（回滚链/失败路径）、任务单与件与清单驱动、review sequence gate、数值不是形容词，层内流程由本层自己把控，L1 只管层面协议（project-docs $^-$）；Use when 用户或 L1 下发技术需求，或提“技术方案/架构/接口设计/新任务/原子任务/联调/模块整合”；Triggers on “技术方案”，“架构”，“接口设计”，“新任务”，“原子任务”，“联调”，“模块”，“architecture”，“API design”，“task breakdown”。'  

---  

**Project Arch — L3 架构层 skill（四层流水线）**  

身份：四层流水线第三层（架构层）。上游 = L1 产品 `project-docs`（需求包，含 L2 设计定案）；下游 = L4 开发测试 `project-dev`。定位（用户原话语义）：接到上层需求 → 拆解技术方案、架构、接口设计 → 拆成原子开发任务下发下去；回收部件，回填上层跑通联调好的整个交付模块。版本：v3（2026-10-16 优化：v2 填实方法论（旧三层架构维度 + AI 前端工厂经验）+ 补回收沉底环）  

**入口契约（由 L1 下发）**  

收到 L1 下发包（协议定义在 project-docs $^-$）：需求陈述 + 验收标准 + 边界 + 溯源；含视觉面的需附 L2 设计定案（规范/token，实现必须遵从）。Bug/点检类：现象描述 + 复现路径，由本层定位根因并拆修复任务。  
层内流程自己把控——方案写多细、任务拆多少、并行度多少、联调怎么组织，本层自定，不请示 L1.  

**层内方法论**  

**1. 拆解技术方案**  
- 选型三问：为什么显它（相对优势）/ 放弃了什么（被否的候选与理由）/ 回退路径（它失效时怎么办）。三问答不全的选型是拍脑袋，写进文档必然失信.  
  - 实例（AI 前端工厂）：PAG 引擎选型——解码比 JSON 快约一个量级、体积小一半、支持目标平台；被否候选与理由同记。  
- 单一真源：每类数据只有一个手写真源（配置文件/常量模块），运行数据由工具从真源内存构建，不靠第二份中间产物文件。已生成的中间产物若被多处直接读取，就是真源失守——废除中间产物、统一从真源构建。  
  - 实例：scenes.toml + petpack.toml 为唯一真源，运行索引由工具内存构建，runtime_index.json 及其全部读取路径被废除。  
- 存储与持久化显式决策：要不要数据库、要不要本地存储、缓存归属，逐项写决策与理由，不默认不跟风。  
  - 实例：静态看板选“无 DB、文件系统直读”；跨会话状态浏览器本地存储并明确失效语义。  
- 无状态优先：能不持有状态就不持有；必须持有的（缓存/队列/会话），写明生命周期与清理路径。  

**2. 架构（模块地图与结构）**  
- 分层抽象：把领域组织成层级模型，每层职责一句话说清；跨层引用只许向下依赖。  
  - 实例：资产四层模型 Pack → Scene → Segment → Variant，逐层有唯一职责与命名规则。  
- 命名前缀使标识全局唯一、用途自明：位置/类别/来源等语义编进命名前缀，任何文件名/接口名/事件名在全仓范围内不重义。  
  - 实例：位置前缀体系（c1/c2/c4/c5/c6/c7/c10/p2/p3），文件名自带位置语义，索引与排障零歧义。  
- 仓拓扑与目录边界成文：哪些仓、什么可见性、谁引用谁；工具、私有文档、公开交付物分仓不混放；跨仓访问路径参数化（环境变量），不硬编码机器路径。  
  - 实例：工厂私有库（docs+tools）与产出公开库（资产+说明）分离，双推镜像使部署机只需访问一个 origin。  
- 载体无关：核心逻辑与宿主解耦，宿主则保持最小（只做展示与上报），换壳不换芯。  
  - 实例：模拟 tick 收口在服务端，宿主协议只保留最小握手；接入原生壳无需重写模拟逻辑。  

**3. 接口设计**  
- 契约先行：接口先于实现定稿并落盘；契约即 L4 的法律，实现与契约冲突以契约为准，改契约走本层。  
- 环境参数统一契约：同类配置跨服务统一命名与语义，一处定义处处引用。  
  - 实例：资产根路径参数在三个服务统一命名（ASSETS_ROOT/ASSETS_DIR 家族），部署文档只讲一套.  
- 无实体响应也必须显式收尾：HTTP 层 writeHead/设置状态后连接不自动关闭，必须显式 end；一切“看起来应该自动结束”的协议路径都要复查收尾动作。  
  - 实例：网关 302 分支漏 end() 导致手数 URL 永久挂起、代理超时 502（复现 6.2s；补 end 后 6-156ms 立即跳转）。  
- 容错是架构属性，不是实现细节：每个外部依赖（LLM/网络/文件系统/下游服务）在设计期就定义失败路径——超时多少、回滚到谁、最终兜底什么行为；回滚链写进契约，不许“失败就崩”。  
  - 实例：LLM 决策三级回落（主模型 → 备用通道 → 确定性兜底），断网降级行为有定义。  
- 安全边界默认收紧：跨源访问 allowlist 回显；不可信输入先 resume 再拒绝，防慢速连接挂起。  

**4. 原子任务拆分**  
- 任务单五件：目标 / 涉及文件与模块 / 验收 case / 依赖顺序 / 契约引用。缺一件 L4 就得猜，猜错返工算本层的.  
- 原子判据：一单一部件，可独立实现、可独立验证，需要“顺便改一下别处”= 拆得不够原子，回去重拆。  
- 验收 case 可自测化：每个 case 写成 L4 拿到就能自验的形式——可执行断言、可复现的输入输出对、可观察的最终状态；写不出来的 case 是需求没分析完，退回 L1.  
- 清单驱动：任务列表穷尽方案范围（对照需求边界逐条映射），执行期不临时加活；发现遗漏 → 补单进清单并记录，不口头塞。  
  - 实例：“全清单清偿”批示执行：方案批一次性列全任务清单，逐项清偿、逐项记账。  

**5. 下发与回收（L4 管理）**  

agent 技能文档 · 28 个自建技能 SKILL.md 逐字渲染（排除 lark-*）  
第 17 页 / 共 34 页


