#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试GPU-QA数据集格式的脚本
专门用于验证GPU知识问答数据集的格式是否正确
"""

import json
import os

def test_gpu_qa_dataset():
    """测试GPU-QA数据集格式是否正确"""
    dataset_files = [
        "GPU-QA/train.jsonl",
        "GPU-QA/validation.jsonl", 
        "GPU-QA/test.jsonl"
    ]
    
    for file_path in dataset_files:
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            continue
            
        print(f"\n📁 检查文件: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            print(f"   📊 总行数: {len(lines)}")
            
            # 检查前几行的格式
            for i, line in enumerate(lines[:3]):
                try:
                    data = json.loads(line.strip())
                    
                    # 检查是否有question和answer字段
                    if "question" not in data:
                        print(f"   ❌ 第{i+1}行缺少question字段")
                        continue
                        
                    if "answer" not in data:
                        print(f"   ❌ 第{i+1}行缺少answer字段")
                        continue
                    
                    question = data["question"]
                    answer = data["answer"]
                    
                    print(f"   ✅ 第{i+1}行格式正确")
                    print(f"   📝 GPU问题: {question[:50]}...")
                    print(f"   💡 专业解答: {answer[:50]}...")
                    
                    # 检查是否包含GPU相关关键词
                    gpu_keywords = ["GPU", "显卡", "图形处理器", "CUDA", "OpenCL", "显存", "渲染", "计算", "并行"]
                    has_gpu_keyword = any(keyword in question or keyword in answer for keyword in gpu_keywords)
                    if has_gpu_keyword:
                        print(f"   ✅ 包含GPU相关关键词")
                    else:
                        print(f"   ⚠️  未检测到明显的GPU相关关键词")
                        
                except json.JSONDecodeError as e:
                    print(f"   ❌ 第{i+1}行JSON格式错误: {e}")
                    
        except Exception as e:
            print(f"   ❌ 读取文件失败: {e}")
    
    print("\n✅ GPU-QA数据集格式检查完成!")
    print("💡 提示: 确保你的数据集包含GPU相关的专业问答内容")

if __name__ == "__main__":
    test_gpu_qa_dataset()