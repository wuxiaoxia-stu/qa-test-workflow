# QA Test Workflow

[English](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`qa-test-workflow` 是一个用于端到端 QA 工作的 Codex skill，覆盖需求评审、测试用例生成和测试用例评审。它将已确认的需求事实、未解决的缺口和基于行业基线的候选项明确区分，使生成的用例保持可追溯、可评审。

生成的 QA 交付物默认使用简体中文；API 名称、配置键、ID 和文档中的字面消息保持原样。

## 能力

| 模式 | 适用场景 | 主要交付物 |
| --- | --- | --- |
| `requirements-review` | 评审 PRD、用户故事、验收标准、API/UI 规范或需求的可测试性 | 需求理解、缺口、风险、可测试性影响、待澄清问题和后续建议 |
| `test-case-generation` | 基于需求创建或补充测试用例 | 可追溯测试用例、测试点 XMind companion、覆盖矩阵、需求分析和最终用例评审 |
| `test-case-review` | 在测试执行或发布前审计既有测试用例 | 按严重度分级的问题、缺失的高风险覆盖、回归顺序和残余风险 |

该 skill 会自动选择模式。当请求同时包含需求和既有用例、但你希望明确产出时，请显式指定模式。

## 在 Codex 中安装

当 skill 目录位于 Codex skills 目录下且包含 `SKILL.md` 时，Codex 会加载该个人 skill。

### macOS 和 Linux

```bash
git clone https://github.com/wuxiaoxia-stu/qa-test-workflow.git
mkdir -p ~/.codex/skills
cp -R qa-test-workflow ~/.codex/skills/
```

### Windows PowerShell

```powershell
git clone https://github.com/wuxiaoxia-stu/qa-test-workflow.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force .\qa-test-workflow "$env:USERPROFILE\.codex\skills\"
```

安装后请新建一个 Codex 任务，使 skill 列表刷新。

## 在其他 Agent 中安装

本仓库遵循 Agent Skills 的目录规范：请安装完整的 `qa-test-workflow` 文件夹，而不只是 `SKILL.md`。`references/`、`scripts/`、`templates/`、`examples/` 和 `evals/` 均属于 skill 的组成部分。

先克隆仓库一次，再将其根目录复制到对应 Agent 的 skills 目录：

```bash
git clone https://github.com/wuxiaoxia-stu/qa-test-workflow.git
```

| Agent | 个人级安装 | 项目级安装 | 说明 |
| --- | --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/qa-test-workflow/` | `.claude/skills/qa-test-workflow/` | 个人级对所有项目生效；项目级可随代码仓库提交并供团队复用。 |
| [Cursor](https://cursor.com/docs/context/skills) | `~/.cursor/skills/qa-test-workflow/` | `.cursor/skills/qa-test-workflow/` | Cursor 也兼容 `.agents/skills/` 目录规范。 |
| [Trae](https://forum.trae.cn/t/topic/19464) | 中国版使用 `~/.trae-cn/skills/qa-test-workflow/` | `.trae/skills/qa-test-workflow/` | 若当前 Trae 发行版的个人目录不同，优先采用项目级路径。 |

### 文件目录安装

在 macOS 或 Linux 上，将 `<skills-parent>` 替换为上表中相应的父目录，例如 `~/.claude/skills` 或 `.cursor/skills`：

```bash
mkdir -p <skills-parent>
cp -R qa-test-workflow <skills-parent>/
```

在 Windows PowerShell 中，将目标父目录替换为所选 Agent 的目录：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force .\qa-test-workflow "$env:USERPROFILE\.claude\skills\"
```

安装到项目级目录时，请在项目根目录执行对应命令，并将 `<skills-parent>` 设置为 `.claude/skills`、`.cursor/skills` 或 `.trae/skills`。安装完成后新建一个 Agent 会话。

### 腾讯 WorkBuddy

腾讯 WorkBuddy 通过界面导入 skill，而不是扫描固定的文件系统目录。打开 **技能** > **添加技能** > **导入本地技能包**，再导入本仓库下载的本地技能包。如果当前客户端要求选择目录或压缩包，请以导入对话框提示为准；授予权限前应先审阅 `SKILL.md` 和其中引用的脚本。

## 使用

提供需求材料、已有用例和期望执行的动作。该 skill 支持 PRD、用户故事、验收标准、API/UI 规范、技术说明、发布范围、缺陷历史和既有测试用例。

```text
评审这份 PRD 的可测试性，并列出会阻塞发布的需求缺口。

为这项 API 变更生成 Excel 测试用例，包含需求分析和最终用例评审。

从飞书群汇总最近 24 小时的退款需求，然后生成测试用例。

根据提供的验收标准，审计这些已有的结算测试用例。
```

在生成模式下，工作流先建立需求源清单并完成需求分析，再导出测试点 XMind companion，然后评审测试用例草稿并交付修订后的用例。每个测试点都必须包含可观察的预期结果；缺少 `expected_result` 的测试点无法生成 XMind。XMind 文件是详细用例的补充，不会替代用户指定或默认的详细用例格式。已确认需求、因数据缺失而阻塞的条件性用例，以及由需求缺口派生的候选用例会被分别管理；候选用例不会计入已确认的验收覆盖。

只有当测试用例生成请求的原始输入包含连续关键词 `飞书群` 时，才会先读取飞书群消息并输出《飞书群需求摘要》。`飞书`、`Feishu group`、`Lark group` 或被空格拆开的关键词不会触发该前置流程。未指定时间窗时默认读取最近 24 小时；该流程依赖已安装且已授权的 `feishu-cli-messaging` skill。

## 仓库结构

```text
SKILL.md                         面向模型的工作流与模式路由
references/                      需求、生成和评审的详细指引
scripts/                         常见交付物格式的标准库辅助脚本
templates/                       输出模板
examples/                        评审输入与输出样例
evals/                           skill 评估用例
tests/                           包完整性回归测试
```

## 本地验证

内置脚本只依赖 Python 标准库。在仓库根目录运行：

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q scripts
```

在 Codex Desktop 中，如果系统 Python 不可用，请将 `python` 替换为其内置 Python 运行时。

## 贡献与安全

发起 Pull Request 前，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。敏感问题应通过 [SECURITY.md](SECURITY.md) 中的私有渠道报告，不要在公开 Issue 中披露。

## 许可证

本项目采用 [MIT License](LICENSE) 许可。
