# archive-vault — 截图转写（仅供追溯）

- 来源：1028 版截图第 31 页
- 方式：机器转写（Qwen-VL），保留原文顺序与命令，未做改写；识别噪声以 [?] 或错字形式存在
- 状态：**不复刻、不注册**（用户 2026-10-31 指示："archive-vault 不要注册，进文本存下来参考"）
- 说明：曾按泛用方式实现并跑通 26 条断言，随后按要求移除，只保留本文本。核心可迁移结论记在下节
- 边界：文中出现的库路径 <vault-root>、收件箱路径、人员信息仅为原文残留，不得复制进任何技能或脚本

## 可保留的结论（与其实现无关）

1. 索引是唯一真源：分类规则、项目关键词、计数都在库根 INDEX.md，脚本不自带规则副本，换库只改索引。
2. 决策链顺序：项目关键词 → 扩展名规则 → 兜底；兜底不确定时留在收件箱并报告，不猜。
3. 干跑优先：入库与去重默认只报告，--apply 才动手。
4. 去重三重保障：用户明示授权 + 同名同大小 + SHA256 验证，产物进回收站而非删除。
5. 内容相同但文件名不同的，通常是"交付件 + 存档件"两份合法副本，不合并。

---
extra_moods 与参照包 mood_map 已有键重叠 → 警告并自动跳过（参照包语义优先，硬规则 7）  
守卫基准 = mood_words 全集（含参照包全部键 + extra_moods）  

# — 第 4 步 变体块生成 —  
每变体：id=vid；vl_description = "类别 · 动作（情绪：X）"（表字段直译占位，硬规则 12）；  
　vl_tag；mood：断言 mood ∈ mood_words（缺 → sys.exit［情绪值必须被 mood_map 覆盖］）  
mood_secondary = 动作标签（生熟人行为词除外）；voice_command 数组形态生成器按 [0] 取值  
PHUD 场景按 phud_rules by tag 准则 effect<->context二段式；scene_state_map 场景->state_tags（进出场/梦境）  
business_tags_by_tag 动作标签→生熟人标记；business_mood_markers〈config 门控〉情绪内嵌生熟人→business_tags  
转场变体带 effect_tags → sys.exit（口径：转场零特效）  
delta 包变体附道具四字段 prop_fields + prop_id  

# — 第 5 步 dist 落盘 —  
rmtree(cfg.dist_root) 重建；base 包 = 全部常规变体，delta_N = 按 cfg.prop_order 各道具  
每包写：petpack.toml（顶层 vl_common 占位空串 + [package] id=cfg.toml_id version=cfg.version  
　　　　　type-base/delta_N + identity + render_defaults + states_block + mood_block + extra_moods）  
　　　scenes.toml（场景头同构 + 变体块）  
　　　PAG 落位 <场景>/<位置码>_d1_<vid>.pag  
　　　base 另拷 query_profiles.json；全包拷 cfg.index_generator 的 generate_pag_index.mjs  
写 dist/build_map.json（packs{type, prop_id, files{目标→源}, prop_values} / scenes_base / deleted）  
打印 [== build 完成 ==] + report + 排除行 + 下一步提示  

inject_prop_fields.mjs（道具字段注入）  
# — 后处理：索引生成器不透传 prop 字段时补注入 —  
读 cfg.dist_root/build_map.json  
for (name, pack) in build_map.packs:  
　pack.prop_id 为空（base 包）→ continue  
　读 dist/name/pag_index.json 的 pag_index 对象  
　for key in pack.files 键（包内每个 .pag 相对路径）：  
　　　断言 key ∈ pag_index ← 「MISSING KEY」→ exit 1  
　　　Object.assign(pag_index[key], pack.prop_values)  
　　　# prop_values = cfg.prop_fields + prop_id: 道具四字段  
　　　#〈prop_id = asset_kind / trigger_state / anchor_position〉  
　写回 pag_index.json  

zip_verify.py（打 zip + 九项验收 + 出包清单）  
# — 第 0 步 打 zip —  
PACKS = [pack_id] + prop_order 各后缀包  
for p in PACKS:  
　files = os.walk(dist/p) 全部文件；ZIP_EXCLUDE = set(cfg.zip_exclude)（生成器等非数据文件，  
　　　　　柴犬批拍板：交付物只含数据文件）  
　entries = 相对路径（\）∈ ZIP_EXCLUDE 且 basename ∉ ZIP_EXCLUDE  
　ZIP_DEFALTED 打包 output_dir/p.zip；记录 zip sha256 / 条目数 / MB  

