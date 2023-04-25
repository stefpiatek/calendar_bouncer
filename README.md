# calendar_bouncer

[![Actions Status][actions-badge]][actions-link]

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/stefpiatek/calendar_bouncer/workflows/CI/badge.svg
[actions-link]:             https://github.com/stefpiatek/calendar_bouncer/actions

<!-- prettier-ignore-end -->

A pretty dumb application to delete all possible shared permissions on your work
Outlook calendars.

## Setup instructions

Register application in azure and create API permissions

- Select `App registrations` in <https://portal.azure.com>, using your work
  account
- Select `+ New Registation` and create a new registration
  - Ensure that
    `Accounts in this organizational directory only (University College London only - Single tenant)`
    is selected
  - For the redirect URI select `Public client/native (mobile & desktop)` and
    enter `https://login.microsoftonline.com/common/oauth2/nativeclient` for the
    URL
  - Click `Register`
- Note down the `Application (client) ID` value and `Directory (tenant) ID`
  value in the redirect page
- The redirect page will have a _Client Credentials_ in the table: click
  `Add a certificate or secret`
  - Add a new secret with a sensible name and expiration date, noting down the
    secret value
- On the left hand side of the main page click on the `API permissions`
  - Click on `+ Add a permission` and select `Microsoft Graph`
  - Select `Delegated Permissions`
  - In the `Select Permissions` search box, enter `Calendars`
  - From the permission table below, expand `Calendars` and tick
    `Calendars.ReadWrite`
  - Then select `Add permissions`

Configure local application

- Clone and install the repository
  ```shell
  git clone git@github.com:stefpiatek/calendar_bouncer.git
  cd calendar_bouncer
  pip install -e .
  ```
- Copy and the secret credentials and replace dummy values with those noted down
  from the previous steps, along with your work email and password
  ```shell
  cp example.secrets.toml .secrets.toml
  # Now edit the file
  ```
- If you haven't run the application before, run it from the command line so
  that it will generate a URL for you to consent to the application carrying out
  delegated calendar actions for you
  ```shell
  calendar_bouncer
  ```
- Click on the link in the STD out, logging in and accepting the permissions
  (redirect is expected to be a blank page)
- The application should now be able to run from the CLI successfully
  ```shell
  calendar_bouncer
  ```
