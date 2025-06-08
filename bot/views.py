import json
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("EAAI73aaseIABOwq5bfIWxdLBlhk8M858TZCZA6WDQ8sbXyIZBotngBqtSHOHtYv8b2K2y6rZBekoTcwRxiQmT2uzwn4NvXtHO53Em87yXtrUnzyLsm0Y6diGi4BoZAMSZCYiWbP5ZCqvhC9sbMjKAXOOUfD52Ac3JTkU2aH8NzYlPp9lujcBYTsCziiSGFVPitMGfTavEBN0hQwM3aKbpNdZC7lkZCjc9KIQZD")
PHONE_NUMBER_ID = os.getenv("662993340220587")

DOCUMENT_MENU = {
    "1.income certificate": [
        "✅ Coupon Copy",
        "✅ Photo - 1",
        "✅ Aadhaar Card Copy",
        "✅ Election Card Copy",
        "✅ Address Proof",
        "✅ Light Bill Copy"
    ],
    "2.domicile certificate": [
        "✅ Coupon Copy",
        "✅ Aadhaar Card Copy",
        "✅ Light Bill Copy",
        "✅ Photo - 1",
        "✅ Father's Photo - 1",
        "✅ Father's Aadhaar Card",
        "✅ Father's School Leaving Certificate",
        "✅ School Leaving Certificate",
        "✅ Police Station Certificate",
        "✅ Birth Certificate",
        "✅ Income Certificate",
        "✅ Mark Sheets from Std. 1 to Last"
    ],
    "rte": [
        "✅ Child's Birth Certificate",
        "✅ Child's Aadhaar Card",
        "✅ Child's Photo",
        "✅ Coupon",
        "✅ Aadhaar Cards of Parents",
        "✅ Father's Income Certificate",
        "✅ Bank Passbook",
        "✅ BPL Card (if applicable)",
        "✅ PAN Card",
        "✅ Caste Certificate (if applicable)"
    ],
    "girl child assistance": [
        "✅ Girl's Birth Certificate and Aadhaar Card",
        "✅ Girl's Photo",
        "✅ Parents' Marriage Certificate",
        "✅ Parents' School Leaving Certificates",
        "✅ Parents' Coupons",
        "✅ Parents' Aadhaar Cards",
        "✅ Father's Income Certificate",
        "✅ Bank Passbook (Mother or Father)",
        "✅ Birth & Aadhaar of all previous children"
    ],
    "senior citizen assistance": [
        "✅ Coupon Copy",
        "✅ Aadhaar Card Copy",
        "✅ Age Proof (Birth Cert/School LC/Hospital)",
        "✅ Bank Passbook",
        "✅ BPL Card/Certificate",
        "✅ Photo - 1"
    ],
    "widow assistance": [
        "✅ Coupon Copy",
        "✅ Aadhaar Card Copy",
        "✅ Income Certificate Copy",
        "✅ Age Proof (Birth Cert/LC/Hospital)",
        "✅ Light Bill Copy",
        "✅ Photos - 4",
        "✅ Bank Passbook",
        "✅ Husband's Death Certificate",
        "✅ Aadhaar Cards of Dependents",
        "✅ Income Certificates with separate coupons"
    ],
    "non criminal": [
        "✅ Coupon Copy",
        "✅ Aadhaar Card Copy",
        "✅ Light Bill Copy",
        "✅ Father's Photo - 1",
        "✅ Father's Aadhaar Card",
        "✅ School Leaving Certificate",
        "✅ Father's/Uncle's School LC",
        "✅ Father's Income Certificate",
        "✅ Caste Certificate",
        "✅ Address Proof",
        "✅ Panchayat Income Certificate"
    ],
    "ebc": [
        "✅ Coupon Copy",
        "✅ Aadhaar Card Copy",
        "✅ Light Bill Copy",
        "✅ Address Proof",
        "✅ Photo - 1",
        "✅ Father's/Husband's Income Certificate",
        "✅ Father's Photo - 1",
        "✅ Father's Aadhaar Card",
        "✅ Applicant's School LC",
        "✅ Father's/Uncle's School LC"
    ],
    "guardian parent": [
        "✅ Child's Birth Certificate",
        "✅ Child's Aadhaar Card",
        "✅ Child's Bonafide Certificate",
        "✅ Parents' Death Certificates & Aadhaar Cards",
        "✅ Child's Photo (Single)",
        "✅ Child + Guardian Photo (Joint)",
        "✅ Joint Bank Passbook",
        "✅ Guardian's Coupon",
        "✅ Guardian's Aadhaar Card",
        "✅ Guardian Father's Income Certificate",
        "✅ Light Bill Copy"
    ],
    "caste certificate": [
        "✅ Coupon Copy",
        "✅ Aadhaar Card Copy",
        "✅ Light Bill Copy",
        "✅ Address Proof",
        "✅ Photo - 1",
        "✅ Father's Photo - 1",
        "✅ Father's Aadhaar Card",
        "✅ Applicant's School LC",
        "✅ Father's/Uncle's School LC"
    ],
    "inheritance certificate": [
        "✅ Affidavit of Deceased",
        "✅ Coupon Copy",
        "✅ Aadhaar Card Copy",
        "✅ Death Certificate",
        "✅ Photo - 1",
        "✅ Aadhaar of all Dependents"
    ],
    "7/12/8a": [
        "✅ 7/12/8-A Document",
        "✅ Inheritance Affidavit",
        "✅ Inheritance Certificate",
        "✅ Death Certificate",
        "✅ No Encumbrance Certificate"
    ],
    "kumarbai marriage": [
        "✅ Girl's Aadhaar & Photo",
        "✅ Father's Aadhaar",
        "✅ Father's Income Certificate",
        "✅ Girl & Boy Caste Certificates",
        "✅ Marriage Registration Certificate",
        "✅ Bank Passbook (Girl)",
        "✅ Boy's Aadhaar",
        "✅ Ration Card KYC",
        "✅ Joint Photo",
        "✅ Marriage Registration Form Copy"
    ],
    "satyavadi harishchandra": [
        "✅ Residence Proof",
        "✅ Death Certificate",
        "✅ Bank Passbook or Cancelled Cheque",
        "✅ Aadhaar Card",
        "✅ Annual Income Certificate",
        "✅ Caste Certificate"
    ],
    "marriage registration": [
        "✅ Bride & Groom School LC",
        "✅ Bride & Groom Coupons",
        "✅ Aadhaar Cards (Bride & Groom)",
        "✅ Father's Aadhaar (Bride)",
        "✅ Aadhaar of 2 Witnesses",
        "✅ Wedding Photo",
        "✅ Marriage Form Copy"
    ],
    "scholarship": [
        "✅ Student's Aadhaar",
        "✅ Bank Passbook",
        "✅ Academic Mark Sheets",
        "✅ Caste Certificate",
        "✅ School Leaving Certificate",
        "✅ Bonafide Certificate",
        "✅ Guardian's Income Certificate",
        "✅ Student's Photo",
        "✅ Hostel Fee Receipt (if applicable)",
        "✅ Fee Receipt from College",
        "✅ Gap Certificate (if any)"
    ]
}

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        if request.GET.get("hub.mode") == "subscribe" and request.GET.get("hub.verify_token") == "verifyme":
            return JsonResponse({"hub.challenge": request.GET.get("hub.challenge")})
        return JsonResponse({"error": "Invalid token"}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]
            user_message = message["text"]["body"].strip().lower()

            response = DOCUMENT_MENU.get(user_message)

            if response:
                text = f"📑 Required documents for {user_message.title()}:\n" + "\n".join(response)
            else:
                text = "⚠️ Service not found. Please enter a valid keyword like: income certificate, rte, caste certificate"

            url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": sender,
                "type": "text",
                "text": {"body": text}
            }

            requests.post(url, headers=headers, json=payload)

        except Exception as e:
            print("❌ Error:", e)

        return JsonResponse({"status": "received"}, status=200)
