from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, chat, character
from .database import create_tables, Base, engine
from . import models  # This will register all models with SQLAlchemy

app = FastAPI(title="ChatBot API")

# Configure CORS with secure defaults
origins = [
    "http://localhost:3000",  # React development server
    "http://localhost:5000",  # Production build
    "https://*.supabase.co",  # Allow Supabase domains
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
    expose_headers=["Authorization"],
    max_age=3600  # Cache preflight requests for 1 hour
)

# Include the routes
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(character.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the FastAPI Chatbot API!",
        "version": "1.0.0",
        "status": "healthy"
    }