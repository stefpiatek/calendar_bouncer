"""Experimenting using the SDK, but having some issues currently"""

import asyncio

from loguru import logger
from msgraph.generated.me.calendar.calendar_permissions.calendar_permissions_request_builder import (
    CalendarPermissionsRequestBuilder,
)
from msgraph.generated.models.o_data_errors.o_data_error import ODataError

from calendar_bouncer.config import client


async def delete_calendar_permissions_using_sdk():
    """
    Delete calendar permissions using SDK API

    Currently, failing because it looks like there are no permissions and also get this error:

    > The following parameters are not supported with change tracking over the 'FindCalendarPermissions' resource:
    > '$orderby, $filter, $select, $expand, $search, $delta'

    """
    user = await client.users_by_id("sejjpia@ucl.ac.uk").get()
    logger.debug(user)

    query_params = CalendarPermissionsRequestBuilder.CalendarPermissionsRequestBuilderGetQueryParameters(
        select=["isRemovable"]
    )
    request_config = CalendarPermissionsRequestBuilder.CalendarPermissionsRequestBuilderGetRequestConfiguration(
        query_parameters=query_params
    )
    permission_count = await client.me.calendar.calendar_permissions.count.get(
        request_config
    )
    logger.debug("Number of permissions: {count}", count=permission_count)

    message_template = "Error: {message}"
    try:
        permission = await client.me.calendar.calendar_permissions.get(request_config)
        logger.success(permission)
    except ODataError as exception:
        logger.error(message_template, message=exception.error.message)
    except Exception as exception:
        logger.error(message_template, message=exception)


def delete_permissions():
    """Wrap async call in function"""
    asyncio.run(delete_calendar_permissions_using_sdk())
    logger.success("All done")


if __name__ == "__main__":
    delete_permissions()
