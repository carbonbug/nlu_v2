import sys
sys.path.append(".")

from fastapi import APIRouter


from handlers.IntentHandler import router as intent_router
from handlers.ConverstaionHandler import router as conversation_router

router = APIRouter()
router.include_router(intent_router)
router.include_router(conversation_router)

