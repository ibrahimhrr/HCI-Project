import json
from backend.google_api import create_service

client_service = 'client-secret.json'

def construct_google_calendar_client(client_service):
    '''
    This function will create the calendar agent 
    it takes in the secret json file path and outputs a google calendar API instance
    '''
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    service = create_service(client_service,API_NAME,API_VERSION,SCOPES)
    return service

google_calendar_service = construct_google_calendar_client(client_service)

def create_calendar_list(calendar_name):
    """
    Creates a new calendar list
    
    """

    