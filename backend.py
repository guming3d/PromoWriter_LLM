import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read Azure OpenAI credentials from environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Set the OpenAI API key
openai.api_key = AZURE_OPENAI_API_KEY

def generate_content_azure(prompt):
    """
    Generate content using Azure OpenAI service.
    
    Args:
        prompt (str): The prompt to send to the OpenAI service.
    
    Returns:
        str: The generated content.
    """
    response = openai.Completion.create(
        engine=AZURE_OPENAI_DEPLOYMENT_NAME,
        prompt=prompt,
        max_tokens=800
    )
    return response.choices[0].text.strip()

# Example usage
if __name__ == "__main__":
    system_prompt = "Generate a marketing content based on the following details."
    user_input = "Product: XYZ, Target Audience: Tech Enthusiasts, Key Features: Innovative, User-friendly"
    full_prompt = f"{system_prompt}\n{user_input}"
    
    generated_content = generate_content_azure(full_prompt)
    print(generated_content)
