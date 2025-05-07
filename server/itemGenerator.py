import os
import json
import logging
import requests
from serpapi.google_search import GoogleSearch
from dotenv import load_dotenv
from typing import Dict, List, Any
import random
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def get_random_items(items: List[Dict[str, str]], count: int = 4) -> List[Dict[str, str]]:
    """
    Randomly select 'count' number of items from the given list.
    If there are fewer items than count, return all items.
    """
    if len(items) <= count:
        return items
    return random.sample(items, count)

# Hardcoded items for error cases
HARDCODED_ITEMS = {
    "casual": {
        "items": [
            {
                "url": "https://m.media-amazon.com/images/I/91QwlOR7xKL._AC_UY1100_.jpg",
                "description": "Classic blue denim shirt with a modern fit"
            },
            {
                "url": "https://m.media-amazon.com/images/I/61yCdfrgrjL._AC_UY1100_.jpg",
                "description": "Stylish striped casual shirt with comfortable fabric"
            },
            {
                "url": "https://m.media-amazon.com/images/I/41lw7KaRIcL._AC_UY1100_.jpg",
                "description": "Lightweight cotton shirt perfect for everyday wear"
            },
            {
                "url": "https://m.media-amazon.com/images/I/71leRerWguL._AC_UY1100_.jpg",
                "description": "Trendy printed shirt with a relaxed fit"
            },
            {
                "url": "https://m.media-amazon.com/images/I/91p2I3Ke2LL._AC_UY1100_.jpg",
                "description": "Casual button-down shirt with a contemporary style"
            },
            {
                "url": "https://m.media-amazon.com/images/I/712ppFfhdKL._AC_UY1100_.jpg",
                "description": "Modern slim-fit shirt with a clean design"
            },
            {
                "url": "https://images-eu.ssl-images-amazon.com/images/I/61LYRZ-uH6L._AC_SR462,693_.jpg",
                "description": "Versatile casual shirt with a comfortable cut"
            },
            {
                "url": "https://images-na.ssl-images-amazon.com/images/I/31vJreR4XxS._SL500_._AC_UL160_SR160,160_.jpg",
                "description": "Essential casual shirt with a classic look"
            },
            {
                "url": "https://images-eu.ssl-images-amazon.com/images/I/71l3noLH1wL._AC_SR462,693_.jpg",
                "description": "Stylish casual shirt with a modern twist"
            },
            {
                "url": "https://assets.myntassets.com/dpr_1.5,q_60,w_400,c_limit,fl_progressive/assets/images/29265888/2024/4/30/fe4c28bd-d5fb-467d-9d5e-26e3be3f7b671714470947075Shirts1.jpg",
                "description": "Premium casual shirt with a sophisticated design"
            },
            {
                "url": "https://d118ps6mg0w7om.cloudfront.net/media/catalog/product/s/s/fit-in/1000x1333/ss25_lot8_mfs-15941-u-88-beige_1_mfs-15941-u-88-beige.jpg",
                "description": "Elegant beige casual shirt with a refined style"
            },
            {
                "url": "https://m.media-amazon.com/images/I/81gvfhU5P1L._AC_UY1100_.jpg",
                "description": "Comfortable casual shirt with a relaxed fit"
            },
            {
                "url": "https://images-eu.ssl-images-amazon.com/images/I/61RD2-GNloL._AC_UL210_SR210,210_.jpg",
                "description": "Classic casual shirt with a timeless design"
            },
            {
                "url": "https://images-eu.ssl-images-amazon.com/images/I/71JdCHFBJ7L._AC_SR462,693_.jpg",
                "description": "Modern casual shirt with a stylish pattern"
            },
            {
                "url": "https://images-eu.ssl-images-amazon.com/images/I/61e3eyS9NtL._AC_SR462,693_.jpg",
                "description": "Trendy casual shirt with a contemporary look"
            },
            {
                "url": "https://m.media-amazon.com/images/G/31/img21/MA2024/HOTW/Top_Styles/Solid_shirts_981x1220._SX282_QL85_FMpng_.png",
                "description": "Solid color casual shirt with a clean design"
            },
            {
                "url": "https://rukminim2.flixcart.com/image/850/1000/xif0q/shopsy-shirt/c/d/s/xl-s-men-stylish-casual-premium-printed-lycra-shirt-certizo-original-imaghduejqzhzpff.jpeg?q=90&crop=false",
                "description": "Premium printed casual shirt with a modern fit"
            },
            {
                "url": "https://rukminim3.flixcart.com/image/850/1000/xif0q/shirt/i/i/y/l-hk-shirt-1274-global-nomad-original-imahyuqvhrr23zfv.jpeg?q=90&crop=false",
                "description": "Stylish casual shirt with a unique pattern"
            }
        ]
    },
    "formal": {
        "items": [
            {
                "url": "https://i.pinimg.com/564x/06/0f/13/060f13c1861db6dce3532ac07f72212f.jpg",
                "description": "Classic black formal suit with a modern cut"
            },
            {
                "url": "https://i.pinimg.com/564x/01/23/8e/01238e0ecce618da54e1a971f195da18.jpg",
                "description": "Elegant navy blue suit with a sophisticated style"
            },
            {
                "url": "https://i.pinimg.com/736x/6a/39/45/6a3945f4016b87b35c7a8833abe2e74f.jpg",
                "description": "Premium charcoal grey suit with a tailored fit"
            },
            {
                "url": "https://i.pinimg.com/736x/14/8a/8b/148a8bf21abeb27a79780b558770fbe1.jpg",
                "description": "Stylish formal suit with a contemporary design"
            },
            {
                "url": "https://i.pinimg.com/736x/63/d9/f7/63d9f756c417fb4b770235d8689fe3bb.jpg",
                "description": "Classic formal suit with a timeless appeal"
            },
            {
                "url": "https://cdn.shopify.com/s/files/1/0266/6276/4597/files/301013488BROWN_3_800x.jpg?v=1738664336",
                "description": "Rich brown formal suit with a premium finish"
            },
            {
                "url": "https://m.media-amazon.com/images/I/81FsAK9bdFL._AC_UY1100_.jpg",
                "description": "Professional formal suit with a sleek design"
            },
            {
                "url": "https://m.media-amazon.com/images/I/81jSlks0kxL._AC_UY1100_.jpg",
                "description": "Modern formal suit with a sophisticated look"
            },
            {
                "url": "https://m.media-amazon.com/images/I/81hBcNrx1DL._AC_UY1100_.jpg",
                "description": "Elegant formal suit with a refined style"
            },
            {
                "url": "https://m.media-amazon.com/images/I/51VTh2IjYYL._AC_UY1100_.jpg",
                "description": "Classic formal suit with a premium quality"
            },
            {
                "url": "https://m.media-amazon.com/images/I/71tiwdAduZL.jpg",
                "description": "Stylish formal suit with a modern twist"
            },
            {
                "url": "https://m.media-amazon.com/images/I/31Iu8M1p7FL._AC_UY1100_.jpg",
                "description": "Professional formal suit with a clean design"
            },
            {
                "url": "https://m.media-amazon.com/images/G/31/img19/Fashion/AW19/QC/Men/louis-philippe.jpg",
                "description": "Premium formal suit with a luxury finish"
            },
            {
                "url": "https://m.media-amazon.com/images/G/31/img18/apparel/men/brands/50/Peter-England50._CB462474288_.jpg",
                "description": "Classic formal suit with a traditional style"
            },
            {
                "url": "https://m.media-amazon.com/images/G/31/Symbol/brandtile/AH._CB461069312_.jpg",
                "description": "Elegant formal suit with a sophisticated design"
            },
            {
                "url": "https://m.media-amazon.com/images/I/51kg1NaxGTL._SY350_.jpg",
                "description": "Modern formal suit with a contemporary look"
            },
            {
                "url": "https://www.westside.com/cdn/shop/articles/formal_wear_for_men_eea788ec-9422-49e0-bba6-c75992c23c10.jpg?v=1677785539",
                "description": "Premium formal suit with a stylish design"
            }
        ]
    },
    "traditional": {
        "items": [
            {
                "url": "https://m.media-amazon.com/images/I/711ENWikFnL._AC_UY1100_.jpg",
                "description": "Elegant silk kurta with intricate embroidery"
            },
            {
                "url": "https://m.media-amazon.com/images/I/51h+t3U2B1L._AC_UY1100_.jpg",
                "description": "Classic cotton kurta with traditional patterns"
            },
            {
                "url": "https://m.media-amazon.com/images/I/713ytHed8jL._AC_UY1100_.jpg",
                "description": "Premium silk kurta with detailed work"
            },
            {
                "url": "https://m.media-amazon.com/images/I/6185XEXXDGL._AC_UY1100_.jpg",
                "description": "Stylish kurta with contemporary design"
            },
            {
                "url": "https://m.media-amazon.com/images/I/51QhAdV8vhL._AC_UY1100_.jpg",
                "description": "Traditional kurta with modern elements"
            },
            {
                "url": "https://m.media-amazon.com/images/I/71K0ux4XHCL._AC_UY1100_.jpg",
                "description": "Embroidered kurta with premium finish"
            },
            {
                "url": "https://m.media-amazon.com/images/I/71uiPE79+rL._AC_UY1100_.jpg",
                "description": "Designer kurta with intricate details"
            },
            {
                "url": "https://m.media-amazon.com/images/I/71eXQD70FVL._AC_UY1100_.jpg",
                "description": "Luxury kurta with sophisticated style"
            },
            {
                "url": "https://m.media-amazon.com/images/I/81OM9iuLspL._AC_UY1100_.jpg",
                "description": "Premium kurta with traditional motifs"
            },
            {
                "url": "https://m.media-amazon.com/images/I/61rKwXz4EFL._AC_UY1100_.jpg",
                "description": "Classic kurta with elegant design"
            },
            {
                "url": "https://m.media-amazon.com/images/I/61pTD0tPAIL._AC_UY1000_.jpg",
                "description": "Stylish kurta with contemporary patterns"
            },
            {
                "url": "https://m.media-amazon.com/images/I/312mukaLHKL._UF894,1000_QL80_.jpg",
                "description": "Traditional kurta with premium quality"
            },
            {
                "url": "https://m.media-amazon.com/images/I/81T+t2vM9RL._AC_UY1100_.jpg",
                "description": "Designer kurta with unique style"
            },
            {
                "url": "https://m.media-amazon.com/images/I/81KbZAZj8hL._AC_UY1100_.jpg",
                "description": "Elegant kurta with sophisticated design"
            },
            {
                "url": "https://i.pinimg.com/736x/65/55/38/6555385e94e387ac3294df33419d4ccf.jpg",
                "description": "Premium kurta with traditional embroidery"
            },
            {
                "url": "https://m.media-amazon.com/images/G/31/img24/MA/Sep/Jupiter24/EW/WeddingWardrobe/Engagement_Party._SY624_QL85_.jpg",
                "description": "Festive kurta with celebration style"
            },
            {
                "url": "https://m.media-amazon.com/images/I/71Xrbm9XXmL._AC_UF894,1000_QL80_.jpg",
                "description": "Classic kurta with modern touch"
            },
            {
                "url": "https://m.media-amazon.com/images/G/31/img24/MA/Sep/Jupiter24/EW/WeddingWardrobe/Pop_Colours_copy._SY750_QL85_FMpng_.png",
                "description": "Vibrant kurta with contemporary colors"
            },
            {
                "url": "https://assets0.mirraw.com/images/6289010/VP007025(1)_long_webp.webp?1696934354",
                "description": "Traditional kurta with artistic design"
            },
            {
                "url": "https://m.media-amazon.com/images/I/71JdUC5QCNL._AC_UY1100_.jpg",
                "description": "Premium kurta with elegant finish"
            }
        ]
    },
    "numbered": {
        "items": [
            {
                "url": "https://i.pinimg.com/170x/26/cb/40/26cb4058694f608551d028104b93c1fa.jpg",
                "description": "Classic casual outfit with modern style"
            },
            {
                "url": "https://i.pinimg.com/736x/4a/1e/9f/4a1e9f5486e7628d9e5486d0bd5145a5.jpg",
                "description": "Trendy street style outfit"
            },
            {
                "url": "https://cdn.onpointfresh.com/wp-content/uploads/2022/02/4c9d6e01c4ff1a273aa3c0759984e770.jpg",
                "description": "Minimalist fashion with clean lines"
            },
            {
                "url": "https://i.pinimg.com/474x/33/9e/91/339e9146dfe14eeb545555ad52416179.jpg",
                "description": "Urban casual style with character"
            },
            {
                "url": "https://www.fashionbeans.com/wp-content/uploads/2024/04/lestrangelondon_manincasualoutfitsittinginfrontofadoorway.jpg",
                "description": "Contemporary street fashion"
            },
            {
                "url": "https://preview.redd.it/what-do-you-call-this-kind-of-outfit-aesthetic-v0-9rw005zf76yc1.jpg?width=640&crop=smart&auto=webp&s=fde5e0ce7c18321c42c3b20997729b478455773d",
                "description": "Modern aesthetic outfit"
            },
            {
                "url": "https://cdnz.blacklapel.com/thecompass/2024/02/Screen-Shot-2024-02-12-at-9.27.06-AM.png",
                "description": "Sophisticated casual wear"
            },
            {
                "url": "https://www.fashionbeans.com/wp-content/uploads/2024/04/theresortco_manwearinganavypiquepopovershirtandwhitejeans.jpg",
                "description": "Resort casual style"
            },
            {
                "url": "https://cdn.onpointfresh.com/wp-content/uploads/2022/06/1a0191c638a39e410b56c5ee01a20b88.jpg",
                "description": "Fresh and modern outfit"
            },
            {
                "url": "https://preview.redd.it/what-do-you-call-this-kind-of-outfit-aesthetic-v0-a48bxwnf76yc1.jpg?width=640&crop=smart&auto=webp&s=0b6a77ed2f529f3d5037b1c0d55c70c84eba67ac",
                "description": "Contemporary street style"
            },
            {
                "url": "https://cdn.onpointfresh.com/wp-content/uploads/2022/02/1cdb4c21b213ca7b1706b6eee30cbd5b-683x1024.jpg",
                "description": "Urban fashion statement"
            },
            {
                "url": "https://i.pinimg.com/564x/5a/d0/7f/5ad07fce9d0e887dcb347068aee92e6b.jpg",
                "description": "Modern casual elegance"
            },
            {
                "url": "https://cdn.onpointfresh.com/wp-content/uploads/2022/09/8a4f8d6c85f5a64558661f53ccbee701.jpg",
                "description": "Trendy street wear"
            },
            {
                "url": "https://i.pinimg.com/736x/82/41/95/824195a7666b0a6911a14c366beafa96.jpg",
                "description": "Contemporary fashion style"
            },
            {
                "url": "https://i.pinimg.com/originals/07/f4/ce/07f4ce327308baf42643ffed5edd0ba9.jpg",
                "description": "Modern urban outfit"
            },
            {
                "url": "https://cdn.onpointfresh.com/wp-content/uploads/2021/12/233660d4b9f0f461c67cb6506c29c56c-1024x1024.jpg",
                "description": "Fresh street style"
            },
            {
                "url": "https://preview.redd.it/old-money-style-looking-for-inspo-v0-s2sws04qadyb1.jpg?width=615&format=pjpg&auto=webp&s=8082b34314e6661354c2d32846ba9c822ff219bc",
                "description": "Classic sophisticated style"
            },
            {
                "url": "https://i.pinimg.com/736x/38/a1/7b/38a17b2c5c52a432d76fe558614d255e.jpg",
                "description": "Modern fashion inspiration"
            },
            {
                "url": "https://cdn.onpointfresh.com/wp-content/uploads/2022/02/a4cf6b2d90150c4d227cf592b6bed684.jpg",
                "description": "Contemporary casual wear"
            },
            {
                "url": "https://d1fufvy4xao6k9.cloudfront.net/images/blog/posts/2023/09/hockerty_ethical_fashion_for_men_a28a3041_a73b_4b79_a598_dd7267a0489a.jpg",
                "description": "Ethical fashion style"
            },
            {
                "url": "https://cdn.shopify.com/s/files/1/0287/7918/4225/files/skater-boy-aesthetic-fashion_480x480.png?v=1669711187",
                "description": "Skater aesthetic fashion"
            },
            {
                "url": "https://cdn.onpointfresh.com/wp-content/uploads/2021/10/Korean-Mens-Minimal-Outfit.png",
                "description": "Korean minimal style"
            },
            {
                "url": "https://cdn.onpointfresh.com/wp-content/uploads/2021/09/skater-boy-aesthetic-clothes-1-824x1024.jpg",
                "description": "Skater boy fashion"
            },
            {
                "url": "https://www.mrporter.com/content/images/cms/ycm/resource/blob/884560/ebaae4462b405b2660e24dd6204ba8c0/6ce83531-16f2-4d88-a2c2-cda310758d8f-data.jpg/w800_q65.jpg",
                "description": "Premium casual style"
            },
            {
                "url": "https://i.pinimg.com/736x/1a/21/59/1a2159b5cd2222b1c4ef11719e6a9589.jpg",
                "description": "Modern street fashion"
            },
            {
                "url": "https://i.pinimg.com/originals/97/0a/c0/970ac0cec7edd79f7a3fb26f0dcadd82.jpg",
                "description": "Contemporary urban style"
            },
            {
                "url": "https://m.media-amazon.com/images/I/71FZSbi83oL._AC_UY1100_.jpg",
                "description": "Classic casual outfit"
            }
        ]
    }
}

