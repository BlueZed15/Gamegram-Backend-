from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Annotated

from core import session_int
from crud import get_user_games
from tables import Like, Comment
from auth_routes import get_current_user
from schemas import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# ── Helper: build game dict for user's games ──────────────────────

def build_game_dict(game, db: Session) -> dict:
    like_count    = db.query(Like).filter(Like.game_id == game.id, Like.is_like == True).count()
    dislike_count = db.query(Like).filter(Like.game_id == game.id, Like.is_like == False).count()

    return {
        "game_id":       game.id,
        "title":         game.title,
        "creator_id":    game.creator_id,
        "creator_name":  game.creator.username,
        "like_count":    like_count,
        "dislike_count": dislike_count,
        "play_count":    game.play_count,
        "runnable_url":  f"{game.sandbox.sandbox_url}?level_id={game.id}",
        "icon_url":      game.icon_url,
        "created_at":    game.created_at,
    }


# ── GET: games created by user ────────────────────────────────────

@router.get("/{user_id}/games")
def get_games(user_id: UUID, db: session_int, current_user= Annotated[UserResponse, Depends(get_current_user)]):
    games = get_user_games(db=db, user_id=current_user.id)
    return {
        "games": [build_game_dict(g, db) for g in games],
        "total": len(games),
    }