import base64
import mimetypes
import os
from email.message import EmailMessage
from re import split
from typing import Optional, Any
from pydantic import BaseModel
from dataclasses import dataclass


class TmsMessageQuery(BaseModel):
    filename: str = None
    username: str = None
    save_dir: str = None
    thread_id: str = None
    from_email: str = None
    subject: str = None
    q: str = None


class TmsMessage(BaseModel):
    From: dict
    To: list = None
    CC: Optional[list] = None
    BCC: Optional[list] = None
    Subject: str = None
    body: str = None
    Attachment: Optional[list[str]] = None
    username: str = None
    alias: str = None
    id: Optional[list] = None
    thread_id: Optional[str] = None
    message_id: Optional[str] = None

    def __init__(self, **data: Any) -> None:
        super().__init__(
            **data
        )  # Validate that From is provided and is a non-empty dict
        if self.From and isinstance(self.From, dict) and len(self.From) > 0:
            self.username, self.alias = next(iter(self.From.items()))
        else:
            # Set default values or raise an error depending on your requirements
            self.username = None
            self.alias = None

    def get_email_message(self):
        # Validate that username and alias are set before creating email
        if not self.username or not self.alias:
            raise ValueError(
                "From field must be provided with valid username and alias"
            )
        message = EmailMessage()
        message.add_alternative(self.body, subtype="html")
        message["Subject"] = self.Subject
        message["From"] = f"{self.alias}<{self.username}>"
        message["To"] = self.To

        if self.CC:
            message["CC"] = self.CC

        if self.BCC:
            message["BCC"] = self.BCC

        if self.message_id:
            message["In-Reply-To"] = self.message_id
            message["References"] = self.message_id

        # attachment
        if self.Attachment:
            for attachment_path in self.Attachment:
                if os.path.exists(attachment_path):
                    attachment_data, maintype, subtype, filename = self.add_attachment(
                        attachment_path
                    )
                    message.add_attachment(
                        attachment_data, maintype, subtype, filename=filename
                    )
        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        if self.thread_id:
            create_message["threadId"] = self.thread_id
        return create_message

    @staticmethod
    def add_attachment(attachment_path: str):
        filename = split("/", attachment_path)[-1:][0]
        # guessing the MIME type
        type_subtype, _ = mimetypes.guess_type(attachment_path)
        maintype, subtype = type_subtype.split("/")
        with open(attachment_path, "rb") as fp:
            attachment_data = fp.read()
        return attachment_data, maintype, subtype, filename


@dataclass
class Headers:
    Delivered_To: str
    Received: str
    X_Received: str
    ARC_Seal: str
    ARC_Message_Signature: str
    ARC_Authentication_Results: str
    Return_Path: str
    Received_SPF: str
    Authentication_Results: str
    DKIM_Signature: str
    X_Google_DKIM_Signature: str
    X_Gm_Message_State: str
    X_Gm_Gg: str
    X_Google_Smtp_Source: str
    MIME_Version: str
    From: str
    Date: str
    X_Gm_Features: str
    Message_ID: str
    Subject: str
    To: str
    CC: str
    Content_Type: str

    @staticmethod
    def from_dict(obj: Any) -> "Headers":
        _Delivered_To = str(obj.get("Delivered-To"))
        _Received = str(obj.get("Received"))
        _X_Received = str(obj.get("X-Received"))
        _ARC_Seal = str(obj.get("ARC-Seal"))
        _ARC_Message_Signature = str(obj.get("ARC-Message_Signature"))
        _ARC_Authentication_Results = str(obj.get("ARC-Authentication-Results"))
        _Return_Path = str(obj.get("Return-Path"))
        _Received_SPF = str(obj.get("Received-SPF"))
        _Authentication_Results = str(obj.get("Authentication-Results"))
        _DKIM_Signature = str(obj.get("DKIM-Signature"))
        _X_Google_DKIM_Signature = str(obj.get("X-Google-DKIM-Signature"))
        _X_Gm_Message_State = str(obj.get("X-Gm-Message-State"))
        _X_Gm_Gg = str(obj.get("X-Gm-Gg"))
        _X_Google_Smtp_Source = str(obj.get("X-Google_Smtp-Source"))
        _MIME_Version = str(obj.get("MIME-Version"))
        _From = str(obj.get("From"))
        _Date = str(obj.get("Date"))
        _X_Gm_Features = str(obj.get("X-Gm-Features"))
        _Message_ID = (
            str(obj.get("Message-ID"))
            if obj.get("Message-ID")
            else obj.get("Message-Id")
        )
        _Subject = str(obj.get("Subject"))
        _To = str(obj.get("To"))
        _CC = str(obj.get("CC"))
        _Content_Type = str(obj.get("Content-Type"))
        return Headers(
            _Delivered_To,
            _Received,
            _X_Received,
            _ARC_Seal,
            _ARC_Message_Signature,
            _ARC_Authentication_Results,
            _Return_Path,
            _Received_SPF,
            _Authentication_Results,
            _DKIM_Signature,
            _X_Google_DKIM_Signature,
            _X_Gm_Message_State,
            _X_Gm_Gg,
            _X_Google_Smtp_Source,
            _MIME_Version,
            _From,
            _Date,
            _X_Gm_Features,
            _Message_ID,
            _Subject,
            _To,
            _CC,
            _Content_Type,
        )
