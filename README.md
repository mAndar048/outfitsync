# OutfitSync 👔

An AI-powered outfit recommendation system that analyzes your clothing preferences and style to suggest personalized fashion items. Upload images of your outfits, and let AI help you discover new styles that match your taste!

## 📋 Project Overview

OutfitSync is a full-stack web application that combines modern web technologies with AI/ML capabilities to provide intelligent fashion recommendations. The system uses machine learning models to analyze user-uploaded images, generate style profiles, and recommend outfit items from various categories (casual, formal, traditional).

## 🛠️ Tech Stack

### Frontend
- **Next.js 15.1.0** - React framework with App Router for server-side rendering and routing
- **React 19** - UI library for building interactive user interfaces
- **TypeScript** - Type-safe development
- **Tailwind CSS 3.4.1** - Utility-first CSS framework for styling
- **Radix UI** - Accessible component primitives (@radix-ui/react-slot)
- **Lucide React** - Beautiful icon library
- **React Dropzone** - Drag-and-drop file upload component
- **shadcn/ui** - Re-usable component library (Button, Card, Image Upload)

### Backend
- **FastAPI** - Modern Python web framework for building APIs
- **Python 3.x** - Core programming language
- **Uvicorn 0.24.0** - ASGI server for running FastAPI
- **PyTorch & Transformers** - Machine learning models for image analysis
- **SerpAPI** - Google search integration for finding fashion items
- **Python-Jose** - JWT token authentication
- **Passlib & Bcrypt** - Password hashing and security
- **Python-dotenv** - Environment variable management

### DevOps & Infrastructure
- **Docker** - Containerization for both client and server
- **Docker Compose** - Multi-container orchestration
- **Git** - Version control

## 🏗️ Architecture & Component Connections

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (Next.js + React)                        │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Navigation  │  │ ImageUpload  │  │ ItemDisplay  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│              └──────────┬──────────┘                        │
│                         │ HTTP Requests                     │
└─────────────────────────┼─────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                         Backend                              │
│                    (FastAPI + Python)                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              main.py (API Routes)                    │  │
│  │  • /login - User authentication                      │  │
│  │  • /generate - Upload images & get recommendations   │  │
│  │  • /generate-profile - Create user style profile     │  │
│  │  • /generate-outfits - Get outfit suggestions        │  │
│  │  • /generate-items - Get shopping items              │  │
│  └─────────────────────────────────────────────────────┘  │
│           │                │                  │             │
│           ▼                ▼                  ▼             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │
│  │    auth.py   │ │ profileGen   │ │ outfitGen    │      │
│  │ JWT tokens   │ │ AI analysis  │ │ AI outfits   │      │
│  └──────────────┘ └──────────────┘ └──────────────┘      │
│                                       │                     │
│                                       ▼                     │
│                              ┌──────────────┐              │
│                              │  itemGen.py  │              │
│                              │ Product Search│              │
│                              └──────────────┘              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
              External APIs (SerpAPI, AI Models)
```

### Data Flow

1. **User Authentication**
   - User logs in via `/login` endpoint
   - Backend validates credentials using `auth.py`
   - JWT token issued for authenticated requests
   - Guest access also supported for demo purposes

2. **Image Upload & Processing**
   - User uploads outfit images through `ImageUpload.tsx` component
   - Files sent to `/generate` endpoint via multipart/form-data
   - Images temporarily stored in `img/` directory on server
   - Category detection from filename (casual/formal/traditional/numbered)

3. **AI Profile Generation**
   - `profileGenerator.py` analyzes uploaded images
   - Uses AI models to extract style characteristics
   - Generates user profile with:
     - Age estimation
     - Occupation inference
     - Style archetype
     - Color palette preferences
     - Fashion influences

4. **Outfit Recommendations**
   - `outfitGenerator.py` uses the profile data
   - Generates 4 outfit suggestions with descriptions
   - Returns image URLs and detailed outfit descriptions
   - Falls back to hardcoded recommendations if AI unavailable

5. **Shopping Item Search**
   - `itemGenerator.py` searches for purchasable items
   - Uses SerpAPI to find products matching the style
   - Returns curated items by category
   - Displays items in `ItemDisplay.tsx` component

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v20 or higher)
- **Python** (v3.9 or higher)
- **Docker** and **Docker Compose** (for containerized deployment)

### Environment Variables

Create a `.env` file in the `server/` directory:

```env
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
SERPAPI_KEY=your_serpapi_key
```

### Local Development

#### Running the Backend (FastAPI)

```bash
cd server
pip install -r requirements.txt
python main.py
# Server runs on http://localhost:8000
```

#### Running the Frontend (Next.js)

```bash
cd client
npm install
npm run dev
# Client runs on http://localhost:3000
```

### Docker Deployment

The easiest way to run the entire application:

```bash
# Build and start both frontend and backend
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

The Docker setup includes:
- **Client container**: Next.js app with hot-reload enabled
- **Server container**: FastAPI with auto-reload
- **Volume mounting**: For development file changes
- **Network**: Internal Docker network for service communication

## 📡 API Endpoints

### Authentication
- `POST /login` - User authentication with email/password

### Main Features
- `POST /generate` - Upload images and get recommendations
- `POST /generate-profile` - Generate user style profile from text
- `POST /generate-outfits` - Get outfit recommendations from profile
- `POST /generate-items` - Search for shopping items

### Utility
- `GET /` - Health check endpoint
- `GET /items/{item_id}` - Get specific item details

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **CORS Configuration**: Controlled cross-origin resource sharing
- **OAuth2 Flow**: Industry-standard authentication pattern

## 📦 Key Dependencies

### Frontend
```json
{
  "next": "15.1.0",
  "react": "^19.0.0",
  "tailwindcss": "^3.4.1",
  "typescript": "^5",
  "react-dropzone": "^14.3.5",
  "lucide-react": "^0.475.0"
}
```

### Backend
```txt
fastapi[standard]
torch
transformers
serpapi
python-jose[cryptography]
passlib
bcrypt
uvicorn
```

## 🎯 Features

- ✅ **AI-Powered Analysis**: Uses machine learning to understand fashion preferences
- ✅ **Smart Recommendations**: Personalized outfit suggestions based on your style
- ✅ **Category Detection**: Automatically identifies outfit types (casual, formal, etc.)
- ✅ **Product Search**: Finds purchasable items matching your style
- ✅ **Responsive Design**: Mobile-friendly interface built with Tailwind CSS
- ✅ **Secure Authentication**: JWT-based user authentication
- ✅ **Docker Support**: Easy deployment with containers
- ✅ **Fallback Mechanisms**: Graceful degradation when APIs are unavailable

## 🔄 Development Workflow

1. **Frontend Development**: Edit components in `client/components/`
2. **Backend Development**: Modify API routes in `server/main.py`
3. **Styling**: Update Tailwind classes or `tailwind.config.ts`
4. **Testing**: Run linters with `npm run lint` (client)

## 📝 Project Structure

```
outfitsync/
├── client/                 # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── lib/              # Utility functions
│   └── public/           # Static assets
├── server/                # FastAPI backend
│   ├── main.py           # API routes
│   ├── auth.py           # Authentication logic
│   ├── profileGenerator.py   # AI profile generation
│   ├── outfitGenerator.py    # Outfit recommendations
│   └── itemGenerator.py      # Product search
├── docker-compose.yml     # Container orchestration
└── README.md             # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

---

Built with ❤️ using Next.js, FastAPI, and AI