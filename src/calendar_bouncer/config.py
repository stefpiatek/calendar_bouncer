from azure.identity import UsernamePasswordCredential
from dynaconf import Dynaconf
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider,
)
from loguru import logger
from msgraph import GraphRequestAdapter, GraphServiceClient

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

consent_url = (
    f"https://login.microsoftonline.com/{settings.tenant_id}/oauth2/authorize?client_id={settings.client_id}"
    "&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient&response_type=code&prompt=consent"
)
logger.info(
    "If consent hasn't been given to this application before, navigate to this url:\n{consent_url}",
    consent_url=consent_url,
)

# Username and password less secure, but does allow this to be run non-interactively
credential = UsernamePasswordCredential(
    client_id=settings.client_id,
    username=settings.username,
    password=settings.password,
    tenant_id=settings.tenant_id,
    client_credential=settings.client_secret,
)
scopes = ["Calendars.ReadWrite"]
auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes)
request_adapter = GraphRequestAdapter(auth_provider)
client = GraphServiceClient(request_adapter)
