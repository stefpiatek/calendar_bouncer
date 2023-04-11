"""Experimenting using the SDK, but having some issues currently"""

import asyncio

from loguru import logger
from msgraph.generated.me.calendar.calendar_permissions.calendar_permissions_request_builder import (
    CalendarPermissionsRequestBuilder,
)

from calendar_bouncer.config import client


async def delete_calendar_permissions_using_sdk():
    user = await client.users_by_id("sejjpia@ucl.ac.uk").get()
    me = await client.me.get()
    logger.debug(user)
    logger.debug(me)

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

    try:
        permission = await client.me.calendar.calendar_permissions.get(request_config)
        logger.success(permission)
    except Exception as e:
        message_template = "Error: {message}"
        if e.__getattribute__("error"):
            logger.error(message_template, message=e.error.message)
        else:
            logger.error(message_template, message=e)

        raise e


def delete_permissions():
    asyncio.run(delete_calendar_permissions_using_sdk())
    logger.success("All done")
