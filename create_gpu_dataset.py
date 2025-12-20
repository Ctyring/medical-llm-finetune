#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU-QA数据集创建工具
帮助用户将GPU问答数据转换为标准的训练格式
"""

import json
import os
from typing import List, Dict, Any

def create_gpu_qa_entry(question: str, answer: str) -> Dict[str, Any]:
    """
    创建单个GPU问答条目
    
    Args:
        question: 用户问题
        answer: 助手回答
    
    Returns:
        格式化的数据条目
    """
    return {
        "question": question,
        "answer": answer
    }

def save_dataset(data: List[Dict[str, Any]], filepath: str) -> None:
    """
    保存数据集到JSONL文件
    
    Args:
        data: 数据列表
        filepath: 输出文件路径
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"✅ 已保存 {len(data)} 条数据到 {filepath}")

def create_sample_gpu_dataset():
    """创建示例GPU数据集"""
    
    # 示例GPU问答数据
    sample_qa_pairs = [
        {
            "question": "什么是GPU？",
            "answer": "GPU（Graphics Processing Unit，图形处理器）是一种专门用于处理图形和并行计算任务的处理器。与CPU不同，GPU拥有数千个较小的核心，能够同时处理大量简单的计算任务，特别适合图形渲染、深度学习、科学计算等需要大量并行处理的应用。"
        },
        {
            "question": "GPU和CPU有什么区别？",
            "answer": "GPU和CPU的主要区别在于架构设计：\n1. **核心数量**：CPU通常有4-16个强大的核心，GPU有数百到数千个较小的核心\n2. **处理方式**：CPU擅长复杂的顺序处理和分支预测，GPU擅长简单的并行计算\n3. **内存**：CPU有大容量缓存和复杂的内存层次，GPU有高带宽的显存\n4. **应用场景**：CPU适合通用计算和复杂逻辑，GPU适合图形渲染和并行计算"
        },
        {
            "question": "如何选择合适的显卡？",
            "answer": "选择显卡需要考虑以下因素：\n1. **用途**：游戏、专业设计、深度学习等不同需求\n2. **预算**：确定价格范围\n3. **性能需求**：根据目标分辨率和帧率选择\n4. **兼容性**：检查主板、电源、机箱空间\n5. **品牌和型号**：NVIDIA RTX系列适合游戏和AI，AMD RX系列性价比较高\n6. **显存容量**：4K游戏建议8GB+，AI训练建议12GB+"
        },
        {
            "question": "什么是CUDA？",
            "answer": "CUDA（Compute Unified Device Architecture）是NVIDIA开发的并行计算平台和编程模型。它允许开发者使用GPU进行通用计算，而不仅仅是图形处理。CUDA提供了C/C++扩展，让程序员能够编写在GPU上运行的代码，大大加速科学计算、深度学习、图像处理等应用的性能。"
        },
        {
            "question": "显存不足怎么办？",
            "answer": "显存不足的解决方案：\n1. **降低设置**：减少纹理质量、分辨率或模型复杂度\n2. **批处理优化**：减小batch size或使用梯度累积\n3. **模型优化**：使用模型压缩、量化或剪枝技术\n4. **内存管理**：及时释放不用的变量，使用内存映射\n5. **硬件升级**：更换更大显存的显卡\n6. **分布式计算**：使用多GPU或模型并行"
        }
    ]
    
    # 转换为标准格式
    dataset = []
    for qa in sample_qa_pairs:
        entry = create_gpu_qa_entry(qa["question"], qa["answer"])
        dataset.append(entry)
    
    # 分割数据集 (70% 训练, 20% 验证, 10% 测试)
    total = len(dataset)
    train_size = int(total * 0.7)
    val_size = int(total * 0.2)
    
    train_data = dataset[:train_size]
    val_data = dataset[train_size:train_size + val_size]
    test_data = dataset[train_size + val_size:]
    
    # 保存数据集
    save_dataset(train_data, "GPU-QA/train.jsonl")
    save_dataset(val_data, "GPU-QA/validation.jsonl") 
    save_dataset(test_data, "GPU-QA/test.jsonl")
    
    print(f"\n📊 数据集统计:")
    print(f"   训练集: {len(train_data)} 条")
    print(f"   验证集: {len(val_data)} 条")
    print(f"   测试集: {len(test_data)} 条")
    print(f"   总计: {total} 条")

