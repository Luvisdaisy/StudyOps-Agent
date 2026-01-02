## 阶段一：项目初始化与基础工程（Project Bootstrap）

**目标**：本地 `uv run python main.py` 能启动，工程结构清晰，可持续演进。

### 1. 项目结构初始化

- [ ] 创建 Git 仓库
- [ ] 初始化基础目录结构

  ```
  studyops-agent/
  ├─ main.py
  ├─ app/
  │  ├─ cli/
  │  ├─ agent/
  │  ├─ ingest/
  │  ├─ rag/
  │  ├─ graph/
  │  ├─ storage/
  │  └─ utils/
  ├─ configs/
  ├─ docker/
  ├─ data/
  └─ README.md
  ```

- [ ] 明确 `main.py` 为**唯一入口**

### 2. Python & uv 环境

- [ ] 使用 Python 3.14
- [ ] 初始化 `pyproject.toml`
- [ ] 使用 `uv` 管理依赖
- [ ] 划分依赖分组（core / dev / llm）

### 3. Docker 基础环境

- [ ] 编写 `docker-compose.yml`
- [ ] 启动以下服务：

  - Redis
  - Neo4j

- [ ] 验证容器可本地访问

---

## 阶段二：CLI 框架与运行流程设计

**目标**：所有操作从 CLI 驱动，形成“可复现的 Agent 工作流”。

### 1. CLI 框架

- [ ] 设计 CLI 命令规范

  - `ingest <path>`
  - `chat`
  - `graph build`
  - `graph query`

- [ ] 实现基础命令解析（如 Typer / Click）

### 2. 启动流程

- [ ] `main.py` 启动流程：

  1. 初始化配置
  2. 检查 Redis / Neo4j 连接
  3. 进入 CLI 交互循环

- [ ] 支持 `--config` 指定配置文件

---

## 阶段三：数据接入与知识库构建（Ingestion）

**目标**：你的学习资料 → 可检索、可推理的结构化知识。

### 1. 文档加载

- [ ] 支持目录级加载
- [ ] 支持格式：

  - Markdown
  - PDF
  - TXT

- [ ] 文档元数据标准化（来源、时间、标签）

### 2. 文本切分

- [ ] 设计 Chunk 策略
- [ ] 保留文档层级信息
- [ ] 可配置 Chunk Size / Overlap

### 3. 向量化

- [ ] 集成 Embedding 模型
- [ ] 将向量存入向量数据库（如 Chroma）
- [ ] 建立 文档 → Chunk → 向量 映射

---

## 阶段四：RAG 问答链路（Retrieval-Augmented Generation）

**目标**：Agent 能基于你自己的资料进行高质量问答。

### 1. 检索模块

- [ ] 实现相似度检索
- [ ] Top-K 可配置
- [ ] 支持 metadata filter

### 2. Prompt 工程

- [ ] 设计系统 Prompt
- [ ] 设计检索增强 Prompt
- [ ] 明确引用规则（基于哪些资料回答）

### 3. 基础对话能力

- [ ] CLI 中实现 `chat` 模式
- [ ] 支持多轮上下文
- [ ] Context 存入 Redis

---

## 阶段五：Neo4j 知识图谱（GraphRAG）

**目标**：从“文本检索”升级为“结构化推理”。

### 1. 图谱 Schema 设计

- [ ] 节点类型：

  - Document
  - Concept
  - Person / Method / Tool

- [ ] 关系类型：

  - MENTIONS
  - DEPENDS_ON
  - RELATED_TO

### 2. 图谱构建

- [ ] 从文档中抽取实体
- [ ] 写入 Neo4j
- [ ] 建立索引与约束

### 3. GraphRAG 查询

- [ ] 基于问题生成 Cypher
- [ ] 图查询结果 + 向量检索融合
- [ ] 将结构化结果注入 Prompt

---

## 阶段六：Agent 能力封装（核心亮点）

**目标**：这是你面试时**最有价值的部分**。

### 1. Agent 架构

- [ ] 定义 Agent State
- [ ] 定义 Tool 接口
- [ ] 使用 LangGraph 构建流程图

### 2. Agent 工具集

- [ ] 文档搜索 Tool
- [ ] 图谱查询 Tool
- [ ] 文件读写 Tool
- [ ] 总结 / 重写 Tool

### 3. 任务驱动能力

- [ ] 支持：

  - “帮我总结这门课的核心知识”
  - “基于现有资料生成学习计划”
  - “重写某段笔记”

---

## 阶段七：工程化与可展示性优化

**目标**：让项目**像一个真实 AI 应用，而不是 Demo**。

### 1. 配置与日志

- [ ] 多环境配置
- [ ] 结构化日志
- [ ] 错误可追踪

### 2. Docker 化

- [ ] Agent 本体 Dockerfile
- [ ] 一键启动完整环境

### 3. README 与展示

- [ ] 项目背景
- [ ] 技术栈说明
- [ ] 架构图
- [ ] CLI 示例

---

## 阶段八（可选）：扩展方向（面试加分）

- [ ] 用户体系（JWT）
- [ ] Web UI（React + FastAPI）
- [ ] MCP 协议接入
- [ ] 多 Agent 协作
