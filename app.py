#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from datetime import datetime, timedelta
import json
import os
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
import uuid
import requests
import qrcode
from io import BytesIO
import base64
import platform
import subprocess
import psutil

app = Flask(__name__)
app.secret_key = 'becreative_secret_key_2026'

EMAIL_ADDRESS = 'nabiljouat602@gmail.com'
EMAIL_PASSWORD = 'wxtq ojih fsse ikpw'
MISTRAL_API_KEY = ''
MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat/completions'

LANGUAGES = {
    'fr': {
        'site_name': 'BeCreative',
        'tagline': 'Présentations Scolaires Professionnelles',
        'login': 'Connexion',
        'register': 'Inscription',
        'logout': 'Déconnexion',
        'dashboard': 'Tableau de bord',
        'new_request': 'Nouvelle demande',
        'my_requests': 'Mes demandes',
        'chatbot': 'Assistant IA',
        'profile': 'Profil',
        'email': 'Email',
        'password': 'Mot de passe',
        'name': 'Nom complet',
        'subject': 'Matière',
        'level': 'Niveau scolaire',
        'type': 'Type de document',
        'theme': 'Thème',
        'deadline': 'Date limite',
        'description': 'Description détaillée',
        'submit': 'Envoyer',
        'cancel': 'Annuler',
        'processing': 'Traitement en cours...',
        'loading': 'Chargement...',
        'success': 'Succès',
        'error': 'Erreur',
        'warning': 'Attention',
        'download': 'Télécharger',
        'view': 'Voir',
        'edit': 'Modifier',
        'delete': 'Supprimer',
        'status': 'Statut',
        'pending': 'En attente',
        'in_progress': 'En cours',
        'completed': 'Terminé',
        'cancelled': 'Annulé',
        'presentation_number': 'Numéro de présentation',
        'qr_code': 'QR Code',
        'forgot_password': 'Mot de passe oublié',
        'reset_password': 'Réinitialiser le mot de passe',
        'verify_account': 'Vérifier le compte',
        'otp_code': 'Code OTP',
        'send_code': 'Envoyer le code',
        'resend_code': 'Renvoyer le code',
        'new_password': 'Nouveau mot de passe',
        'confirm_password': 'Confirmer le mot de passe',
        'change_password': 'Changer le mot de passe',
        'admin_dashboard': 'Administration',
        'admin_requests': 'Gestion des demandes',
        'admin_users': 'Gestion des utilisateurs',
        'admin_logs': 'Journaux d\'activité',
        'admin_settings': 'Paramètres',
        'upload_file': 'Télécharger un fichier',
        'send_message': 'Envoyer un message',
        'reply': 'Répondre',
        'mark_completed': 'Marquer comme terminé',
        'generate_presentation': 'Générer la présentation',
        'no_requests': 'Aucune demande',
        'no_notifications': 'Aucune notification',
        'welcome': 'Bienvenue',
        'logout_confirm': 'Êtes-vous sûr de vouloir vous déconnecter',
        'delete_confirm': 'Êtes-vous sûr de vouloir supprimer',
        'file_required': 'Fichier requis',
        'file_size_limit': 'Taille maximale 50MB',
        'supported_formats': 'Formats supportés: PDF, PPT, DOC',
        'request_sent': 'Demande envoyée avec succès',
        'request_updated': 'Demande mise à jour',
        'request_completed': 'Demande terminée',
        'notification_new': 'Nouvelle notification',
        'chatbot_welcome': 'Bonjour, comment puis-je vous aider avec votre présentation',
        'chatbot_placeholder': 'Écrivez votre message...',
        'chatbot_send': 'Envoyer',
        'chatbot_typing': 'En train d\'écrire...',
        'history': 'Historique',
        'no_history': 'Aucun historique',
        'statistics': 'Statistiques',
        'total_requests': 'Total des demandes',
        'pending_requests': 'Demandes en attente',
        'completed_requests': 'Demandes terminées',
        'total_users': 'Utilisateurs',
        'recent_activity': 'Activité récente',
        'search': 'Rechercher',
        'filter': 'Filtrer',
        'sort_by': 'Trier par',
        'date': 'Date',
        'actions': 'Actions',
        'details': 'Détails',
        'close': 'Fermer',
        'save': 'Enregistrer',
        'print': 'Imprimer',
        'export': 'Exporter',
        'import': 'Importer',
        'settings': 'Paramètres',
        'language': 'Langue',
        'french': 'Français',
        'english': 'Anglais',
        'dark_mode': 'Mode sombre',
        'light_mode': 'Mode clair',
        'help': 'Aide',
        'contact': 'Contact',
        'about': 'À propos',
        'terms': 'Conditions d\'utilisation',
        'privacy': 'Politique de confidentialité',
        'all_rights_reserved': 'Tous droits réservés',
        'copyright': 'Copyright',
        'version': 'Version',
        'update': 'Mise à jour',
        'new': 'Nouveau',
        'old': 'Ancien',
        'first': 'Premier',
        'last': 'Dernier',
        'previous': 'Précédent',
        'next': 'Suivant',
        'page': 'Page',
        'of': 'sur',
        'results': 'Résultats',
        'no_results': 'Aucun résultat',
        'clear': 'Effacer',
        'refresh': 'Actualiser',
        'more': 'Plus',
        'less': 'Moins',
        'show': 'Afficher',
        'hide': 'Masquer',
        'enable': 'Activer',
        'disable': 'Désactiver',
        'on': 'Activé',
        'off': 'Désactivé',
        'yes': 'Oui',
        'no': 'Non',
        'ok': 'OK',
        'back': 'Retour',
        'home': 'Accueil',
        'menu': 'Menu',
        'open': 'Ouvrir',
        'collapse': 'Réduire',
        'expand': 'Développer',
        'usb_detected': 'Clé USB détectée',
        'usb_not_detected': 'Aucune clé USB détectée',
        'usb_copy': 'Copier sur la clé USB',
        'usb_copy_success': 'Copié sur la clé USB avec succès',
        'usb_copy_error': 'Erreur lors de la copie sur la clé USB'
    },
    'en': {
        'site_name': 'BeCreative',
        'tagline': 'Professional School Presentations',
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'dashboard': 'Dashboard',
        'new_request': 'New Request',
        'my_requests': 'My Requests',
        'chatbot': 'AI Assistant',
        'profile': 'Profile',
        'email': 'Email',
        'password': 'Password',
        'name': 'Full Name',
        'subject': 'Subject',
        'level': 'School Level',
        'type': 'Document Type',
        'theme': 'Theme',
        'deadline': 'Deadline',
        'description': 'Detailed Description',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'processing': 'Processing...',
        'loading': 'Loading...',
        'success': 'Success',
        'error': 'Error',
        'warning': 'Warning',
        'download': 'Download',
        'view': 'View',
        'edit': 'Edit',
        'delete': 'Delete',
        'status': 'Status',
        'pending': 'Pending',
        'in_progress': 'In Progress',
        'completed': 'Completed',
        'cancelled': 'Cancelled',
        'presentation_number': 'Presentation Number',
        'qr_code': 'QR Code',
        'forgot_password': 'Forgot Password',
        'reset_password': 'Reset Password',
        'verify_account': 'Verify Account',
        'otp_code': 'OTP Code',
        'send_code': 'Send Code',
        'resend_code': 'Resend Code',
        'new_password': 'New Password',
        'confirm_password': 'Confirm Password',
        'change_password': 'Change Password',
        'admin_dashboard': 'Administration',
        'admin_requests': 'Request Management',
        'admin_users': 'User Management',
        'admin_logs': 'Activity Logs',
        'admin_settings': 'Settings',
        'upload_file': 'Upload File',
        'send_message': 'Send Message',
        'reply': 'Reply',
        'mark_completed': 'Mark as Completed',
        'generate_presentation': 'Generate Presentation',
        'no_requests': 'No requests',
        'no_notifications': 'No notifications',
        'welcome': 'Welcome',
        'logout_confirm': 'Are you sure you want to logout',
        'delete_confirm': 'Are you sure you want to delete',
        'file_required': 'File required',
        'file_size_limit': 'Maximum size 50MB',
        'supported_formats': 'Supported formats: PDF, PPT, DOC',
        'request_sent': 'Request sent successfully',
        'request_updated': 'Request updated',
        'request_completed': 'Request completed',
        'notification_new': 'New notification',
        'chatbot_welcome': 'Hello, how can I help you with your presentation',
        'chatbot_placeholder': 'Type your message...',
        'chatbot_send': 'Send',
        'chatbot_typing': 'Typing...',
        'history': 'History',
        'no_history': 'No history',
        'statistics': 'Statistics',
        'total_requests': 'Total Requests',
        'pending_requests': 'Pending Requests',
        'completed_requests': 'Completed Requests',
        'total_users': 'Users',
        'recent_activity': 'Recent Activity',
        'search': 'Search',
        'filter': 'Filter',
        'sort_by': 'Sort by',
        'date': 'Date',
        'actions': 'Actions',
        'details': 'Details',
        'close': 'Close',
        'save': 'Save',
        'print': 'Print',
        'export': 'Export',
        'import': 'Import',
        'settings': 'Settings',
        'language': 'Language',
        'french': 'French',
        'english': 'English',
        'dark_mode': 'Dark Mode',
        'light_mode': 'Light Mode',
        'help': 'Help',
        'contact': 'Contact',
        'about': 'About',
        'terms': 'Terms of Use',
        'privacy': 'Privacy Policy',
        'all_rights_reserved': 'All rights reserved',
        'copyright': 'Copyright',
        'version': 'Version',
        'update': 'Update',
        'new': 'New',
        'old': 'Old',
        'first': 'First',
        'last': 'Last',
        'previous': 'Previous',
        'next': 'Next',
        'page': 'Page',
        'of': 'of',
        'results': 'Results',
        'no_results': 'No results',
        'clear': 'Clear',
        'refresh': 'Refresh',
        'more': 'More',
        'less': 'Less',
        'show': 'Show',
        'hide': 'Hide',
        'enable': 'Enable',
        'disable': 'Disable',
        'on': 'On',
        'off': 'Off',
        'yes': 'Yes',
        'no': 'No',
        'ok': 'OK',
        'back': 'Back',
        'home': 'Home',
        'menu': 'Menu',
        'open': 'Open',
        'collapse': 'Collapse',
        'expand': 'Expand',
        'usb_detected': 'USB drive detected',
        'usb_not_detected': 'No USB drive detected',
        'usb_copy': 'Copy to USB drive',
        'usb_copy_success': 'Successfully copied to USB drive',
        'usb_copy_error': 'Error copying to USB drive'
    }
}

