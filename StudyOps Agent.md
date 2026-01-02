# StudyOps Agent 项目规划书（正式版）

---

## 一、项目概述

**项目名称**：StudyOps Agent（学习资料智能体）

**项目定位**：
StudyOps Agent 是一个面向 AI 应用开发学习与转型的本地智能体系统。项目以“学习资料目录”为核心输入，通过自动化流程构建 **向量数据库（Chroma）+ 知识图谱（Neo4j）+ 元数据索引（SQLite）**，并基于此实现可对话、可检索、可编辑文件的智能体应用。

**核心目标**：

- 覆盖主流 AI 应用开发技术栈（RAG、GraphRAG、Agent、工具调用、缓存、工程化部署）。
- 以最小可行实现（MVP）为优先，确保快速落地与可持续扩展。
- 保持本地运行模式，便于学习、调试与长期维护。

**最终运行方式**：

```bash
uv run python main.py
```

---

## 二、总体设计原则

1. **本地优先、依赖容器化**
   应用本体本地运行，Redis 与 Neo4j 等基础设施通过 Docker 提供。

2. **快速可用、渐进增强**
   优先保证完整闭环，再逐步增强文本质量、图谱语义与检索效果。

3. **工程可复现**
   使用 uv 锁定 Python 版本与依赖，确保环境一致性。

4. **安全可控**
   文件操作限制在指定 workspace 内，所有修改均具备版本备份。

---

## 三、技术栈选型

### 3.1 运行与工程化

- Python 3.14
- uv（依赖管理与锁定）
- SQLite（元数据与 workspace 登记）
- Docker / Docker Compose（基础服务）

### 3.2 AI 与智能体

- LangChain（文档加载、检索、工具封装）
- LangGraph（Agent 状态机与流程编排）
- Chroma（本地向量数据库）

### 3.3 知识图谱

- Neo4j（Docker 部署，Bolt 协议访问）
- Neo4j Python Driver（Cypher 写入与查询）

### 3.4 缓存与状态

- Redis（Docker 部署）

  - Embedding 缓存
  - 检索结果缓存
  - 会话状态缓存
  - 索引任务状态管理

---

## 四、系统架构

### 4.1 架构组成

- **本地应用层**

  - CLI 交互入口（main.py）
  - 文档处理与索引构建
  - 智能体（对话、检索、工具调用）
  - Workspace 注册与管理

- **基础设施层（Docker）**

  - Redis（缓存与状态）
  - Neo4j（知识图谱）

### 4.2 数据流说明

```
学习资料目录
   ↓
文本抽取与分块
   ↓
向量嵌入 → Chroma
   ↓
结构与实体关系 → Neo4j
   ↓
Agent（RAG + GraphRAG）
   ↓
CLI 对话 / 文件操作
```

---

## 五、Workspace 设计

### 5.1 Workspace 定义

Workspace 对应一个学习资料根目录，是索引、向量库与图谱的最小管理单元。

### 5.2 Workspace 映射表（SQLite）

表：`workspaces`

- `id`（UUID）
- `root_path`
- `dir_fingerprint`
- `chroma_path`
- `neo4j_namespace`
- `created_at`
- `updated_at`

表：`files`

- `workspace_id`
- `rel_path`
- `content_hash`
- `mtime`
- `file_type`
- `status`
- `error_msg`

### 5.3 目录复用逻辑

- 启动时输入目录路径
- 计算目录指纹
- 若已存在对应 workspace，则直接复用索引
- 若不存在，则新建 workspace 并执行全量处理

---

## 六、知识图谱设计（Neo4j）

### 6.1 节点类型

- `Workspace`
- `Document`
- `Chunk`
- `Entity`（可选）
- `Topic`（可选）

### 6.2 关系类型

- `(Workspace)-[:HAS_DOC]->(Document)`
- `(Document)-[:CONTAINS]->(Chunk)`
- `(Chunk)-[:MENTIONS]->(Entity)`
- `(Chunk)-[:ABOUT]->(Topic)`
- `(Entity)-[:RELATED_TO]->(Entity)`

### 6.3 隔离策略

- 所有节点与关系均携带 `workspace_id` 属性
- 所有查询统一按 `workspace_id` 过滤
- 单 Neo4j 数据库，多 workspace 共存

---

## 七、向量检索与 GraphRAG

### 7.1 向量检索

- 使用 Chroma 对 Chunk 向量进行 Top-K 检索
- Redis 缓存查询结果以降低重复计算

### 7.2 图谱增强检索（GraphRAG）

- 从命中 Chunk 出发：

  - 扩展同一 Document 的相邻 Chunk
  - 通过 Entity/Topic 查找相关 Chunk

- 合并并排序召回结果作为上下文

---

## 八、智能体能力设计

### 8.1 对话能力

- 基于 LangGraph 的状态机对话
- 支持上下文记忆与多轮问答
- 回答必须包含引用来源

### 8.2 工具能力

- 文件读取（read）
- 文件写入（write）
- 文件补丁修改（patch）
- 文件列表与搜索
- 笔记与总结导出（markdown）

### 8.3 安全约束

- 所有文件操作限制在 workspace 目录内
- 修改操作生成版本备份
- 禁止越权路径访问

---

## 九、CLI 命令设计

- `/help`：查看命令说明
- `/use <path>`：加载或切换 workspace
- `/index`：构建或重建索引
- `/search <query>`：仅执行检索
- `/graph <keyword>`：图谱查询
- `/open <file>`：查看文件
- `/edit <file>`：修改文件
- `/export <file>`：导出总结
- `/exit`：退出程序

---

## 十、项目结构

```
studyops-agent/
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
├── .env.example
├── docker/
│   └── docker-compose.yml
├── data/
│   ├── workspaces.db
│   └── ws_<id>/
│       ├── chroma/
│       └── versions/
└── src/
    ├── core/
    ├── workspace/
    ├── ingest/
    ├── graph/
    ├── rag/
    ├── agent/
    └── cli/
```

---

## 十一、部署与运行方式

1. 启动基础服务：

```bash
docker compose up -d
```

2. 本地运行应用：

```bash
uv run python main.py
```

---

## 十二、实施里程碑

1. **基础设施阶段**

   - uv 项目初始化
   - Redis 与 Neo4j 容器启动

2. **Workspace 管理阶段**

   - 目录指纹
   - SQLite 映射表

3. **索引构建阶段**

   - 文本抽取
   - 向量库构建
   - Neo4j 结构图写入

4. **智能体阶段**

   - RAG 对话
   - GraphRAG 增强

5. **工具与文件操作阶段**

   - 文件读写与修改
   - 导出与版本管理

---

## 十三、交付标准

- 支持通过 `uv run python main.py` 本地启动
- Redis 与 Neo4j 通过 Docker 提供服务
- 同一资料目录可复用索引
- 支持基于资料的对话问答并返回引用来源
- 支持安全的本地文件修改与导出

---

**本规划书作为 StudyOps Agent 项目的统一实施蓝本，后续开发、扩展与评估均以此为依据。**
