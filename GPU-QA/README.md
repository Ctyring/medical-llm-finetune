# GPU-QA GPU知识问答数据集

## 数据集简介

GPU-QA是一个专门用于训练GPU知识助手的中文问答数据集，涵盖GPU硬件、软件、应用等各个方面的专业知识。

## 数据集结构

```
GPU-QA/
├── train.jsonl      # 训练集
├── validation.jsonl # 验证集
├── test.jsonl       # 测试集
└── README.md        # 说明文档
```

## 数据格式

每个 JSONL 文件包含GPU相关问答对，采用简单的问答格式：

```json
{
  "question": "什么是GPU？",
  "answer": "GPU（Graphics Processing Unit，图形处理器）是一种专门用于处理图形和并行计算任务的处理器。与CPU不同，GPU拥有数千个较小的核心，能够同时处理大量简单的计算任务，特别适合图形渲染、深度学习、科学计算等需要大量并行处理的应用。"
}
```

### 字段说明

- `question`: 用户提出的GPU相关问题
- `answer`: 对应的专业解答

## 涵盖领域

- GPU硬件架构和规格
- 显卡选购和对比
- GPU编程（CUDA、OpenCL等）
- 深度学习和AI应用
- 游戏和图形渲染
- GPU超频和调优
- 故障诊断和维护
- 挖矿和计算应用

## 使用说明

1. 将你的GPU问答数据按照上述简单格式整理
2. 分别放入对应的 train.jsonl、validation.jsonl、test.jsonl 文件中
3. 每行一个完整的 JSON 对象，不要使用 JSON 数组格式
4. 确保问题和答案都是GPU相关的专业内容

### 数据准备步骤

```python
# 示例：创建GPU问答数据
import json

qa_pairs = [
    {"question": "什么是GPU？", "answer": "GPU是图形处理器..."},
    {"question": "GPU和CPU有什么区别？", "answer": "GPU和CPU的主要区别..."},
    # 更多问答对
]

with open("train.jsonl", "w", encoding="utf-8") as f:
    for qa in qa_pairs:
        f.write(json.dumps(qa, ensure_ascii=False) + "\n")
```

## 示例数据

文件中已包含少量示例数据，涵盖GPU基础知识、硬件对比、编程应用等方面。

## 注意事项

- 所有文件使用 UTF-8 编码
- 每行必须是有效的 JSON 格式
- 建议训练集数据量 > 验证集 > 测试集
- 数据质量直接影响模型效果，请确保答案的专业性和准确性
- 可以包含技术规格、性能数据、使用建议等内容