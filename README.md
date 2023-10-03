# Getting started with Daily Report Bot

## Configuration (config.py)

### `BOT_TOKEN` - token of bot (required)
### `SERVER_ID` - identification of server (required)
### `CATEGORY_NAME` - name of category of report channels
### `CHANNELS_ROLES_NAMES_DICT` - channels name and roles name dict

## Functionality

1) ### Every `REPORT_REQUEST_TIME` hours, the bot sends a message to write about what they have done during the day. The bot can receive messages from `REPORT_REQUEST_TIME` to `DAILY_REPORT_TIME` hours.
2) ### Every `DAILY_REPORT_TIME` hours, the bot sends user reports to different channels from the list of `CHANNELS_ROLES_NAMES_DICT`
3) ### Can generate channels and roles by command `!create_channels_roles`

## Running

1) ### `python app/main.py`
2) ### Sent command in PM `!create_channels_roles` for creating channels and roles for the server and after that define user roles