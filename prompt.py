# Define the prompts

# 1. 基于产品信息和目标人群生成卖点
system_prompt_1 = """
你是一名非常有天赋和资深的营销专家，海信是一家中国非常著名的家电企业，我需要你帮助我根据提供的产品信息，产品描述，用户反馈以及目标用户这些信息生成这个产品的独特的卖点，海信市场营销部门会根据您输出的卖点做市场推广和营销，卖点的好坏对产品的销量有非常巨大的影响力。
"""
user_input_1 = "产品: XYZ, 目标人群: 科技爱好者, 关键特性: 创新, 用户友好"
full_prompt_1 = f"{system_prompt_1}\n{user_input_1}"

# 2. 卖点优化及排序
system_prompt_2 = "优化并排序以下卖点。"
user_input_2 = "卖点: 1. 创新设计 2. 高性能 3. 用户友好"
full_prompt_2 = f"{system_prompt_2}\n{user_input_2}"

# 3. 基于产品信息和目标人群生成短文案
system_prompt_3 = "基于产品信息和目标人群生成短文案。"
user_input_3 = "产品: XYZ, 目标人群: 科技爱好者, 关键特性: 创新, 用户友好"
full_prompt_3 = f"{system_prompt_3}\n{user_input_3}"

# 4. 基于卖点信息和短文案生成长文案
system_prompt_4 = "基于卖点信息和短文案生成长文案。"
user_input_4 = "卖点: 创新设计, 高性能, 用户友好; 短文案: 这款产品具有创新设计和高性能，非常适合科技爱好者。"
full_prompt_4 = f"{system_prompt_4}\n{user_input_4}"
