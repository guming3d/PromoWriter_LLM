import os
import requests
from dotenv import load_dotenv

import os
import requests
from dotenv import load_dotenv, find_dotenv

def check_env_file():
    """
    Check if .env file exists and contains required parameters.
    
    Returns:
        bool: True if .env file exists and contains required parameters, False otherwise.
        str: Error message if .env file is missing or incomplete.
    """
    env_file = find_dotenv()
    if not env_file:
        return False, ".env file is missing. Please create a .env file with the following content:\n\n"
                       "AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>\n"
                       "AZURE_OPENAI_DEPLOYMENT_NAME=<your_azure_openai_deployment_name>\n"
                       "AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>"
    
    load_dotenv(env_file)
    
    required_vars = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT_NAME", "AZURE_OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        return False, f"Missing required parameters in .env file: {', '.join(missing_vars)}"
    
    return True, ""

# Check .env file
env_valid, env_error = check_env_file()

if env_valid:
    # Load environment variables from .env file
    load_dotenv()

    # Read Azure OpenAI credentials from environment variables
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
else:
    AZURE_OPENAI_ENDPOINT = None
    AZURE_OPENAI_DEPLOYMENT_NAME = None
    AZURE_OPENAI_API_KEY = None

# Set the headers for the API request
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_OPENAI_API_KEY
}

def generate_content_azure(system_prompt, user_input):
    """
    Generate content using Azure OpenAI service.
    
    Args:
        prompt (str): The prompt to send to the OpenAI service.
    
    Returns:
        str: The generated content.
    """
    full_prompt = f"{system_prompt}\n{user_input}"
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-15-preview"
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()

#  test usage
# if __name__ == "__main__":
#     system_prompt = "Generate marketing content based on the following details."
#     user_input = "Product: XYZ, Target Audience: Tech Enthusiasts, Key Features: Innovative, User-friendly"
#     full_prompt = f"{system_prompt}\n{user_input}"
    
#     generated_content = generate_content_azure(full_prompt)
#     print(generated_content)
