import requests
from fastapi import APIRouter,status

router = APIRouter(tags=['Domain'], prefix='/domain')

@router.get("/domain/{domain}")
def get_domain(domain: str):
    response = requests.get("http://ip-api.com/json/" + domain)
    return response.json()