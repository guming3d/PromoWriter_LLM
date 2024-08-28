import streamlit as st
import json
from backend import generate_content_azure, env_valid, env_error
import pprint
from prompt import generate_system_prompt_selling_point, system_prompt_2, system_prompt_short_generation, system_prompt_long_generation, system_prompt_review_selling_points, system_prompt_promotion_generation, system_prompt_long_title_generation, system_prompt_display_framework_generation
import datetime

with open("images/Microsoft_Azure.svg", "r") as f:
    azure_logo = f.read()


st.set_page_config(
    page_title="海信国内营销AI文案生成平台",
    page_icon="images/azure.png",
    layout="wide",  # You can also choose 'wide'
)


# Check if .env file is valid
if not env_valid:
    st.error(env_error)
else:
    # Left column - Input section
    with st.sidebar:
        st.markdown("<h1 style='color: #00008B;'>海信营销文案生成</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 5])
        with col1:
            st.logo(azure_logo)
        st.header("信息输入区")

        # Product Information input
        st.subheader("产品信息")
        
        product_name = st.text_input("产品名称", "海信小哈利洗衣机")
        
        competitor_info = st.text_input('竞品信息', '竞品信息')

        product_description_default_backup = """产品概述
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
        product_description_default = """产品概述

品牌: 海信 (Hisense)

型号: 海信小哈利洗衣机

核心品类联想词/洗衣机营销关键词：小哈利=母婴迷你洗衣机=能除毛屑的洗衣机=活水洗更健康

产品主图卖点规则: 1、平台模板：产品场景图+主卖点（宝宝衣物分类洗，萌宠迷你更懂你）+权益；2、除毛屑；3、活水洗；4、无孔内筒

核心技术点/参数:
1.线屑去除率7*%，专利号* 一刮：5A残渣刷，刮除毛屑 二滤：3维瀑布洗，将毛屑高频次冲向滤网， 三收集：150目滤网，拦截毛屑更干净
2.活水舱-全时活水激发洗衣液的酶活性，配合亿万级细密泡沫，去污能力提升22% 洗净比：0.8
3.95℃高温煮洗，有效去除宝宝衣物上的细菌残留，健康又洁净，呵护宝宝茁壮成长.
4.常温/30/45/60℃四档可调。低温不伤衣，高温除菌螨。60℃除螨洗清除纤维深层螨虫，除螨率高达100%
5.银离子遇水缓释，深入纤维深处，长效抑菌, 不限制面料、无需手动、健康安全无残留、使用寿命长，除菌率99.99%。 
6.密闭式食品级不锈钢无孔内桶，源头拒绝赃桶洗衣，抗菌防霉更彻底
7.无孔设计，衣物磨损率降低12.61%
8.95℃高温桶自洁，高速水流冲刷桶壁，洁净防止二次污染，守护健康洗衣空间
        
        """
        
        product_description = st.text_area("产品描述", product_description_default, max_chars=1280)

        # User Comments
        st.subheader("用户评论")
        use_comments = st.checkbox("是否添加用户评论")
        user_comments = ""
        if use_comments:
            comment_input_method = st.radio("选择输入方式", ("手动输入", "从文件上传"))
            if comment_input_method == "手动输入":
                user_comments = st.text_area("用户评论", "", max_chars=2048)
            else:
                uploaded_file = st.file_uploader("上传用户评论 JSON 文件", type="json")
                if uploaded_file is not None:
                    user_comments = json.load(uploaded_file)
                    user_comments = json.dumps(user_comments, ensure_ascii=False, indent=4)
        
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
        default_usage_scenarios = """1. 当养宠家庭有了宝宝，宝宝衣物手洗无法去除毛屑，宝宝衣物和床上宠物毛难清理；
2. 大人孩子衣服分开洗，拒绝交叉感染；
3. 孩子衣服上沾染食物残渣，普通洗衣机洗完仍有污渍残留。
4. 床品和衣物螨虫容易引起宝宝和家人敏感。
5. 贴身衣物单独洗，呵护私密健康；
"""
        usage_scenarios = st.text_area("请输入使用场景", default_usage_scenarios, max_chars=1024)
        st.write("附加描述")
        additional_description = st.text_area("请输入", "", max_chars=500)

        # Convert collected data to user input string
        user_comments_str = f"{user_comments}\n" if use_comments else ""
        user_input = (
            f"产品名称: {product_name}\n"
            f"目标人群: {', '.join(user_groups)}\n"
            f"性别: {gender}\n"
            f"目标人群特征: {user_traits}\n"
            f"产品描述: {product_description}\n"
            f"用户评论: {user_comments_str}\n"
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

        def log_to_markdown(action, output):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("history.md", "a", encoding="utf-8") as f:
                f.write(f"## {timestamp}\n")
                f.write(f"**Action:** {action}\n")
                f.write(f"**Output:**\n```json\n{json.dumps(output, ensure_ascii=False, indent=4)}\n```\n\n")

        system_prompt = generate_system_prompt_selling_point(generate_number)
        with col1:
            if st.button("生成卖点", key="generate_content"):
                if not product_name or not product_description.strip():
                    st.session_state['error'] = "产品名称和产品描述都不能为空，请输入产品名称和产品描述。"
                else:
                    with st.spinner('卖点生成中......'):
                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt)
                        print(user_input)
                        print('--------------->>INPUT END<<--------------------\n')
                        selling_points = generate_content_azure(system_prompt, user_input, max_tokens=1200)
                        print('--------------->>OUTPUT START<<--------------------')
                        print(selling_points)
                        print('--------------->>OUTPUT END<<--------------------\n')
                        try:
                            response_json = json.loads(selling_points)
                            generated_content = response_json.get("卖点") or response_json.get("卖点列表", [response_json])
                            st.session_state['generated_content'] = generated_content
                            log_to_markdown("生成卖点", generated_content)
                            st.session_state['error'] = None
                        except json.JSONDecodeError:
                            st.session_state['error'] = "生成的内容不是有效的JSON格式。"
                            st.session_state['generated_content'] = selling_points

            if st.button("顺序优化", key="optimize_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content']:
                    st.session_state['error'] = "请先点击“生成卖点”按钮生成卖点"
                else:
                    with st.spinner('卖点优化中......'):
                        selling_points = st.session_state['generated_content']
                        optimized_content = generate_content_azure(system_prompt_2, json.dumps(selling_points, ensure_ascii=False), temperature=0.7, top_p=0.9)
                        pprint.pprint(optimized_content)
                        try:
                            response_json = json.loads(optimized_content)
                            optimized_content = response_json.get("卖点") or response_json.get("卖点列表", [response_json])
                            st.session_state['optimized_content'] = optimized_content
                            st.session_state['optimized_reason'] = response_json.get("优化理由", "未提供")
                            log_to_markdown("顺序优化", {"optimized_content": optimized_content, "optimized_reason": st.session_state['optimized_reason']})
                            st.session_state['optimized_reason'] = response_json.get("优化理由", "未提供")
                            st.session_state['error'] = None
                        except json.JSONDecodeError:
                            st.session_state['error'] = "优化的内容不是有效的JSON格式。"
                            st.session_state['optimized_content'] = optimized_content

            if st.button("卖点评审", key="review_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content']:
                    st.session_state['error'] = "请先点击“生成卖点”按钮生成卖点"
                else:
                    with st.spinner('卖点评审中......'):
                        selling_points = st.session_state['generated_content']
                        content_revew_result = generate_content_azure(system_prompt_review_selling_points, json.dumps(selling_points, ensure_ascii=False), temperature=0.7, top_p=0.9, max_tokens=1600)
                        pprint.pprint(content_revew_result)
                        try:
                            response_json = json.loads(content_revew_result)
                            review_result = response_json.get("评审结果", [response_json])
                            st.session_state['review_result'] = review_result
                            log_to_markdown("卖点评审", review_result)
                            st.session_state['error'] = None
                        except json.JSONDecodeError:
                            st.session_state['error'] = "评审的内容不是有效的JSON格式。"
                            st.session_state['review_result'] = content_revew_result


        with col2:
            if st.button("生成短文案", key="generate_short_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content']:
                    st.session_state['error'] = "请先点击“生成卖点”按钮生成卖点"
                else:
                    with st.spinner('短文案生成中......'):
                        selling_points = st.session_state['generated_content']
                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_short_generation)
                        print(selling_points)
                        print('--------------->>INPUT END<<--------------------\n')

                        short_content = generate_content_azure(system_prompt_short_generation, "卖点信息如下:" + str(selling_points))
                        print('--------------->>OUTPUT START<<--------------------')
                        print(short_content)
                        print('--------------->>OUTPUT END<<--------------------\n')

                        try:
                            response_json = json.loads(short_content)
                            short_content = response_json.get("短文案", [response_json])
                            st.session_state['short_content'] = short_content
                            log_to_markdown("生成短文案", short_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "生成的短文案不是有效的JSON格式。"
                            st.session_state['short_content'] = short_content

            if st.button("生成长文案", key="generate_long_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content'] or 'short_content' not in st.session_state or not st.session_state['short_content']:
                    st.session_state['error'] = "请先点击“生成卖点”和“生成短文案”按钮生成卖点和短文案。长文案生成依赖卖点和短文案"
                else:
                    with st.spinner('长文案生成中......'):
                        selling_points = st.session_state['generated_content']
                        short_content = st.session_state['short_content']

                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_long_generation)
                        print(short_content)
                        print('--------------->>INPUT END<<--------------------\n')


                        long_content = generate_content_azure(system_prompt_long_generation, "卖点信息如下:" + str(selling_points) + "\n短文案信息如下:" + str(short_content), max_tokens=800)
                        print('--------------->>OUTPUT START<<--------------------')
                        print(long_content)
                        print('--------------->>OUTPUT END<<--------------------\n')


                        try:
                            response_json = json.loads(long_content)
                            long_content = response_json.get("长文案", [response_json])
                            st.session_state['long_content'] = long_content
                            log_to_markdown("生成长文案", long_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "生成的长文案不是有效的JSON格式。"
                            st.session_state['long_content'] = long_content

            if st.button("生成推广文", key="generate_promotion_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content'] or 'short_content' not in st.session_state or not st.session_state['short_content']:
                        st.session_state['error'] = "请先点击“生成卖点”和“ 生成短文案”按钮生成卖点和短文案。推广文生成依赖卖点和短文案"
                else:
                    with st.spinner('推广文生成中......'):
                        selling_points = st.session_state['generated_content']
                        short_content = st.session_state['short_content']

                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_promotion_generation)
                        print(short_content)
                        print('--------------->>INPUT END<<--------------------\n')


                        promotion_content = generate_content_azure(system_prompt_promotion_generation, "卖点信息如下:" + str(selling_points) + "\n短文案信息如下:" + str(short_content), max_tokens=800)
                        print('--------------->>OUTPUT START<<--------------------')
                        print(promotion_content)
                        print('--------------->>OUTPUT END<<--------------------\n')

                        try:
                            response_json = json.loads(promotion_content)
                            promotion_content = response_json.get("推广文案", [response_json])
                            st.session_state['promotion_content'] = promotion_content
                            log_to_markdown("生成推广文", promotion_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "生成的推广文案不是有效的JSON格式。"
                            st.session_state['promotion_content'] = promotion_content
            if st.button("生成长标题", key="generate_long_title_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content'] or 'short_content' not in st.session_state or not st.session_state['short_content']:
                        st.session_state['error'] = "请先点击“生成卖点”和“ 生成短文案”按钮生成卖点和短文案。长标题生成依赖卖点和短文案"
                else:
                    with st.spinner('长标题生成中......'):
                        selling_points = st.session_state['generated_content']
                        short_content = st.session_state['short_content']

                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_long_title_generation)
                        print(short_content)
                        print('--------------->>INPUT END<<--------------------\n')


                        long_title_content = generate_content_azure(system_prompt_long_title_generation, "卖点信息如下:" + str(selling_points) + "\n短文案信息如下:" + str(short_content), max_tokens=600)
                        print('--------------->>OUTPUT START<<--------------------')
                        print(long_title_content)
                        print('--------------->>OUTPUT END<<--------------------\n')

                        try:
                            response_json = json.loads(long_title_content)
                            long_title_content = response_json.get("长标题", [response_json])
                            st.session_state['long_title_content'] = long_title_content
                            log_to_markdown("生成长标题", long_title_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "生成的长标题输出不是有效的JSON格式。"
                            st.session_state['long_title_content'] = long_title_content
                            
            if st.button("商详页框架", key="generate_product_detail_page"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content'] or 'short_content' not in st.session_state or not st.session_state['short_content']:
                    st.session_state['error'] = "请先点击“生成卖点”和“生成短文案”按钮生成卖点和短文案。商详页框架生成依赖卖点和短文案"
                else:
                    with st.spinner('商详页框架生成中......'):
                        selling_points = st.session_state['generated_content']
                        short_content = st.session_state['short_content']

                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_display_framework_generation)
                        print("卖点信息如下:" + str(selling_points))
                        print("短文案信息如下:" + str(short_content))
                        print('--------------->>INPUT END<<--------------------\n')

                        product_detail_page_content = generate_content_azure(system_prompt_display_framework_generation, "卖点信息如下:" + str(selling_points) + "\n短文案信息如下:" + str(short_content), max_tokens=2048)
                        print('--------------->>OUTPUT START<<--------------------')
                        print(product_detail_page_content)
                        print('--------------->>OUTPUT END<<--------------------\n')

                        try:
                            response_json = json.loads(product_detail_page_content)
                            product_detail_page_content = response_json.get("商详页框架", [response_json])
                            st.session_state['product_detail_page_content'] = product_detail_page_content
                            log_to_markdown("商详页框架", product_detail_page_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "生成的商详页框架输出不是有效的JSON格式。"
                            print(f"failed to parse response_json, input:{product_detail_page_content}")
                            st.session_state['product_detail_page_content'] = product_detail_page_content
       

        with col3:
            if st.button("全部清空", key="clear_all"):
                keys_to_clear = ['generated_content', 'optimized_content', 'short_content', 'long_content', 'error', 'optimized_reason', 'review_result', 'long_title_content', 'product_detail_page_content', 'promotion_content']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
    # adding separator
    st.title("内容生成区")
    st.logo(azure_logo)
    
    # Retrieve generated content from session state
    if 'error' in st.session_state and st.session_state['error']:
        st.error(st.session_state['error'])

    if 'generated_content' in st.session_state:
        selling_points = st.session_state['generated_content']
        if 'generated_content' in st.session_state:
            st.subheader("卖点：")
            with st.container(border=True):
                st.write(st.session_state['generated_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("查看系统提示和用户输入"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>系统提示:</h3>
                            <pre>{}</pre>
                            <h3>用户输入:</h3>
                            <pre>{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt, user_input),
                        unsafe_allow_html=True
                    )

        if 'short_content' in st.session_state:
            st.write("---")
            st.subheader("短文案：")
            short_content = st.session_state['short_content']
            with st.container(border=True):
                st.write(st.session_state['short_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("查看系统提示和用户输入"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>系统提示:</h3>
                            <pre>{}</pre>
                            <h3>用户输入:</h3>
                            <pre>{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_short_generation, json.dumps(selling_points, ensure_ascii=False)),
                        unsafe_allow_html=True
                    )

        if 'long_content' in st.session_state:
            st.write("---")
            st.subheader("长文案：")
            with st.container(border=True):
                st.write(st.session_state['long_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("查看系统提示和用户输入"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>系统提示:</h3>
                            <pre>{}</pre>
                            <h3>用户输入:</h3>
                            <pre>卖点信息如下:{}\n短文案信息如下:{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_long_generation, json.dumps(selling_points, ensure_ascii=False), short_content),
                        unsafe_allow_html=True
                    )

        if 'promotion_content' in st.session_state:
            st.write("---")
            st.subheader("推广文：")
            with st.container(border=True):
                st.write(st.session_state['promotion_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("查看系统提示和用户输入"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>系统提示:</h3>
                            <pre>{}</pre>
                            <h3>用户输入:</h3>
                            <pre>卖点信息如下:{}\n短文案信息如下:{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_promotion_generation, json.dumps(selling_points, ensure_ascii=False), short_content),
                        unsafe_allow_html=True
                    )

        if 'optimized_content' in st.session_state:
            st.write("---")
            st.subheader("卖点顺序优化：")
            with st.container(border=True):
                st.write("原始卖点：")
                st.write(selling_points)
                st.write("优化后的卖点：")
                st.write(st.session_state['optimized_content'])
                st.write("优化理由:")
                st.write(st.session_state['optimized_reason'])
                with st.expander("查看系统提示和用户输入"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>系统提示:</h3>
                            <pre>{}</pre>
                            <h3>用户输入:</h3>
                            <pre>{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_2, json.dumps(selling_points, ensure_ascii=False)),
                        unsafe_allow_html=True
                    )

        if 'review_result' in st.session_state:
            st.write("---")
            st.subheader("卖点评审：")
            with st.container(border=True):
                st.write("原始卖点：")
                st.write(selling_points)
                st.write("评审结果")
                st.write(st.session_state['review_result'])
                with st.expander("查看系统提示和用户输入"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>系统提示:</h3>
                            <pre>{}</pre>
                            <h3>用户输入:</h3>
                            <pre>{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_review_selling_points, json.dumps(selling_points, ensure_ascii=False)),
                        unsafe_allow_html=True
                    )
        if 'long_title_content' in st.session_state:
            st.write("---")
            st.subheader("长标题：")
            with st.container(border=True):
                st.write(st.session_state['long_title_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("查看系统提示和用户输入"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>系统提示:</h3>
                            <pre>{}</pre>
                            <h3>用户输入:</h3>
                            <pre>卖点信息如下:{}\n短文案信息如下:{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_long_title_generation, json.dumps(selling_points, ensure_ascii=False), short_content),
                        unsafe_allow_html=True
                    )
        
        if 'product_detail_page_content' in st.session_state:
            st.write("---")
            st.subheader("商详页框架：")
            with st.container(border=True):
                st.write(st.session_state['product_detail_page_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("查看系统提示和用户输入"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>系统提示:</h3>
                            <pre>{}</pre>
                            <h3>用户输入:</h3>
                            <pre>卖点信息如下:{}\n短文案信息如下:{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_display_framework_generation, json.dumps(selling_points, ensure_ascii=False), short_content),
                        unsafe_allow_html=True
                    )
