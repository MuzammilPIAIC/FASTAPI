import uvicorn
from fastapi import FastAPI
from routes.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Request, status
from fastapi.responses import JSONResponse


#app = FastAPI()
app = FastAPI(docs_url="/docs", redoc_url=None)
origins = ["http://localhost:8005"]
#origins = ["http://192.168.1.38:8005"] 

# Whitelisted IPs
# WHITELISTED_IPS = ['192.168.0.4', '127.0.0.1']

# @app.middleware('http')
# async def validate_ip(request: Request, call_next):
#     # Get client IP
#     ip = str(request.client.host)
    
#     # Check if IP is allowed
#     if ip not in WHITELISTED_IPS:
#         data = {
#             'message': f'IP {ip} is not allowed to access this resource.'
#         }
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)

#     # Proceed if IP is allowed
#     return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# if __name__ == '__main__':
#     print("running on 192.168.0.82:8005/")
#     uvicorn.run("main:app", host='0.0.0.0', port=8005, log_level="info", reload=True)
#     #print("running on ")