# Ajouter les imports manquants
import gspread  # 6 - Google Sheets et Python
from oauth2client.service_account import ServiceAccountCredentials  # 6 - Google Sheets et Python
from django.shortcuts import render  # Importation manquante pour le rendu Django
from django.http import HttpResponse  # Import manquant

def contact(request):
    # Récupérer le lien de la feuille de calcul Google à partir de la session
    google_sheet_link = request.session.get('google_sheet_link', None)
    if google_sheet_link:
        # Utiliser le lien de la feuille de calcul pour ouvrir la feuille de contact
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('data/secret_key_google.json', scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_url(google_sheet_link).worksheet('Contact')

        # Récupérer toutes les lignes contenant les informations des coachs
        coach_rows = sheet.get_all_values()[1:]  # Commencer à partir de la deuxième ligne pour éviter les en-têtes

        # Initialiser une liste pour stocker les informations de chaque coach
        coachs_data = []

        # Parcourir chaque ligne pour récupérer les informations de chaque coach
        for index, row in enumerate(coach_rows, start=2):  # Commencer à partir de la ligne 2
            nom_du_coach = row[0]
            description_coach = row[1]
            lien_photo_coach = row[2]
            lien_site_internet = row[3]
            message_publicite_coach = row[4]
            email_coach = row[5]

            # Créer un dictionnaire contenant les informations du coach actuel
            coach_data = {
                'nom_du_coach': nom_du_coach,
                'description_coach': description_coach,
                'lien_photo_coach': lien_photo_coach,
                'lien_site_internet': lien_site_internet,
                'message_publicite_coach': message_publicite_coach,
                'email_coach': email_coach
            }

            # Ajouter les informations du coach à la liste des coachs
            coachs_data.append(coach_data)

        # Passer la liste des coachs au template
        context = {
            'coachs_data': coachs_data
        }
        
        return render(request, 'contact.html', context)
    else:
        # Gérer le cas où google_sheet_link n'est pas défini
        # Vous pouvez rediriger l'utilisateur vers une autre page ou afficher un message d'erreur
        return HttpResponse("Le lien de la feuille de calcul Google n'est pas défini.")
