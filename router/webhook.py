from fastapi import APIRouter, Request, Header, HTTPException
import os
import stripe
from dotenv import load_dotenv

load_dotenv()

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


router = APIRouter()

@router.post("/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=ENDPOINT_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"✅ Payment confirmed: {session['id']}")

    return {"status": "success"}



