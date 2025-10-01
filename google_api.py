'''
This Python file defines a helper function create_service that automates authentication and connection to Google APIs using OAuth 2.0.
It:
    Loads or creates OAuth tokens and stores them in a local "token files" folder.
    Refreshes tokens if expired, or prompts the user to log in via a browser if no valid credentials are found.
    Saves refreshed or new credentials for future use.
    Creates and returns a Google API service object that can be used to make API calls (e.g., list Google Drive files, send Gmail, access Calendar events).
    Handles errors by deleting corrupted tokens if service creation fails.

'''
#Dependencies
import os 
from google_auth_oauthlib.flow import InstalledAppFlow #For handling the OAuth 2.0 authorization flow.
from googleapiclient.discovery import build #For constructing a service object for the Google API.
from google.oauth2.credentials import Credentials #For working with OAuth 2.0 credentials.
from google.auth.transport.requests import Request #For refreshing expired credentials.

def create_service(client_secret_file, api_name, api_version, *scopes, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file #Path to the client secret JSON file obtained from Google Cloud Console.
    API_SERVICE_NAME = api_name #The name of the Google API (e.g., "drive", "gmail", "calendar").
    API_VERSION = api_version 
    SCOPES = [scope for scope in scopes[0]] #A list of OAuth 2.0 permissions required.
    
    creds = None
    working_dir = os.getcwd ()
    
    #Stores tokens inside a "token files" directory in the current working directory.
    token_dir = 'token files'
    token_file = f"token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json"
    
    # Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))
    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open (os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(creds.to_json())
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(API_SERVICE_NAME, API_VERSION, "service created successfully")
        return service
    except Exception as e:
        print(e)
        print(f'Failed to execute service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, token_file))
        return None