def read_json(filename):
    try:
        if not os.path.exists(filename):
            if filename == 'users.json':
                default_admin = {
                    "users": [
                        {
                            "id": 1,
                            "email": "nabiljouat602@gmail.com",
                            "password": "nabil2019",
                            "name": "Administrateur",
                            "role": "admin",
                            "verified": True,
                            "created_at": datetime.now().isoformat(),
                            "last_login": datetime.now().isoformat()
                        }
                    ]
                }
                write_json(filename, default_admin)
                return default_admin
            return {}
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not data and filename == 'users.json':
                default_admin = {
                    "users": [
                        {
                            "id": 1,
                            "email": "nabiljouat602@gmail.com",
                            "password": "nabil2019",
                            "name": "Administrateur",
                            "role": "admin",
                            "verified": True,
                            "created_at": datetime.now().isoformat(),
                            "last_login": datetime.now().isoformat()
                        }
                    ]
                }
                write_json(filename, default_admin)
                return default_admin
            return data
    except:
        if filename == 'users.json':
            default_admin = {
                "users": [
                    {
                        "id": 1,
                        "email": "nabiljouat602@gmail.com",
                        "password": "nabil2019",
                        "name": "Administrateur",
                        "role": "admin",
                        "verified": True,
                        "created_at": datetime.now().isoformat(),
                        "last_login": datetime.now().isoformat()
                    }
                ]
            }
            write_json(filename, default_admin)
            return default_admin
        return {}

