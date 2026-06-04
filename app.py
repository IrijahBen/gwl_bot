import os
import requests
import random
from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = FastAPI(title="Goodwill Language Solution Automated Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

# ==========================================
# 🧠 UNIFIED STATE MANAGEMENT
# ==========================================
user_states = {} 
conversation_histories = {}

STATE_BOT = "bot"
STATE_HUMAN = "human"

# ==========================================
# 📱 WHATSAPP MESSAGE SENDERS
# ==========================================

def send_whatsapp_text(to_number: str, text: str):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to_number, "type": "text", "text": {"body": text}}
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code != 200:
        print(f"Meta Error (Text): {r.text}")

def send_whatsapp_list(to_number: str, text: str, button_text: str, sections: list):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp", "to": to_number, "type": "interactive",
        "interactive": {"type": "list", "body": {"text": text}, "action": {"button": button_text, "sections": sections}}
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code != 200:
        print(f"Meta Error (List): {r.text}")

def send_whatsapp_buttons(to_number: str, text: str, buttons: list):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    action_btns = [{"type": "reply", "reply": {"id": b_id, "title": b_title}} for b_id, b_title in buttons]
    payload = {
        "messaging_product": "whatsapp", "to": to_number, "type": "interactive",
        "interactive": {"type": "button", "body": {"text": text}, "action": {"buttons": action_btns}}
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code != 200:
        print(f"Meta Error (Buttons): {r.text}")

# ==========================================
# 🛣️ THE MASTER FLOW LOGIC
# ==========================================

def get_flow_response(user_id: str, text_input: str, action_id: str):
    if user_id not in user_states:
        user_states[user_id] = STATE_BOT
        
    current_state = user_states[user_id]
    
    # 1. Human Takeover Active
    if current_state == STATE_HUMAN:
        if text_input in ["0", "menu"]:
            user_states[user_id] = STATE_BOT
        else:
            return {"type": "ignore"}

    # 2. Initial Greetings (Silent trigger or manual text)
    if text_input in ["hi", "hello", "hey", "good morning", "good afternoon", "good day"] or action_id == "init_greeting":
        return {
            "type": "text",
            "text": "Good day! 👋 How are you doing today?"
        }

    # Small talk response
    if text_input in ["im fine", "i'm fine", "good", "great", "doing well"]:
        return {
            "type": "buttons",
            "text": "Awesome! Glad to hear that. 😊\n\nHow may we help you today? Do you require any of our certified language services?\nSelect an option below",
            "buttons": [("btn_yes_services", "Yes, I need services"), ("btn_browse", "Just browsing menu")]
        }

    # 3. Main Menu Trigger
    if action_id in ["btn_yes_services", "btn_browse"] or text_input in ["0", "menu", "just browsing menu"]:
        user_states[user_id] = STATE_BOT
        return {
            "type": "list_grouped", 
            "text": "Goodwill Language Solution 🌍\n\nWelcome! We are certified language service providers in Africa since 2017.\n\nServing 27 countries worldwide. How can we help you today?\n\ngoodwilllanguage.com",
            "btn_text": "View Our Services",
            "sections": [
                {
                    "title": "Our Services",
                    "rows": [
                        {"id": "service_doc", "title": "📄 Document Translation", "description": "Legal, academic, medical & corporate"},
                        {"id": "service_interp", "title": "🗣️ Interpretation", "description": "Conferences, courts, meetings"},
                        {"id": "service_sub", "title": "🎬 Subtitling & Voiceover", "description": "Videos, films, podcasts"},
                        {"id": "service_class", "title": "📚 Language Classes", "description": "Online 24/7, all languages"},
                        {"id": "service_trans", "title": "📝 Transcription", "description": "Audio & video to text"},
                        {"id": "service_equip", "title": "🎧 Equipment Rental", "description": "Conference interpretation gear"},
                        {"id": "service_help", "title": "Get Help", "description": ""}
                    ]
                }
            ]
        }

    # ==========================================
    # 📁 4. SERVICE SUBCATEGORY ROUTING
    # ==========================================

    # --- DOCUMENT TRANSLATION ---
    if action_id == "service_doc":
        return {
            "type": "list_grouped",
            "text": "🔤 *Document Translation*\n\nWe translate all document types with certified linguists in 30+ languages.\n\nSelect a document category:",
            "btn_text": "Select Document Type",
            "sections": [
                {
                    "title": "Categories",
                    "rows": [
                        {"id": "cat_legal", "title": "⚖️ Legal & Court Docs", "description": "Court orders, affidavits, contracts"},
                        {"id": "cat_academic", "title": "🎓 Academic Papers", "description": "Transcripts, degrees, certificates"},
                        {"id": "cat_medical", "title": "🏥 Medical & Reports", "description": "Clinical studies, patient forms"},
                        {"id": "cat_business", "title": "💼 Business & Corporate", "description": "Financial reports, manuals, pitches"}
                    ]
                },
                {
                    "title": "Quick Actions",
                    "rows": [
                        {"id": "btn_back", "title": "🔙 Back to Menu", "description": "View all services"}
                    ]
                }
            ]
        }

    # --- INTERPRETATION ---
    elif action_id == "service_interp":
        return {
            "type": "list_grouped",
            "text": "📋 *Interpretation Services*\n\nProfessional interpretation for conferences, courts, meetings & NGO events.\n\nSelect an interpretation type:\nAvailable in 30+ languages worldwide",
            "btn_text": "Select Type",
            "sections": [
                {
                    "title": "Interpretation Types",
                    "rows": [
                        {"id": "interp_simul", "title": "🔄 Simultaneous", "description": "Real-time interpretation"},
                        {"id": "interp_consec", "title": "🔄 Consecutive", "description": "After-speech interpretation"},
                        {"id": "interp_remote", "title": "💻 Remote / Online", "description": "Virtual interpretation"},
                        {"id": "interp_whisper", "title": "🗣️ Whisper", "description": "1-on-1 quiet interpretation"}
                    ]
                },
                {
                    "title": "Quick Actions",
                    "rows": [
                        {"id": "btn_quote", "title": "💰 Get a Quote", "description": "Request pricing"},
                        {"id": "btn_back", "title": "🔙 Back to Menu", "description": "View all services"}
                    ]
                }
            ]
        }

    # --- SUBTITLING & VOICEOVER ---
    elif action_id == "service_sub":
        return {
            "type": "list_grouped",
            "text": "🎬 *Subtitling & Voiceover*\n\nTransform your multimedia content for a global audience with localized accents, timed subtitles, and clear tone script translations.",
            "btn_text": "Select Video Service",
            "sections": [
                {
                    "title": "Multimedia Services",
                    "rows": [
                        {"id": "sub_burn", "title": "🎞️ Video Subtitling", "description": "Hardcoded captions or SRT creation"},
                        {"id": "sub_vo", "title": "🎙️ Professional Voiceover", "description": "Multi-language voice talent & synchronization"},
                        {"id": "sub_cc", "title": "💬 Closed Captioning", "description": "Accessibility formats for compliance"}
                    ]
                },
                {
                    "title": "Quick Actions",
                    "rows": [
                        {"id": "btn_back", "title": "🔙 Back to Menu", "description": "View all services"}
                    ]
                }
            ]
        }

    # --- LANGUAGE CLASSES ---
    elif action_id == "service_class":
        return {
            "type": "list_grouped",
            "text": "📚 *Language Classes*\n\nMaster a language with customized study schedules. Available 24/7 online for children, working professionals, and migrating individuals.",
            "btn_text": "Select Class Type",
            "sections": [
                {
                    "title": "Training Programs",
                    "rows": [
                        {"id": "class_corp", "title": "🏢 Corporate Training", "description": "Language skills tailored for teams"},
                        {"id": "class_exam", "title": "📝 Exam Preparation", "description": "IELTS, TOEFL, TEF, DELF training"},
                        {"id": "class_gen", "title": "🗣️ General Conversation", "description": "Fluency from beginner to advanced level"}
                    ]
                },
                {
                    "title": "Quick Actions",
                    "rows": [
                        {"id": "btn_back", "title": "🔙 Back to Menu", "description": "View all services"}
                    ]
                }
            ]
        }

    # --- TRANSCRIPTION ---
    elif action_id == "service_trans":
        return {
            "type": "list_grouped",
            "text": "📝 *Transcription Services*\n\nConvert audio or video recordings into highly accurate text. We accept multiple audio formats and deliver clean files.",
            "btn_text": "Select Transcript Type",
            "sections": [
                {
                    "title": "Transcription Forms",
                    "rows": [
                        {"id": "trans_verbatim", "title": "🎯 Full Verbatim", "description": "Includes filler words, stutters, and laughs"},
                        {"id": "trans_clean", "title": "✨ Clean Read", "description": "Polished text with grammar corrections"},
                        {"id": "trans_legal", "title": "⚖️ Interview & Legal", "description": "Timestamps, court-ready format"}
                    ]
                },
                {
                    "title": "Quick Actions",
                    "rows": [
                        {"id": "btn_back", "title": "🔙 Back to Menu", "description": "View all services"}
                    ]
                }
            ]
        }

    # --- EQUIPMENT RENTAL ---
    elif action_id == "service_equip":
        return {
            "type": "list_grouped",
            "text": "🎧 *Equipment Rental*\n\nHigh-grade physical transmission hardware for multi-lingual physical events, workshops, and international congress conferences.",
            "btn_text": "Select Equipment Type",
            "sections": [
                {
                    "title": "Conference Hardware",
                    "rows": [
                        {"id": "eq_booth", "title": "🛖 Soundproof Booths", "description": "Full-size translation enclosures"},
                        {"id": "eq_headset", "title": "🎧 Headsets & Receivers", "description": "Wireless frequency listener units"},
                        {"id": "eq_pa", "title": "🎙️ Mics & PA Sound Systems", "description": "Complete audio distribution network"}
                    ]
                },
                {
                    "title": "Quick Actions",
                    "rows": [
                        {"id": "btn_back", "title": "🔙 Back to Menu", "description": "View all services"}
                    ]
                }
            ]
        }

    # ==========================================
    # 🔍 5. SUBCATEGORY DETAIL & SCREEN RESPONSES
    # ==========================================

    # --- DOCUMENT SELECTIONS ---
    elif action_id == "cat_legal":
        return {
            "type": "buttons",
            "text": "⚖️ *Legal Documents*\n\nWe handle this translation category with certified native linguists.\n\n✔️ 30+ languages available\n✔️ Certified & accurate\n✔️ Fast turnaround time\n\nWhat would you like to do next?",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "cat_academic":
        return {
            "type": "buttons",
            "text": "🎓 *Academic Papers & Transcripts*\n\nOfficial certified translations recognized by foreign universities, embassies, and evaluation bodies globally.\n\n✔️ Accepted by WES / IQAS\n✔️ Highly precise conversion\n✔️ Global stamp verification",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "cat_medical":
        return {
            "type": "buttons",
            "text": "🏥 *Medical Documentation*\n\nStrictly confidential translations handling diagnostic write-ups, pharmaceutical labels, and laboratory documentation.\n\n✔️ Compliant data standard protocols\n✔️ Experienced subject experts\n✔️ Dual-checked verification systems",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "cat_business":
        return {
            "type": "buttons",
            "text": "💼 *Business & Corporate Content*\n\nLocalization for operational policy profiles, financial statement documents, cross-border marketing, and manuals.\n\n✔️ Matches corporate style guide standards\n✔️ High scale volumes support\n✔️ Native market terminology optimization",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }

    # --- INTERPRETATION SELECTIONS ---
    elif action_id == "interp_simul":
        return {
            "type": "buttons",
            "text": "🔄 *Simultaneous Interpretation*\n\nReal-time delivery ideal for high-profile gatherings, corporate boardrooms, or multi-national live summits.\n\n✔️ Zero latency feedback processing\n✔️ Dual-linguist rotation systems\n✔️ Seamless integration options",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "interp_consec":
        return {
            "type": "buttons",
            "text": "🔄 *Consecutive Interpretation*\n\nThe linguist speaks immediately after the speaker pauses. Perfect for courts, diplomatic meetings, and press rooms.\n\n✔️ Detailed notes capture\n✔️ Professional stage presence\n✔️ 30+ languages available",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "interp_remote":
        return {
            "type": "buttons",
            "text": "💻 *Remote / Online Interpretation*\n\nVirtual language support using digital conference lines via Zoom, MS Teams, or specialized RSI nodes.\n\n✔️ Reduced transit travel expenses\n✔️ Rapid operational setup times\n✔️ Clean digital remote lines",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "interp_whisper":
        return {
            "type": "buttons",
            "text": "🗣️ *Whisper Interpretation*\n\nLow-profile acoustic translation targeting very small executive groups or singular client delegates directly on-site.\n\n✔️ Discreet 1-on-1 language translation\n✔️ Mobile flexibility across floors\n✔️ Ideal for exclusive business tours",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }

    # --- SUBTITLING & VOICEOVER SELECTIONS ---
    elif action_id == "sub_burn":
        return {
            "type": "buttons",
            "text": "🎞️ *Video Subtitling*\n\nAccurately timed captions localized matching contextual humor, terminology, and character styles.\n\n✔️ SRT, VTT, or hardcoded options\n✔️ Highly precise frame timestamps\n✔️ Clean readability designs",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "sub_vo":
        return {
            "type": "buttons",
            "text": "🎙️ *Professional Voiceover*\n\nNative speaker audio actors delivering studio-quality recordings with correct vocal inflections for videos and films.\n\n✔️ Access to male/female voice assets\n✔️ Crystal-clear audio clarity studio files\n✔️ Localized pacing match",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "sub_cc":
        return {
            "type": "buttons",
            "text": "💬 *Closed Captioning (CC)*\n\nFull access accommodation files providing dialogue transcription text plus non-speech audios like sound effect alerts.\n\n✔️ Strict regulatory compliance standards\n✔️ Ideal for broadcasting systems\n✔️ High accuracy verification checking",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }

    # --- LANGUAGE CLASS SELECTIONS ---
    elif action_id == "class_corp":
        return {
            "type": "buttons",
            "text": "🏢 *Corporate Language Training*\n\nEmpower your company team to handle international communication requirements confidently.\n\n✔️ Industry terminology frameworks\n✔️ Group performance analytics tracking\n✔️ Flexible booking routines",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "class_exam":
        return {
            "type": "buttons",
            "text": "📝 *Exam Preparation (IELTS/TEF/DELF)*\n\nStrategic targeted practice designed to guarantee maximum score potentials for migratory compliance tests.\n\n✔️ Mock simulations feedback runs\n✔️ Experienced language instructors\n✔️ Curated custom study materials",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "class_gen":
        return {
            "type": "buttons",
            "text": "🗣️ *General Conversational Classes*\n\nInteractive practical speech practice focusing on everyday socialization vocabulary and accent ease.\n\n✔️ Practical live situational dialogues\n✔️ Fun immersive native tasks\n✔️ All base skill tier tracks",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }

    # --- TRANSCRIPTION SELECTIONS ---
    elif action_id == "trans_verbatim":
        return {
            "type": "buttons",
            "text": "🎯 *Full Verbatim Transcription*\n\nCaptures every acoustic detail exactly as spoken, including ambient noises, false starts, and filler words.\n\n✔️ Great for detailed academic analyses\n✔️ Highly objective records logging\n✔️ Exact raw audio capture tracking",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "trans_clean":
        return {
            "type": "buttons",
            "text": "✨ *Clean Read Transcription*\n\nRemoves verbal pauses, stutters, and filler phrases, leaving a polished, readable document.\n\n✔️ Ideal for corporate memos and press releases\n✔️ Professional presentation format\n✔️ Highly polished grammar checks",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "trans_legal":
        return {
            "type": "buttons",
            "text": "⚖️ *Interview & Legal Transcription*\n\nSpecialized documentation with formal timestamps and speaker tags configured for official court review processes.\n\n✔️ Clean legal formatting standard templates\n✔️ Secure confidential handling protocols\n✔️ Strict cross-referenced spell-checking",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }

    # --- EQUIPMENT SELECTIONS ---
    elif action_id == "eq_booth":
        return {
            "type": "buttons",
            "text": "🛖 *Soundproof Interpretation Booths*\n\nISO-compliant portable acoustic containment enclosures giving translators a quiet environment during events.\n\n✔️ Full sound isolation filters\n✔️ Standard internal ventilation fan units\n✔️ Rapid technical team setup deployment",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "eq_headset":
        return {
            "type": "buttons",
            "text": "🎧 *Headsets & Multi-channel Receivers*\n\nLightweight wireless receiver nodes allowing multi-language audiences to switch channels instantly.\n\n✔️ Long-range signal reception tracking\n✔️ Crystal-clear audio stream fidelity\n✔️ Sanitized individual units packaging",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
    elif action_id == "eq_pa":
        return {
            "type": "buttons",
            "text": "🎙️ *Mics & PA Sound Systems*\n\nComplete venue audio integration combining mixing boards, tabletop micro-units, and amplification arrays.\n\n✔️ Zero frequency drop-off interference\n✔️ Dedicated on-site field engineers\n✔️ Matches both small and large setups",
            "buttons": [("btn_quote", "💰 Get a Quote"), ("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }

    # ==========================================
    # ⚙️ 6. UTILITY GLOBAL ACTIONS
    # ==========================================
    elif action_id == "btn_quote":
        return {
            "type": "buttons",
            "text": "💰 *Request a Quote*\n\nTo give you an accurate quote, please tell us:\n\n1️⃣ Service needed\n2️⃣ Language pair (e.g. English -> French)\n3️⃣ Pages / duration / file length\n4️⃣ Your deadline\n\nWe reply within 30 minutes during business hours ⏱️\n\nMon-Sat 8am-6pm WAT",
            "buttons": [("btn_specialist", "👤 Talk to Specialist"), ("btn_back", "🔙 Back to Menu")]
        }
        
    elif action_id in ["btn_specialist", "service_help"]:
        # IMMEDIATELY hands over without asking for a name or generating tokens
        user_states[user_id] = STATE_HUMAN
        return {
            "type": "handover",
            "text": "📝 *Connecting to Live Specialist...*\n\nPlease stay on the chat. A human Language Specialist will join this conversation and reply to you directly in just a moment.\n\n💡 _If you'd rather keep using the automated service, just type *0* or *menu* at any time._",
            "agent_alert": f"🚨 *NEW CUSTOMER HANDOVER* 🚨\n\n📞 Contact ID: {user_id}\n🌐 Service Required: SPECIALIST ASSISTANCE\n\n🤖 _The chatbot is now OFF for this client._"
        }
        
    elif action_id == "btn_back":
        user_states[user_id] = STATE_BOT
        return get_flow_response(user_id, "menu", "")

    # 7. GROQ AI Fallback (Answers unstructured queries intelligently)
    if text_input:
        try:
            if user_id not in conversation_histories:
                conversation_histories[user_id] = []
            
            conversation_histories[user_id].append({"role": "user", "content": text_input})
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "You are Goodwill Language Solution's AI. Keep replies under 2 sentences. Be helpful."}] + conversation_histories[user_id][-5:]
            )
            ai_reply = response.choices[0].message.content
            conversation_histories[user_id].append({"role": "assistant", "content": ai_reply})
            
            return {
                "type": "buttons",
                "text": ai_reply,
                "buttons": [("btn_back", "📋 View Menu")]
            }
        except Exception as e:
            print(f"Groq Error: {e}")
            return get_flow_response(user_id, "menu", "")

    return {"type": "ignore"}

# ==========================================
# 📱 WHATSAPP WEBHOOK
# ==========================================

def background_whatsapp_worker(sender_phone, message):
    msg_type = message.get("type")
    text_input = message["text"]["body"].strip().lower() if msg_type == "text" else ""
    action_id = ""
    
    if msg_type == "interactive":
        interactive_data = message["interactive"]
        action_id = interactive_data.get("list_reply", {}).get("id") or interactive_data.get("button_reply", {}).get("id")
        
    resp = get_flow_response(sender_phone, text_input, action_id)
    
    if resp.get("type") == "list_grouped":
        send_whatsapp_list(sender_phone, resp["text"], resp["btn_text"], resp["sections"])
    elif resp.get("type") == "buttons":
        send_whatsapp_buttons(sender_phone, resp["text"], resp["buttons"])
    elif resp.get("type") == "text":
        send_whatsapp_text(sender_phone, resp["text"])
    elif resp.get("type") == "handover":
        send_whatsapp_text(sender_phone, resp["text"])
        send_whatsapp_text(sender_phone, resp["agent_alert"])

@app.get("/webhook")
async def verify_webhook(request: Request):
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get("hub.verify_token") == VERIFY_TOKEN:
        return Response(content=request.query_params.get("hub.challenge"), media_type="text/plain")
    return Response(content="Verification failed", status_code=403)

@app.post("/webhook")
async def receive_whatsapp(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    try:
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" in value:
                    for message in value["messages"]:
                        sender_phone = message["from"]
                        background_tasks.add_task(background_whatsapp_worker, sender_phone, message)
    except Exception as e:
        print(f"Webhook Parse Error: {e}")
    return {"status": "ok"}

# ==========================================
# 🌐 WEBSITE CHAT ENDPOINT
# ==========================================

@app.post("/api/webchat")
async def handle_web_chat(request: Request):
    body = await request.json()
    session_id = body.get("session_id", "anonymous_user")
    text_input = body.get("message", "").strip().lower()
    action_id = body.get("action_id", "")
    
    resp = get_flow_response(session_id, text_input, action_id)
    return resp

if __name__ == "__main__":
    import uvicorn
    # Automatically grab Render's port, or default to 8000 locally
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