# — 第 1-9 步 九项验收（任一 fail → exit 1）—  
① 根级必需文件：petpack.toml + scenes.toml + pag_index.json（base 另含 query_profiles.json），缺即 fail  
② 无嵌套前缀：zip 内不得有 "<pack_id>/" 开头成员  
③ pag_index 键集 == 包内 .pag 文件集 == scenes.toml 变体数  
　〈scenes 变体用正则 ^\s+id = "(q\w+)" 计数；三者不等即 fail）  
④ 全包 [package].id/version 全等（regex 抓 id/version/type 行）；type 序列 == [base, delta_1..N]  
⑤ delta 逐条索引带 prop_id==包名后缀 + asset_kind + trigger_state + anchor_position；  
　base 索引零道具字段（含 prop_id 即 fail）  
⑥ 全部 PAG 字节级对账：sha256(包内 PAG) == sha256(staging 源文件)；无多余文件、无进错包；  
　PAG 总数 == build_map.files 总数  
⑦ petpack.toml ≠ scenes.toml 用 tomlib 标准严格解析（TOMLDecodeError → fail）  
　# 标准严格解析器：宽松解析器放过重复表明，tomllib 不会（蜜蜂回测实录抓出 mood_map 重复键）  
⑧ 出包清单 <pack_id>_出包清单.txt 落盘（见下）  
⑨ 词表枚举守卫（cfg.enums 全集为基准）：每变体 n_enum++ 逐查—  
　voice_trigger / voice_command（TOML 数组形态取 [0] 比校验）/ gesture_trigger 各项 /  
　effect_tags 各项（且转场 type 场景带 effect_tags 即 fail）/ business_tags / state_tags /  
　context 各项 ∈ 对应枚举集；mood 与 mood_secondary ∈ mood_map 键集；  
　vl_description 非空时 ≥10 字；petpack 必须有顶层 vl_common + [render_defaults] +  
　[package].id == cfg.toml_id  
　汇总「n 变体 11 类字段全过（voice/command/gesture/effect/business/state/context/mood/M2/vl 长度/petpack 结构）」  

# — 出包清单 txt —  
标题/日期行：【包清单】共 N 包 · M 个 PAG（每包 条目数/MB/base|delta_N/道具名）；  
【base 场景分布】：【道具包】× 计数 + 锚点/触发态/asset_kind；【包结构】根级无嵌套说明；  
【VL 来源】vl_common 非自动动标"帧分析（pet-vl 流水线回写；vl_common 包级 +  
vl_description 个体瘦身稿，双层同批上线）"，空串标"表字段直译占位"；  
【基线】日期：【校验】全部通过/存在失败项 + 各 report 行；【SHA256】各 zip  

# — 退出 —  
打印 == 验收 == 各 report 行 + FAILURES（空则「无 – 全部通过」）+ 交付物清单  
sys.exit(1 if fail else 0)  

repack_from_vl.py（vl 回写后一条命令重出包）  
# — 第 1 步 拉最新 —  
git -C cfg.vl_repo pull（returncode != 0 → exit 1［vl 仓 pull 失败］stderr 尾 300 字）  
打印 vl 仓最新：仓库路径 @ 短 HEAD（git rev-parse --short HEAD）  

# — 第 2 步 同步包目录 + 重建 build_map —  
pack_names = [cfg.pack_id] + prop_order 各后缀包  
dist_root 存在 → rmtree 重建  
for name in pack_names:  
　断言 vl 仓存在该包目录（vl仓/包名），缺失 → exit 1  
　copytree(vl仓/包名 → dist/包名)　　　　　　　# vl 仓 PAG 路径 = 字节对账源  
　tomllib 解析 petpack.toml 取 type；delta 包 prop_id = 包名[len(pack_id)+1:]  
　files{相对路径 → "包名/相对路径"} = walk 包目录全部 .pag  
　base 包另解析 scenes.toml + scenes_base[场景ID]：[全部变体id]  
写 dist/build_map.json（packs{type, prop_id, files, prop_values} / scenes_base / deleted=[]）  

# — 第 3 步 逐包重生成索引 + 道具注入 —  
for name in pack_names:  
　subprocess node generate_pag_index.mjs（cwd=dist/name, capture 输出）  
　returncode != 0 → exit 1［索引生成失败］  
　stdout 不含 '无警告' → exit 1［索引生成有警告（口径：0 警告）］  
subprocess node inject_prop_fields.mjs dist_root（check=True）  

# — 第 4 步 zip + 九项验收 —  
makedirs(OUT)；写 OUT/_repac_config.json = cfg 副本改 staging_dir=vl_repo、output_dir=OUT  
subprocess python -X utf8 zip_verify.py _repac_config.json  
sys.exit(其 returncode)　　# 验收全绿才交付；VL 来源由 vl_common 非空自动标「帧分析」  

28/28 □ 文件治理（1） archive-vault · 本地归档库全流程：入库/索引/审计/去重　skills/archive-vault/SKILL.md 逐字 + 脚本伪代码：10,231 字符  

