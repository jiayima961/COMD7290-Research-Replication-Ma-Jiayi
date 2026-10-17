# COMD7290 · Content Analysis Replication

个人统计课程项目：复现 Löb、Rinke、Weinmann 与 Wessler 的内容分析研究。

**当前阶段：项目初始化。尚未运行研究模型，也未完成最终作业。**

所选论文：Löb, C., Rinke, E. M., Weinmann, C., & Wessler, H. (2024). Unpacking the determinants of outrage and recognition in public discourse: Insights across socio-cultural divides, political systems, and media types. *The International Journal of Press/Politics, 29*(1), 273–294. https://doi.org/10.1177/19401612221084206

论文于2022年在线发表，2024年正式卷期出版，两个年份对应同一篇论文。

## 从哪里开始

1. 看 [当前进度](STATUS.md)，了解已经做了什么、下一步是什么。
2. 看 [作业清单](docs/assignment_checklist.md) 和 [文件结构与工作流程](docs/GitHub文件结构与工作流程.txt)。
3. 看 [理论与假设](docs/theory.md)、[变量字典](docs/variable_dictionary.csv)、[研究设计与模型](docs/design_and_models.md)。这些是待学生核对和批准的初稿。
4. [假设与证据对应表](docs/hypothesis_matrix.csv) 是主索引；[分析覆盖清单](docs/analysis_inventory.csv) 追踪描述统计、信度、正式模型、检验、图和补充分析。
5. 已发表数值在 [outputs/published](outputs/published/)；本项目实际重新计算的结果以后放在 [outputs/reproduced](outputs/reproduced/)。

## 目录

```text
.agents/skills/   三个项目技能
sources/         资料出处和获取说明；local/为仅本地的原文副本
docs/            理论、假设、变量、模型、作业清单和后续研究模板
data/            original/原始材料；prepared/程序整理的数据
analysis/        分析程序的位置和实施计划
tests/           数据、模型和负向测试的位置
outputs/         原文数值、复现输出、诊断、比较与核验报告
records/         来源、决定、AI任务、交接、阶段检查点和运行记录
report/          个人报告提纲及最终提交清单
tools/           仓库材料完整性检查工具
```

## 本地材料检查

安装 Python 3 后，在仓库根目录执行：

```text
python tools/check_repository.py
```

此命令只检查项目结构、CSV字段和已登记本地资料的校验值，不运行统计模型。正式统计环境、经过验证的总运行命令仍待建立，见 [environment.md](environment.md) 与 [analysis/README.md](analysis/README.md)。

## GitHub 与提交状态

- 私有仓库：https://github.com/jiayima961/COMD7290-Content-Analysis-Replication
- 老师账号：`fffchaobu`（按作业原文核对）。按用户2026-10-17的要求，**暂不发送邀请**。
- 学生姓名、学号：待本人填写；不根据登录邮箱推断。
- 最终报告、提交tag和Release：尚未创建。初始化提交不代表最终提交。
- 原文PDF、作者数据和作者程序的再分发权限尚待核对，当前不纳入Git上传；获取方式见 sources/README.md 和 data/README.md。
