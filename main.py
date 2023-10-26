#import Deps
from fastapi import FastAPI
from app.user import router as user_router
from app.auth import router as auth_router
from app.products import router as product_router

app = FastAPI(title="BIGAPP_API",version="0.1",redoc_url=None)

#redoc_url=None
#docs_url="/private_docs

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(product_router.router)


@app.get('/')
async def root():
    return {"Message": "Please refer to http:uri/docs"}