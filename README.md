# GPU知识助手 - 大模型微调项目

## 项目简介

这是一个基于GPU-QA数据集微调大语言模型的项目，旨在创建一个专业的GPU知识助手。该助手能够回答关于GPU硬件、软件、应用等各方面的专业问题。

## 支持的模型

- **Qwen3-1.7B**: 阿里巴巴最新的中等规模模型，平衡性能与效率
- **Qwen3-0.6B**: 轻量级模型，适合资源受限环境和快速推理

## 项目结构

```
├── gpu_llm_finetune.py     # 主训练脚本
├── run_gpu_finetune.sh     # 批量训练脚本
├── create_gpu_dataset.py   # 数据集创建工具
├── test_dataset.py         # 数据集格式验证
├── requirements.txt        # 依赖包列表
├── GPU-QA/                 # GPU知识问答数据集
│   ├── train.jsonl         # 训练数据
│   ├── validation.jsonl    # 验证数据
│   ├── test.jsonl          # 测试数据
│   ├── 基础题集            # 基础GPU知识题目
│   └── README.md           # 数据集说明
└── outputs/                # 模型输出目录
    ├── qwen3-1.7b-gpu-assistant/
    └── qwen3-0.6b-gpu-assistant/
```

## 快速开始

### 方法一：一键启动（推荐新手）

```bash
# 运行快速启动脚本
python start_gpu_assistant.py
```

该脚本提供友好的交互界面，包括：
- 环境检查和依赖安装
- 数据集创建和验证
- 模型训练启动
- 项目状态查看

### 方法二：手动配置

#### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 准备数据集

#### 方法一：使用数据集创建工具（推荐）

```bash
# 运行数据集创建工具
python create_gpu_dataset.py
```

该工具支持：
- 创建示例GPU数据集
- 从CSV文件导入问答数据
- 手动输入问答对
- 自动格式化为标准训练格式

#### 方法二：手动准备数据

将你的GPU问答数据按照以下格式放入 `GPU-QA/` 目录：

```json
{
  "messages": [
    {"role": "system", "content": "you are a helpful GPU assistant."},
    {"role": "user", "content": "什么是GPU？"},
    {"role": "assistant", "content": "GPU是图形处理器..."}
  ]
}
```

#### 验证数据格式

```bash
# 验证数据集格式是否正确
python test_dataset.py
```

#### 3. 开始训练

```bash
# 单个模型训练
python gpu_llm_finetune.py --model_type qwen3-1.7b --do_train --do_eval

# 批量训练所有模型
bash run_gpu_finetune.sh  # Linux/Mac
# 或在Windows PowerShell中运行: .\run_gpu_finetune.sh
```

## 训练参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--model_type` | qwen3-1.7b | 模型类型 (qwen3-1.7b/qwen3-0.6b) |
| `--dataset_path` | GPU-QA | 数据集路径 |
| `--output_dir` | outputs | 输出目录 |
| `--lora_rank` | 8 | LoRA适配器秩 |
| `--learning_rate` | 2e-4 | 学习率 |
| `--max_steps` | 1000 | 最大训练步数 |
| `--max_seq_length` | 1024 | 最大序列长度 |

## 评估指标

项目使用以下指标评估模型性能：
- **ROUGE-1/2/L**: 文本重叠度评估
- **BLEU**: 翻译质量评估
- **生成质量**: 人工评估答案的专业性和准确性

## 使用场景

训练完成的GPU知识助手可以应用于：

- **技术支持**: 回答用户GPU相关问题
- **产品推荐**: 根据需求推荐合适的GPU
- **故障诊断**: 帮助解决GPU使用问题  
- **学习辅助**: 提供GPU技术知识教学
- **内容创作**: 生成GPU相关的技术文档

## 项目工具

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `start_gpu_assistant.py` | 一键启动脚本 | 新手快速开始，提供交互式界面 |
| `create_gpu_dataset.py` | 数据集创建工具 | 将问答数据转换为标准训练格式 |
| `test_dataset.py` | 数据集验证工具 | 检查数据格式是否正确 |
| `gpu_llm_finetune.py` | 主训练脚本 | 单个模型的训练和评估 |
| `run_gpu_finetune.sh` | 批量训练脚本 | 同时训练多个模型 |

## 注意事项

1. **硬件要求**: 建议使用具有足够显存的GPU进行训练（至少8GB显存）
2. **数据质量**: 确保训练数据的专业性和准确性，涵盖GPU各个方面
3. **模型选择**: 根据应用场景选择合适的基础模型
   - Qwen3-1.7B: 中等规模，平衡性能与资源消耗，适合大多数GPU问答场景
   - Qwen3-0.6B: 轻量级，适合资源受限环境和快速推理需求
4. **参数调优**: 可根据数据集大小调整训练参数
5. **数据安全**: 确保训练数据不包含敏感信息

## 许可证

本项目遵循 MIT 许可证。