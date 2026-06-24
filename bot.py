import telebot
import requests
import json
import random
import hashlib
import re
from time import sleep

# ========== BOT CONFIGURATION ==========
BOT_TOKEN = "8575561951:AAHC8G5vGG24_v_W9sslfU38pQdVt0G8GMA"
bot = telebot.TeleBot(BOT_TOKEN)

# ========== CONSTANTS ==========
SECRET_KEY = "*dkaSDs#*k9487ld!*kaSJDsj9784@dsk!!dHD@dka820#SD!sk192@"

# ========== HELPER FUNCTIONS ==========
def generate_mobile():
    prefixes = [6, 7, 8, 9]
    first = str(random.choice(prefixes))
    remaining = str(random.randint(100000000, 999999999))
    return first + remaining

def generate_name():
    names = ["Vasu","Nirmal","Akshay","Chander","Rupinder","Akhil","Shanti","Ravi","Kunal","Chandrakant","Sulabha","Mahinder","Swapnil","Deepa","Sulabha","Neelima","Vijaya","Nikhil","Isha","Siddhi","Ajeet","Kshitija","Anila","Jitender","Sumeet","Preethi","Priti","Gayathri","Dhaval","Mukesh","Lalita","Rachana","Rakhi","Harshal","Shekhar","Rajiv","Balakrishna","Ajeet","Tara","Chander","Deepa","Prabhu","Rajendra","Jeetendra","Nandu","Aniket","Sumati","Prabhu","Vimal","Indira","Laxman","Agni","Kapil","Kailash","Puneet","Pratik","Pankaj","Ishore","Swati","Rupa","Hardeep","Prabhu","Khushi","Gurmeet","Nishant","Rishi","Naveen"]
    return random.choice(names)

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def sort_json_body(json_str):
    try:
        if not json_str or json_str.strip() == "":
            return ""
        decoded = json.loads(json_str)
        if not isinstance(decoded, dict):
            return ""
        sorted_decoded = dict(sorted(decoded.items(), key=lambda x: x[0], reverse=True))
        return json.dumps(sorted_decoded, separators=(',', ':'))
    except:
        return ""

def generate_checksum(data, secret_key):
    secret_hash = sha256(secret_key)
    sorted_body = sort_json_body(data)
    if sorted_body and sorted_body != "{}":
        checksum_input = secret_hash + sorted_body
    else:
        checksum_input = secret_hash
    return sha256(checksum_input)

def http_call(url, method="POST", json_body=None, headers=None):
    try:
        if method.upper() == "POST":
            response = requests.post(url, data=json_body, headers=headers, timeout=30)
        else:
            response = requests.get(url, headers=headers, timeout=30)
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"

