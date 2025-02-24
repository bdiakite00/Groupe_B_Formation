from django.shortcuts import render
from .services import get_all_rows, get_all_rows_by_url, changeExerciceState,getExerciceName,updateStartDate,updateEndDate,updateComment
from django.http import HttpResponse
from .forms import GoogleSheetForm
from contact.models import Coach
import gspread
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils.translation import gettext as _
import xml.etree.ElementTree as ET
from datetime import datetime

def initSessionData(request):
    xml_file_path = "data/app_data.xml"
    
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    title = root.find("title").text
    request.session["app_title"] = title
    return request

def submit_google_sheet(request):
    if request.method == 'POST':
        if 'url_module' in request.POST:
            return getModule(request, request.POST['url_module'])
        else:
            if 'CodeModule' in request.POST:
                return getExercice(request, request.POST['sheetLink'], request.POST['CodeModule'])
            else:
                form = GoogleSheetForm(request.POST)
                if form.is_valid():
                    lien_google_sheet = form.cleaned_data['lien_google_sheet']
                    # Appeler la méthode getProgramsList avec le lien
                    return getProgramsListUrl(request, lien_google_sheet)
                else:
                    form = GoogleSheetForm()
                    # Vider la session utilisateur
                    request.session.flush()
                    
    else:
        form = GoogleSheetForm()
        request = initSessionData(request)
    return render(request, 'submit_google_sheet.html', {'form': form})


def getProgramsListUrl(request, link):
    # Implémentez votre logique pour utiliser le lien Google Sheets ici
    scope = ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file("data/secret_key_google.json", scopes=scope)
    if hasattr(request.user, "email"):
        programsList = get_all_rows_by_url(link,"Liste",creds,request.user.email)
    else:
        programsList = [{"Erreur": "Veuillez vous identifier"}]
    return render(request, 'ListingPrograms.html', {'google_sheet_list': programsList})

def getModule(request,link):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive']
    print(link)
    creds = Credentials.from_service_account_file("data/secret_key_google.json", scopes=scope)
    # Stocker le lien dans une variable de session
    request.session['google_sheet_link'] = link
    if hasattr(request.user, "email"):
        exercicesList = get_all_rows_by_url(link,"Module",creds,request.user.email)
    else:
        exercicesList = [{"Erreur": "Veuillez vous identifier"}]
  
    return render(request, 'ListingModules.html', {'google_sheet_list': exercicesList, "google_sheet_link": link})
    

def getExercice(request,link,module):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file("data/secret_key_google.json", scopes=scope)
    if hasattr(request.user, "email"):
        exercicesAllList = get_all_rows_by_url(link,"Exercices",creds,request.user.email)
        exercicesList = []
        for exercice in exercicesAllList:
            if module in exercice['Code Module']:
                exercicesList.append(exercice)
    else:
        exercicesList = [{"Erreur": "Veuillez vous identifier"}]
    return render(request, 'ListingExercices.html', {'google_sheet_list': exercicesList, "module_link": link})

def send_email(receiver_email, subject, body):
    
   
 # Charger les informations d'email depuis le fichier JSON
    with open('data/secret_key_gmail_google.json') as f:
        email_config = json.load(f)

    # Paramètres de connexion SMTP
    smtp_host = email_config['EMAIL_HOST']
    smtp_port = int(email_config['EMAIL_PORT'])
    smtp_user = email_config['EMAIL_HOST_USER']
    smtp_password = email_config['EMAIL_HOST_PASSWORD']   # Configuration des paramètres de connexion SMTP
    print("dhuzhfhuzihfezuaeugegfui")
    print(smtp_port)
    # Création de l'objet e-mail
    message = MIMEMultipart()
    message['From'] = smtp_user 
    message['To'] = receiver_email
    message['Subject'] = subject

    # Ajout du corps du message
    message.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)

    # Envoi de l'e-mail
    text = message.as_string()
    server.sendmail(smtp_user, receiver_email, text)
    server.quit()

def getCoachEmailFromGoogleSheet(link):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('data/secret_key_google.json', scope)
    
    # Authentifier et ouvrir le Google Sheet correspondant
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(link).worksheet('Contact')

    # Récupérer toutes les lignes contenant les informations des coachs
    coach_rows = sheet.get_all_values()[1:]  # Commencer à partir de la deuxième ligne pour éviter les en-têtes
    
    # Initialiser une liste pour stocker les adresses e-mail des coachs
    coach_emails = []

    # Parcourir chaque ligne pour récupérer les adresses e-mail de chaque coach
    for row in coach_rows:
        email_coach = row[5]  # Récupérer l'e-mail du coach à partir de la colonne F (index 5)
        coach_emails.append(email_coach)

    return coach_emails

