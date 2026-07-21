# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from sandbox_routes import router as sandbox_router
from bootstrap_routes import router as bootstrap_router
from game_routes import router as game_router
from auth_routes import router as auth_router
from users_routes import router as user_router
from fastapi.middleware.cors import CORSMiddleware





load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        # Add deployed React URL here.
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.mount("/sandboxes_data",StaticFiles(directory="sandboxes_data"), name="sandboxes")
app.include_router(sandbox_router)
app.include_router(bootstrap_router)
app.include_router(game_router)
app.include_router(auth_router)
app.include_router(user_router)