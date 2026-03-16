# API Methods Reference

This document lists public HTTP endpoints and key service methods.

## HTTP Endpoints

### Core
- `POST /health`
  - Returns service health status.

### SAFER
- `GET /api/safer/search/{query_field}/{query_value}`
  - Looks up carrier data from SAFER by query field/value.

### TAFS
- `GET /api/tafs/search_broker/{mc}`
  - Searches broker data and debtor details by MC.
- `GET /api/tafs/load_debtor/{account_id}?mc={optional}`
  - Loads a debtor record by account id.

### Gmail
- `POST /api/gmail/send`
  - Sends an email message.
- `POST /api/gmail/search_thread`
  - Finds a thread by subject and filters.
- `POST /api/gmail/find_messages`
  - Lists messages matching subject and filters.
- `POST /api/gmail/getAttachment`
  - Downloads attachment(s) from a thread.
- `POST /api/gmail/get_contacts`
  - Returns unique contacts from matching messages.

### ELD Drivers
- `POST /api/eld/drivers/{driver_id}`
  - Creates driver.
- `GET /api/eld/drivers/{driver_id}`
  - Gets driver by id.
- `PUT /api/eld/drivers/{driver_id}`
  - Updates driver.
- `DELETE /api/eld/drivers/{driver_id}`
  - Deletes/deactivates driver.
- `GET /api/eld/drivers/company/{company_id}`
  - Lists drivers for company.
- `PATCH /api/eld/drivers/{driver_id}/activate`
  - Activates driver.
- `PATCH /api/eld/drivers/{driver_id}/deactivate`
  - Deactivates driver.

## Key Service Methods

### `GoogleApiController`
- `authorize(username)`
- `send_message(tms_message)`
- `find_thread(username, after=None, from_email=None)`
- `search_messages_by_thread_id(username, thread_id, last=-1)`
- `save_attachment(username, thread_id, filename, save_dir)`
- `search_thread(username, query_subject, after=None, before=None, from_email=None)`
- `find_messages(username, query_subject, after=None, before=None, from_email=None)`
- `find_contacts(username, query_subject, after=None, from_email=None)`

### `GoogleServiceAccountApiController`
- `_get_domain(email)`
- `_resolve_account(username)`
- `_resolve_service_account_file(path)`
- `_resolve_subject(username, default_impersonated_user)`
- `authorize(username)`

### `TafsController`
- `_update_asp_state(html_content)`
- `is_authenticated()`
- `login()`
- `get_view(url)`
- `search_broker(query)`
- `load_debtor(account_id)`
- Helper: `select_best_debtor(debtor_list)`

### `ReliableApi`
- `login(force=False)`
- `refresh_token()`
- `is_logged(carrier=None)`
- `get_valid_token()`

### `ELDDriverController`
- `_refresh_token()`
- `_make_request(method, url, **kwargs)`
- `update_authorization_token(token)`
- `create_driver(driver_id, driver_data)`
- `get_driver(driver_id)`
- `update_driver(driver_id, driver_data, rev=None)`
- `delete_driver(driver_id, rev=None)`
- `list_drivers(company_id, limit=100, skip=0)`
- `activate_driver(driver_id, rev=None)`
- `deactivate_driver(driver_id, rev=None)`

### SAFER controller functions
- `find_value_of(soup, text)`
- `is_inactive(soup)`
- `find_operating_status(soup)`
- `parse_address(address_string)`
- `check_company(query_param, query_string)`

### Shared utility functions
- `get_headers_object(headers)`
- `clean_email(str_emails)`
- `get_contact_list(str_emails)`
