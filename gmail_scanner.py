import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailScanner:
    def __init__(self, db):
        self.db = db
        self.creds = None
        self.authenticate()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def authenticate(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def scan_for_updates(self, log_callback=None):
        if log_callback: log_callback("Starting scanning Gmail")

        jobs = self.db.get_all_jobs()
        active_jobs = [job for job in jobs if job[3] == "Applied"]

        updates_found = 0

        results = self.service.users().messages().list(userId='me', q="newer_than:14d").execute()
        messages = results.get('messages', [])

        if not messages:
            if log_callback: log_callback("No new messages in inbox")
            return updates_found
        
        for job in active_jobs:
            job_id, company_name, _, _, _ = job
            company_lower = company_name.lower()

            for msg in messages[:20]:
                msg_data = self.service .users().messages().get(userId='me', id=msg['id'], format='full').execute()

                payload = msg_data.get('payload', {})
                headers = payload.get('headers', [])

                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "").lower()
                sender = next((header['value'] for header in headers if header['name'] == 'From'), "").lower()

                clean_company_string = company_lower.replace('|', ' ').replace('-', ' ').replace('.', ' ')
                company_words = [word.strip() for word in clean_company_string.split() if len(word) > 4]

                match_found = False
                for word in company_words:
                    if word in subject or word in sender:
                        match_found = True
                        break

                if match_found:
                    snippet = msg_data.get('snippet', '').lower()

                    rejection_words = ['unfortunately', 'niestety', 'decline', 'ordzucienie', 'other candidates', 'nie zdecydowaliśmy']
                    interview_words = ['interview', 'zaproszenie', 'rozmowa', 'next steps', 'kolejny etap']

                    new_status = None

                    if any(word in snippet or word in subject for word in rejection_words):
                        new_status = "Rejected"
                    elif any(word in snippet or word in subject for word in interview_words):
                        new_status = "Interviewing"

                    if new_status:
                        self.db.update_status(job_id, new_status)
                        updates_found += 1
                        if log_callback: log_callback(f"Updated: {job_id} | {company_name} -> {new_status}")
                        break
        if log_callback: log_callback(f"Finished. Found updates: {updates_found}")
        return updates_found
