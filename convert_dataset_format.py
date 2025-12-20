#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据集格式转换工具
将messages格式的数据转换为简单的question-answer格式
"""

import json
import os
from typing import List, Dict, Any

def convert_messages_to_qa(input_file: str, output_file: str) -> int:
    """
    将messages格式转换为question-answer格式
    
    Args:
        input_file: 输入文件路径（messages格式）
        output_file: 输出文件路径（question-answer格式）
    
    Returns:
        转换的条目数量
    """
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return 0
    
    converted_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line_num, line in enumerate(infile, 1):
            try:
                data = json.loads(line.strip())
                
                # 检查是否是messages格式
                if "messages" in data:
                    messages = data["messages"]
                    question = ""
                    answer = ""
                    
                    # 提取问题和答案
                    for message in messages:
                        if message.get("role") == "user":
                            question = message.get("content", "")
                        elif message.get("role") == "assistant":
                            answer = message.get("content", "")
                    
                    if question and answer:
                        # 创建新格式
                        new_data = {
                            "question": question,
                            "answer": answer
                        }
                        outfile.write(json.dumps(new_data, ensure_ascii=False) + '\n')
                        converted_count += 1
                    else:
                        print(f"⚠️  第{line_num}行缺少问题或答案，跳过")
                
                # 如果已经是question-answer格式，直接复制
                elif "question" in data and "answer" in data:
                    outfile.write(line)
                    converted_count += 1
                
                else:
                    print(f"⚠️  第{line_num}行格式不识别，跳过")
                    
            except json.JSONDecodeError as e:
                print(f"❌ 第{line_num}行JSON解析错误: {e}")
            except Exception as e:
                print(f"❌ 第{line_num}行处理错误: {e}")
    
    return converted_count

def main():
    """主函数"""
    print("🔄 数据集格式转换工具")
    print("将messages格式转换为question-answer格式")
    print("=" * 50)
    
    # 定义文件映射
    file_mappings = [
        ("GPU-QA/train.jsonl", "GPU-QA/train_new.jsonl"),
        ("GPU-QA/validation.jsonl", "GPU-QA/validation_new.jsonl"),
        ("GPU-QA/test.jsonl", "GPU-QA/test_new.jsonl")
    ]
    
    total_converted = 0
    
    for input_file, output_file in file_mappings:
        if os.path.exists(input_file):
            print(f"\n📝 转换 {input_file} -> {output_file}")
            count = convert_messages_to_qa(input_file, output_file)
            print(f"✅ 转换完成，共 {count} 条记录")
            total_converted += count
        else:
            print(f"⚠️  文件不存在: {input_file}")
    
    if total_converted > 0:
        print(f"\n🎉 转换完成！总共转换了 {total_converted} 条记录")
        
        # 询问是否替换原文件
        choice = input("\n是否用新格式替换原文件？(y/N): ").strip().lower()
        
        if choice in ['y', 'yes']:
            for input_file, output_file in file_mappings:
                if os.path.exists(output_file):
                    # 备份原文件
                    backup_file = input_file + ".backup"
                    if os.path.exists(input_file):
                        os.rename(input_file, backup_file)
                        print(f"📦 备份原文件: {backup_file}")
                    
                    # 替换为新文件
                    os.rename(output_file, input_file)
                    print(f"✅ 替换文件: {input_file}")
            
            print("\n🎯 格式转换完成！原文件已备份为 .backup")
            print("💡 提示: 运行 'python test_dataset.py' 验证新格式")
        else:
            print("\n📁 新格式文件保存为 *_new.jsonl")
            print("💡 提示: 手动检查后可以替换原文件")
    else:
        print("\n❌ 没有转换任何记录")

if __name__ == "__main__":
    main()