# ========== MAIN PROCESSING FUNCTION ==========
def process_upi(upi):
    # Validate UPI format
    if not re.match(r'^[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}$', upi):
        return "❌ Invalid UPI format. Please enter a valid UPI (e.g., name@upi)"

    fname = generate_name()
    email = f"{fname}{random.randint(1000,9000)}@gmail.com"
    num = generate_mobile()
    
    results = []
    
    # ---------- 1. Save User Detail ----------
    url = "https://web.myfidelity.in/api/v1/parachute_rosemary/save-user-detail"
    data = json.dumps({
        "msisdn": num,
        "firstName": fname,
        "lastName": "",
        "email": email,
        "pinCode": "",
        "consent1": 1,
        "ssoId": "NA"
    })
    checksum = generate_checksum(data, SECRET_KEY)
    headers = {
        "Host": "web.myfidelity.in",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua": '"Android WebView";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "utm-source": "unknown",
        "appVersion": "1.0",
        "checksum": checksum,
        "authorization": "Bearer",
        "msisdn": num,
        "appName": "Merico_Nihar",
        "Accept": "application/json",
        "channel": "WEB",
        "Content-Type": "application/json",
        "campaignId": "1",
        "clientId": "LKnVCeozqpO9CIsMXW0yzBKgo2NDLUT40RtAbFU+dMw=",
        "utm-medium": "unknown",
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; V2303) AppleWebKit/537.36",
        "utm-campaign": "unknown",
        "Origin": "https://microsite.ad.paytm.com",
        "X-Requested-With": "lodu.hehe.com",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://microsite.ad.paytm.com/"
    }
    response = http_call(url, "POST", data, headers)
    results.append(f"📝 User Detail: {response[:100]}...")
    
    # ---------- 2. Save Answers ----------
    url = "https://web.myfidelity.in/api/v1/parachute_rosemary/save-answers"
    data = json.dumps({
        "msisdn": num,
        "answersMap": {
            "trivia1": {
                "answer": "Repair Damaged Hair",
                "question": "Which hair concern is currently your most urgent priority to resolve?"
            },
            "trivia2": {
                "answer": "Rosemary",
                "question": "Which of these natural super-ingredients do you believe helps you get the most beautiful hair?"
            }
        }
    })
    checksum = generate_checksum(data, SECRET_KEY)
    headers["checksum"] = checksum
    headers["utm-source"] = ""
    headers["utm-medium"] = ""
    response = http_call(url, "POST", data, headers)
    results.append(f"📋 Answers: {response[:100]}...")
    
    # ---------- 3. Save UPI Info ----------
    url = "https://web.myfidelity.in/api/v1/parachute_rosemary/save-upi-info"
    data = json.dumps({"vpa": upi})
    checksum = generate_checksum(data, SECRET_KEY)
    headers["checksum"] = checksum
    response = http_call(url, "POST", data, headers)
    results.append(f"💳 UPI Save: {response[:100]}...")
    
    try:
        json_response = json.loads(response)
        msg = json_response.get("msg", "No message")
        status = json_response.get("status", "")
    except:
        msg = "Could not parse response"
        status = ""
    
    # ---------- 4. Redemption (if SUCCESS) ----------
    if status == "SUCCESS":
        url = "https://web.myfidelity.in/api/v1/parachute_rosemary/redemption"
        data = json.dumps({"redemptionType": "CASHBACK"})
        checksum = generate_checksum(data, SECRET_KEY)
        headers["checksum"] = checksum
        response = http_call(url, "POST", data, headers)
        try:
            json_response = json.loads(response)
            msg = json_response.get("msg", "Redemption done")
        except:
            msg = "Redemption response received"
        results.append(f"🎉 Redemption: {msg}")
    
    final_msg = f"""
✅ **Processing Complete!**

👤 Name: {fname}
📱 Mobile: {num}
📧 Email: {email}
💳 UPI: {upi}

📌 Status: {msg}

📊 **Details:**
{chr(10).join(results)}
"""
    return final_msg

# ========== TELEGRAM BOT HANDLERS ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🌟 **Welcome to UPI Referral Bot!** 🌟

Send me your UPI ID and I'll process it.

📌 **How to use:**
Just type your UPI ID and send.

Example: `example@paytm` or `example@upi`

⚠️ Make sure UPI is in correct format.
"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
📖 **Help Guide**

1️⃣ Send your UPI ID
2️⃣ Bot will process it
3️⃣ Get cashback/referral status

✅ Valid UPI formats:
- username@paytm
- username@upi
- username@oksbi
- username@ybl

❌ Invalid formats:
- username (missing @)
- username@gmail.com (not UPI)
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_upi(message):
    upi = message.text.strip()
    
    # Send processing message
    processing_msg = bot.reply_to(message, "⏳ Processing your UPI... Please wait.")
    
    try:
        result = process_upi(upi)
        bot.edit_message_text(result, chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode='Markdown')
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", chat_id=message.chat.id, message_id=processing_msg.message_id)

# ========== RUN BOT ==========
if __name__ == "__main__":
    print("🤖 Bot is running...")
    print("Bot Username: @UPIRefeerBot")
    print("Press Ctrl+C to stop.")
    bot.infinity_polling()
