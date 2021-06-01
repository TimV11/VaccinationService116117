# This file works with Twilio. To use it create a twilio account and insert your account_sid and auth_token.
# You get the from_whatsapp_number on this Twilio page too.
# Insert your phone number into to_whatsapp_number formatted like: "whatsapp: +49 11111111111"

from twilio.rest import Client

def send_wa(message):
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    from_whatsapp_number = ""
    to_whatsapp_number = ""
    client.messages.create(body = message, from_ = from_whatsapp_number, to = to_whatsapp_number)