import telebot
import requests
import json
import random
import hashlib
import re
from time import sleep
import sys

# ========== BOT CONFIGURATION ==========
BOT_TOKEN = "8575561951:AAHC8G5vGG24_v_W9sslfU38pQdVt0G8GMA"
SECRET_KEY = "*dkaSDs#*k9487ld!*kaSJDsj9784@dsk!!dHD@dka820#SD!sk192@"

# ========== FORCE CLEANUP - CRITICAL ==========
def force_cleanup():
    print("🧹 Cleaning up previous bot instances...")
    
    # Delete webhook
    try:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
        print(f"✅ Webhook deleted: {response.json()}")
    except Exception as e:
        print(f"❌ Webhook delete error: {e}")
    
    # Clear all pending updates with massive offset
    try:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=1000000000000&timeout=1")
        print(f"✅ Pending updates cleared: {response.json()}")
    except Exception as e:
        print(f"❌ Clear updates error: {e}")
    
    # Try multiple times to ensure cleanup
    sleep(2)
    try:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=-1")
        print(f"✅ Final cleanup: {response.json()}")
    except Exception as e:
        print(f"❌ Final cleanup error: {e}")
    
    sleep(3)
    print("✅ Cleanup complete!\n")

# Run cleanup first
force_cleanup()

# ========== INIT BOT ==========
print("🤖 Initializing bot...")
bot = telebot.TeleBot(BOT_TOKEN)

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
    print(f"📝 Processing UPI: {upi}")
    
    # Validate UPI format
    if not re.match(r'^[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}$', upi):
        return "❌ *Invalid UPI Format!*\n\nPlease send a valid UPI ID.\n\n✅ Examples:\n- `example@paytm`\n- `example@upi`\n- `example@oksbi`"

    fname = generate_name()
    email = f"{fname}{random.randint(1000,9000)}@gmail.com"
    num = generate_mobile()
    
    results = []
    msg = "Processing..."
    status = ""
    
    print(f"👤 Generated: {fname} | 📱 {num} | 📧 {email}")
    
    # ---------- 1. Save User Detail ----------
    try:
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
        results.append("✅ User detail saved")
        print(f"📝 User response: {response[:100]}...")
    except Exception as e:
        results.append(f"❌ User detail error: {str(e)}")
        print(f"❌ User detail error: {e}")
    
    # ---------- 2. Save Answers ----------
    try:
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
        results.append("✅ Answers saved")
        print(f"📋 Answers response: {response[:100]}...")
    except Exception as e:
        results.append(f"❌ Answers error: {str(e)}")
        print(f"❌ Answers error: {e}")
    
    # ---------- 3. Save UPI Info ----------
    try:
        url = "https://web.myfidelity.in/api/v1/parachute_rosemary/save-upi-info"
        data = json.dumps({"vpa": upi})
        checksum = generate_checksum(data, SECRET_KEY)
        headers["checksum"] = checksum
        response = http_call(url, "POST", data, headers)
        results.append("✅ UPI saved")
        print(f"💳 UPI response: {response[:100]}...")
        
        # Parse response
        json_response = json.loads(response)
        msg = json_response.get("msg", "UPI saved successfully")
        status = json_response.get("status", "")
    except Exception as e:
        results.append(f"❌ UPI save error: {str(e)}")
        print(f"❌ UPI save error: {e}")
        msg = "Error saving UPI"
    
    # ---------- 4. Redemption (if SUCCESS) ----------
    if status == "SUCCESS":
        try:
            url = "https://web.myfidelity.in/api/v1/parachute_rosemary/redemption"
            data = json.dumps({"redemptionType": "CASHBACK"})
            checksum = generate_checksum(data, SECRET_KEY)
            headers["checksum"] = checksum
            response = http_call(url, "POST", data, headers)
            json_response = json.loads(response)
            msg = json_response.get("msg", "🎉 Cashback Redeemed Successfully!")
            results.append("✅ Redemption completed")
            print(f"🎉 Redemption response: {response[:100]}...")
        except Exception as e:
            results.append(f"❌ Redemption error: {str(e)}")
            print(f"❌ Redemption error: {e}")
            msg = "Redemption attempt made"
    
    # Build final message
    final_msg = f"""✅ *UPI Processing Complete!*

👤 *Name:* {fname}
📱 *Mobile:* {num}
📧 *Email:* {email}
💳 *UPI:* {upi}

📌 *Status:* {msg}

📊 *Steps:*
{chr(10).join(results)}

🤖 *Bot:* @UPIRefeerBot"""
    
    return final_msg

# ========== TELEGRAM BOT HANDLERS ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user.first_name or "User"
    welcome_text = f"""🌟 *Welcome to 10₹ UPI Bot!* 🌟

Hello {user}! 👋

Send me your UPI ID and I'll process it.

📌 *How to use:*
Just type your UPI ID and send.

📝 *Example:* `example@paytm`

⚠️ Make sure UPI is in correct format.

Type /help for more info"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """📖 *Help Guide*

1️⃣ Send your UPI ID
2️⃣ Bot will process it
3️⃣ Get confirmation

✅ *Valid UPI formats:*
• `username@paytm`
• `username@upi`
• `username@oksbi`
• `username@ybl`

❌ *Invalid formats:*
• username (no @)
• username@gmail.com

🔗 *Bot:* @UPIRefeerBot"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def send_status(message):
    status_text = """🤖 *Bot Status*

✅ Bot is running
✅ Connected to Telegram
✅ Ready to process UPIs

📊 *Commands:*
/start - Welcome
/help - Help guide
/status - Bot status

💳 Send any UPI to process"""
    bot.reply_to(message, status_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_upi(message):
    upi = message.text.strip()
    
    # Skip if too short
    if len(upi) < 5:
        bot.reply_to(message, "❌ Please send a valid UPI ID.\n\nExample: `example@paytm`", parse_mode='Markdown')
        return
    
    # Send processing message
    processing_msg = bot.reply_to(message, "⏳ *Processing your UPI...*\nPlease wait a moment.", parse_mode='Markdown')
    
    try:
        result = process_upi(upi)
        bot.edit_message_text(result, chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode='Markdown')
    except Exception as e:
        error_msg = f"❌ *Error:* {str(e)}\n\nPlease try again or contact support."
        bot.edit_message_text(error_msg, chat_id=message.chat.id, message_id=processing_msg.message_id, parse_mode='Markdown')
        print(f"❌ Error processing UPI: {e}")

# ========== ERROR HANDLER ==========
def handle_errors(message, error):
    print(f"❌ Error: {error}")
    bot.reply_to(message, "❌ Something went wrong. Please try again.")

# ========== RUN BOT WITH RETRY ==========
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 UPI Referral Bot Starting...")
    print(f"📱 Bot: @UPIRefeerBot")
    print("=" * 50)
    
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        try:
            print(f"🔄 Attempt {retry_count + 1}/{max_retries}")
            print("✅ Bot is running...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            retry_count += 1
            print(f"❌ Error: {e}")
            print(f"🔄 Retry {retry_count}/{max_retries} in 10 seconds...")
            sleep(10)
            
            # Try cleanup again
            try:
                requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
                requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=1000000000")
            except:
                pass
            
            if retry_count >= max_retries:
                print("❌ Max retries reached. Exiting...")
                sys.exit(1)
            continue
        break
