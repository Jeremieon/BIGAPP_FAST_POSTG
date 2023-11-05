#import Deps
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.user import router as user_router
from app.auth import router as auth_router
from app.products import router as product_router
from app.orders import router as order_router
from app.cart import router as cart_router
from app.tasks import router as task_router
from app.domain import router as domain_router
from app.note import router as note_router
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title="BIGAPP_API",description="Jeremiah BigAPP",version="0.1",redoc_url=None)

#http://localhost:3000
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#redoc_url=None
#docs_url="/private_docs

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(cart_router.router)
app.include_router(task_router.router)
app.include_router(domain_router.router)
app.include_router(note_router.router)



@app.get('/')
async def root():
    return {"Message": "Please refer to http:uri/docs"}