def write_json(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception as e:
        print(f"Erreur ecriture JSON: {e}")
        return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        if session['user']['role'] != 'admin':
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_lang():
    return session.get('lang', 'fr')

def get_text(key):
    lang = get_lang()
    return LANGUAGES.get(lang, LANGUAGES['fr']).get(key, key)

def send_email(to_email, subject, html_content):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg.attach(MIMEText(html_content, 'html'))
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Erreur email: {e}")
        return False

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def generate_id():
    return str(uuid.uuid4())[:12]

def generate_presentation_number():
    return f"BC-{random.randint(100000, 999999)}"

def generate_qr_code(data):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()
    except:
        return None

def get_usb_drives():
    drives = []
    system = platform.system()
    
    try:
        if system == 'Windows':
            import win32file
            for drive in win32file.GetLogicalDrives():
                if win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE:
                    drives.append(drive)
        elif system == 'Linux':
            for part in psutil.disk_partitions():
                if 'usb' in part.device.lower() or '/media/' in part.mountpoint:
                    drives.append(part.mountpoint)
        elif system == 'Darwin':
            for part in psutil.disk_partitions():
                if '/Volumes/' in part.mountpoint and part.mountpoint != '/':
                    drives.append(part.mountpoint)
    except:
        try:
            for part in psutil.disk_partitions():
                if part.opts and ('rw' in part.opts or 'removable' in part.opts.lower()):
                    drives.append(part.mountpoint)
        except:
            pass
    
    return drives

def copy_to_usb(filepath, usb_path):
    try:
        import shutil
        filename = os.path.basename(filepath)
        dest_path = os.path.join(usb_path, filename)
        shutil.copy2(filepath, dest_path)
        return True
    except:
        return False

def call_mistral_api(system_prompt, user_message):
    if not MISTRAL_API_KEY:
        return None
    try:
        headers = {
            'Authorization': f'Bearer {MISTRAL_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'mistral-tiny',
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message}
            ],
            'max_tokens': 2000,
            'temperature': 0.7
        }
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return None
    except:
        return None

def log_action(action, details):
    logs = read_json('admin_logs.json')
    if 'logs' not in logs:
        logs['logs'] = []
    logs['logs'].append({
        'id': generate_id(),
        'action': action,
        'details': details,
        'user': session.get('user', {}).get('email', 'system'),
        'date': datetime.now().isoformat(),
        'ip': request.remote_addr
    })
    write_json('admin_logs.json', logs)

