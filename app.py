import os
import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import Response
from src.tsp.pipeline.prediction_piplin import PredictionPipeline

text:str= " what is summarization ?"

app=FastAPI()

@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train():
    try:
        os.system('python main.py')
        return Response('traning Completed ....')
    except Exception as e:
        return Response(e)

@app.post('/predict')
async def predict(text):
    try:
        obj=PredictionPipeline()
        text=obj.predict(text)
    except Exception as e:
        raise e

if __name__ =="__main__":
    uvicorn.run(app,host='0.0.0.0', port=8000)

