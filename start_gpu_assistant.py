#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU知识助手快速启动脚本
提供简单的命令行界面来管理GPU助手项目
"""

import os
import subprocess
import sys

def print_banner():
    """打印项目横幅"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 GPU知识助手项目                        ║
║                  GPU Knowledge Assistant                     ║
╠══════════════════════════════════════════════════════════════╣
║  基于Qwen3大语言模型微调的专业GPU知识问答助手              ║
║  支持GPU硬件、软件、应用等各方面的专业咨询                   ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python版本过低，需要Python 3.8+")
        return False
    else:
        print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查虚拟环境
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 虚拟环境已激活")
    else:
        print("⚠️  建议使用虚拟环境")
    
    # 检查关键文件
    required_files = [
        "gpu_llm_finetune.py",
        "requirements.txt",
        "create_gpu_dataset.py",
        "test_dataset.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ 缺少文件: {file}")
            return False
    
    # 检查GPU-QA目录
    if os.path.exists("GPU-QA"):
        print("✅ GPU-QA数据集目录存在")
        
        # 检查数据文件
        data_files = ["train.jsonl", "validation.jsonl", "test.jsonl"]
        for file in data_files:
            filepath = os.path.join("GPU-QA", file)
            if os.path.exists(filepath):
                # 检查文件大小
                size = os.path.getsize(filepath)
                if size > 0:
                    print(f"✅ {file} ({size} bytes)")
                else:
                    print(f"⚠️  {file} 文件为空")
            else:
                print(f"❌ 缺少数据文件: {file}")
    else:
        print("⚠️  GPU-QA数据集目录不存在")
    
    return True

def install_dependencies():
    """安装依赖包"""
    print("\n📦 安装依赖包...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True,
                      encoding='utf-8', errors='replace')
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def create_dataset():
    """创建数据集"""
    print("\n📝 启动数据集创建工具...")
    try:
        subprocess.run([sys.executable, "create_gpu_dataset.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据集创建失败: {e}")
        return False

def validate_dataset():
    """验证数据集"""
    print("\n🔍 验证数据集格式...")
    try:
        # 在Windows上指定编码为UTF-8
        result = subprocess.run([sys.executable, "test_dataset.py"], 
                              check=True, capture_output=True, text=True, 
                              encoding='utf-8', errors='replace')
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据集验证失败: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False
    except UnicodeDecodeError as e:
        print(f"❌ 编码错误: {e}")
        print("💡 尝试直接运行验证...")
        # 如果还是有编码问题，直接调用函数而不是subprocess
        try:
            import test_dataset
            test_dataset.test_gpu_qa_dataset()
            return True
        except Exception as e2:
            print(f"❌ 直接调用也失败: {e2}")
            return False

def start_training():
    """开始训练"""
    print("\n🚀 启动模型训练...")
    
    # 选择模型类型
    print("\n请选择要训练的模型:")
    print("1. Qwen3-1.7B (推荐，平衡性能与效率)")
    print("2. Qwen3-0.6B (轻量级，快速推理)")
    print("3. 全部模型")
    
    choice = input("请输入选择 (1-3): ").strip()
    
    model_map = {
        "1": "qwen3-1.7b",
        "2": "qwen3-0.6b"
    }
    
    if choice in model_map:
        model_type = model_map[choice]
        output_dir = f"outputs/{model_type}-gpu-assistant"
        
        cmd = [
            sys.executable, "gpu_llm_finetune.py",
            "--model_type", model_type,
            "--dataset_path", "GPU-QA",
            "--output_dir", output_dir,
            "--do_train", "--do_eval"
        ]
        
        print(f"\n🔥 开始训练 {model_type} 模型...")
        print(f"输出目录: {output_dir}")
        print("=" * 60)
        
        try:
            subprocess.run(cmd, check=True)
            print(f"\n🎉 {model_type} 模型训练完成!")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ {model_type} 模型训练失败: {e}")
            
    elif choice == "3":
        # 运行批量训练脚本
        print("\n🔥 开始批量训练所有模型...")
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "run_gpu_finetune.sh"], check=True)
            else:  # Linux/Mac
                subprocess.run(["bash", "run_gpu_finetune.sh"], check=True)
            print("\n🎉 所有模型训练完成!")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ 批量训练失败: {e}")
    else:
        print("❌ 无效选择")

def main():
    """主函数"""
    print_banner()
    
    if not check_environment():
        print("\n❌ 环境检查失败，请解决上述问题后重试")
        return
    
    while True:
        print("\n" + "=" * 60)
        print("🎯 请选择操作:")
        print("1. 安装依赖包")
        print("2. 创建/准备数据集")
        print("3. 验证数据集格式")
        print("4. 开始训练模型")
        print("5. 查看项目状态")
        print("6. 退出")
        
        choice = input("\n请输入选择 (1-6): ").strip()
        
        if choice == "1":
            install_dependencies()
            
        elif choice == "2":
            create_dataset()
            
        elif choice == "3":
            validate_dataset()
            
        elif choice == "4":
            if not os.path.exists("GPU-QA/train.jsonl") or os.path.getsize("GPU-QA/train.jsonl") == 0:
                print("⚠️  训练数据不存在或为空，请先创建数据集")
                continue
            start_training()
            
        elif choice == "5":
            check_environment()
            
        elif choice == "6":
            print("\n👋 感谢使用GPU知识助手项目！")
            break
            
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()