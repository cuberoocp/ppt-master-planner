# Content Polish Workflow — 内容打磨

> Run AFTER planner.py generates outline/page_plan and BEFORE presenting to user for confirmation. Can be repeated iteratively until manual approval.

## Purpose

Optimize per-slide content quality through three structured passes:
1. **结构定型** — 为每一页定义内容组织结构
2. **语言压缩** — 长句变短句，短句变短语
3. **五维评分** — 按五项指标评分并迭代修改

## Input

- `planning/outline.md` — slide-by-slide title hierarchy
- `planning/page_plan.json` — per-page type and key points
- `_internal/01_content/page_content.json` — full per-page content

## Output

- Updated `planning/outline.md` — with condensed content per slide
- Updated `_internal/01_content/page_content.json` — polished content ready for design spec
- `planning/content_polish_report.md` — per-page structure type, compression delta, 5-dimension scores

## Process

### Pass 1: 结构定型

For each page, determine and document the internal content structure:

| 结构类型 | 适用场景 | 三段式 | 格式标记 |
|---------|---------|--------|---------|
| **总分总** | 论点→论据→验证/案例/总结升华 | thesis + details + validation | `[结构:总分总]` |
| **总分** | 论点→并列论据展开，无收束 | thesis + details | `[结构:总分]` |
| **并列** | 多个同等重要的点，无主次之分 | items[] | `[结构:并列]` |
| **递进** | 层层深入，后一步依赖前一步 | steps[] | `[结构:递进]` |
| **对比** | 正反/前后/AB双方对比 | left_title+left vs right_title+right + case | `[结构:对比]` |

### 结构鉴别规则（避免误判）

判断流程：看内容的最后一个段落是什么

```
内容中是否有"收束段"（案例/数据验证/总结升华）？
├─ 是 → 看倒数第二段是"论点"还是"展开"
│   ├─ thesis + details + validation → 总分总
│   └─ 纯并列对比 → 对比（如A方案 vs B方案 + 数据验证）
└─ 否 → 看段落间关系
    ├─ thesis + 多条并列展开 → 总分
    ├─ 多条同等无主次 → 并列
    ├─ 后一步依赖前一步 → 递进
    └─ 正反两方对比 → 对比
```

**常见误判及纠正** (来自实际案例):

| 误判 | 原因 | 纠正 |
|------|------|------|
| `总分` 写成 `总分总` | 把 details 末尾的案例误认为 validation | 案例如果只是示例而非总结升华→还是总分 |
| `总分` 写成 `并列` | 把 thesis 当成 items[0] | 看首句是否为总起论点→是则总分/总分总 |
| `总分总` 写成 `总分` | 把 validation 混入 details 末尾 | 看最后一项是"并列展开"还是"验证收束"→案例/数据/结论是validation |

### JSON 字段约定

结构类型决定了 page_content.json 中 content 字段的组织方式：

| 结构 | 字段 | 说明 |
|------|------|------|
| 总分总 | thesis + details[] + validation | details是并列展开，validation是验证收束 |
| 总分 | thesis + details[] | details是并列展开，无validation字段 |
| 并列 | items[] | 每条 item 有 title + desc |
| 递进 | steps[] + note | steps 有序，note 是总结说明 |
| 对比 | left_title + left + right_title + right + case(可选) | 明确标记 A vs B |

Write per-page structure annotation to `outline.md`.

### Pass 2: 语言压缩

Apply the compression chain on each page's text content:

```
长句（>30字）→ 短句（15-30字）→ 短语（<15字）→ 关键词
```

Rules:
- **删除** 修饰性副词（"非常"/"相当"/"很"/"真的"）
- **替换** 长词为短词（"横空出世"→"出现"）
- **合并** 重复概念
- **分割** 超过30字的句子
- **增补** 必要的主语（AI产品/模型/团队）
- 保持口语化节奏，每句控制在 15-25 字

Example:
```
原文: "当ChatGPT横空出世那天起，产品经理这个职业就站在了十字路口。我在一线摸爬滚打三年，见证了太多传统PM在AI浪潮下手足无措的场景。"
→ "ChatGPT出现后，产品经理走到了十字路口。一线三年，看到太多传统PM在AI浪潮中手足无措。"
```

Measure and record compression ratio per page.

### Pass 3: 五维评分与迭代

For each page or group of pages, score on 5 dimensions (1-5 scale):

| 维度 | 标准 | 5分定义 |
|------|------|--------|
| **逻辑清晰度** | 听众能否3秒内理解本页在讲什么 | 一眼看懂论点→论据→结论 |
| **信息密度** | 有无冗余词/空话/废话 | 每句话都有信息量，无废话 |
| **内容焦点** | 一页是否只讲一个核心观点 | 整页聚焦一个论点，无跑题 |
| **口语化** | 读起来像在说话而不是念文章 | 自然口语，适合现场演讲 |
| **感染力** | 有没有让人记住的金句/数字/案例 | 有记忆点（金句/震撼数字/故事） |

Criteria for passing:
- All 5 dimensions ≥ 4分 → PASS
- Any dimension ≤ 2分 → 必须修改
- 3分项 ≤ 2项 → 建议修改

Iterate: modify → re-score → repeat until all ≥ 4 or user approves.

## Report Format

Write to `planning/content_polish_report.md`:

```markdown
# Content Polish Report

## Page N: [标题]
- 结构: [总分总/总分/并列/递进/对比]
- 压缩: 原文X字 → 压缩后Y字 (压缩率Z%)
- 评分: 逻辑清晰度N | 信息密度N | 内容焦点N | 口语化N | 感染力N
- 修改要点: ...

## 逐页报告...
```

## Integration

This workflow is called from SKILL.md Step 1 (Content) as step 1.4 after planner artifacts are reviewed and before presenting to user (1.5). Run `pipeline_gate.py <project_dir> content-polished` upon completion.
