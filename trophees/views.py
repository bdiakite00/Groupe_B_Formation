from django.shortcuts import render
from django.http import HttpResponse
from google.oauth2.service_account import Credentials
from google_sheet_manager.services import get_all_rows_by_url

def trophees(request):
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file("data/secret_key_google.json", scopes=scope)

    # URL du fichier principal contenant la liste des programmes
    main_sheet_url = "https://docs.google.com/spreadsheets/d/1FiALJYp5Y7HHyQf6yIPZNvHJ8z3pdErqIaVXkORucAo/edit#gid=0"
    if hasattr(request.user, "email"):
        programs = get_all_rows_by_url(main_sheet_url, "Liste", creds, request.user.email)
        all_programs_progress = []
        challenges = []
        for program in programs:
            program_name = program.get("Titre du programme")
            program_url = program.get("Lien vers le fichier Google Sheet du Programme")

            # Récupérer tous les modules et exercices pour ce programme
            modules = get_all_rows_by_url(program_url, "Module", creds, request.user.email)
            exercises = get_all_rows_by_url(program_url, "Exercices", creds, request.user.email)

            modules_progress = []

            total_module_exercises = 0
            completed_module_exercises = 0

            # Utiliser un dictionnaire pour stocker les exercices par module pour un accès rapide
            module_exercises_map = {}
            for exercise in exercises:
                module_code = exercise.get("Code Module", "")
                if module_code not in module_exercises_map:
                    module_exercises_map[module_code] = []
                module_exercises_map[module_code].append(exercise)

                # Collect challenges
                if exercise.get("Type") == "Défi":
                    challenges.append({
                        "module_code": module_code,
                        "challenge_name": exercise.get("Titre"),
                        "status": exercise.get("Etat")
                    })

            for module in modules:
                module_name = module.get("Libelle")
                module_code = module.get("CodeModule")
                module_image = module.get("Image") 

                # Récupérer les exercices pour ce module à partir du dictionnaire
                module_exercises = [ex for ex in exercises if ex.get("Code Module", "").startswith(module_code)]
                total_exercises = len(module_exercises)
                completed_exercises = sum(1 for ex in module_exercises if ex.get("Etat") == "Terminé")

                progress_percentage = (completed_exercises / total_exercises * 100) if total_exercises > 0 else 0

                modules_progress.append({
                    "module_name": module_name,
                    "module_image": module_image,
                    "progress_percentage": progress_percentage
                })

                total_module_exercises += total_exercises
                completed_module_exercises += completed_exercises

            overall_progress_percentage = (completed_module_exercises / total_module_exercises * 100) if total_module_exercises > 0 else 0

            all_programs_progress.append({
                "program_name": program_name,
                "modules_progress": modules_progress,
                "overall_progress_percentage": overall_progress_percentage
            })

        return render(request, 'trophees.html', {'all_programs_progress': all_programs_progress, 'challenges': challenges})
    else:
        return HttpResponse("Veuillez vous identifier")
