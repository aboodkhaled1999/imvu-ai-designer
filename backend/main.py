from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import analyze
from app.routes import process
from app.routes import upload
from app.startup import initialize_project_directories


# ================================
# Application Lifespan
# ================================

@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    """
    Application startup and shutdown events.
    """

    # Initialize required directories
    initialize_project_directories()

    print(
        "AI Clothing to IMVU Creator API started."
    )

    yield

    print(
        "AI Clothing to IMVU Creator API stopped."
    )


# ================================
# FastAPI Application
# ================================

app = FastAPI(
    title="AI Clothing to IMVU Creator API",
    description=(
        "AI-powered API for converting "
        "clothing images into IMVU-ready assets."
    ),
    version="1.0.0",
    lifespan=lifespan,
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
# Register API Routes
# ================================

app.include_router(
    upload.router,
    prefix="/api",
)

app.include_router(
    process.router,
    prefix="/api",
)

app.include_router(
    analyze.router,
    prefix="/api",
)


# ================================
# Root Endpoint
# ================================

@app.get("/")
async def root():
    return {
        "success": True,
        "project": (
            "AI Clothing to IMVU Creator"
        ),
        "message": (
            "API is running successfully."
        ),
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
        "name": (
            "AI Clothing to IMVU Creator API"
        ),
        "version": "1.0.0",
        "endpoints": {
            "upload": (
                "POST /api/upload/clothing"
            ),
            "remove_background": (
                "POST /api/process/remove-background"
            ),
            "analyze": (
                "POST /api/analyze/clothing"
            ),
        },
        "features": [
            "Clothing Image Upload",
            "Background Removal",
            "Clothing Image Analysis",
            "Color Detection",
            "Texture Generation",
            "IMVU Asset Preparation",
        ],
    }
