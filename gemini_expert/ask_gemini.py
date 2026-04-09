import os
import sys

# ================= 配置区域 =================
# 1. 填入你的 Gemini API Key
API_KEY = "你滴key"

# 2. 填入你的代理地址 (通常 Clash 是 7890, V2Ray 是 10808)
PROXY_URL = "http://127.0.0.1:10809" 

# 设置代理环境变量
if PROXY_URL:
    os.environ['HTTP_PROXY'] = PROXY_URL
    os.environ['HTTPS_PROXY'] = PROXY_URL
# ===========================================

try:
    from google import genai
except ImportError:
    print("❌ 缺少必要的库，请运行: pip install google-genai")
    sys.exit(1)

def call_gemini(user_query):
    try:
        # 初始化客户端
        client = genai.Client(api_key=API_KEY)
        
        # 根据你的截图，模型优先级排序如下：
        # 1. Gemini 2.5 Pro (最强专家)
        # 2. Gemini 3 Flash (最新速度模型)
        # 3. Gemini 2 Flash (稳定备选)
        model_list = [
            "gemini-2.5-pro", 
            "gemini-3-flash", 
            "gemini-2-flash", 
            "gemini-1.5-pro"
        ]
        
        response = None
        current_used_model = ""

        # 循环尝试，直到找到你账号下可用的最强模型
        for model_name in model_list:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=f"你现在是 OpenClaw 的高级顾问。请为以下问题提供专家级建议：\n\n{user_query}"
                )
                if response:
                    current_used_model = model_name
                    break
            except:
                continue
        
        if response and response.text:
            print(f"--- [专家模型: {current_used_model} 响应中] ---")
            print(response.text)
            print("-" * 40)
        else:
            print("⚠️ 无法获取模型响应。请检查 API Key 状态或网络连接。")

    except Exception as e:
        print(f"❌ 运行出错了：{e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 支持 OpenClaw 传递长字符串参数
        input_query = " ".join(sys.argv[1:])
        call_gemini(input_query)
    else:
        # 直接运行脚本时的测试
        call_gemini("你好，请确认你的模型版本并向我打个招呼。")