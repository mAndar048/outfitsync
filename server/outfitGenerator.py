import os
import json
import logging
import requests

logger = logging.getLogger(__name__)

# Hardcoded outfit data for error cases
HARDCODED_OUTFITS = {
    "outfit_recommendations": [
        {
            "url": "https://m.media-amazon.com/images/I/41KWq9jTUWL._SX679_.jpg",
            "description": "A classic red t-shirt perfect for casual outings"
        },
        {
            "url": "https://m.media-amazon.com/images/I/71WSdgKd1kL._SX679_.jpg",
            "description": "A trendy red t-shirt for a modern look"
        },
        {
            "url": "https://m.media-amazon.com/images/I/61msssMmb3L._SX679_.jpg",
            "description": "A stylish red t-shirt for everyday wear"
        },
        {
            "url": "https://m.media-amazon.com/images/I/61msssMmb3L._SX679_.jpg",
            "description": "A comfortable red t-shirt for any occasion"
        }
    ]
}

def generateOutfits(profile_data: dict) -> dict:
    # Get Cloudflare credentials
    api_token = os.getenv('CLOUDFLARE_API_TOKEN')
    account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
    
    # If credentials are missing, return hardcoded outfits immediately
    if not api_token or not account_id:
        logger.info("Missing Cloudflare credentials - returning hardcoded outfits")
        return HARDCODED_OUTFITS
    
    # Construct the system prompt
    system_prompt = """
    Generate 4 outfit recommendations in JSON format with:
    - url: Image URL
    - description: Brief outfit description

    Example:
    {
    "outfit_recommendations": [
        {
            "url": "https://example.com/image1.jpg",
            "description": "Casual red t-shirt"
        }
    ]
    }
    """
    
    # Make the API request to Cloudflare Workers AI
    try:
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
                    "content": json.dumps(profile_data)
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        # If API call fails, return hardcoded outfits
        if response.status_code != 200:
            logger.info(f"API call failed with status {response.status_code} - returning hardcoded outfits")
            return HARDCODED_OUTFITS
            
        result = response.json()
        
        # If response parsing fails, return hardcoded outfits
        if 'result' not in result or 'response' not in result['result']:
            logger.info("Invalid API response format - returning hardcoded outfits")
            return HARDCODED_OUTFITS
            
        try:
            outfits = json.loads(result['result']['response'])
            if isinstance(outfits, dict) and 'outfit_recommendations' in outfits:
                return outfits
        except json.JSONDecodeError:
            logger.info("Failed to parse API response - returning hardcoded outfits")
            return HARDCODED_OUTFITS
            
        # If we get here, something went wrong with the response format
        logger.info("Invalid outfit format in API response - returning hardcoded outfits")
        return HARDCODED_OUTFITS

    except Exception as e:
        logger.error(f"Error in outfit generation: {str(e)}")
        logger.info("Returning hardcoded outfits due to error")
        return HARDCODED_OUTFITS
