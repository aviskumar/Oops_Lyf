import os
import asyncio
import aiofiles
import json
import requests

from pyrogram import Client, filters, idle
from pyrogram.types import Messages


dog_ = "https://dogebin.up.railway.app/"
spaceb = "https://spaceb.in/api/v1/documents/"

def spacebin(text, ext="txt"):
    try:
        request = requests.post(
            spaceb, 
            data={
                "content": text.encode("UTF-8"),
                "extension": ext,
            },
        )
        r = request.json()
        key = r.get('payload').get('id')
        return {
            "bin": "SpaceBin",
            "id": key,
            "link": f"https://spaceb.in/{key}",
            "raw": f"{spaceb}{key}/raw",
        }
    except Exception as e:
        return str(e)
        print(e)

def dogbin(text, ext="txt"):
    url = f"{dog_}documents"
    try:
        request = requests.post(
            url=url,
            data=json.dumps({"content": text}),
            headers={"content-type": "application/json"},
        )
        r = request.json()
        key = r.get("key")
        dogg = (
            f"{dog_}v/{key}" if r.get("isUrl") else f"{dog_}{key}"
        )
        raw = f"{dog_}raw/{key}"
        return {
            "bin": "DogBin",
            "id": key,
            "link": f"{dogg}.{ext}",
            "raw": raw,
        }
    except Exception as e:
        return str(e)
        print(e)
    
DOWNLOAD_DIR = "/app/pastebin/"
        
@Client.on_message(filters.command('paste', prefixes='!'))
async def pastebin(client, message: Message):
    replied = message.reply_to_message
    file_type = "txt"
    if replied:
        huehue = await client.send_message(message.chat.id, "`...`", reply_to_message_id=replied.message_id)
    else:
        huehue = await message.reply_text("`...`")

    if replied and replied.document:
        try:
            file_type = os.path.splitext(replied.document.file_name)[1].lstrip('.')
        except Exception as e:
            file_type = "txt"
        path = await replied.download(DOWNLOAD_DIR)
        async with aiofiles.open(path, 'r') as d_f:
            text = await d_f.read()                  
        os.remove(path)
    elif replied and replied.text:
        text = replied.text
        file_type = "txt"
    elif not replied:
        try:
            text = message.text.split(" ", maxsplit=1)[1]
            file_type = "txt"
        except Exception as e:
            await huehue.edit("`Give me Something to Paste 🙄`")
            return
    else:
        await huehue.edit("`Damn! Gib Some Txt File to Paste`")

    
    _paste = spacebin(text, file_type)
    
    if isinstance(_paste, dict) and _paste['link'] != f"https://spaceb.in/None":
        c1m = f"<b>Pasted to <a href='{_paste['link']}'>{_paste['bin']}</a> "\
        f"| <a href='{_paste['raw']}'>Raw</a></b>"
        await huehue.edit(c1m, parse_mode="html", disable_web_page_preview=True)
    else:
        try:
            _pastee = dogbin(text, file_type)
            if isinstance(_pastee, dict):
                dgbin = _pastee['link']
                draw = _pastee['raw']
                await huehue.edit(f"__SpaceBin Down__ \n**Pasted to [DogBin]({dgbin}) | [Raw]({draw})**", disable_web_page_preview=True)
            else:
                await huehue.edit(f"{str(e)}")
        except Exception as ex:
            await huehue.edit(str(ex))
