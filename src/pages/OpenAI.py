# 导入必要的库
import streamlit as st  # Streamlit web应用框架
import openai  # OpenAI官方Python客户端
import streamlit_openai  # Streamlit的OpenAI集成库

# 可用的OpenAI模型列表
AVAILABLE_MODELS = {
    "gpt-4o-latest": "GPT-4o 最新版本",
    "gpt-o4-mini": "GPT-o4 Mini",
}

# 在侧边栏添加模型选择器
st.sidebar.title("模型设置")
selected_model = st.sidebar.selectbox(
    "选择AI模型:",
    options=list(AVAILABLE_MODELS.keys()),
    format_func=lambda x: AVAILABLE_MODELS[x],
    index=4  # 默认选择gpt-4o-search-preview
)

# 显示选中模型的信息
st.sidebar.info(f"当前模型: {AVAILABLE_MODELS[selected_model]}")

# 检查会话状态中是否已存在聊天实例，如果不存在则创建新的
if "chat" not in st.session_state:
    # 定义网络搜索处理函数
    def handler(prompt):
        """
        处理网络搜索请求的函数
        
        Args:
            prompt (str): 搜索查询字符串
            
        Returns:
            str: 搜索结果内容
        """
        # 创建OpenAI客户端实例
        client = openai.OpenAI(api_key=st.secrets.openai_api_key)
        # 调用选定的模型进行网络搜索（仅支持搜索的模型才添加web_search_options）
        if "search" in selected_model:
            response = client.chat.completions.create(
                model=selected_model,  # 使用用户选择的模型
                web_search_options={},  # 网络搜索选项配置
                messages=[{"role": "user", "content": prompt}],  # 用户消息
            )
        else:
            response = client.chat.completions.create(
                model=selected_model,  # 使用用户选择的模型
                messages=[{"role": "user", "content": prompt}],  # 用户消息
            )
        # 返回AI生成的回复内容
        return response.choices[0].message.content
    
    # 创建自定义网络搜索函数配置
    search_web = streamlit_openai.CustomFunction(
        name="search_web",  # 函数名称
        description="Search the web using a query.",  # 函数描述
        parameters={  # 函数参数定义
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Search query.",  # 搜索查询参数说明
                }
            },
            "required": ["prompt"]  # 必需参数
        },
        handler=handler  # 绑定处理函数
    )

    # 创建聊天实例，集成自定义搜索功能
    st.session_state.chat = streamlit_openai.Chat(
        functions=[search_web],  # 添加自定义函数
        api_key=st.secrets.openai_api_key  # 使用存储在secrets中的API密钥
    )

# 运行聊天界面
st.session_state.chat.run()