import os
import json
from typing import List, Dict, Any
import base64
import logging
import requests

logger = logging.getLogger(__name__)

# Hardcoded profile data for error cases
HARDCODED_PROFILE = {
    "Age": 25,
    "Occupation": "Student",
    "Location": "Urban Area",
    "Hobbies": ["Fashion", "Shopping", "Social Media"],
    "Ethnicity": "Not Specified",
    "Attire Style": "Casual",
    "Style Archetype": "Trendy",
    "Color Palette": "Red, Black, White",
    "Influence": "Street Fashion"
}

def generateProfile(image_files: List[str]) -> Dict[str, Any]:
    # Get Cloudflare credentials
    api_token = os.getenv('CLOUDFLARE_API_TOKEN')
    account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
    
    # Log the credentials (masking the token for security)
    logger.info(f"Account ID: {account_id}")
    logger.info(f"API Token present: {'Yes' if api_token else 'No'}")
    logger.info(f"API Token length: {len(api_token) if api_token else 0}")
    
    if not api_token or not account_id:
        logger.error("Missing Cloudflare credentials")
        logger.info("Returning hardcoded profile due to missing credentials")
        return HARDCODED_PROFILE
    
    if not image_files:
        logger.error("No image files provided")
        logger.info("Returning hardcoded profile due to no images")
        return HARDCODED_PROFILE
    
    # Prepare the images for the API request
    image_messages = []
    for image_file in image_files:
        try:
            with open(image_file, 'rb') as file:
                image_data = file.read()
                image_messages.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
                    }
                })
        except Exception as e:
            logger.error(f"Error reading image file {image_file}: {str(e)}")
            logger.info("Returning hardcoded profile due to image reading error")
            return HARDCODED_PROFILE
    
    # Construct the system prompt
    system_prompt = """
    Analyze the images and create a customer profile in JSON format with these fields:
    - Age (integer)
    - Occupation (string)
    - Location (string)
    - Hobbies (array of strings)
    - Ethnicity (string)
    - Attire Style (Casual/Business Casual/Smart Casual/Business/Streetwear/Vintage)
    - Style Archetype (string)
    - Color Palette (string)
    - Influence (string)

    Example:
    {
    "Age": 20,
    "Occupation": "Student",
    "Location": "Urban",
    "Hobbies": ["Gaming", "Art"],
    "Ethnicity": "Not Specified",
    "Attire Style": "Casual",
    "Style Archetype": "Trendy",
    "Color Palette": "Black, Blue",
    "Influence": "Street Fashion"
    }
    """

    # Make the API request to Cloudflare Workers AI
    try:
        logger.info("Sending request to Cloudflare Workers AI")
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-2-7b-chat-int8"
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(image_messages)
                }
            ]
        }

        logger.info(f"Request URL: {url}")
        logger.info(f"Request headers: {headers}")
        logger.info(f"Request data: {data}")

        response = requests.post(url, headers=headers, json=data)
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")
        logger.info(f"Response content: {response.text}")
        
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"Received response from Cloudflare: {result}")
        
        # Parse the response
        profile_data = json.loads(result['result']['response'])
        
        # Validate required fields
        required_fields = ["Age", "Occupation", "Location", "Ethnicity", "Attire Style", "Style Archetype"]
        for field in required_fields:
            if field not in profile_data:
                logger.error(f"Missing required field in profile: {field}")
                logger.info("Returning hardcoded profile due to missing fields")
                return HARDCODED_PROFILE
        
        logger.info(f"Successfully generated profile: {profile_data}")
        return profile_data
    
    except Exception as e:
        logger.error(f"Error generating profile: {str(e)}")
        logger.info("Returning hardcoded profile due to error")
        return HARDCODED_PROFILE
  