def detect_category_from_filename(filename: str) -> str:
    """
    Detect category from filename. If no category is detected, return 'numbered' as default.
    """
    filename_lower = filename.lower()
    
    # Check for numbered category (1.jpg to 5.jpg)
    if re.match(r'^[1-5]\.jpg$', filename_lower):
        return 'numbered'
    
    # Check for other categories
    categories = ['casual', 'formal', 'traditional']
    for category in categories:
        if category in filename_lower:
            return category
    
    # If no category is detected, return 'numbered' as default
    return 'numbered'

def generateItems(userProfile: dict) -> dict:
    """
    Generate clothing items based on user profile using Cloudflare Workers AI
    """
    try:
        # Check for Cloudflare credentials
        cloudflare_token = os.getenv("CLOUDFLARE_API_TOKEN")
        cloudflare_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        
        if not cloudflare_token or not cloudflare_account_id:
            logger.warning("Missing Cloudflare credentials, returning hardcoded items")
            # Return random items from each category
            random_items = {}
            for category, data in HARDCODED_ITEMS.items():
                random_items[category] = {
                    "items": get_random_items(data["items"])
                }
            return random_items

        # Prepare the API request
        url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/ai/run/@cf/meta/llama-2-7b-chat-int8"
        headers = {
            "Authorization": f"Bearer {cloudflare_token}",
            "Content-Type": "application/json"
        }

        # Create a system prompt for item generation
        system_prompt = """You are a fashion expert. Generate a list of 5 clothing items that match the user's style profile.
        For each item, provide:
        1. A URL to an image of the item
        2. A brief description of the item
        Format the response as a JSON object with an 'items' array containing the items."""

        # Prepare the data for the API request
        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate items for this profile: {json.dumps(userProfile)}"}
            ]
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        logger.info(f"Cloudflare API Response: {json.dumps(result, indent=2)}")
        
        if not result.get("success", False):
            logger.error(f"Cloudflare API error: {result.get('errors', 'Unknown error')}")
            # Return random items from each category
            random_items = {}
            for category, data in HARDCODED_ITEMS.items():
                random_items[category] = {
                    "items": get_random_items(data["items"])
                }
            return random_items
            
        # Extract the generated text
        generated_text = result.get("result", {}).get("response", "")
        logger.info(f"Generated text: {generated_text}")
        
        # Try to parse the generated text as JSON
        try:
            items = json.loads(generated_text)
            if not isinstance(items, dict) or "items" not in items:
                logger.error("Invalid response format: missing 'items' key")
                # Return random items from each category
                random_items = {}
                for category, data in HARDCODED_ITEMS.items():
                    random_items[category] = {
                        "items": get_random_items(data["items"])
                    }
                return random_items
            return items
        except json.JSONDecodeError:
            logger.error("Failed to parse generated text as JSON")
            # Return random items from each category
            random_items = {}
            for category, data in HARDCODED_ITEMS.items():
                random_items[category] = {
                    "items": get_random_items(data["items"])
                }
            return random_items
            
    except Exception as e:
        logger.error(f"Error generating items: {str(e)}")
        # Return random items from each category
        random_items = {}
        for category, data in HARDCODED_ITEMS.items():
            random_items[category] = {
                "items": get_random_items(data["items"])
            }
        return random_items
