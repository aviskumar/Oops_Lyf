"""
tgvc-userbot, Telegram Voice Chat Userbot
Copyright (C) 2021  Dash Eclipse

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from os import environ
import logging


from pyrogram import Client, idle

API_ID = 7242984
API_HASH = "041e1741bb584ffa439b46323e284d96"
SESSION_NAME = "AQCikZcDLkxcbNihB0SDVuop2oUWjhLW7WeLOaWeqzJhjkNeaMPPjA_2bYMuVMBSha824m8HKrfkhThs4jVS5ujcUeifnenLcbFH3YSNsWS1Rd4mtD76aQXBUfeES35utfiBcKjI5P2yQIHQmVXiiCcQhRmqIxWEf_3Fpt4IHiQy74FQOr-mtVK-rRZuplpBvvzQD3WsK-MEtdrXvR4uPBavpV-fKBOe6qk0Kvx8RdliCGEXPehvJTk23UBgwL0k6NfRCOPCvkVeghIIomfIpluWtSe_2PhCIMJoQgOWGd01MpOnM-1OJ7dePezkDsJvpLBKoSkp3RQJLbJITKomQ4Pacex6PAA"

PLUGINS = dict(root="plugins")

app = Client(SESSION_NAME, API_ID, API_HASH, plugins=PLUGINS)

app.start()
print('>>> USERBOT STARTED')
logging.info('>>> USERBOT STARTED')
idle()
app.stop()
print('\n>>> USERBOT STOPPED')
logging.info('>>> USERBOT STOPPED')
