from typing import Union, Dict, Any, List
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from profileGenerator import generateProfile
from outfitGenerator import generateOutfits, HARDCODED_OUTFITS
from itemGenerator import generateItems, HARDCODED_ITEMS, get_random_items
from auth import (
    authenticate_user, create_access_token, verify_token,
    USERS_DB, Token, User, ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from serpapi.google_search import GoogleSearch
import traceback
import logging
import json
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# Mount the static files directory
app.mount("/images", StaticFiles(directory="public/images"), name="images")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class UserInput(BaseModel):
    text: str

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Allow guest access
    if token == "guest":
        return User(email="guest@example.com", full_name="Guest User")
    
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    user = USERS_DB.get(token_data.email)
    if user is None:
        raise credentials_exception
    return User(email=user["email"], full_name=user["full_name"])

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(USERS_DB, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/generate")
def generate_img():
    def get_image_files():
        import os

        img_dir = "./img"
        return [
            os.path.join(img_dir, f)
            for f in os.listdir(img_dir)
            if f.endswith((".jpg", ".jpeg", ".png"))
        ]

    image_files = get_image_files()
    profile = generateProfile(image_files)

    # Generate outfit recommendations
    outfits = generateOutfits(profile)

    items = generateItems(outfits)

    return JSONResponse(
        {"profile": profile, "outfit_recommendations": outfits, "items": items}
    )

@app.get("/generate-outfits")
def generate_outfits(profile: str):
    try:
        # Parse the profile string into a dictionary
        profile_data = json.loads(profile)
        
        # Generate outfit recommendations
        logger.info("Generating outfits...")
        outfits = generateOutfits(profile_data)
        logger.info(f"Generated outfits: {outfits}")
        
        # Ensure we have a valid response structure
        response_data = {
            "outfit_recommendations": outfits.get("outfit_recommendations", []),
            "status": "success"
        }
        
        return JSONResponse(content=response_data)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing profile JSON: {str(e)}")
        # Return hardcoded outfits if JSON parsing fails
        return JSONResponse(
            content={
                "outfit_recommendations": HARDCODED_OUTFITS["outfit_recommendations"],
                "status": "error",
                "message": "Invalid profile format, using default outfits"
            }
        )
    except Exception as e:
        logger.error(f"Error generating outfits: {str(e)}")
        logger.error(traceback.format_exc())
        # Return hardcoded outfits if any other error occurs
        return JSONResponse(
            content={
                "outfit_recommendations": HARDCODED_OUTFITS["outfit_recommendations"],
                "status": "error",
                "message": str(e)
            }
    )

def detect_category_from_filename(filename: str) -> str:
    """
    Detect the category from the filename.
    Returns 'casual', 'formal', 'traditional', or 'numbered' (default) if no specific category is detected.
    """
    filename_lower = filename.lower()
    
    # Check for numbered category (just numbers)
    if re.match(r'^\d+\.(jpg|jpeg|png)$', filename_lower):
        return 'numbered'
    
    # Check for other categories
    if 'casual' in filename_lower:
        return 'casual'
    elif 'formal' in filename_lower:
        return 'formal'
    elif 'traditional' in filename_lower:
        return 'traditional'
    
    # Return 'numbered' as default for any other filename
    return 'numbered'

@app.post("/generate")
async def generate(
    images: list[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
    try:
        # Create img directory if it doesn't exist
        os.makedirs("img", exist_ok=True)
        
        # Save uploaded images and detect categories
        image_files = []
        categories = set()
        
        for image in images:
            file_path = f"img/{image.filename}"
            with open(file_path, "wb") as f:
                content = await image.read()
                f.write(content)
            image_files.append(file_path)
            
            # Detect category from filename (will always return a category now)
            category = detect_category_from_filename(image.filename)
            categories.add(category)
        
        try:
            # Return category-based items
            category_items = {}
            for category in categories:
                if category in HARDCODED_ITEMS:
                    # Get 4 random items from the category
                    random_items = get_random_items(HARDCODED_ITEMS[category]["items"])
                    category_items[category] = {
                        "items": random_items
                    }
            
            # Clean up uploaded images
            for file_path in image_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            return JSONResponse({
                "status": "success",
                "categories": list(categories),
                "items": category_items
            })
            
        except Exception as e:
            logger.error(f"Error during generation: {str(e)}")
            logger.error(traceback.format_exc())
            # Clean up uploaded images in case of error
            for file_path in image_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            return JSONResponse(
                status_code=500,
                content={"error": str(e)}
            )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/generate-items")
def generate_items():
    sampleOutfits = {
        "profile": {
            "Age": 20,
            "Occupation": "Student/Gamer",
            "Location": "Urban Area",
            "Hobbies": ["Gaming", "Anime/Manga", "Cosplay"],
            "Ethnicity": "Not Specified",
            "Attire Style": "Casual",
            "Style Archetype": "Youthful/Trendy",
            "Color Palette": "Black, Blue, Pink, White",
            "Influence": "Anime Culture",
        },
        "outfit_recommendations": [
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-8dPXd0hqp3Nwe5IHNXTIhprB.png?st=2025-02-16T00%3A27%3A43Z&se=2025-02-16T02%3A27%3A43Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T04%3A20%3A44Z&ske=2025-02-16T04%3A20%3A44Z&sks=b&skv=2024-08-04&sig=fUGC0ktFR1kz4BB/DYEREN3%2BOqQfZ%2BLp4JoUvYsakFM%3D",
                "description": "A comfortable black oversized graphic tee featuring a popular anime character paired with distressed denim shorts, perfect for a casual day at campus or hanging out with friends.",
            },
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-EPqS9NKd63GBJ16pnR8yhX6V.png?st=2025-02-16T00%3A27%3A56Z&se=2025-02-16T02%3A27%3A56Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T05%3A03%3A16Z&ske=2025-02-16T05%3A03%3A16Z&sks=b&skv=2024-08-04&sig=o5WvBo/8yW/xfyGVH2P%2BUAUaaAL2W4s4sHDbcvRqOr4%3D",
                "description": "A vibrant pink hoodie layered over a fitted white long-sleeve shirt, combined with black joggers and white sneakers, ideal for a cozy gaming marathon or a casual stroll in the urban area.",
            },
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-uda2WBxaxc1pzPtAgW7tgJR2.png?st=2025-02-16T00%3A28%3A05Z&se=2025-02-16T02%3A28%3A05Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T05%3A54%3A23Z&ske=2025-02-16T05%3A54%3A23Z&sks=b&skv=2024-08-04&sig=LPTSw39H3oZjkRNulxZNRQPUDXgsXUKfcHU3Lq/B6so%3D",
                "description": "A trendy black bomber jacket over a blue anime anime-printed t-shirt, matched with skinny jeans and chunky high-top sneakers, suitable for a night out at a cosplay event or anime convention.",
            },
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-YDgpJymWOr11GHdLcvKtpnCH.png?st=2025-02-16T00%3A28%3A23Z&se=2025-02-16T02%3A28%3A23Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T06%3A37%3A36Z&ske=2025-02-16T06%3A37%3A36Z&sks=b&skv=2024-08-04&sig=18ReazqV3E0eXckafappaKooJQjuLePq0pGBdXoY/tQ%3D",
                "description": "A stylish white crop top with subtle pink accents, paired with high-waisted black skirt and combat boots, making it a great outfit for a lunch date or attending a themed party.",
            },
            {
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-aVDulKeGtpr1CBgZXlvIY56M/user-uWU7fTePdltLDans7xQVlRIR/img-gwOy0Tsxsb0qVDwKF9k9QGhp.png?st=2025-02-16T00%3A28%3A36Z&se=2025-02-16T02%3A28%3A36Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-15T07%3A37%3A40Z&ske=2025-02-16T07%3A37%3A40Z&sks=b&skv=2024-08-04&sig=pcx5ZXS0uwjGoMOwJYQzlwusevaTh6/kpTnwIY5rxMQ%3D",
                "description": "A relaxed-fit blue flannel shirt worn over a fitted graphic tee, teamed with black leggings and ankle boots, perfect for an easygoing day spent catching up on your favorite anime or hanging out at a local café.",
            },
        ],
        "items": [],
    }
    return generateItems(sampleOutfits)

@app.post("/generate-profile")
async def create_profile(user_input: UserInput):
    try:
        logger.info(f"Received profile generation request with input: {user_input.text}")
        profile = generateProfile(user_input.text)
        logger.info(f"Generated profile: {profile}")
        return profile
    except Exception as e:
        logger.error(f"Error generating profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-outfits")
async def create_outfits(profile: Dict[str, Any]):
    try:
        logger.info(f"Received outfit generation request with profile: {profile}")
        outfits = generateOutfits(profile)
        logger.info(f"Generated outfits: {outfits}")
        return outfits
    except Exception as e:
        logger.error(f"Error generating outfits: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-items")
async def create_items(profile: Dict[str, Any]):
    try:
        logger.info(f"Received item generation request with profile: {profile}")
        items = generateItems(profile)
        logger.info(f"Generated items: {items}")
        return items
    except Exception as e:
        logger.error(f"Error generating items: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
