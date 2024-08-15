import streamlit as st
from backend import generate_content_azure
import pprint
from prompt import full_prompt

# Backend function to generate content based on inputs
def generate_content(user_groups=[], gender="", user_traits="", additional_description="", generate_number=""):
    # Simulate content generation logic
    content = []
    
    # Simple logic to generate content based on user inputs
    for i in range(generate_number):
        content_item = f"Generated Content {i+1}: "
        content_item += f"人群圈层 - {', '.join(user_groups)}; "
        content_item += f"性别 - {gender}; "
        
        if user_traits:
            content_item += f"特征 - {user_traits}; "
        
        if additional_description:
            content_item += f"描述 - {additional_description}; "
        
        content.append(content_item)
    
    return content

# Set page configuration
st.set_page_config(layout="wide")

# Title of the app
st.title("卖点生成")

# Left column - Input section
with st.sidebar:
    st.header("信息输入区")

    # Product Information input
    st.subheader("产品信息")
    
    st.text_input("产品名称", "产品名称")
    
    st.text_input('竞品信息', '竞品信息')
    
    st.text_area("产品描述", "产品描述", max_chars=1280)


    # Target User Characteristics
    st.subheader("目标用户特征")
    
    target_user_type = st.radio("目标用户", ("不限", "自定义用户", "CDP用户"))
    
    if target_user_type == "自定义用户":
        st.checkbox("目标用户")
        
        # User Groups
        st.write("人群圈层")
        user_groups = st.multiselect(
            "选择人群圈层", 
            ["游戏圈层", "科技圈层", "家装圈层", "体育圈层"],
            ["体育圈层"]
        )
        
        # Gender Selection
        st.write("性别")
        gender = st.radio("", ["不限", "男", "女"])
        
        # User Traits
        st.write("人群特征")
        user_traits = st.text_input("请选择标签", "")
    elif target_user_type == "不限":
        user_groups = []
        gender = "不限"
        user_traits = ""
    
    # Generate Number
    st.write("生成数量")
    generate_number = st.slider("生成数量", 1, 6, 3)
    
    # Additional Description
    st.write("附加描述")
    additional_description = st.text_area("请输入", "", max_chars=500)
    
    
    # Button for generating content
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: blue;
            color: white;
        }
        .stButton>button:active {
            color: yellow;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    content_placeholder = st.empty()

    with col1:
        if st.button("生成内容"):
            with content_placeholder.spinner('内容生成中...'):
                # generated_content = generate_content(user_groups, gender, user_traits, additional_description, generate_number)
                generated_content = generate_content_azure(full_prompt)
                pprint.pprint(generated_content)
                st.session_state['generated_content'] = generated_content

    with col2:
        if st.button("优化内容"):
            st.session_state['generated_content'] = ""

    with col3:
        if st.button("全部清空"):
            st.session_state['generated_content'] = ""

# Right column - Output section
st.subheader("内容生成区")

# Display Generated Content
st.write("生成内容结果")

# Retrieve generated content from session state
if 'generated_content' in st.session_state:
    content_placeholder.write(st.session_state['generated_content'])

# retry_button = st.button("再试一次")

if st.button("再试一次"):
    if st.button("再试一次"):
        with st.spinner('内容生成中...'):
            st.session_state['generated_content'] = generate_content(user_groups, gender, user_traits, additional_description, generate_number)

