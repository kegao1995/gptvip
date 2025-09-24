# 导入必要的库
import streamlit as st  # Streamlit web应用框架
import openai  # OpenAI官方Python客户端
import streamlit_openai  # Streamlit的OpenAI集成库

# 可用的OpenAI模型列表
AVAILABLE_MODELS = {
    "chatgpt-4o": "chatgpt-4o",
    "gpt-o3": "gpt-o3",
}

# 在侧边栏添加模型选择器
st.sidebar.title("模型设置")
selected_model = st.sidebar.selectbox(
    "选择AI模型:",
    options=list(AVAILABLE_MODELS.keys()),
    format_func=lambda x: AVAILABLE_MODELS[x],
    index=0  
)

# 显示选中模型的信息
st.sidebar.info(f"当前模型: {AVAILABLE_MODELS[selected_model]}")

# 检查会话状态中是否已存在聊天实例，如果不存在则创建新的
if "chat" not in st.session_state:

    # 创建聊天实例，集成自定义搜索功能
    st.session_state.chat = streamlit_openai.Chat(
        api_key=st.secrets.openai_api_key,  # 使用存储在secrets中的API密钥
        model=selected_model  # 设置默认使用的模型
    )

# 运行聊天界面
st.session_state.chat.run()