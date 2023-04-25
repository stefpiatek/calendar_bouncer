import requests
from azure.core.exceptions import ClientAuthenticationError
from loguru import logger

from calendar_bouncer.config import consent_url, credential, scopes

REQUEST_TIMEOUT_SECONDS = 10


def delete_permissions():
    """Delete all shared permissions on all calendars where that permission is removable (using REST API)"""
    try:
        access = credential.get_token(" ".join(scopes))
    except ClientAuthenticationError:
        logger.info(
            "If consent hasn't been given to this application before, navigate to this url:\n{consent_url}",
            consent_url=consent_url,
        )
        return

    headers = {"Authorization": f"Bearer {access.token}", "Accept": "application/json"}
    permissions_url = (
        "https://graph.microsoft.com/v1.0/me/calendar/calendarPermissions/"
    )
    response = requests.get(
        permissions_url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS
    )
    shared_calendars = response.json().get("value")
    deletion_count = 0
    for calendar in shared_calendars:
        if calendar.get("isRemovable") is True:
            delete_shared_calendar(calendar, headers)
            deletion_count += 1
    if deletion_count > 0:
        logger.success(
            f"Deleted {deletion_count} shared permissions on calendars",
            deletion_count=deletion_count,
        )
    else:
        logger.info(
            "No share permissions to delete, these probably have already been deleted"
        )


def delete_shared_calendar(calendar, headers):
    """Delete a single shared calendar via REST API"""
    delete_calendar_template = (
        "https://graph.microsoft.com/v1.0/me/calendar/calendarPermissions/{calendar_id}"
    )
    calendar_id = calendar.get("id")
    logger.info(
        "Deleting calendar shared with {shared_with}",
        shared_with=calendar.get("emailAddress").get("name"),
    )
    requests.delete(
        delete_calendar_template.format(calendar_id=calendar_id),
        headers=headers,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
