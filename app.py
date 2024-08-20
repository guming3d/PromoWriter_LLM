import streamlit as st
import json
from backend import generate_content_azure, env_valid, env_error
import pprint
from prompt import system_prompt_1, system_prompt_2

with open("images/Microsoft_Azure.svg", "r") as f:
    azure_logo = f.read()

# Backend function to generate content based on inputs
def generate_content(user_groups=[], gender="", user_traits="", additional_description="", generate_number=1):
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

st.set_page_config(
    page_title="海信国内营销AI文案生成平台",
    layout="wide",  # You can also choose 'wide'
)


# Check if .env file is valid
if not env_valid:
    st.error(env_error)
else:
    # Left column - Input section
    with st.sidebar:
        st.markdown("<h1 style='color: #00008B;'>营销文案生成</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 5])
        with col1:
            st.logo(azure_logo)
        st.header("信息输入区")

        # Product Information input
        st.subheader("产品信息")
        
        product_name = st.text_input("产品名称", "海信小哈利洗衣机")
        
        competitor_info = st.text_input('竞品信息', '竞品信息')

        product_description_default_backup = """
产品概述
品牌: 海信 (Hisense)
型号: KFR-35GW/A820-X1 (A型号)
主要特点和技术
舒适性和制冷能力:

制冷性能: 这款空调设计用于提供高效制冷，可能在极端条件下也能表现出色。
智能控制: 具备智能控制功能，可以通过应用程序进行远程操作，并支持语音控制集成。
精准温控: 设计用于精确的温度调节，以实现最佳的舒适度。
节能效能:

节能特点: 该空调被宣传为高度节能，能够有效降低电费支出。
健康相关功能:

空气质量提升: 产品可能包括旨在改善室内空气质量的技术，例如过滤或净化功能。
环保: 强调环保操作，可能涉及其制冷剂或整体能耗。
设计与构造:

时尚设计: 空调具有现代感和时尚的设计，适用于多种室内装饰风格。
耐用性: 可能采用确保长久使用的材料或技术，能够在恶劣环境中也能稳定运行。
用户体验:

静音运行: 注重低噪音设计，适合卧室或其他安静空间使用。
便利性: 宣传易于安装和用户友好的界面，可能包括便捷的维护功能。
其他信息
推广内容: 页面可能还包括客户评价、产品视频或互动元素，以展示空调的各项功能。
技术规格: 图片的最后部分包含一个技术规格表，列出了如功耗、制冷能力、尺寸等详细规格。
整个页面的设计目的是全面介绍这款空调，强调其先进功能、用户利益，以及适用于各种生活环境的特点。
        """
        product_description_default = """
产品概述
品牌: 海信 (Hisense)
型号: 海信小哈利洗衣机
核心品类联想词/洗衣机营销关键词：小哈利=母婴迷你洗衣机=能除毛屑的洗衣机=活水洗更健康
        
        """
        
        product_description = st.text_area("产品描述", product_description_default, max_chars=1280)

        # Target User Characteristics
        st.subheader("目标用户特征")
        
        target_user_type = st.radio("目标用户", ("不限", "自定义用户"))
        
        if target_user_type == "自定义用户":
            
            # User Groups
            st.write("人群圈层")
            user_groups = st.multiselect(
                "选择人群圈层", 
                ["游戏圈层", "科技圈层", "家装圈层", "体育圈层","精致妈妈","萌宠人群","年龄段18-24岁","年龄段24-35岁","年龄段35-45岁","年龄段45-55岁","年龄段55岁以上"],
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
        
        # Usage Scenarios
        st.write("使用场景")
        usage_scenarios = st.text_area("请输入使用场景", "", max_chars=500)
        st.write("附加描述")
        additional_description = st.text_area("请输入", "", max_chars=500)

        # Convert collected data to user input string
        user_input = (
            f"产品名称: {product_name}\n"
            f"目标人群: {', '.join(user_groups)}\n"
            f"性别: {gender}\n"
            f"目标人群特征: {user_traits}\n"
            f"产品描述: {product_description}\n"
            f"使用场景: {usage_scenarios}\n"
            f"附加描述和要求: {additional_description}\n"
            f"生成卖点的数量: {generate_number}"
        )
        
        # Button for generating content
        st.markdown(
            """
            <style>
            .stButton>button {
                background-color: #5F9EA0; /* Darker Blue */
                border: none;
                color: white;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 12px;
            }
            .stButton>button:active {
                color: black;
            }
            .stButton>button:hover {
                background-color: white;
                color: black;
                border: 2px solid #ADD8E6;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("生成卖点", key="generate_content"):
                if not product_name or not product_description.strip():
                    st.session_state['error'] = "产品名称和产品描述都不能为空，请输入产品名称和产品描述。"
                else:
                    with st.spinner('卖点生成中......'):
                        selling_points = generate_content_azure(system_prompt_1, user_input)
                        pprint.pprint(selling_points)
                        response_json = json.loads(selling_points)
                        st.session_state['generated_content'] = response_json.get("卖点列表", [response_json])
                        st.session_state['error'] = None

        with col2:
            if st.button("优化卖点", key="optimize_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content']:
                    st.session_state['error'] = "请先点击“生成卖点”按钮生成卖点。"
                else:
                    with st.spinner('卖点优化中......'):
                        selling_points = st.session_state['generated_content']
                        optimized_content = generate_content_azure(system_prompt_2, json.dumps(selling_points, ensure_ascii=False))
                        pprint.pprint(optimized_content)
                        response_json = json.loads(optimized_content)
                        st.session_state['optimized_content'] = response_json.get("卖点列表", [response_json])
                        st.session_state['error'] = None

        with col3:
            if st.button("全部清空", key="clear_all"):
                if 'generated_content' in st.session_state:
                    del st.session_state['generated_content']
                if 'optimized_content' in st.session_state:
                    del st.session_state['optimized_content']
                if 'error' in st.session_state:
                    del st.session_state['error']

    # Right column - Output section
    # adding separator
    st.title("内容生成区")
    st.logo(azure_logo)
    st.write("---")

    # Retrieve generated content from session state
    if 'error' in st.session_state and st.session_state['error']:
        st.error(st.session_state['error'])

    elif 'generated_content' in st.session_state and not 'optimized_content' in st.session_state:
        st.table(st.session_state['generated_content'])

    elif 'optimized_content' in st.session_state:
        st.write("原始的卖点：")
        st.table(st.session_state['generated_content'])
        st.write("---")
        st.write("优化后的卖点：")
        st.table(st.session_state['optimized_content'])

    if st.button("再试一次", key="retry"):
        with st.spinner('内容生成中...'):
            st.session_state['generated_content'] = ""
            selling_points = generate_content_azure(system_prompt_1, user_input)
            pprint.pprint(selling_points)
            response_json = json.loads(selling_points)
            st.session_state['generated_content'] = json.loads(selling_points).get("卖点列表", [response_json])
            st.session_state['error'] = None
            st.table(st.session_state['generated_content'])