def doExercice(request):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file("data/secret_key_google.json", scopes=scope)
    
    if request.method == 'POST':
        link_module = request.POST.get("linkModule", "")
        link_exercice = request.POST.get("linkExercice", "")
        action = request.POST.get("action", "")  # Ajouter un champ "action" dans le formulaire
        # Vérification de la présence du lien d'exercice dans la requête POST
        if link_exercice:
            if action == "start":
                exercicesAllList = get_all_rows_by_url(link_module,"Exercices",creds=creds,mail=request.user.email)
                row_index = 2
                for ex in exercicesAllList:
                    if ex["Lien"] == link_exercice:
                        changeExerciceState(link_module,"Exercices",creds,request.user.email, row_index, "En cours")
                        # Enregistrement de la date de début
                        updateStartDate(link_module, "Exercices", creds,request.user.email, row_index, datetime.now())
                        coach_emails = getCoachEmailFromGoogleSheet(link_module)
                        # Récupérer le nom de l'exercice terminé
                        exercice_name = getExerciceName(link_module, "Exercices", creds, row_index)
                        if coach_emails:
                            subject = "Changement d'état de l'exercice"
                            body = f"Bonjour, l'état de l'exercice {exercice_name} a été changé dans le google sheet {link_module}. Il est maintenant en cours"
                            for coach_email in coach_emails:
                                send_email(coach_email, subject, body)    
                           
                    row_index = row_index + 1
            
            elif action == "Soumettre":

                exercicesAllList = get_all_rows_by_url(link_module, "Exercices", creds=creds, mail=request.user.email)
                row_index = 2
                for ex in exercicesAllList:
                  if ex["Lien"] == link_exercice:
                        # Récupérer l'entrée de l'utilisateur à partir du formulaire
                        input = request.POST.get('commentaire_stagiaire')
                        # Mettre à jour le commentaire dans la feuille Google
                        updateComment(link_module, "Exercices", creds, request.user.email, row_index, input)
                        row_index += 1
         
            elif action == "finish":
                
              exercicesAllList = get_all_rows_by_url(link_module,"Exercices",creds=creds,mail=request.user.email)
              row_index = 2

              for ex in exercicesAllList:
                if ex["Lien"] == link_exercice:
                    changeExerciceState(link_module,"Exercices",creds,request.user.email, row_index, "Terminé")
                    updateEndDate(link_module, "Exercices", creds, request.user.email,row_index, datetime.now())
                    coach_emails = getCoachEmailFromGoogleSheet(link_module)
                    # Récupérer le nom de l'exercice terminé
                    exercice_name= getExerciceName(link_module, "Exercices", creds, row_index)
                    if coach_emails:
                        subject = "Changement d'état de l'exercice"
                        body = f"Bonjour, l'état de l'exercice {exercice_name} a été changé dans le google sheet {link_module}. Il est maintenant terminer"
                        for coach_email in coach_emails:
                            send_email(coach_email, subject, body)    
                           
                    row_index = row_index + 1
                    
            elif action == "return_to_todo":
                
              exercicesAllList = get_all_rows_by_url(link_module,"Exercices",creds=creds,mail=request.user.email)
              row_index = 2
              for ex in exercicesAllList:
                if ex["Lien"] == link_exercice:
                    changeExerciceState(link_module,"Exercices",creds,request.user.email, row_index, "A faire")
                    updateStartDate(link_module, "Exercices", creds,request.user.email, row_index, "0")
                    updateEndDate(link_module, "Exercices", creds, request.user.email,row_index, "0")
                    coach_emails = getCoachEmailFromGoogleSheet(link_module)
                    # Récupérer le nom de l'exercice terminé
                    exercice_name= getExerciceName(link_module, "Exercices", creds, row_index)
                    if coach_emails:
                        subject = "Changement d'état de l'exercice"
                        body = f"Bonjour, l'état de l'exercice {exercice_name} a été changé dans le google sheet {link_module}. Il est maintenant à faire"
                        for coach_email in coach_emails:
                            send_email(coach_email, subject, body)    
                           
                    row_index = row_index + 1
                    
            elif action == "return_to_in_progress":
                
              exercicesAllList = get_all_rows_by_url(link_module,"Exercices",creds=creds,mail=request.user.email)
              row_index = 2
              for ex in exercicesAllList:
                if ex["Lien"] == link_exercice:
                    changeExerciceState(link_module,"Exercices",creds,request.user.email, row_index, "En cours")
                    updateEndDate(link_module, "Exercices", creds, request.user.email,row_index, "0")
                    coach_emails = getCoachEmailFromGoogleSheet(link_module)
                    # Récupérer le nom de l'exercice terminé
                    exercice_name= getExerciceName(link_module, "Exercices", creds, row_index)
                    if coach_emails:
                        subject = "Changement d'état de l'exercice"
                        body = f"Bonjour, l'état de l'exercice {exercice_name} a été changé dans le google sheet {link_module}. Il est maintenant à en cours"
                        for coach_email in coach_emails:
                            send_email(coach_email, subject, body)    
                           
                    row_index = row_index + 1
            
            
            # Récupérer les exercices mis à jour
            exercices = get_all_rows_by_url(link_module, "Exercices", creds, request.user.email)
            
            # Remplacer les espaces par des tirets bas pour chaque attribut ayant un espace
            for exercice in exercices:
                new_exercice = {}
                for key, value in exercice.items():
                    new_key = key.replace(' ', '_') # Remplacer l'espace par un tiret bas
                    new_exercice[new_key] = value
                exercices[exercices.index(exercice)] = new_exercice
            
            return render(request, 'exercice.html', {'google_sheet_list': exercices, "module_link": link_module,'link_exercice' : link_exercice })
        else:
            return render(request, 'exercice.html', {"Result": "Que fais-tu ici petit malin ?"})
    else:
        return render(request, 'exercice.html', {"Result": "Que fais-tu ici petit malin ?"})
