from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AI Clothing to IMVU Creator API",
    description="AI-powered API for converting clothing images into IMVU-ready assets.",
    version="1.0.0",
)


# ================================
# CORS Configuration
# ================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# Root Endpoint
# ================================

@app.get("/")
async def root():
    return {
        "success": True,
        "project": "AI Clothing to IMVU Creator",
        "message": "API is running successfully",
        "version": "1.0.0",
    }


# ================================
# Health Check
# ================================

@app.get("/health")
async def health_check():
    return {
        "success": True,
        "status": "healthy",
    }


# ================================
# API Information
# ================================

@app.get("/api")
async def api_info():
    return {
        "success": True,
        "name": "AI Clothing to IMVU Creator API",
        "version": "1.0.0",
        "features": [
            "Clothing Detection",
            "Background Removal",
            "Clothing Segmentation",
            "Texture Generation",
            "Color Detection",
            "Texture Enhancement",
            "IMVU Asset Preparation",
        ],
    }
