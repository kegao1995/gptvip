# import streamlit as st
# import streamlit_openai

# if "chat" not in st.session_state:
#     st.session_state.chat = streamlit_openai.Chat(api_key=st.secrets.openai_api_key)

# st.session_state.chat.run()


import streamlit as st
import openai
import streamlit_openai

if "chat" not in st.session_state:
    def handler(prompt):
        client = openai.OpenAI(api_key=st.secrets.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-search-preview",
            web_search_options={},
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    
    search_web = streamlit_openai.CustomFunction(
        name="search_web",
        description="Search the web using a query.",
        parameters={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Search query.",
                }
            },
            "required": ["prompt"]
        },
        handler=handler
    )

    st.session_state.chat = streamlit_openai.Chat(
        functions=[search_web],
        api_key=st.secrets.openai_api_key
    )

st.session_state.chat.run()