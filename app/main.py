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


def paraphrase(text, max_length=128):

  input_ids = paraphrasing_tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)

  generated_ids = paraphrasing_model.generate(input_ids=input_ids, num_return_sequences=20, num_beams=20, max_length=max_length, no_repeat_ngram_size=2, repetition_penalty=3.5, length_penalty=1.0, early_stopping=True)

  preds = [paraphrasing_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]

  return preds




app = create_app()


@router.get('/')
async def root():
    return "Welcome to EdCheck Backend API"



@router.post('/paraphraser_sentiment_checker/')
async def paraphraser_sentiment_checker(data: text_data):
  text = data.text
  original_score = sentiment_analysis(text)[0]['score']
    
  return_array = []
  if sentiment_analysis(text)[0]['label'] == "NEGATIVE":
    preds = paraphrase("paraphrase: " + text)

    for pred in preds:
      if sentiment_analysis(pred)[0]['label'] == "POSITIVE":
        return_array.append(str(pred))
    return ["Negative", return_array[:3]]
  else:
    return ["Positive", return_array]


