# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from sandbox_routes import router as sandbox_router
from bootstrap_routes import router as bootstrap_router
from game_routes import router as game_router
#from users_routes import router as user_router

load_dotenv()

app = FastAPI()
app.mount("/sandboxes_data",StaticFiles(directory="sandboxes_data"), name="sandboxes")
print('hey')
app.include_router(sandbox_router)
app.include_router(bootstrap_router)
app.include_router(game_router)
#app.include_router(user_router)