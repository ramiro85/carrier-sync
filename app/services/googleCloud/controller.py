import base64
import os
from datetime import datetime, timedelta

from googleapiclient.errors import HttpError

from app.core.schemas import ResponseModel
from app.core.utils import get_headers_object, clean_email, get_contact_list
from app.services.googleCloud.schemas import TmsMessage
from app.config import settings


class GoogleApiController:
    creds, service, logged = None, None, False

    def __init__(self):
        super().__init__()

    def authorize(self, username):
        """Authenticate an API client for the provided mailbox user."""
        raise NotImplementedError(
            "GoogleApiController.authorize must be implemented by a subclass"
        )

    def send_message(self, tms_message: TmsMessage):
        """Send an email and return a standardized response payload."""
        success, message, send_message = False, "", None
        self.authorize(tms_message.username)
        # if it is replying to
        if tms_message.thread_id:
            last_msg = self.search_messages_by_thread_id(
                tms_message.username, tms_message.thread_id, 0
            )
            msg_headers = last_msg.get("payload", {}).get("headers", [])
            headers = get_headers_object(msg_headers)
            tms_message.message_id = headers.Message_ID
        create_message = tms_message.get_email_message()
        try:
            send_message = (
                self.service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            success = "id" in send_message.keys() and send_message["id"] is not None
            message = "Email sent successfully!"
        except HttpError as error:
            message = f"An error occurred: {error}"

        return ResponseModel(success=success, message=message, data=send_message)

    def find_thread(self, username, after=None, from_email=None):
        """Fetch threads filtered by date and optional recipient."""
        self.authorize(username)
        if self.logged:
            five_days_ago = datetime.today() - timedelta(days=5)
            formatted = five_days_ago.strftime("%Y/%m/%d")
            query = f"after:{after}" if after else f"after:{formatted}"
            if from_email:
                query += f' to:{from_email.replace(",", "|")}'
                search = self.service.users().threads().list(userId="me", q=query)
            else:
                search = self.service.users().threads().list(userId="me")

            return search.execute().get("threads", [])
            # tdata = (self.service.users().threads().get(userId="me", id=threads[0]["id"]).execute())
        return None

    def search_messages_by_thread_id(self, username, thread_id, last=-1):
        """Get a message by index from a thread id."""
        self.authorize(username)
        results = (
            self.service.users().threads().get(userId="me", id=thread_id).execute()
        )
        messages = results.get("messages", [])
        return messages[
            last
        ]  # return the last message in thread(the one with the attachment)

    def save_attachment(self, username, thread_id, filename, save_dir):
        """Download attachment(s) from a thread and save them to disk."""
        message = self.search_messages_by_thread_id(username, thread_id)
        msg_id = message["id"]
        parts = message.get("payload", {}).get("parts", [])
        save_path = settings.attachment_path + save_dir
        multiple = False
        save_path_temp = ""
        pdf_file_names = []
        if len(parts) > 2:
            save_path_temp = settings.attachment_path + save_dir + f"/{filename[:-4]}"
            os.makedirs(save_path_temp, exist_ok=True)
            multiple = True
        else:
            os.makedirs(save_path, exist_ok=True)

        for part in parts:
            if part["filename"] and "attachmentId" in part["body"]:
                attachment = (
                    self.service.users()
                    .messages()
                    .attachments()
                    .get(userId="me", messageId=msg_id, id=part["body"]["attachmentId"])
                    .execute()
                )

                data = base64.urlsafe_b64decode(attachment["data"])
                if multiple:
                    file_path = os.path.join(
                        save_path_temp if multiple else save_path, part["filename"]
                    )
                    pdf_file_names.append(file_path)
                else:
                    file_path = os.path.join(save_path, filename)
                with open(file_path, "wb") as f:
                    f.write(data)

        return ResponseModel(success=True, message="Saved attachment!", data={})

    def search_thread(
        self, username, query_subject, after=None, before=None, from_email=None
    ):
        """Find the latest matching thread by subject."""
        success, message, result, _send_message = False, "", {}, None
        threads = self.find_thread(
            username=username, after=after, from_email=from_email
        )
        if threads:
            for thread in threads:
                tdata = (
                    self.service.users()
                    .threads()
                    .get(userId="me", id=thread["id"])
                    .execute()
                )
                msg = tdata["messages"][0]["payload"]
                headers = get_headers_object(msg["headers"])
                subject = headers.Subject
                if subject and query_subject in subject:  # skip if no Subject line
                    success = True
                    message = subject
                    thread["message"] = {
                        "thread_id": thread["id"],
                        "subject": subject,
                        "message_id": headers.Message_ID,
                        "to": headers.To,
                        "from": headers.From,
                    }
                    result = thread
        return ResponseModel(success=success, message=message, data=result)

    def find_messages(
        self, username, query_subject, after=None, before=None, from_email=None
    ):
        """Return all matching message summaries for a subject query."""
        success, message, result, _send_message = False, "", [], None
        threads = self.find_thread(
            username=username, after=after, from_email=from_email
        )
        message = f"Threads found : {len(threads)}"
        for thread in threads:
            tdata = (
                self.service.users()
                .threads()
                .get(userId="me", id=thread["id"])
                .execute()
            )
            msg = tdata["messages"][0]["payload"]
            headers = get_headers_object(msg["headers"])
            subject = headers.Subject
            if subject and query_subject in subject:  # skip if no Subject line
                success = True
                result.append(
                    {
                        "thread_id": thread["id"],
                        "subject": subject,
                        "message_id": headers.Message_ID,
                        "to": clean_email(headers.To),
                        "from": headers.From,
                    }
                )
        return ResponseModel(success=success, message=message, data=result)

    def find_contacts(self, username, query_subject, after=None, from_email=None):
        """Extract unique contacts from matching threads."""
        success, message, result, = False, "", []
        threads = self.find_thread(
            username=username, after=after, from_email=from_email
        )
        message = f"Threads found : {len(threads)}"
        for thread in threads:
            tdata = (
                self.service.users()
                .threads()
                .get(userId="me", id=thread["id"])
                .execute()
            )
            msg = tdata["messages"][0]["payload"]
            headers = get_headers_object(msg["headers"])
            subject = headers.Subject
            if subject and query_subject in subject:
                success = True
                for contact in get_contact_list(headers.To):
                    result.append(contact)
        contacts = list({tuple(sorted(d.items())): d for d in result}.values())
        return ResponseModel(success=success, message=message, data=contacts)
