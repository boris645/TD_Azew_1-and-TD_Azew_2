from twilio.rest import Client

# Identifiants Twilio
account_sid = 'ACdc28752f047d34b18ebf7d1d3a146da3'
auth_token = '5fa79b167b5045022b66b95fa6043abb'

# Initialisation du client Twilio
client = Client(account_sid, auth_token)

# Envoi du message
message = client.messages.create(
    body="Ceci est un message de test depuis Twilio.",
    from_='+18777804236',  # Numéro Twilio
    to='+237655480368'      # Numéro du destinataire
)

print(f"Message envoyé : {message.sid}")
