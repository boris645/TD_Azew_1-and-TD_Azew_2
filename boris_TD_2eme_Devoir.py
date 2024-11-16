"""
1
Avant de commencer, il te faudra :

Créer un compte Twilio ici.
Installer les bibliothèques nécessaires :
bash
Copier le code


"""

#pip install Flask twilio schedule

"""
2

Phase 1 : Authentification à deux facteurs (2FA)
Étape 1 : Configuration Twilio
Obtiens les identifiants nécessaires sur le tableau de bord Twilio, à savoir le SID, le Token et le numéro de téléphone Twilio (ex : +1234567890).

"""

#from twilio.rest import Client

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

"""
3

Étape 2 : Code Python pour l'authentification à deux facteurs
Voici un exemple d'implémentation d'un système d'authentification à deux facteurs utilisant Twilio pour envoyer un OTP par SMS :

"""
#from flask import Flask, request, render_template, redirect, url_for, flash
from twilio.rest import Client
import random
import os

# Configuration Twilio
TWILIO_PHONE = '+1234567890'  # Numéro Twilio
TWILIO_SID = 'your_twilio_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'

#Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Liste fictive des utilisateurs
users_db = {
    'john_doe': {
        'password': 'password123',
        'phone': '+0987654321'  # Numéro de téléphone de l'utilisateur
    }
}

# Fonction pour envoyer un OTP par SMS via Twilio
def send_otp(phone_number):
    otp = random.randint(100000, 999999)
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Votre code de validation est : {otp}",
        from_=TWILIO_PHONE,
        to=phone_number
    )
    return otp

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Vérification des informations de connexion
    if username in users_db and users_db[username]['password'] == password:
        # Envoi de l'OTP
        otp = send_otp(users_db[username]['phone'])
        # Stockage temporaire de l'OTP pour la vérification suivante
        session['otp'] = otp
        session['username'] = username
        return render_template('verify_otp.html')
    else:
        flash('Nom d\'utilisateur ou mot de passe incorrect.')
        return redirect(url_for('home'))

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    otp_input = int(request.form['otp'])
    if otp_input == session.get('otp'):
        return redirect(url_for('dashboard'))
    else:
        flash('Le code OTP est incorrect.')
        return redirect(url_for('verify_otp'))

@app.route('/dashboard')
def dashboard():
    return f"Bienvenue, {session.get('username')}! Vous êtes connecté."

if __name__ == '__main__':
    app.run(debug=True)
 """
 Explication du code :

Flask Application : On crée une application web avec Flask.
Twilio API : Utilisation de la bibliothèque Twilio pour envoyer un OTP par SMS.
Login et Vérification de l'OTP : L'utilisateur se connecte avec un nom d'utilisateur et un mot de passe.
 Si ces informations sont valides, un OTP est envoyé au téléphone de l'utilisateur via Twilio.
 L'utilisateur doit ensuite entrer ce code dans un formulaire pour vérifier l'authentification.
 
 """

"""
Phase 2 : Rappels et Gestion des Rendez-vous
Cette phase implique l'envoi de rappels de rendez-vous et la possibilité de modifier ou annuler les rendez-vous par SMS.

Étape 1 : Rappels 30 minutes avant le rendez-vous
On va utiliser schedule pour gérer l'envoi de rappels 30 minutes avant un rendez-vous.


"""

from twilio.twiml.messaging_response import MessagingResponse

@app.route('/sms', methods=['POST'])
def sms_reply():
    message_body = request.form['Body'].strip().lower()
    user_phone = request.form['From']
    
    response = MessagingResponse()
    
    if message_body == 'annuler':
        # Annuler le rendez-vous
        for appointment in appointments:
            if appointment['phone'] == user_phone:
                appointments.remove(appointment)
                response.message("Votre rendez-vous a été annulé.")
                break
    elif message_body == 'modifier':
        # Exemple de modification du rendez-vous
        for appointment in appointments:
            if appointment['phone'] == user_phone:
                appointment['time'] = datetime(2024, 11, 15, 15, 0)  # Nouvelle heure
                response.message("Votre rendez-vous a été modifié.")
                break
    else:
        response.message("Veuillez répondre par 'Annuler' ou 'Modifier' pour gérer votre rendez-vous.")
    
    return str(response)