name: archive-vault  
description: 本地文件归档库（vault）全流程；收件箱待归档批次处理（分类决策链：扩展名规则→项目归属→vision 看图兜底→通用 vault 兜底）、manifest 驱动入库、INDEX.md 索引自动重算（数字只由脚本写）、全库审计（计数对表/0字节/空目录/同名同大小重复/错位文件）、批次日志、授权去重清理（vault_dedup.ps1：同名同大小+SHA256验证→保贩规则→回收站）。与实际内容解耦；目录清单、分类规则（扩展约定）、项目名、计数全部以库根 INDEX.md 为唯一真源，本 skill 只载流程、决策链与脚本，换库不改 skill。当用户说归档、处理 to archive/待归档、整理文件进归档库、查归档库、归档审计/check、INDEX 对表、去重/清理重复副本时使用。关键词：归档、待归档、to archive、archive_folder、INDEX.md、vault、入库、批次日志、归档审计、去重。不负责：飞书云盘文件（lark-drive）、调研仓库结构（research-report）、删除或解压现有归档（库宪法：不删除、不解压；唯一例外=用户明示授权的去重，须走 SHA256 验证+回收站三重保障）。  

0. 解耦原则（本 skill 的边界）  
· 唯一真源 = 库根 INDEX.md：顶层结构、分类规则（［扩展约定］节）、项目清单、批次日志全部在库内；本 skill 不复制这些内容，不硬编码项目名/计数/路径 · 实例指针（换库只改这里，流程不变）：库根 <vault-root>，收件箱 <profile>\Desktop\to_archive（常设收件箱，清空但保留文件夹） · 规则演化发生在 INDEX［扩展约定］区；本 skill 的决策链从 INDEX 读取规则，不自带规则副本 · 库宪法（不可演化）：不删除文件、不解压归档；唯一例外 = 用户明示授权的去重清理（见 §3 协议），且必须走 vault_dedup.ps1 三重保障（授权+SHA256 验证+回收站）  

1. 入库流程（用户说「处理归档 / to archive / 待归档」时）  
1. 读规则：读库根 INDEX.md 的［顶层结构］+［扩展约定］，拿到当前目录与分类规则  
2. 扫收件箱：枚举收件箱全部内容（-Recurse -Force）；文件名常含（）@ 中文 空格 → 后续一律 -LiteralPath  
3. 分类决策链（顺序执行，前者命中即停）：  
　· 扩展名规则：msi/exe 安装包→工具\安装包\；apk→工具\APK\；zip/7z/rar/分卷 整包→归档\（不拆）  
　· 项目归属：文件名/内容能对上 INDEX 项目表 → 项目\⟨名⟩\，项目内跟随其既有 vault 子目录（文档/图片/视频/佳作...），不发明新结构 · 图片/视频拿不准 → vision-recognition 的 vision.ps1 看内容（大图先 thumb 降分辨率；视频用 python cv2 抽帧，本机无 ffmpeg） · 无法归属 → 通用 vault（图片/视频/文档/3D资产/脚本）；表情包/梗图→图片\杂项\ · 仍拿不准 → 归通用 vault + 报告里标［存疑］，不猜项目  
4. 生成 manifest（UTF-8 TSV：每行 路径径<TAB>目标目录，目标目录先建好）→ vault_ingest.ps1 -DryRun 出计划核对 → 去掉 -DryRun 执行  
5. 脚本自动完成：冲突检查（同名跳过不覆盖）、移动、重算全库计数改写 INDEX.ME。追加批次日志  
6. 人工检验：收件箱清空、落位清单、存疑项告知用户  

2. 铁律（违反即事故）  
· 不删除、不解压（库宪法） · -LiteralPath 一律使用（() @ 中文 空格 文件名） · INDEX 数字单元格只允许脚本写（ingest / audit -FixTable）；说明列才由人/agent 写。手算数字 = 漂移之源。实证 2026-10-21：项目表 12/17 行漂移，最重 AI萌宠 1556（手抄）vs 实测 330 · 移动前冲突检查；同名冲突跳过并报告，不覆盖 · 报告用测量值，不用估算值  
· 去重删除的唯一合法路径：用户明示授权 + vault_dedup.ps1（执行时全量重扫，每个删除项必须有不在删除集内的同哈希孪生，否则拒删；删除一律进回收站可恢复）；其余任何情况不删文件  

3. 审计协议（用户说［Check 归档 / 审计 / 对表］时，或每批次入库后自动跑）  
vault_audit.ps1 输出：计数对表（顶层表、项目表、各分节表全覆盖）、0字节文件、空目录、同名同大小重复、扩展名分布。发现项分类处置：  

　自建 Skill 全档 · 28 技能整编 v4（SKILL.md 逐字 + 脚本伪代码）　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　第 34 页 / 共 36 页



