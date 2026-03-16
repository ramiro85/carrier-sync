from fastapi import APIRouter, Body, Depends
from app.core.schemas import ResponseModel
from app.services.googleCloud.controller import GoogleApiController
from app.services.googleCloud.dependencies import get_gmail_service_account_controller
from app.services.googleCloud.schemas import (
    TmsMessage as MessageSchema,
    TmsMessageQuery,
)

router = APIRouter()


@router.api_route(
    path="/api/gmail/send", methods=["POST"], response_model=ResponseModel
)
def send_message(
    message: MessageSchema = Body(...),
    gmail_api: GoogleApiController = Depends(get_gmail_service_account_controller),
):
    """Send an email message through Gmail API."""
    return gmail_api.send_message(message)


@router.api_route(methods=["POST"], path="/api/gmail/search_thread", deprecated=False)
def search_thread(
    query: TmsMessageQuery,
    gmail_api: GoogleApiController = Depends(get_gmail_service_account_controller),
) -> ResponseModel:
    """Find a thread by subject and optional sender/recipient filters."""
    return gmail_api.search_thread(
        query_subject=query.subject,
        username=query.username,
        from_email=query.from_email,
    )


@router.api_route(methods=["POST"], path="/api/gmail/find_messages", deprecated=False)
def find_messages(
    query: TmsMessageQuery,
    gmail_api: GoogleApiController = Depends(get_gmail_service_account_controller),
) -> ResponseModel:
    """List matching messages by subject and optional sender/recipient filters."""
    return gmail_api.find_messages(
        query_subject=query.subject,
        username=query.username,
        from_email=query.from_email,
    )


@router.api_route(methods=["POST"], path="/api/gmail/getAttachment", deprecated=False)
def get_attachment(
    query: TmsMessageQuery,
    gmail_api: GoogleApiController = Depends(get_gmail_service_account_controller),
) -> ResponseModel:
    """Download and persist an attachment from a thread message."""
    return gmail_api.save_attachment(
        thread_id=query.thread_id,
        filename=query.filename,
        username=query.username,
        save_dir=query.save_dir,
    )


@router.api_route(methods=["POST"], path="/api/gmail/get_contacts", deprecated=False)
def get_contacts(
    query: TmsMessageQuery,
    gmail_api: GoogleApiController = Depends(get_gmail_service_account_controller),
) -> ResponseModel:
    """Extract unique contacts from messages matching the provided filters."""
    return gmail_api.find_contacts(
        query_subject=query.subject,
        username=query.username,
        from_email=query.from_email,
    )
