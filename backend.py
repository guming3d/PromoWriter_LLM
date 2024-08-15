import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read Azure OpenAI credentials from environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Set the headers for the API request
headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_OPENAI_API_KEY
}

def generate_content_azure(prompt):
    """
    Generate content using Azure OpenAI service.
    
    Args:
        prompt (str): The prompt to send to the OpenAI service.
    
    Returns:
        str: The generated content.
    """
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-15-preview"
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
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
