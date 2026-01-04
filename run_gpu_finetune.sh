#!/bin/bash

# 基于GPU-QA数据集微调GPU知识助手大模型的脚本

# 设置环境变量
export HF_HOME=./hf_cache
export TRANSFORMERS_CACHE=./hf_cache

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 下载GPU-QA数据集
if [ ! -d "GPU-QA" ]; then
    echo "下载GPU-QA数据集..."
    # 注意：这里需要替换为实际的数据集下载链接
    wget https://example.com/GPU-QA.zip
    unzip GPU-QA.zip
fi

# 微调Qwen3-1.7B模型
echo "开始微调Qwen3-1.7B模型（GPU知识助手）..."
python gpu_llm_finetune.py \
    --model_type qwen3-1.7b \
    --dataset_path GPU-QA \
    --output_dir outputs/qwen3-1.7b-gpu-assistant \
    --lora_rank 16 \
    --learning_rate 5e-5 \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --max_steps 2000 \
    --max_seq_length 1024 \
    --do_train \
    --do_eval

# 微调Qwen3-0.6B模型
echo "开始微调Qwen3-0.6B模型（GPU知识助手）..."
python gpu_llm_finetune.py \
    --model_type qwen3-0.6b \
    --dataset_path GPU-QA \
    --output_dir outputs/qwen3-0.6b-gpu-assistant \
    --lora_rank 16 \
    --learning_rate 5e-5 \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --max_steps 2000 \
    --max_seq_length 1024 \
    --do_train \
    --do_eval

echo "Qwen3 GPU知识助手模型微调完成！"