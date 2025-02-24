import os
import gspread
from typing import List
from django.conf import settings

def initialize_gspread() -> gspread.client.Client:
  """
  Initialize a gspread client with the given credentials.
  """
  return gspread.service_account_from_dict(get_credentials())  # Note: we could move this to settings to do this once.

def get_credentials() -> dict:
  """
  Return gspread credentials.
  """
  return {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
  }

def get_all_rows(doc_name: str, sheet_name: str = None) -> List[dict]:
  """
  Fetches all rows from a given Google Sheet worksheet.
  """
  sh = settings.GSPREAD_CLIENT.open(doc_name)
  worksheet = sh.worksheet(sheet_name) if sheet_name else sh.get_worksheet(0)
  return worksheet.get_all_records()

def get_all_rows_by_url(link: str, sheet_name: str = None, creds: str = None, mail: str = None) -> List[dict]:
  """
  Fetches all rows from a given Google Sheet worksheet.
  """
  client = gspread.authorize(creds)
  sh = client.open_by_url(link)
  if isWriter(sh.list_permissions(),mail):
    worksheet = sh.worksheet(sheet_name) if sheet_name else sh.get_worksheet(0)
    list_of_row = worksheet.get_all_records()
  else:
    list_of_row = [{"Not Allowed": "Vous ne disposez pas des droits suffisants pour editer ce document"}]
  return list_of_row

def isWriter(json_permisons, email):
  retour = False
  for user in json_permisons:
    if "emailAddress" in user:
      if (user["emailAddress"] == email and (user["role"] == "owner" or user["role"] == "writer")):
        retour = True
  return retour

def changeExerciceState(link, sheet_name, creds, mail,row_index,state):
  client = gspread.authorize(creds)
  sh = client.open_by_url(link)
  if isWriter(sh.list_permissions(),mail):
    worksheet = sh.worksheet(sheet_name)
    worksheet.update_cell(row_index,7,state)
    
def updateComment(link, sheet_name, creds, mail,row_index,state):
  client = gspread.authorize(creds)
  sh = client.open_by_url(link)
  if isWriter(sh.list_permissions(),mail):
    worksheet = sh.worksheet(sheet_name)
    worksheet.update_cell(row_index,12,state)
    
    
def updateStartDate(link, sheet_name, creds, mail,row_index,date):
  client = gspread.authorize(creds)
  sh = client.open_by_url(link)
  if isWriter(sh.list_permissions(),mail):
    worksheet = sh.worksheet(sheet_name)
    if(date!="0") :
      date_str = date.strftime('%d/%m/%Y %H:%M:%S')
    else :
      date_str=""
    worksheet.update_cell(row_index,9,date_str)
    
def updateEndDate(link, sheet_name, creds, mail,row_index,date):
  client = gspread.authorize(creds)
  sh = client.open_by_url(link)
  if isWriter(sh.list_permissions(),mail):
    worksheet = sh.worksheet(sheet_name)
    if(date!="0") :
      date_str = date.strftime('%d/%m/%Y %H:%M:%S')
    else :
      date_str=""
    worksheet.update_cell(row_index,11,date_str)
    
def getExerciceName(link, sheet_name, creds, row_index):
    client = gspread.authorize(creds)
    sh = client.open_by_url(link)
    worksheet = sh.worksheet(sheet_name)
    exercice_name = worksheet.cell(row_index, 2).value
    return exercice_name