def load_from_csv(csv_file: str, question_col: str = "question", answer_col: str = "answer"):
    """
    从CSV文件加载问答数据
    
    Args:
        csv_file: CSV文件路径
        question_col: 问题列名
        answer_col: 答案列名
    """
    try:
        import pandas as pd
        
        df = pd.read_csv(csv_file)
        qa_pairs = []
        
        for _, row in df.iterrows():
            qa_pairs.append({
                "question": str(row[question_col]),
                "answer": str(row[answer_col])
            })
        
        return qa_pairs
    
    except ImportError:
        print("❌ 需要安装pandas: pip install pandas")
        return []
    except Exception as e:
        print(f"❌ 读取CSV文件失败: {e}")
        return []

def main():
    """主函数"""
    print("🚀 GPU-QA数据集创建工具")
    print("=" * 50)
    
    choice = input("""
请选择操作:
1. 创建示例数据集
2. 从CSV文件导入
3. 手动输入问答对
4. 退出

请输入选择 (1-4): """).strip()
    
    if choice == "1":
        print("\n📝 创建示例GPU数据集...")
        create_sample_gpu_dataset()
        
    elif choice == "2":
        csv_file = input("请输入CSV文件路径: ").strip()
        if os.path.exists(csv_file):
            question_col = input("问题列名 (默认: question): ").strip() or "question"
            answer_col = input("答案列名 (默认: answer): ").strip() or "answer"
            
            qa_pairs = load_from_csv(csv_file, question_col, answer_col)
            if qa_pairs:
                dataset = [create_gpu_qa_entry(qa["question"], qa["answer"]) for qa in qa_pairs]
                
                # 简单分割
                total = len(dataset)
                train_size = int(total * 0.7)
                val_size = int(total * 0.2)
                
                train_data = dataset[:train_size]
                val_data = dataset[train_size:train_size + val_size]
                test_data = dataset[train_size + val_size:]
                
                save_dataset(train_data, "GPU-QA/train.jsonl")
                save_dataset(val_data, "GPU-QA/validation.jsonl")
                save_dataset(test_data, "GPU-QA/test.jsonl")
                
                print(f"\n📊 从CSV导入完成:")
                print(f"   训练集: {len(train_data)} 条")
                print(f"   验证集: {len(val_data)} 条") 
                print(f"   测试集: {len(test_data)} 条")
        else:
            print("❌ 文件不存在")
            
    elif choice == "3":
        print("\n✏️  手动输入问答对 (输入空行结束)")
        qa_pairs = []
        
        while True:
            question = input("\n问题: ").strip()
            if not question:
                break
                
            answer = input("答案: ").strip()
            if not answer:
                break
                
            qa_pairs.append({"question": question, "answer": answer})
            print(f"✅ 已添加第 {len(qa_pairs)} 条问答")
        
        if qa_pairs:
            dataset = [create_gpu_qa_entry(qa["question"], qa["answer"]) for qa in qa_pairs]
            
            # 如果数据量少，全部放入训练集
            if len(dataset) < 10:
                save_dataset(dataset, "GPU-QA/train.jsonl")
                save_dataset([], "GPU-QA/validation.jsonl")
                save_dataset([], "GPU-QA/test.jsonl")
            else:
                # 正常分割
                total = len(dataset)
                train_size = int(total * 0.7)
                val_size = int(total * 0.2)
                
                train_data = dataset[:train_size]
                val_data = dataset[train_size:train_size + val_size]
                test_data = dataset[train_size + val_size:]
                
                save_dataset(train_data, "GPU-QA/train.jsonl")
                save_dataset(val_data, "GPU-QA/validation.jsonl")
                save_dataset(test_data, "GPU-QA/test.jsonl")
            
            print(f"\n📊 手动输入完成，共 {len(dataset)} 条问答")
        else:
            print("❌ 没有输入任何问答对")
            
    elif choice == "4":
        print("👋 再见!")
        return
    else:
        print("❌ 无效选择")
        return
    
    print("\n🎉 数据集创建完成!")
    print("💡 提示: 运行 'python test_dataset.py' 验证数据格式")

if __name__ == "__main__":
    main()