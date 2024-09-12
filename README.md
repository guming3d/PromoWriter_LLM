# Marketing Copy Generator

This is a Streamlit-based application for generating and optimizing marketing copy. Users can input product information, target user characteristics, etc., to generate unique selling points and copy.

## Installation Guide

Please follow these steps to install and run this project:



### 1. Create a Virtual Environment

It is recommended to use a Python virtual environment to isolate project dependencies:

```bash
cd <your-repo-directory>
python3 -m venv venv
source venv/bin/activate  # For Windows users, use `venv\Scripts\activate`
```

### 2. Install Dependencies

Use pip to install the required project dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file and add the following content:

```plaintext
AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint> # e.g., https://minggu-aoai.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=<your_azure_openai_deployment_name> # e.g., gpt-4o
AZURE_OPENAI_API_KEY=<your_azure_openai_api_key> # e.g., xxxx8186851d94efeb0d13fcxxxxxxxxxx
```

### 4. Run the Application

Use Streamlit to run the application:

```bash
streamlit run app.py
```

Open a browser and visit `http://localhost:8501` to view the application.

### 5. Button Function Descriptions

The application includes the following buttons, each with a specific function:

- **Generate Selling Points**: Generate product selling points based on the input product information and user characteristics.
- **Optimize Order**: Optimize the order of the generated selling points.
- **Review Selling Points**: Review the generated selling points and provide improvement suggestions.
- **Generate Short Copy**: Generate short copy to attract users based on the generated selling points.
- **Generate Long Copy**: Generate detailed long copy based on the generated selling points and short copy.
- **Generate Promotional Copy**: Generate promotional copy based on the generated selling points and short copy.
- **Generate Long Title**: Generate a long title to attract users based on the generated selling points and short copy.
- **Detailed Page Framework**: Generate a detailed page framework based on the generated selling points and short copy.
- **Clear All**: Clear all generated content and error messages.
