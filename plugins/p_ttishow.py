from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp
from Script import script
from pyrogram.errors import ChatAdminRequired

"""-----------------------------------------https://t.me/GetTGLink/4179 --------------------------------------"""

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspired from a boat of a banana tree
            buttons = [[
                InlineKeyboardButton('Support', url=f'https://t.me/{SUPPORT_CHAT}')
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>CHAT NOT ALLOWED 🐞\n\nමට මේකෙ message දාන්න බෑ ( Restrickted )</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
            InlineKeyboardButton('ℹ️ උදව්', url=f"https://t.me/{temp.U_NAME}?start=help"),
            InlineKeyboardButton('📢 යාවත්කාලීන කිරීම්', url='https://t.me/sinhalafilmsgo')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>මාව මේකට add කරාට ස්තූතියි👉 {message.chat.title} ❣️\n\n👨</b>",
            reply_markup=reply_markup)
    else:
        for u in message.new_chat_members:
            if (temp.MELCOW).get('welcome') is not None:
                try:
                    await (temp.MELCOW['welcome']).delete()
                except:
                    pass
            temp.MELCOW['welcome'] = await message.reply(f"<b>Hey , {u.mention}, Welcome to {message.chat.title}</b>")


@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('මට chat id එක දෙන්න')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('Support', url=f'https://t.me/{SUPPORT_CHAT}')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>හායි කස්ටිය.. මගෙ adminල මාව මේකෙ වැඩකරන එක තහනම් කරා... වැඩිදුර තොරතුරු @sinhalafilmsgo එකෙන් දැනගන්න</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
    except Exception as e:
        await message.reply(f'Error - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "හේතුවක් දෙන්න"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('වලංගු chat id එකක් දෙන්න')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("ඒ chat එක මගෙ database එකේ නෑ")
    if cha_t['is_disabled']:
        return await message.reply(f"මේ chat එක දැනටමත් disable කරල තියෙන්නෙ:\nReason-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('හරි chat එක disable කරා')
    try:
        buttons = [[
            InlineKeyboardButton('Support', url=f'https://t.me/{SUPPORT_CHAT}')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>හායි කස්ටිය.. මගෙ adminල මාව මේකෙ වැඩකරන එක තහනම් කරා... වැඩිදුර තොරතුරු @sinhalafilmsgo එකෙන් දැනගන්න.</b> \nහේතුව : <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"ප්‍රශ්නයක් - {e}")


@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('මට chat id එක දෙන්න')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('වලංගු chat id එකක් දෙන්න')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("ඒ chat එක මගෙ database එකේ නෑ")
    if not sts.get('is_disabled'):
        return await message.reply('මේක තාම disable කරල නෑනෙ')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("හරි ආයෙ enable කරා")


@Client.on_message(filters.command('stats') & filters.incoming)
async def get_ststs(bot, message):
    rju = await message.reply('තත්වය හොයන ගමන්...')
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await rju.edit(script.STATUS_TXT.format(files, total_users, totl_chats, size, free))


# a function for trespassing into others groups, Inspired by a Vazha
# Not to be used , But Just to showcase his vazhatharam.
# @Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("බෑ... මට නිසි permission නෑ")
    except Exception as e:
        return await message.reply(f'ප්‍රශ්නයක් {e}')
    await message.reply(f'මෙන්න ඔයාගෙ invite link එක {link.invite_link}')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    # https://t.me/GetTGLink/4185
    if len(message.command) == 1:
        return await message.reply('මට user id එකක් හරි usename එකක් හරි දෙන්න')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "හේතුවක් නෑනෙ.. හේතුව දෙන්න"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("මෙහෙම user කෙනෙක් මට හොයාගන්න බෑ... ආයෙ හරියට බලන්න.")
    except IndexError:
        return await message.reply("sure ද මේ සියල්ල හරි කියලා? ... මේ user Channel / group එකේ ඉන්නවද?")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} මෙයා දැනටමත් ban කරල තියෙන්නෙ\nහේතුව: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"Succesfully banned {k.mention}")


    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('මට user id එකක් හරි usename එකක් හරි දෙන්න')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "හේතුවක් නෑනෙ.. හේතුව දෙන්න"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("මෙහෙම user කෙනෙක් මට හොයාගන්න බෑ... ආයෙ හරියට බලන්න.")
    except IndexError:
        return await message.reply("මෙහෙම user කෙනෙක් මට හොයාගන්න බෑ... ආයෙ හරියට බලන්න.( User or Bot )")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} තාම ban කරල නෑ.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f" ban කරා {k.mention}")


    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # https://t.me/GetTGLink/4184
    raju = await message.reply('පරිශීලකයන් සෙට් එක ගන්නවා')
    users = await db.get_all_users()
    out = "මගෙ DB එකේ ඉන්න Users ල:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>\n"
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="Users List එක")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Chat සෙට් එක ගන්නව')
    chats = await db.get_all_chats()
    out = "මගෙ DB එකේ තියෙන Chats:\n\n"
    async for chat in chats:
        out += f"**Title:** `{chat['title']}`\n**- ID:** `{chat['id']}`\n"
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="Chat list එක")
