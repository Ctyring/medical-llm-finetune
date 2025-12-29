#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版ModelScope上传脚本
"""

from modelscope.hub.api import HubApi
from modelscope.hub.repository import Repository
import os
import tempfile
import shutil

def upload_model_to_modelscope():
    """上传模型到ModelScope"""
    
    # ========== 配置信息 - 请修改这里 ==========
    MODEL_NAME = "qwen-gpu-assistant-v2"  # 修改模型名称避免冲突
    USERNAME = "ctyring"  # 你的ModelScope用户名
    API_TOKEN = "ms-cbabe324-b8a7-49c4-ae96-23480a4ae219"  # 替换为你的API Token
    # ==========================================
    
    MODEL_ID = f"{USERNAME}/{MODEL_NAME}"
    LOCAL_MODEL_PATH = "qwen-output3"
    
    print("🚀 开始上传模型到ModelScope...")
    print(f"📦 模型ID: {MODEL_ID}")
    print(f"📁 本地路径: {LOCAL_MODEL_PATH}")
    
    # 检查配置
    if API_TOKEN == "your_token_here":
        print("\n❌ 请先配置API Token!")
        print("在脚本中填入API_TOKEN")
        return
    
    try:
        # 初始化API
        print("\n🔐 使用Token登录...")
        api = HubApi()
        api.login(API_TOKEN)
        print("✅ 登录成功")
        
        # 创建模型仓库
        print("\n📝 创建模型仓库...")
        try:
            api.create_model(
                model_id=MODEL_ID,
                visibility=1,  # 1=公开, 0=私有
                license='Apache License 2.0',
                chinese_name='Qwen GPU知识助手 v2',
                original_model_id='Qwen/Qwen1.5-7B'
            )
            print("✅ 模型仓库创建成功")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("✅ 模型仓库已存在，继续上传")
            else:
                print(f"⚠️  创建仓库警告: {e}")
        
        # 使用Repository方式上传
        print("\n📤 准备上传文件...")
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"📁 临时目录: {temp_dir}")
            
            # 初始化Repository
            repo = Repository(
                model_dir=temp_dir,
                clone_from=MODEL_ID,
                token=API_TOKEN
            )
            
            # 复制需要的文件
            files_to_copy = [
                "adapter_config.json",
                "adapter_model.safetensors", 
                "README.md",
                "tokenizer_config.json",
                "tokenizer.json",
                "special_tokens_map.json",
                "training_params.json",
                "evaluation_results.json"
            ]
            
            copied_count = 0
            for file_name in files_to_copy:
                src_path = os.path.join(LOCAL_MODEL_PATH, file_name)
                dst_path = os.path.join(temp_dir, file_name)
                
                if os.path.exists(src_path):
                    shutil.copy2(src_path, dst_path)
                    print(f"  📄 复制 {file_name} ✅")
                    copied_count += 1
                else:
                    print(f"  ⚠️  跳过不存在的文件: {file_name}")
            
            print(f"\n📤 推送 {copied_count} 个文件到ModelScope...")
            
            # 推送到远程仓库
            repo.push(commit_message="Upload Qwen GPU Assistant LoRA adapter v2")
            
            print("\n🎉 上传完成!")
            print(f"🔗 访问地址: https://modelscope.cn/models/{MODEL_ID}")
        
    except Exception as e:
        print(f"\n❌ 上传失败: {e}")
        print("\n💡 建议使用Git方式上传:")
        print_git_instructions(MODEL_ID, API_TOKEN)

def print_git_instructions(model_id, token):
    """打印Git上传指令"""
    print(f"""
📋 Git上传步骤:

1. 先在ModelScope网站创建模型:
   https://modelscope.cn/models/create
   模型名称: {model_id.split('/')[-1]}

2. 然后执行以下命令:
   cd qwen-output
   git init
   git lfs install
   git lfs track "*.safetensors"
   git add .
   git commit -m "Upload Qwen GPU Assistant"
   git remote add origin https://oauth2:{token}@www.modelscope.cn/{model_id}.git
   git push -u origin master
""")

if __name__ == "__main__":
    upload_model_to_modelscope()