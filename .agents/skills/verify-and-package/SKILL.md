---
name: verify-and-package
description: Independently audit COMD7290 reproduction quantities, discrepancies and coverage, then prepare a traceable report and final package after completion.
---

# verify-and-package


输入：原始来源、批准方案、输入版本、实现代码、实际输出/日志、全部分析清单；先看原始证据，不能只读实现者总结。

步骤：检查方案到代码和结果对应。以另外实现的计算/方法独立核验一个重要描述量及一个核心复杂模型量，写清检查范围。对副本/模拟数据执行无害负向测试，证明能捕获问题后恢复。比较数值、区间、样本、方差、检验、诊断与概率，不仅比较显著性。审查至少三项重要AI决定，记录学生接受/修改；完成全部覆盖状态、单列敏感性、后续设计和干净重跑。在真实完成后准备APA7报告、提交tag/Release清单及完整commit。

输出：outputs/comparison.csv、review_report.md、docs/limitations.md、records/decisions.md和checkpoints.md、report/；每项证据有路径和命令。

验证：另一个会话重复作者脚本不算独立统计核验；空目录/模板不算执行证据。模型和数据权限、完整覆盖、同一报告与学生最终接受均须核实。记录实际技能调用、失败与检查，不预填通过。

停止条件：缺少真实完整结果、独立核验、干净重跑或学生最终检查时，不宣布完成，不创建最终提交版；当前用户要求不邀请老师。最终打包范围须符合届时用户授权。
