import uvicorn
from fastapi import APIRouter, Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware


from pydantic import BaseModel

from celery.result import AsyncResult


from transformers import AutoModelWithLMHead, AutoTokenizer
paraphrasing_tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-small-finetuned-quora-for-paraphrasing")
paraphrasing_model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-small-finetuned-quora-for-paraphrasing")
from transformers import pipeline
sentiment_analysis = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")

####################################################
class text_data(BaseModel):
    text : str
#####################################################

router = APIRouter()

def create_app() -> CORSMiddleware:
    """Create app wrapper to overcome middleware issues."""
    fastapi_app = FastAPI()
    fastapi_app.include_router(router)
    return CORSMiddleware(
        fastapi_app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )




app = create_app()


@router.get('/')
async def root():
    return "Welcome to HKN DevOps Workshop! This message is the confirmation that your API server is up and running perfectly!"


