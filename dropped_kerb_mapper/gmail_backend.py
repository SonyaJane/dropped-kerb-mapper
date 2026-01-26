"""
Custom email backend for sending emails via Gmail API with Service Account
"""
import base64
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.mail.backends.base import BaseEmailBackend
from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class GmailBackend(BaseEmailBackend):
    """
    Email backend that uses Gmail API with Service Account for sending emails.
    Suitable for production container environments.
    """

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.service = None

    def open(self):
        """Authenticate using Service Account and create Gmail API service."""
        if self.service:
            return False

        # Get service account credentials from environment variable (JSON string)
        service_account_json = os.environ.get('GMAIL_SERVICE_ACCOUNT_JSON')
        delegated_email = os.environ.get('EMAIL_HOST_USER')
        
        if not service_account_json:
            raise ValueError(
                "GMAIL_SERVICE_ACCOUNT_JSON environment variable not set. "
                "This should contain the service account JSON key."
            )

        # Parse the JSON credentials
        service_account_info = json.loads(service_account_json)
        
        # Create credentials with domain-wide delegation
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES,
            subject=delegated_email  # Impersonate this user
        )

        self.service = build('gmail', 'v1', credentials=credentials)
        return True

    def close(self):
        """Close the connection (not needed for API)."""
        pass

    def send_messages(self, email_messages):
        """Send email messages via Gmail API."""
        if not email_messages:
            return 0

        self.open()
        num_sent = 0

        for message in email_messages:
            try:
                mime_message = self._create_mime_message(message)
                self._send_message(mime_message)
                num_sent += 1
            except Exception as e:
                if not self.fail_silently:
                    raise
                print(f"Failed to send email: {e}")

        return num_sent

    def _create_mime_message(self, message):
        """Create MIME message from Django EmailMessage."""
        if message.alternatives and message.alternatives[0][1] == 'text/html':
            mime_message = MIMEMultipart('alternative')
            mime_message.attach(MIMEText(message.body, 'plain'))
            mime_message.attach(MIMEText(message.alternatives[0][0], 'html'))
        else:
            mime_message = MIMEText(message.body)

        mime_message['to'] = ', '.join(message.to)
        mime_message['from'] = message.from_email
        mime_message['subject'] = message.subject

        if message.cc:
            mime_message['cc'] = ', '.join(message.cc)
        if message.bcc:
            mime_message['bcc'] = ', '.join(message.bcc)
        if message.reply_to:
            mime_message['reply-to'] = ', '.join(message.reply_to)

        return mime_message

    def _send_message(self, mime_message):
        """Send MIME message via Gmail API."""
        raw_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode('utf-8')
        message = {'raw': raw_message}
        
        self.service.users().messages().send(
            userId='me',
            body=message
        ).execute()
