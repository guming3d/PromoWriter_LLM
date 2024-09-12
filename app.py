import streamlit as st
import json
from backend import generate_content_azure, env_valid, env_error
import pprint
from prompt import generate_system_prompt_selling_point, system_prompt_2, system_prompt_short_generation, system_prompt_long_generation, system_prompt_review_selling_points, system_prompt_promotion_generation, system_prompt_long_title_generation, system_prompt_display_framework_generation
import datetime
import streamlit.components.v1 as components
from streamlit_modal import Modal

with open("images/Microsoft_Azure.svg", "r") as f:
    azure_logo = f.read()


st.set_page_config(
    page_title="AI Marketing Copywriting Generation Platform",
    page_icon="images/azure.png",
    layout="wide",  # You can also choose 'wide'
)


# Check if .env file is valid
if not env_valid:
    st.error(env_error)
else:
    # Left column - Input section
    with st.sidebar:
        st.markdown("<h1 style='color: #00008B;'>AI Marketing Copy Generation</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 5])
        with col1:
            st.logo(azure_logo)
        st.header("Information Input Area")

        # Product Information input
        st.subheader("Product Information")
        
        product_name = st.text_input("Product Name", "Hisense Little Harry Washing Machine")
        
        competitor_info = st.text_input('Competitor Information', 'Competitor Information')


        product_description_default = """
Product Overview

Brand: Hisense

Model: Hisense Little Harry Washing Machine

Core Category Keywords/Washing Machine Marketing Keywords: Little Harry = Mini Washing Machine for Babies and Mothers = Lint-Removing Washing Machine = Healthier with Active Water Washing

Main Product Selling Points Guidelines:  
0. Platform Template: Product Scene Image + Main Selling Point (Baby Clothes Separate Washing, Mini Pet-Friendly, Understands You Better) + Benefits;  
2. Lint Removal;  
3. Active Water Washing;  
4. Drum without Holes

Core Technical Points/Specifications:  
0. Lint removal efficiency 7*%, patent number*  
   One Scrape: 5A Residue Brush, scrapes off lint  
   Two Filters: 3D Waterfall Wash, frequently flushes lint toward the filter  
   Three Collections: 150-mesh filter, intercepts lint more effectively
1. Active Water Chamber - Constant active water enhances the enzyme activity of laundry detergent, paired with billions of fine bubbles, improves cleaning power by 22%, Cleaning Ratio: 0.8
2. 95°C high-temperature boil wash, effectively removes bacteria residue from baby clothes, ensuring health and cleanliness, caring for the baby's healthy growth.
3. Adjustable in four levels: Normal temperature/30/45/60°C. Low temperature protects fabrics, high temperature sterilizes and removes mites. The 60°C mite removal wash eliminates deep fiber mites with a removal rate of up to 100%
4. Silver ions are slowly released upon contact with water, penetrating deep into fibers for long-lasting antibacterial effects. Suitable for all fabrics, no manual intervention needed, safe and residue-free, with a long lifespan, 99.99% antibacterial rate.
5. Sealed food-grade stainless steel drum without holes, preventing dirty tub washing at the source, thoroughly antibacterial and anti-mold.
6. Non-porous design reduces clothing wear by 12.61%
7. 95°C high-temperature self-cleaning drum, high-speed water flow scrubs the drum walls, ensuring cleanliness and preventing secondary pollution, protecting a healthy laundry space.
        
        """
        
        product_description = st.text_area("Product Description", product_description_default, max_chars=1280)

        # User Comments
        st.subheader("User Comments")
        use_comments = st.checkbox("Add User Comments")
        user_comments = ""
        if use_comments:
            comment_input_method = st.radio("Select Input Method", ("Manual Input", "Upload from File"))
            if comment_input_method == "Manual Input":
                user_comments = st.text_area("User Comments", "", max_chars=2048)
            else:
                uploaded_file = st.file_uploader("Upload User Comments JSON File", type="json")
                if uploaded_file is not None:
                    user_comments = json.load(uploaded_file)
                    user_comments = json.dumps(user_comments, ensure_ascii=False, indent=4)
        
        st.subheader("Target User Characteristics")
        
        target_user_type = st.radio("Target User", ("Unlimited", "Custom User"))
        
        if target_user_type == "Custom User":
            
            # User Groups
            st.write("User Groups")
            user_groups = st.multiselect(
                "Select User Groups", 
                ["Gaming Circle", "Tech Circle", "Home Improvement Circle", "Sports Circle","Exquisite Moms","Pet Owners","Age Group 18-24","Age Group 24-35","Age Group 35-45","Age Group 45-55","Age Group 55+"],
                ["Sports Circle"]
            )
            
            # Gender Selection
            st.write("Gender")
            gender = st.radio("", ["Unlimited", "Male", "Female"])
            
            # User Traits
            st.write("User Traits")
            user_traits = st.text_input("Select Tags", "")
        elif target_user_type == "Unlimited":
            user_groups = []
            gender = "Unlimited"
            user_traits = ""
        
        # Generate Number
        st.write("Generate Number")
        generate_number = st.slider("Generate Number", 1, 6, 3)
        
        # Usage Scenarios
        st.write("Usage Scenarios")
        default_usage_scenarios = """1. When a pet-owning family has a baby, hand washing baby clothes cannot remove pet hair, and pet hair on baby clothes and bedding is difficult to clean;
2. Separate washing of adult and children's clothes to avoid cross-infection;
3. Food residues on children's clothes, ordinary washing machines still leave stains after washing.
4. Bed linens and clothes mites can easily cause sensitivity in babies and family members.
5. Separate washing of intimate clothing to protect private health;
"""
        usage_scenarios = st.text_area("Enter Usage Scenarios", default_usage_scenarios, max_chars=1024)
        st.write("Additional Description")
        additional_description = st.text_area("Enter", "", max_chars=500)

        # Convert collected data to user input string
        user_comments_str = f"{user_comments}\n" if use_comments else ""
        user_input = (
            f"Product Name: {product_name}\n"
            f"Target User Groups: {', '.join(user_groups)}\n"
            f"Gender: {gender}\n"
            f"User Traits: {user_traits}\n"
            f"Product Description: {product_description}\n"
            f"User Comments: {user_comments_str}\n"
            f"Usage Scenarios: {usage_scenarios}\n"
            f"Additional Description: {additional_description}\n"
            f"Number of Selling Points to Generate: {generate_number}"
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
            import os
            if not os.path.exists("history.md"):
                with open("history.md", "w", encoding="utf-8") as f:
                    f.write("")
            with open("history.md", "r", encoding="utf-8") as f:
                existing_content = f.read()
            new_log = f"## {timestamp}  {action}\n\n**Output:**\n```json\n{json.dumps(output, ensure_ascii=False, indent=4)}\n```\n\n"
            with open("history.md", "w", encoding="utf-8") as f:
                f.write(new_log + existing_content)

        system_prompt = generate_system_prompt_selling_point(generate_number)
        with col1:
            if st.button("Generate Selling Points", key="generate_content"):
                if not product_name or not product_description.strip():
                    st.session_state['error'] = "The product name and product description cannot be empty. Please enter the product name and product description."
                else:
                    with st.spinner('Generating Selling Points...'):
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
                            generated_content = response_json.get("Selling Points") or response_json.get("Selling Points List", [response_json])
                            st.session_state['generated_content'] = generated_content
                            log_to_markdown("Generating Selling Points", generated_content)
                            st.session_state['error'] = None
                        except json.JSONDecodeError:
                            st.session_state['error'] = "The generated content is not a valid JSON format."
                            st.session_state['generated_content'] = selling_points

            if st.button("Optimize Order", key="optimize_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content']:
                    st.session_state['error'] = "Please click the 'Generate Selling Points' button to generate selling points first."
                else:
                    with st.spinner('Optimizing Selling Points...'):
                        selling_points = st.session_state['generated_content']
                        optimized_content = generate_content_azure(system_prompt_2, json.dumps(selling_points, ensure_ascii=False), temperature=0.7, top_p=0.9)
                        pprint.pprint(optimized_content)
                        try:
                            response_json = json.loads(optimized_content)
                            optimized_content = response_json.get("Selling Points") or response_json.get("Selling Points List", [response_json])
                            st.session_state['optimized_content'] = optimized_content
                            st.session_state['optimized_reason'] = response_json.get("Optimization Reason", "Not provided")
                            log_to_markdown("Optimizing Order", {"optimized_content": optimized_content, "optimized_reason": st.session_state['optimized_reason']})
                            st.session_state['optimized_reason'] = response_json.get("Optimization Reason", "Not provided")
                            st.session_state['error'] = None
                        except json.JSONDecodeError:
                            st.session_state['error'] = "The optimized content is not a valid JSON format."
                            st.session_state['optimized_content'] = optimized_content

            if st.button("Review Selling Points", key="review_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content']:
                    st.session_state['error'] = "Please click the 'Generate Selling Points' button to generate selling points first."
                else:
                    with st.spinner('Selling Points Review...'):
                        selling_points = st.session_state['generated_content']
                        content_review_result = generate_content_azure(system_prompt_review_selling_points, json.dumps(selling_points, ensure_ascii=False), temperature=0.7, top_p=0.9, max_tokens=1600)
                        pprint.pprint(content_review_result)
                        try:
                            response_json = json.loads(content_review_result)
                            review_result = response_json.get("Review Result", [response_json])
                            st.session_state['review_result'] = review_result
                            log_to_markdown("Selling Points Review", review_result)
                            st.session_state['error'] = None
                        except json.JSONDecodeError:
                            st.session_state['error'] = "The reviewed content is not a valid JSON format."
                            st.session_state['review_result'] = content_review_result


        with col2:
            if st.button("Generate Short Copy", key="generate_short_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content']:
                    st.session_state['error'] = "Please click the 'Generate Selling Points' button to generate selling points first."
                else:
                    with st.spinner('Generating Short Copy...'):
                        selling_points = st.session_state['generated_content']
                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_short_generation)
                        print(selling_points)
                        print('--------------->>INPUT END<<--------------------\n')

                        short_content = generate_content_azure(system_prompt_short_generation, "Selling Points Information:" + str(selling_points))
                        print('--------------->>OUTPUT START<<--------------------')
                        print(short_content)
                        print('--------------->>OUTPUT END<<--------------------\n')

                        try:
                            response_json = json.loads(short_content)
                            short_content = response_json.get("Short Copy", [response_json])
                            st.session_state['short_content'] = short_content
                            log_to_markdown("Generated Short Copy", short_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "The generated short copy is not a valid JSON format."
                            st.session_state['short_content'] = short_content

            if st.button("Generate Long Copy", key="generate_long_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content'] or 'short_content' not in st.session_state or not st.session_state['short_content']:
                    st.session_state['error'] = "Please click the 'Generate Selling Points' and 'Generate Short Copy' buttons to generate selling points and short copy. Generating long copy depends on selling points and short copy."
                else:
                    with st.spinner('Generating Long Copy...'):
                        selling_points = st.session_state['generated_content']
                        short_content = st.session_state['short_content']

                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_long_generation)
                        print(short_content)
                        print('--------------->>INPUT END<<--------------------\n')


                        long_content = generate_content_azure(system_prompt_long_generation, "Selling Points Information:" + str(selling_points) + "\nShort Copy Information:" + str(short_content), max_tokens=2048)
                        print('--------------->>OUTPUT START<<--------------------')
                        print(long_content)
                        print('--------------->>OUTPUT END<<--------------------\n')


                        try:
                            response_json = json.loads(long_content)
                            long_content = response_json.get("Long Copy", [response_json])
                            st.session_state['long_content'] = long_content
                            log_to_markdown("Generated Long Copy", long_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "The generated long copy is not a valid JSON format."
                            st.session_state['long_content'] = long_content

            if st.button("Generate Promotion Copy", key="generate_promotion_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content'] or 'short_content' not in st.session_state or not st.session_state['short_content']:
                        st.session_state['error'] = "Please click the 'Generate Selling Points' and 'Generate Short Copy' buttons to generate selling points and short copy. Generating promotion copy depends on selling points and short copy."
                else:
                    with st.spinner('Generating Promotion Copy...'):
                        selling_points = st.session_state['generated_content']
                        short_content = st.session_state['short_content']

                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_promotion_generation)
                        print(short_content)
                        print('--------------->>INPUT END<<--------------------\n')


                        promotion_content = generate_content_azure(system_prompt_promotion_generation, "Selling Points Information:" + str(selling_points) + "\nShort Copy Information:" + str(short_content), max_tokens=4096)
                        print('--------------->>OUTPUT START<<--------------------')
                        print(promotion_content)
                        print('--------------->>OUTPUT END<<--------------------\n')

                        try:
                            response_json = json.loads(promotion_content)
                            promotion_content = response_json.get("Promotion Copy", response_json)
                            st.session_state['promotion_content'] = promotion_content
                            log_to_markdown("Generated Promotion Copy", promotion_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "The generated promotion copy is not a valid JSON format."
                            st.session_state['promotion_content'] = promotion_content

            if st.button("Generate Long Title", key="generate_long_title_content"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content'] or 'short_content' not in st.session_state or not st.session_state['short_content']:
                        st.session_state['error'] = "Please click the 'Generate Selling Points' and 'Generate Short Copy' buttons to generate selling points and short copy. Generating long title depends on selling points and short copy."
                else:
                    with st.spinner('Generating Long Title...'):
                        selling_points = st.session_state['generated_content']
                        short_content = st.session_state['short_content']

                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_long_title_generation)
                        print(short_content)
                        print('--------------->>INPUT END<<--------------------\n')


                        long_title_content = generate_content_azure(system_prompt_long_title_generation, "Selling Points Information:" + str(selling_points) + "\nShort Copy Information:" + str(short_content), max_tokens=600)
                        print('--------------->>OUTPUT START<<--------------------')
                        print(long_title_content)
                        print('--------------->>OUTPUT END<<--------------------\n')

                        try:
                            response_json = json.loads(long_title_content)
                            long_title_content = response_json.get("Long Title", [response_json])
                            st.session_state['long_title_content'] = long_title_content
                            log_to_markdown("Generated Long Title", long_title_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "The generated long title is not a valid JSON format."
                            st.session_state['long_title_content'] = long_title_content
                            
            if st.button("Generate Product Detail Page", key="generate_product_detail_page"):
                if 'generated_content' not in st.session_state or not st.session_state['generated_content'] or 'short_content' not in st.session_state or not st.session_state['short_content']:
                    st.session_state['error'] = "Please click the 'Generate Selling Points' and 'Generate Short Copy' buttons to generate selling points and short copy. Generating product detail page depends on selling points and short copy."
                else:
                    with st.spinner('Generating Product Detail Page...'):
                        selling_points = st.session_state['generated_content']
                        short_content = st.session_state['short_content']

                        print('--------------->>INPUT START<<--------------------')
                        print(system_prompt_display_framework_generation)
                        print("Selling Points Information:" + str(selling_points))
                        print("Short Copy Information:" + str(short_content))
                        print('--------------->>INPUT END<<--------------------\n')

                        product_detail_page_content = generate_content_azure(system_prompt_display_framework_generation, "Selling Points Information:" + str(selling_points) + "\nShort Copy Information:" + str(short_content), max_tokens=2048)
                        print('--------------->>OUTPUT START<<--------------------')
                        print(product_detail_page_content)
                        print('--------------->>OUTPUT END<<--------------------\n')

                        try:
                            response_json = json.loads(product_detail_page_content)
                            product_detail_page_content = response_json.get("Product Detail Page", [response_json])
                            st.session_state['product_detail_page_content'] = product_detail_page_content
                            log_to_markdown("Generated Product Detail Page", product_detail_page_content)
                        except json.JSONDecodeError:
                            st.session_state['error'] = "The generated product detail page is not a valid JSON format."
                            print(f"Failed to parse response_json, input:{product_detail_page_content}")
                            st.session_state['product_detail_page_content'] = product_detail_page_content
       

        with col3:
            if st.button("Clear All", key="clear_all"):
                keys_to_clear = ['generated_content', 'optimized_content', 'short_content', 'long_content', 'error', 'optimized_reason', 'review_result', 'long_title_content', 'product_detail_page_content', 'promotion_content']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
            if st.button("View History", key="view_history"):
                st.session_state['show_history_modal'] = True

    if 'show_history_modal' in st.session_state and st.session_state['show_history_modal']:
        modal = Modal(key="history_modal", title="History Records")
        with modal.container():
            with open("history.md", "r", encoding="utf-8") as f:
                history_content = f.read()
            st.markdown(
                f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
                    <pre style="white-space: pre-wrap; word-wrap: break-word;">{history_content}</pre>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.session_state['show_history_modal'] = False

    st.title("Content Generation Area")
    st.logo(azure_logo)
    
    # Retrieve generated content from session state
    if 'error' in st.session_state and st.session_state['error']:
        st.error(st.session_state['error'])

    if 'generated_content' in st.session_state:
        selling_points = st.session_state['generated_content']
        if 'generated_content' in st.session_state:
            st.subheader("Selling Points:")
            with st.container(border=True):
                st.write(st.session_state['generated_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("View System Prompt and User Input"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>System Prompt:</h3>
                            <pre>{}</pre>
                            <h3>User Input:</h3>
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
            st.subheader("Short Copy:")
            short_content = st.session_state['short_content']
            with st.container(border=True):
                st.write(st.session_state['short_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("View System Prompt and User Input"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>System Prompt:</h3>
                            <pre>{}</pre>
                            <h3>User Input:</h3>
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
            st.subheader("Long Copy:")
            with st.container(border=True):
                st.write(st.session_state['long_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("View System Prompt and User Input"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>System Prompt:</h3>
                            <pre>{}</pre>
                            <h3>User Input:</h3>
                            <pre>Selling Points Information:{}\nShort Copy Information:{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_long_generation, json.dumps(selling_points, ensure_ascii=False), short_content),
                        unsafe_allow_html=True
                    )

        if 'promotion_content' in st.session_state:
            st.write("---")
            st.subheader("Promotion Copy:")
            with st.container(border=True):
                st.write(st.session_state['promotion_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("View System Prompt and User Input"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>System Prompt:</h3>
                            <pre>{}</pre>
                            <h3>User Input:</h3>
                            <pre>Selling Points Information:{}\nShort Copy Information:{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_promotion_generation, json.dumps(selling_points, ensure_ascii=False), short_content),
                        unsafe_allow_html=True
                    )

        if 'optimized_content' in st.session_state:
            st.write("---")
            st.subheader("Selling Points Order Optimization:")
            with st.container(border=True):
                st.write("Original Selling Points:")
                st.write(selling_points)
                st.write("Optimized Selling Points:")
                st.write(st.session_state['optimized_content'])
                st.write("Optimization Reason:")
                st.write(st.session_state['optimized_reason'])
                with st.expander("View System Prompt and User Input"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>System Prompt:</h3>
                            <pre>{}</pre>
                            <h3>User Input:</h3>
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
            st.subheader("Selling Points Review:")
            with st.container(border=True):
                st.write("Original Selling Points:")
                st.write(selling_points)
                st.write("Review Results")
                st.write(st.session_state['review_result'])
                with st.expander("View System Prompt and User Input"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>System Prompt:</h3>
                            <pre>{}</pre>
                            <h3>User Input:</h3>
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
            st.subheader("Long Title:")
            with st.container(border=True):
                st.write(st.session_state['long_title_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("View System Prompt and User Input"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>System Prompt:</h3>
                            <pre>{}</pre>
                            <h3>User Input:</h3>
                            <pre>Selling Points Information:{}\nShort Copy Information:{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_long_title_generation, json.dumps(selling_points, ensure_ascii=False), short_content),
                        unsafe_allow_html=True
                    )
        
        if 'product_detail_page_content' in st.session_state:
            st.write("---")
            st.subheader("Product Detail Page Framework:")
            with st.container(border=True):
                st.write(st.session_state['product_detail_page_content'])
                # Add expandable container for system_prompt and user_input
                with st.expander("View System Prompt and User Input"):
                    st.markdown(
                        """
                        <div style="color: #5F9EA0;">
                            <h3>System Prompt:</h3>
                            <pre>{}</pre>
                            <h3>User Input:</h3>
                            <pre>Selling Points Information:{}\nShort Copy Information:{}</pre>
                        </div>
                        <div style="text-align: right;">
                            <img src="https://img.icons8.com/ios-filled/50/000000/expand-arrow.png" width="20" height="20"/>
                        </div>
                        """.format(system_prompt_display_framework_generation, json.dumps(selling_points, ensure_ascii=False), short_content),
                        unsafe_allow_html=True
                    )
