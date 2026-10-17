---
name: reproduce-and-diagnose
description: Execute approved MedCon independent-coder reliability, ordinal tone and three-level actor-reference logistic models while preserving units, coding and diagnostics.
---

# reproduce-and-diagnose


输入：已批准的模型版本与矩阵、未改写的作者数据、原始独立评分、数据字典、环境与作者代码。

步骤：核对SHA-256、变量标签、特殊缺失、原始评分配对及有向关系唯一性/嵌套；程序化生成样本。信度使用讨论前的独立评分，明确系数测量水平、权重、缺失处理。重拟合tone比例优势有序logit，执行作者假设检查；分别拟合outrage与recognition三层随机截距二项logit，层级为关系→文章内行动者/发言→文章，不能改成国家层级。先获准小规模诊断，再完整估计；保存优化/积分、收敛、方差、区间及实际模型对象。按原约定重新计算概率和AME，说明随机效应处理。原文与本项目值分开。

输出：analysis/可执行程序、data/prepared/、outputs/reproduced/与diagnostics/、records/run_logs/；在覆盖清单记录数据/方案版本、命令、耗时及未完成项。

验证：样本筛选可追踪，量纲区分b/OR/概率/百分点；模型设置对齐来源。不是复制已保存参数，也不以显著与否作为软件测试。显式调用和检查结果登记。

停止条件：无学生批准、无必需原始评分/数据、非法类别或错误配对/嵌套、未收敛、未获准改变模型时，停止受影响计算，记录原因。不得为得到一致结果悄改编码、估计器或简化主要模型。
