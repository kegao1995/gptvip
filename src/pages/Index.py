import streamlit as st
# 设置页面宽度
st.set_page_config(layout="wide")
pages = {
    "Global": [
        st.Page("OpenAI.py", title="OpenAI"),
    ]
}
pg = st.navigation(pages)
pg.run()