def add_notification(user_email, message):
    notif_data = read_json('notifications.json')
    if 'notifications' not in notif_data:
        notif_data['notifications'] = []
    notif_data['notifications'].append({
        'id': generate_id(),
        'user_email': user_email,
        'message': message,
        'date': datetime.now().isoformat(),
        'read': False
    })
    write_json('notifications.json', notif_data)

@app.context_processor
def inject_globals():
    return {
        'get_text': get_text,
        'current_lang': get_lang(),
        'now': datetime.now()
    }

@app.route('/')
def index():
    if 'user' in session:
        if session['user']['role'] == 'admin':
            return redirect('/admin')
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/set-language/<lang>')
def set_language(lang):
    if lang in ['fr', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        if session['user']['role'] == 'admin':
            return redirect('/admin')
        return redirect('/dashboard')
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            return render_template('login.html', error='Tous les champs sont obligatoires / All fields are required')
        
        users = read_json('users.json')
        
        for user in users.get('users', []):
            if user['email'] == email and user['password'] == password:
                if not user.get('verified', False):
                    return render_template('login.html', error='Veuillez vérifier votre compte / Please verify your account')
                
                session['user'] = user
                user['last_login'] = datetime.now().isoformat()
                
                for i, u in enumerate(users['users']):
                    if u['id'] == user['id']:
                        users['users'][i] = user
                        break
                
                write_json('users.json', users)
                log_action('login', f"Connexion réussie: {email} / Successful login: {email}")
                
                if user['role'] == 'admin':
                    return redirect('/admin')
                return redirect('/dashboard')
        
        return render_template('login.html', error='Email ou mot de passe incorrect / Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect('/dashboard')
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        errors = []
        
        if not name:
            errors.append('Le nom est obligatoire / Name is required')
        
        if not email or '@' not in email:
            errors.append('Email invalide / Invalid email')
        
        if not password or len(password) < 6:
            errors.append('Mot de passe trop court (min 6 caractères) / Password too short (min 6 characters)')
        
        if password != confirm_password:
            errors.append('Les mots de passe ne correspondent pas / Passwords do not match')
        
        if errors:
            return render_template('register.html', errors=errors)
        
        users = read_json('users.json')
        if 'users' not in users:
            users['users'] = []
        
        for user in users['users']:
            if user['email'] == email:
                errors.append('Cet email est déjà utilisé / This email is already registered')
                return render_template('register.html', errors=errors)
        
        otp = generate_otp()
        new_user = {
            'id': len(users['users']) + 1,
            'name': name,
            'email': email,
            'password': password,
            'role': 'user',
            'verified': False,
            'created_at': datetime.now().isoformat(),
            'last_login': datetime.now().isoformat()
        }
        
        otp_data = read_json('otp_codes.json')
        if 'codes' not in otp_data:
            otp_data['codes'] = []
        
        otp_data['codes'] = [c for c in otp_data['codes'] if c['email'] != email or c['type'] != 'verification']
        otp_data['codes'].append({
            'email': email,
            'code': otp,
            'expires': (datetime.now() + timedelta(minutes=10)).isoformat(),
            'type': 'verification',
            'attempts': 0,
            'max_attempts': 5
        })
        
        users['users'].append(new_user)
        write_json('users.json', users)
        write_json('otp_codes.json', otp_data)
        
        email_html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="font-family:Arial;background:#f0f4f8;padding:20px">
            <div style="max-width:500px;margin:0 auto;background:white;border-radius:15px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12)">
                <div style="background:linear-gradient(135deg,#0a1628,#1a2744);padding:25px;text-align:center">
                    <h1 style="color:#4facfe;margin:0">BeCreative</h1>
                    <p style="color:#8a9bb5;margin:5px 0 0">Présentations Scolaires Professionnelles</p>
                </div>
                <div style="padding:30px;text-align:center">
                    <h2 style="color:#1a2744">Vérification de votre compte</h2>
                    <p style="color:#5a6a7a">Utilisez le code ci-dessous pour activer votre compte</p>
                    <div style="background:linear-gradient(135deg,#0a1628,#1a2744);color:#4facfe;font-size:36px;letter-spacing:8px;padding:18px 30px;border-radius:10px;display:inline-block;margin:20px 0;font-weight:bold">{otp}</div>
                    <p style="color:#5a6a7a;font-size:12px">Ce code expire dans 10 minutes</p>
                </div>
                <div style="background:#f0f4f8;padding:15px;text-align:center">
                    <p style="color:#8a9bb5;font-size:11px;margin:0">2026 BeCreative - Tous droits réservés</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        send_email(email, 'BeCreative - Vérification de compte / Account Verification', email_html)
        log_action('register', f"Nouvelle inscription: {email}")
        
        return redirect(f'/verify?email={email}')
    
    return render_template('register.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    email = request.args.get('email', '')
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        code = request.form.get('code', '').strip()
        
        if not email or not code:
            return render_template('verify.html', email=email, error='Tous les champs sont obligatoires / All fields are required')
        
        otp_data = read_json('otp_codes.json')
        
        found_otp = None
        for otp in otp_data.get('codes', []):
            if otp['email'] == email and otp['code'] == code and otp['type'] == 'verification':
                found_otp = otp
                break
        
        if not found_otp:
            return render_template('verify.html', email=email, error='Code incorrect / Invalid code')
        
        if found_otp.get('attempts', 0) >= found_otp.get('max_attempts', 5):
            otp_data['codes'] = [o for o in otp_data['codes'] if not (o['email'] == email and o['code'] == code)]
            write_json('otp_codes.json', otp_data)
            return render_template('verify.html', email=email, error='Trop de tentatives / Too many attempts')
        
        if datetime.fromisoformat(found_otp['expires']) < datetime.now():
            otp_data['codes'] = [o for o in otp_data['codes'] if not (o['email'] == email and o['code'] == code)]
            write_json('otp_codes.json', otp_data)
            return render_template('verify.html', email=email, error='Code expiré / Code expired')
        
        users = read_json('users.json')
        for i, user in enumerate(users.get('users', [])):
            if user['email'] == email:
                users['users'][i]['verified'] = True
                write_json('users.json', users)
                log_action('verify', f"Compte vérifié: {email}")
                break
        
        otp_data['codes'] = [o for o in otp_data['codes'] if not (o['email'] == email and o['code'] == code)]
        write_json('otp_codes.json', otp_data)
        
        return redirect('/login?verified=1')
    
    return render_template('verify.html', email=email)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            return render_template('forgot_password.html', error='Email requis / Email required')
        
        users = read_json('users.json')
        user_found = False
        for user in users.get('users', []):
            if user['email'] == email:
                user_found = True
                break
        
        if not user_found:
            return render_template('forgot_password.html', error='Aucun compte avec cet email / No account found')
        
        otp = generate_otp()
        
        reset_data = read_json('password_reset.json')
        if 'resets' not in reset_data:
            reset_data['resets'] = []
        
        reset_data['resets'] = [r for r in reset_data['resets'] if r['email'] != email]
        reset_data['resets'].append({
            'email': email,
            'code': otp,
            'expires': (datetime.now() + timedelta(minutes=15)).isoformat(),
            'attempts': 0,
            'max_attempts': 5
        })
        write_json('password_reset.json', reset_data)
        
        email_html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="font-family:Arial;background:#f0f4f8;padding:20px">
            <div style="max-width:500px;margin:0 auto;background:white;border-radius:15px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12)">
                <div style="background:linear-gradient(135deg,#0a1628,#1a2744);padding:25px;text-align:center">
                    <h1 style="color:#4facfe;margin:0">BeCreative</h1>
                </div>
                <div style="padding:30px;text-align:center">
                    <h2 style="color:#1a2744">Réinitialisation du mot de passe</h2>
                    <p style="color:#5a6a7a">Code de réinitialisation :</p>
                    <div style="background:linear-gradient(135deg,#0a1628,#1a2744);color:#4facfe;font-size:36px;letter-spacing:8px;padding:18px 30px;border-radius:10px;display:inline-block;margin:20px 0;font-weight:bold">{otp}</div>
                    <p style="color:#5a6a7a;font-size:12px">Code valable 15 minutes</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        send_email(email, 'BeCreative - Réinitialisation du mot de passe / Password Reset', email_html)
        
        return redirect(f'/reset-password?email={email}')
    
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email', '')
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        code = request.form.get('code', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not all([email, code, new_password, confirm_password]):
            return render_template('reset_password.html', email=email, error='Tous les champs sont obligatoires / All fields required')
        
        if new_password != confirm_password:
            return render_template('reset_password.html', email=email, error='Les mots de passe ne correspondent pas / Passwords do not match')
        
        if len(new_password) < 6:
            return render_template('reset_password.html', email=email, error='Mot de passe trop court / Password too short')
        
        reset_data = read_json('password_reset.json')
        valid_reset = False
        
        for reset in reset_data.get('resets', []):
            if reset['email'] == email and reset['code'] == code:
                if datetime.fromisoformat(reset['expires']) < datetime.now():
                    return render_template('reset_password.html', email=email, error='Code expiré / Code expired')
                
                if reset.get('attempts', 0) >= reset.get('max_attempts', 5):
                    return render_template('reset_password.html', email=email, error='Trop de tentatives / Too many attempts')
                
                valid_reset = True
                break
        
        if not valid_reset:
            return render_template('reset_password.html', email=email, error='Code incorrect / Invalid code')
        
        users = read_json('users.json')
        for i, user in enumerate(users.get('users', [])):
            if user['email'] == email:
                users['users'][i]['password'] = new_password
                write_json('users.json', users)
                log_action('reset_password', f"Mot de passe réinitialisé: {email}")
                break
        
        reset_data['resets'] = [r for r in reset_data['resets'] if not (r['email'] == email and r['code'] == code)]
        write_json('password_reset.json', reset_data)
        
        return redirect('/login?reset=1')
    
    return render_template('reset_password.html', email=email)

@app.route('/logout')
def logout():
    if 'user' in session:
        log_action('logout', f"Déconnexion: {session['user']['email']}")
    session.pop('user', None)
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    if session['user']['role'] == 'admin':
        return redirect('/admin')
    
    requests_data = read_json('requests.json')
    user_requests = [r for r in requests_data.get('requests', []) if r.get('user_email') == session['user']['email']]
    
    notifications_data = read_json('notifications.json')
    user_notifications = [n for n in notifications_data.get('notifications', []) if n.get('user_email') == session['user']['email']]
    unread_count = len([n for n in user_notifications if not n.get('read', False)])
    
    return render_template('dashboard.html', 
                         user=session['user'], 
                         requests=user_requests, 
                         notifications=user_notifications,
                         unread_count=unread_count)

@app.route('/new-request', methods=['GET', 'POST'])
@login_required
def new_request():
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        level = request.form.get('level', '').strip()
        doc_type = request.form.get('type', '').strip()
        theme = request.form.get('theme', '').strip()
        deadline = request.form.get('deadline', '').strip()
        description = request.form.get('description', '').strip()
        
        if not all([subject, level, doc_type, theme, deadline, description]):
            return render_template('new_request.html', error='Tous les champs sont obligatoires / All fields required')
        
        request_id = generate_id()
        new_req = {
            'id': request_id,
            'user_email': session['user']['email'],
            'user_name': session['user']['name'],
            'subject': subject,
            'level': level,
            'type': doc_type,
            'theme': theme,
            'deadline': deadline,
            'description': description,
            'status': 'pending',
            'presentation_number': None,
            'qr_code': None,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'file': None,
            'admin_file': None,
            'usb_path': None
        }
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                filename = f"{request_id}_{file.filename}"
                filepath = os.path.join('uploads', filename)
                os.makedirs('uploads', exist_ok=True)
                file.save(filepath)
                new_req['file'] = filename
        
        requests_data = read_json('requests.json')
        if 'requests' not in requests_data:
            requests_data['requests'] = []
        requests_data['requests'].append(new_req)
        write_json('requests.json', requests_data)
        
        log_action('new_request', f"Nouvelle demande: {subject} par {session['user']['email']}")
        add_notification(session['user']['email'], f"Votre demande '{subject}' a été créée avec succès")
        
        return redirect('/dashboard?success=1')
    
    return render_template('new_request.html')
@app.route('/cih')
def cih():
    return render_template('cih.html')
@app.route('/binance')
def binance():
    return render_template('binance.html')

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    filepath = os.path.join('uploads', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return 'Fichier non trouvé / File not found', 404

@app.route('/api/usb/detect')
@login_required
def api_usb_detect():
    drives = get_usb_drives()
    return jsonify({
        'success': True,
        'drives': drives,
        'detected': len(drives) > 0
    })

@app.route('/api/usb/copy/<request_id>')
@login_required
def api_usb_copy(request_id):
    requests_data = read_json('requests.json')
    
    req = None
    for r in requests_data.get('requests', []):
        if r['id'] == request_id:
            req = r
            break
    
    if not req:
        return jsonify({'success': False, 'error': 'Demande non trouvée / Request not found'})
    
    file_to_copy = req.get('admin_file') or req.get('file')
    if not file_to_copy:
        return jsonify({'success': False, 'error': 'Aucun fichier à copier / No file to copy'})
    
    filepath = os.path.join('uploads', file_to_copy)
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': 'Fichier source non trouvé / Source file not found'})
    
    drives = get_usb_drives()
    if not drives:
        return jsonify({'success': False, 'error': 'Aucune clé USB détectée / No USB drive detected'})
    
    usb_path = drives[0]
    if copy_to_usb(filepath, usb_path):
        for i, r in enumerate(requests_data['requests']):
            if r['id'] == request_id:
                requests_data['requests'][i]['usb_path'] = usb_path
                write_json('requests.json', requests_data)
                break
        
        log_action('usb_copy', f"Fichier copié sur USB: {request_id}")
        return jsonify({'success': True, 'message': f'Copié sur {usb_path} / Copied to {usb_path}'})
    
    return jsonify({'success': False, 'error': 'Erreur lors de la copie / Copy error'})

@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message vide / Empty message'}), 400
        
        history = read_json('chatbot_history.json')
        if 'conversations' not in history:
            history['conversations'] = []
        
        conv = {
            'id': generate_id(),
            'user': session['user']['email'],
            'message': message,
            'response': '',
            'date': datetime.now().isoformat()
        }
        
        system_prompt = """Tu es l'assistant IA de BeCreative, une plateforme professionnelle de création de présentations scolaires. 
        Tu aides les étudiants et enseignants à créer des présentations PowerPoint, des PDF, des discours et des résumés.
        Tu dois répondre en français et en anglais selon la langue de l'utilisateur.
        Sois professionnel, précis et utile.
        Tu peux suggérer des structures de présentation, des idées de contenu, des conseils de design.
        Ne mentionne pas d'autres plateformes ou services concurrents.
        Reste dans le contexte éducatif et scolaire."""
        
        ai_response = call_mistral_api(system_prompt, message)
        
        if not ai_response:
            ai_response = generate_local_response(message)
        
        conv['response'] = ai_response
        history['conversations'].append(conv)
        write_json('chatbot_history.json', history)
        
        return jsonify({'response': ai_response})
    
    conversations = read_json('chatbot_history.json').get('conversations', [])
    user_convs = [c for c in conversations if c.get('user') == session['user']['email']]
    return render_template('chatbot.html', conversations=user_convs[-50:])

def generate_local_response(message):
    message_lower = message.lower()
    
    responses = {
        'plan': """Voici une structure de présentation professionnelle :

1. Page de titre
   - Titre accrocheur
   - Sous-titre explicatif
   - Nom et date

2. Introduction
   - Contexte du sujet
   - Problématique
   - Plan de la présentation

3. Développement (3 parties)
   - Partie 1 : Fondements théoriques
   - Partie 2 : Analyse approfondie
   - Partie 3 : Applications pratiques

4. Conclusion
   - Synthèse des points clés
   - Perspectives
   - Remerciements

5. Questions / Discussion

Voulez-vous que je développe une partie spécifique ?""",
        
        'powerpoint': """Conseils pour un PowerPoint professionnel :

- Une idée par diapositive
- Maximum 6 lignes par slide
- Police sans-serif (Arial, Calibri)
- Taille minimum 24pt
- Contraste élevé (texte foncé sur fond clair)
- Images de qualité professionnelle
- Animations sobres et cohérentes
- Graphiques clairs et lisibles

Quel est votre thème pour des conseils plus spécifiques ?""",
        
        'resume': """Pour créer un résumé efficace :

1. Identifiez les 3-5 points essentiels
2. Utilisez des phrases courtes
3. Structure logique (cause-effet, chronologie)
4. Évitez le jargon inutile
5. Terminez par l'idée principale

Quel sujet souhaitez-vous résumer ?""",
        
        'introduction': """Structure d'une introduction réussie :

1. Phrase d'accroche (statistique, citation, question)
2. Contexte (pourquoi ce sujet est important)
3. Problématique (question centrale)
4. Annonce du plan (ce que vous allez couvrir)

Exemple : "Saviez-vous que... Cette question est au cœur de notre présentation qui explorera..." """
    }
    
    for key, response in responses.items():
        if key in message_lower:
            return response
    
    return "Je suis votre assistant BeCreative. Je peux vous aider avec la structure de votre présentation, des conseils PowerPoint, des résumés, des introductions et bien plus. Quel est votre besoin spécifique ? / I am your BeCreative assistant. I can help with presentation structure, PowerPoint tips, summaries, introductions and more. What do you need specifically?"

@app.route('/admin')
@admin_required
def admin():
    requests_data = read_json('requests.json')
    users_data = read_json('users.json')
    
    all_requests = requests_data.get('requests', [])
    all_users = users_data.get('users', [])
    
    total_requests = len(all_requests)
    pending_requests = len([r for r in all_requests if r['status'] == 'pending'])
    in_progress_requests = len([r for r in all_requests if r['status'] == 'in_progress'])
    completed_requests = len([r for r in all_requests if r['status'] == 'completed'])
    total_users = len(all_users)
    
    subjects = {}
    for r in all_requests:
        subj = r.get('subject', 'Autre')
        subjects[subj] = subjects.get(subj, 0) + 1
    
    logs = read_json('admin_logs.json').get('logs', [])
    recent_logs = sorted(logs, key=lambda x: x.get('date', ''), reverse=True)[:10]
    
    return render_template('admin.html',
                         requests=all_requests,
                         users=all_users,
                         total_requests=total_requests,
                         pending_requests=pending_requests,
                         in_progress_requests=in_progress_requests,
                         completed_requests=completed_requests,
                         total_users=total_users,
                         subjects=subjects,
                         recent_logs=recent_logs)

@app.route('/admin/request/<request_id>', methods=['GET', 'POST'])
@admin_required
def admin_request_detail(request_id):
    requests_data = read_json('requests.json')
    
    req = None
    for r in requests_data.get('requests', []):
        if r['id'] == request_id:
            req = r
            break
    
    if not req:
        return redirect('/admin')
    
    if request.method == 'POST':
        action = request.form.get('action', '')
        
        for i, r in enumerate(requests_data['requests']):
            if r['id'] == request_id:
                if action == 'update_status':
                    new_status = request.form.get('status', 'pending')
                    requests_data['requests'][i]['status'] = new_status
                    requests_data['requests'][i]['updated_at'] = datetime.now().isoformat()
                    
                    add_notification(r['user_email'], f"Votre demande '{r['subject']}' est maintenant: {new_status}")
                    log_action('update_status', f"Demande {request_id}: {new_status}")
                
                elif action == 'complete_presentation':
                    presentation_number = generate_presentation_number()
                    qr_data = f"BeCreative|{presentation_number}|{request_id}|{r['user_email']}|{datetime.now().isoformat()}"
                    qr_code = generate_qr_code(qr_data)
                    
                    requests_data['requests'][i]['status'] = 'completed'
                    requests_data['requests'][i]['presentation_number'] = presentation_number
                    requests_data['requests'][i]['qr_code'] = qr_code
                    requests_data['requests'][i]['completed_at'] = datetime.now().isoformat()
                    requests_data['requests'][i]['updated_at'] = datetime.now().isoformat()
                    
                    if 'file' in request.files:
                        file = request.files['file']
                        if file.filename:
                            filename = f"completed_{request_id}_{file.filename}"
                            filepath = os.path.join('uploads', filename)
                            os.makedirs('uploads', exist_ok=True)
                            file.save(filepath)
                            requests_data['requests'][i]['admin_file'] = filename
                    
                    add_notification(r['user_email'], f"Votre présentation '{r['subject']}' est terminée! Numéro: {presentation_number}")
                    
                    email_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head><meta charset="UTF-8"></head>
                    <body style="font-family:Arial;background:#f0f4f8;padding:20px">
                        <div style="max-width:500px;margin:0 auto;background:white;border-radius:15px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.12)">
                            <div style="background:linear-gradient(135deg,#0a1628,#1a2744);padding:25px;text-align:center">
                                <h1 style="color:#4facfe;margin:0">BeCreative</h1>
                                <p style="color:#8a9bb5;margin:5px 0 0">Présentation terminée</p>
                            </div>
                            <div style="padding:30px;text-align:center">
                                <h2 style="color:#1a2744">Votre présentation est prête!</h2>
                                <p style="color:#5a6a7a">Numéro de présentation:</p>
                                <div style="background:linear-gradient(135deg,#0a1628,#1a2744);color:#4facfe;font-size:28px;letter-spacing:4px;padding:15px 25px;border-radius:10px;display:inline-block;margin:15px 0;font-weight:bold">{presentation_number}</div>
                                <p style="color:#5a6a7a;margin:20px 0">Connectez-vous pour télécharger votre fichier</p>
                            </div>
                            <div style="background:#f0f4f8;padding:15px;text-align:center">
                                <p style="color:#8a9bb5;font-size:11px;margin:0">2026 BeCreative - Tous droits réservés</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    
                    send_email(r['user_email'], f'BeCreative - Présentation terminée: {presentation_number}', email_html)
                    log_action('complete_presentation', f"Présentation {presentation_number} générée pour {request_id}")
                
                elif action == 'send_message':
                    message = request.form.get('message', '').strip()
                    if message:
                        add_notification(r['user_email'], f"Message de l'administrateur: {message}")
                        log_action('send_message', f"Message envoyé pour {request_id}")
                
                break
        
        write_json('requests.json', requests_data)
        return redirect(f'/admin/request/{request_id}')
    
    return render_template('admin_request_detail.html', request=req)

@app.route('/admin/logs')
@admin_required
def admin_logs():
    logs = read_json('admin_logs.json').get('logs', [])
    sorted_logs = sorted(logs, key=lambda x: x.get('date', ''), reverse=True)
    return render_template('admin_logs.html', logs=sorted_logs)

@app.route('/api/notifications/read', methods=['POST'])
@login_required
def api_mark_notification_read():
    data = request.get_json()
    notif_id = data.get('id', '')
    
    notif_data = read_json('notifications.json')
    for notif in notif_data.get('notifications', []):
        if notif['id'] == notif_id:
            notif['read'] = True
            break
    write_json('notifications.json', notif_data)
    
    return jsonify({'success': True})

@app.route('/api/notifications/unread-count')
@login_required
def api_unread_count():
    notif_data = read_json('notifications.json')
    user_notifications = [n for n in notif_data.get('notifications', []) if n.get('user_email') == session['user']['email']]
    count = len([n for n in user_notifications if not n.get('read', False)])
    return jsonify({'count': count})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    os.makedirs('presentations', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)