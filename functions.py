import requests
from dotenv import load_dotenv
import os
import sqlite3


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
greeting=['HI','HELLO','SALAM','SLM','SALUT','BONJOUR','HEY']
#the main function
def handle_messages(data):
    sender_id, text = get_message(data)
    text_splited = text.upper().split(' ')
    commande = text_splited[0].upper()
    if commande in greeting: #greeting
        send_text_message(sender_id,"Hello! How can I help you?\nmy friend")
    elif commande.upper() !='GET':
        send_text_message(sender_id, f"la commande '{commande}' n'existe pas f had lbot lhrban")
    elif commande.upper() == 'GET' and len(text_splited) == 4:
        course_name, course_type, indice = text_splited[1], text_splited[2], text_splited[3]

        # Connect to SQLite DB
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()

        # Query the database
        cursor.execute("SELECT url FROM courses WHERE element = ? AND type = ? AND indice = ? AND state = 1", (course_name, course_type, indice))
        result = cursor.fetchone()

        conn.close()

        # Check result and respond
        if result:
            File_URL = result[0]
            send_pdf_message(File_URL, sender_id)
        else:
            send_text_message(sender_id, "Not found")
    else:
        send_text_message(sender_id, "Invalid Syntax")

def get_message(data):
    sender_id = ''  
    text = ''       
    
    for entry in data.get('entry', []):
        for change in entry.get('changes', []):
            if change.get('field') == 'messages':
                for msg in change.get('value', {}).get('messages', []):
                    sender_id = msg.get('from','')
                    sender_id='+'+sender_id
                    text = msg.get('text', {}).get('body', '')
                    print(sender_id, ':', text)
    return sender_id, text 

def send_text_message(recipient_id, text):
    url = f"https://graph.facebook.com/v13.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=data)
    
def send_pdf_message(pdf_url, recipient_id):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "document",
        "document": {
            "link": pdf_url,
            "caption": "here is ur pdf ^_^"
        }
    }
    requests.post(url, headers=headers, json=data)

def send_image_message(image_url, recipient_id):
    """
    Send an image to a WhatsApp number via a link.

    Args:
    image_url (str): Direct URL to the image.
    recipient_id (str): WhatsApp ID of the recipient.
    """
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": "here is ur img ^_^"
        }
    }

    requests.post(url, headers=headers, json=data)