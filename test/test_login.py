from SmartApi import SmartConnect
import pyotp
import os
from dotenv import load_dotenv

load_dotenv()

smartApi = SmartConnect(api_key=os.getenv("ANGEL_API_KEY"))

totp = pyotp.TOTP(os.getenv("ANGEL_TOTP_SECRET")).now()

session = smartApi.generateSession(
    os.getenv("ANGEL_CLIENT_CODE"),
    os.getenv("ANGEL_PIN"),
    totp
)

print("FULL SESSION RESPONSE:")
print(session)

if session.get("status"):
    print("✅ LOGIN SUCCESS")
    print("Auth token (short):", session["data"]["jwtToken"][:25])
    print("Feed token:", smartApi.getfeedToken())
else:
    print("❌ LOGIN FAILED")
