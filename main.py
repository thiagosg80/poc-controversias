from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware

from function.get_identificadas import get_identificadas

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.post('/controversias/identificar')
async def identificar(input_upload: UploadFile):
    return get_identificadas(input_upload)
