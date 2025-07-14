from fastapi import APIRouter, Depends, HTTPException,status
from core.auth import get_current_user
from models.user import User
from fastapi.security import OAuth2PasswordBearer
import os
import stripe
from dotenv import load_dotenv

load_dotenv()

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

YOUR_DOMAIN = "http://localhost:3000"

@router.post("/pro")
def get_pro(user: User = Depends(get_current_user)):
    if True:
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'My Product',
                            },
                            'unit_amount': 1000,  # $10.00
                        },
                        'quantity': 1,
                    },
                ],
                success_url=YOUR_DOMAIN + '/success',
                cancel_url=YOUR_DOMAIN + '/cancel',
                api_key=STRIPE_API_KEY
            )
            return {"id": checkout_session.id, "url": checkout_session.url}
        except Exception as e:
            return {"error": str(e)}


@router.post("/status")
def get_status(user: User = Depends(get_current_user)):
    return {
        "mobile_no":user.mobile_no,
        "is_pro":user.is_pro
    }
