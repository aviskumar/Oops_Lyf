# PORTED EVAL FROM TheCodents/DevelopersUserbot
# PORTED BASH FROM TeamUltroid/Ultroid

import traceback
import sys
import os
import re
import subprocess
import io
import asyncio
from io import StringIO
from pyrogram import Client, filters
from pyrogram.types import Message


self_or_contact_filter = filters.create(
    lambda _, __, message:
    (message.from_user and message.from_user.is_contact) or message.outgoing
)


async def aexec(code, client, m):
    c = m.chat.id
    message = m
    rm = m.reply_to_message
    exec(
        f"async def __aexec(client, m, c, rm, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, m, c, rm, message)

p = print

@Client.on_message(self_or_contact_filter & filters.command('eval', prefixes='!'))
async def evaluate(client, m: Message):

    status_message = await m.reply_text("`Running ...`")
    try:
        cmd = m.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    reply_to_id = m.message_id
    if m.reply_to_message:
        reply_to_id = m.reply_to_message.message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, m)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"<b>Command:</b>\n<code>{cmd}</code>\n\n<b>Output</b>:\n<code>{evaluation.strip()}</code>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await m.reply_document(
            document=filename,
            caption="Pyrogram Eval",
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove(filename)
        await status_message.delete()
    else:
        await status_message.edit(final_output)
        
        
p = print

@Client.on_message(self_or_contact_filter & filters.command('bash', prefixes='!'))
async def terminal(client, m: Message):
    shtxt = await m.reply_text("`Processing...`")
    try: 
        cmd = m.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await shtxt.edit("`No cmd given`")
    
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    OUT = f"**☞ BASH\n\n• COMMAND:**\n`{cmd}` \n\n"
    e = stderr.decode()
    if e:
        OUT += f"**• ERROR:** \n`{e}`\n\n"
    t = stdout.decode()
    if t:
        _o = t.split("\n")
        o = "\n".join(_o)
        OUT += f"**• OUTPUT:**\n`{o}`"
    if not e and not t:
        OUT += f"**• OUTPUT:**\n`Success`"
    if len(OUT) > 4096:
        ultd = OUT.replace("`", "").replace("*", "").replace("_", "")
        with io.BytesIO(str.encode(ultd)) as out_file:
            out_file.name = "bash.txt"
            await m.reply_document(
                document=out_file,
                caption="`Output file`",
                reply_to_message_id=m.message_id
            )
            await shtxt.delete()
    else:
        await shtxt.edit(OUT)        
        

@Client.on_message(filters.command('id', prefixes='!'))
async def msgid(client, message: Message):
    replied = message.reply_to_message
    chat_id = message.chat.id
    if replied:
        sender_id = message.reply_to_message.from_user.id
        try:
            if replied.sticker:
                bot_api_file_id = replied.sticker.file_id
            if replied.document:
                bot_api_file_id = replied.document.file_id
            if replied.photo:
                bot_api_file_id = replied.photo.file_id
            if replied.video:
                bot_api_file_id = replied.video.file_id
            if replied.audio:
                bot_api_file_id = replied.audio.file_id
            if replied.voice:
                bot_api_file_id = replied.voice.file_id
            await client.send_message(message.chat.id, f"**Chat ID:** `{chat_id}` \n**User ID:** `{sender_id}` \n**File ID:** `{bot_api_file_id}`", reply_to_message_id=replied.message_id)
        except Exception as e:
            await client.send_message(message.chat.id, f"**Chat ID:** `{chat_id}` \n**User ID:** `{sender_id}`", reply_to_message_id=replied.message_id)
    else:
        await message.reply_text(f"**Chat ID:** `{chat_id}`")
