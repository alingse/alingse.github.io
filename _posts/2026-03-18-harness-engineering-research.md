---
layout: post
title: Harness Engineering 学习调研
date: 2026-03-18 12:00:00 +0800
categories: AI开发
tags:
  - AI
  - Agent
  - Harness Engineering
  - 架构设计
---

*本文包含 AI 辅助创作内容*

## 目录

- [背景](#背景)
- [Harness Engineering 解决什么问题？](#harness-engineering-解决什么问题)
  - [Prompt Engineering 解决什么问题？](#prompt-engineering-解决什么问题)
  - [Context Engineering 解决什么问题？](#context-engineering-解决什么问题)
  - [Harness Engineering 解决什么问题？](#harness-engineering-解决什么问题-1)
- [Agent 可靠执行需要解决的问题](#agent-可靠执行需要解决的问题)
- [可观测性](#可观测性)
- [治理与安全](#治理与安全)
- [Memory 管理](#memory-管理)
- [测评与评估以及训练](#测评与评估以及训练)
  - [Agent 测评体系的三个层次](#agent-测评体系的三个层次)
  - [评估基础设施](#评估基础设施)
  - [Evals 驱动的提示词优化（轻量级训练）](#evals-驱动的提示词优化轻量级训练)
  - [评估与训练的飞轮（Eval-Train Loop）](#评估与训练的飞轮eval-train-loop)
  - [Judge 机制的选择](#judge-机制的选择)
- [所以最后，Harness Engineering 是什么呢？](#所以最后harness-engineering-是什么呢)

---

## 背景

昨天有一个二面的面试，我感觉她说的挺有道理的，有许多是我之前做过但是没有真正认真想过的。主要内容是关于如何做一个类 Claw 的产品，以及做这种类 Claw 产品的核心竞争力。

其中就涉及到「**Harness Engineering**」，因此这篇文章，我就从初学者入手，做一些资料收集和总结。后续我会挑选一个之前实现的 Agent 来做，再写另外一篇实践的文章。

---

## Harness Engineering 解决什么问题？

介绍 Harness Engineering 之前，我们看看它试图解决什么问题。

在这之前，我们还可以更先看看 **Prompt Engineering** 和 **Context Engineering** 解决了什么问题。

### Prompt Engineering 解决什么问题？

**核心问题**：如何正确地向 AI 下达指令（意图表达与对齐）

- **痛点**：早期大模型（**LLM**）虽然聪明，但往往是非确定性的。如果提问方式不对，它会输出不符合预期的结果。
- **解决方案**：通过精心设计输入文本（如 Few-shot、Chain-of-Thought、角色扮演等技巧），引导模型按照人类的期望进行推理和生成。
- **作用范围**：单次交互（Single Interaction）。它关注的是"我们该怎么问"（What should be asked）。

主要关注一次 LLM 调用的提示词编写。

### Context Engineering 解决什么问题？

**核心问题**：如何给 AI 提供正确的背景知识（信息供给与状态感知）

- **痛点**：随着模型能力的增强，人们发现单靠"问得好"不够了。模型缺乏领域私有知识，容易产生幻觉（Hallucination），或者在长对话中遗忘之前的状态。
- **解决方案**：在把 Prompt 发给模型之前，系统化地管理模型的**上下文窗口（Context Window）**。这包括 RAG（检索增强生成）、长短期记忆管理、状态注入等。
- **作用范围**：**模型视野（What the model sees）**。它关注的是"我们该给模型看什么"（What should be shown）。如果说 Prompt 解决的是"AI 愿不愿意做好"，Context 解决的就是"AI 有没有足够的知识做好"。

主要关注在同一个会话的管理。主要是记忆、状态、领域知识相关。

### Harness Engineering 解决什么问题？

现在我们已经通过 Agent 的方式来解决任务，所以在 Agent 时代，**核心问题**变成了：**如何让自主运行的 AI Agent 变得可控、可靠且安全？**（执行环境的边界与工程闭环）

这里我们需要解决如下的一些问题：

- **可靠性问题**
  - 执行错误 / 重试循环 / 错误恢复

- **安全问题**
  - 沙箱 / 精细化权限控制 / 用户权限

- **方向控制问题**
  - 长链路任务 / 状态记录 / checkpoint / 对齐目标 / 人类接关 human-in-the-loop
  - 编排 / 记忆 / 护栏

- **可度量**
  - 规模化评估体系 / Agentic RL / Evals / 可观测 / Reward Signal

这几个其实也和 Google Agent 白皮书里面说的一些 Agent 测评的四个方向相关。**四个测评方向：正确性、效率、稳定性、安全。**

```
                AI System Stack

        ┌──────────────────────┐
        │   Harness Engineering │
        │  (Execution Control)  │
        └──────────▲───────────┘
                   │
        ┌──────────┴───────────┐
        │  Context Engineering │
        │     (Knowledge)      │
        └──────────▲───────────┘
                   │
        ┌──────────┴───────────┐
        │  Prompt Engineering  │
        │     (Instruction)    │
        └──────────────────────┘
```

---

## Agent 可靠执行需要解决的问题

- **执行边界控制（Execution Boundary）**

  限制 Agent 的权限，例如：
  - 文件系统访问
  - shell 命令
  - API 调用
  - 网络访问

- **工具调度（Tool Orchestration）**

  管理 Agent 可调用的工具：
  - tool registry
  - tool schema
  - tool routing
  - tool execution

- **生命周期管理（Agent Lifecycle）**

  管理 Agent 的执行流程，例如：
  - 最大步骤数
  - 超时控制
  - 终止条件
  - 任务流程控制

- **状态与任务管理**
  - 任务状态管理（Task State） → `tasks.json`
  - 执行历史记录（Execution History） → `history`
  - 中间结果存储（Intermediate Results） → `checkpoints`

这里面要做的事情还挺多，任何一个需要在系统上实现 Agent 执行的可能都需要考虑。

---

## 可观测性

这里的可观测性，其实可以和上面的状态、任务管理一起做。

- 执行 trace
- tool logs
- 推理记录
- 指标/日志
- 成本统计

此外为了下面的测评和评估，我们还可以顺带做这些事情：

- **评估与优化（Evaluation Loop）**
  - 成功率统计
  - agent 评估
  - 数据收集

---

## 治理与安全

这部分的安全也可以和上面的执行逻辑一起结合来做：

- prompt injection
- 数据泄露
- 越权操作
- 高成本调用

更细化后需要实施的是这样的：

- **安全防护（Safety Guardrails）**
  - 权限检查
  - 输入输出过滤
  - policy enforcement

- **成本治理（Cost Governance）**
  - token 限制
  - step 限制
  - API 调用预算

- **人类介入（Human-in-the-loop）**
  - 高风险操作审批
  - 人工确认

---

## Memory 管理

> TODO: 另外写一篇文章详细介绍 Agent 的 Memory 管理机制

---

## 测评与评估以及训练

除了最上面的执行之外，看完系列文档我觉得最复杂的还是如何做好一个 Agent 的测评、评估、以及训练相关的。

以下是 AI 给出需要做的一些事情。这里我会备注一些我的理解。

### Agent 测评体系的三个层次

- **工具级评估（Unit Eval）**
  - 原子能力验证：Schema 合规性、语义正确性、参数准确性
  - 方法：Mock 工具调用，不执行真实 API

- **链路级评估（Integration Eval）**
  - 组合能力验证：调用顺序合理性、上下文传递、错误恢复
  - 方法：沙盒化仿真环境

- **任务级评估（End-to-End Eval）**
  - 业务价值验证：结果正确性、完成效率、用户体验
  - 方法：人工或更强模型作为 Judge

### 评估基础设施

- **对抗性测试（Adversarial Testing）**
  - Prompt 注入攻击
  - 逻辑矛盾需求（测试澄清能力）
  - 需拒绝的违规操作（测试安全护栏）
  - 超长上下文/超多步骤（测试稳定性）

- **回归测试套件（Regression Suite）**
  - 维护黄金测试集（Golden Dataset）
  - 发布前自动运行，防止能力回退

- **Evals as Code**
  - 测试用例代码化管理（版本控制）
  - 评估指标可配置（准确率、召回率、成本上限）
  - 结果可视化（成功/失败分布、错误聚类）

### Evals 驱动的提示词优化（轻量级训练）

当无法训练模型权重时，将系统提示词作为超参数，用 Evals 作为损失函数进行搜索优化。

- **A/B 测试框架**
  - 同一批测试集运行不同版本 System Prompt
  - 对比成功率、步数、Token 成本，选出最优版本
  - 工具：DSPy、PromptLayer、LangSmith 等

- **元提示词优化（Meta-prompt Optimization）**
  - 用更强模型分析 Evals 中的失败案例
  - 自动生成改进建议并迭代 System Prompt
  - 动态选择最有效的 Few-shot Examples

- **类 RL 的离散优化算法**
  - **OPRO**：用 LLM 作为优化器，根据历史 Prompt-Score 生成新版本
  - **TextGrad**：将 Prompt 视为可优化变量，用 Evals 反馈计算"伪梯度"
  - **GrIPS**：基于编辑操作（增删改）搜索提示词变体

### 评估与训练的飞轮（Eval-Train Loop）

- **从 Evals 到训练数据**
  - 成功轨迹 → 正样本（SFT/RL 奖励参考）
  - 失败轨迹 → 负样本对（DPO）
  - 边界案例 → 示范数据（Demonstrations）

- **在线评估（Online Eval）与持续学习**
  - 沙盒中自主探索，环境给予奖励信号
  - 实时记录"行动-观察-反思"链条
  - Harness 层提供可复现的 RL 环境

- **Eval-Driven Development（EDD）**
  1. 先写评估用例（定义成功标准）
  2. 跑通评估（初始成功率可能很低）
  3. 迭代 Prompt、工具描述、微调模型
  4. 观察成功率曲线，直至满足发布阈值

### Judge 机制的选择

- **规则匹配**：结构化输出验证，快速但易被绕过
- **人工标注**：最准确，成本高，适合抽检
- **模型即裁判（LLM-as-a-Judge）**：用更强模型评估，需注意偏见
- **执行验证（Execution-based）**：生成代码真正跑一遍，结果客观（如 SWE-bench）

> 实践中常采用分层裁判：规则快速过滤 → 模型评估中间案例 → 人工抽检边界案例

---

## 所以最后，Harness Engineering 是什么呢？

Harness Engineering 是 AI Agent 时代的一门系统级工程范式。

- **本质**：AI Agent 时代的系统级工程范式
- **核心任务**：用确定性代码包裹非确定性 LLM
- **目标转化**：聪明但不可控的"概率引擎" → 安全、稳定、可度量的"工业级软件系统"

**一句话**：Harness Engineering 就是给会犯错的 AI 装上工程化的缰绳和仪表盘，让它从实验室玩具变成可交付的生产工具。
