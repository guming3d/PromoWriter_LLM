# 营销文案生成器

这是一个基于Streamlit的应用程序，用于生成和优化营销文案。用户可以输入产品信息、目标用户特征等，生成独特的卖点和文案。

## 安装指南

请按照以下步骤安装和运行此项目：

### 1. 克隆仓库

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. 创建虚拟环境

建议使用Python虚拟环境来隔离项目依赖：

```bash
python3 -m venv venv
source venv/bin/activate  # 对于Windows用户，使用 `venv\Scripts\activate`
```

### 3. 安装依赖

使用pip安装项目所需的依赖：

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建一个`.env`文件，并添加以下内容：

```plaintext
AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
AZURE_OPENAI_DEPLOYMENT_NAME=<your_azure_openai_deployment_name>
AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
```

### 5. 运行应用程序

使用Streamlit运行应用程序：

```bash
streamlit run app.py
```

打开浏览器并访问 `http://localhost:8501` 查看应用程序。