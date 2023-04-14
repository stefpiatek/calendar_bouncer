import requests
from loguru import logger

from calendar_bouncer.config import credential, scopes

REQUEST_TIMEOUT_SECONDS = 10


def delete_permissions():
    """Delete all shared permissions on all calendars where that permission is removable (using REST API)"""
    access = credential.get_token(" ".join(scopes))
    headers = {"Authorization": f"Bearer {access.token}", "Accept": "application/json"}
    permissions_url = (
        "https://graph.microsoft.com/v1.0/me/calendar/calendarPermissions/"
    )
    response = requests.get(
        permissions_url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS
    )
    shared_calendars = response.json().get("value")
    for calendar in shared_calendars:
        if calendar.get("isRemovable") is True:
            delete_shared_calendar(calendar, headers)
    logger.success("No more deletable calendars are left!")


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
