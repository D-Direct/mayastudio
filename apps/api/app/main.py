"""
MayaStudio AI - Main FastAPI Application
Entry point for the backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings, setup_google_credentials
from app.api.routes import (
    auth,
    projects,
    scenes,
    dialogue,
    voices,
    parsing,
    render,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🌍 Environment: {settings.ENVIRONMENT}")

    # Setup Google credentials
    setup_google_credentials()

    yield

    # Shutdown
    print("👋 Shutting down gracefully...")


# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-Speaker AI Voice & Video Studio for YouTube Shorts & Series",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Disabled in production",
    }


# Include API routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    projects.router,
    prefix=f"{settings.API_V1_PREFIX}/projects",
    tags=["Projects"]
)

app.include_router(
    scenes.router,
    prefix=f"{settings.API_V1_PREFIX}/scenes",
    tags=["Scenes"]
)

app.include_router(
    dialogue.router,
    prefix=f"{settings.API_V1_PREFIX}/dialogue",
    tags=["Dialogue"]
)

app.include_router(
    voices.router,
    prefix=f"{settings.API_V1_PREFIX}/voices",
    tags=["Voices"]
)

app.include_router(
    parsing.router,
    prefix=f"{settings.API_V1_PREFIX}/parsing",
    tags=["Script Parsing"]
)

app.include_router(
    render.router,
    prefix=f"{settings.API_V1_PREFIX}/render",
    tags=["Video Rendering"]
)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected errors gracefully"""
    if settings.DEBUG:
        raise exc

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
