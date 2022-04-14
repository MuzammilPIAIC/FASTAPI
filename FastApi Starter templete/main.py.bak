import uvicorn
from fastapi import FastAPI
from routes.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["http://localhost:8005"]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == '__main__':
    print("running on 192.168.0.82:8005/")
    uvicorn.run("main:app", host='0.0.0.0', port=8005, log_level="info", reload=False)
    #print("running on ")