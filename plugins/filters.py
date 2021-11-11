import io
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.filters_mdb import(
   add_filter,
   get_filters,
   delete_filter,
   count_filters
)

from database.connections_mdb import active_connection
from utils import get_file_id, parser, split_quotes
from info import ADMINS


@Client.on_message(filters.command(['filter', 'add']) & filters.incoming)
async def addfilter(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ඔයා anonymous admin දාගෙන ඉන්නෙ...මගෙ private chat එකට ඇවිත් /connect ගහල channel / group  එක connect කරන්න {message.chat.id} ")
    chat_type = message.chat.type
    args = message.text.html.split(None, 1)

    if chat_type == "private":
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("මම ඔයාග groupෙ එකේ ඉන්නවද කියල බලන්න", quote=True)
                return
        else:
            await message.reply_text("මම දැනට කිසිම group එකකට connect වෙලා නෑ", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
        st.status != "administrator"
        and st.status != "creator"
        and str(userid) not in ADMINS
    ):
        return


    if len(args) < 2:
        await message.reply_text("Command Incomplete :(", quote=True)
        return

    extracted = split_quotes(args[1])
    text = extracted[0].lower()

    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("ෆිල්ටර් කරන්න මොකක්හරි දෙන්න​", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = parser(extracted[1], text)
        fileid = None
        if not reply_text:
            await message.reply_text("බටන් එකට text එකෙක් දෙන්නම වෙනවා", quote=True)
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = get_file_id(message.reply_to_message)
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None

    elif message.reply_to_message and message.reply_to_message.media:
        try:
            msg = get_file_id(message.reply_to_message)
            fileid = msg.file_id if msg else None
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = parser(message.reply_to_message.text.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    else:
        return

    await add_filter(grp_id, text, reply_text, btn, fileid, alert)

    await message.reply_text(
        f"Filter for  `{text}`  added in  **{title}**",
        quote=True,
        parse_mode="md"
    )


@Client.on_message(filters.command(['viewfilters', 'filters']) & filters.incoming)
async def get_all(client, message):
    
    chat_type = message.chat.type
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ඔයා anonymous admin දාගෙන ඉන්නෙ...මගෙ private chat එකට ඇවිත් /connect ගහල channel / group  එක connect කරන්න {message.chat.id}")
    if chat_type == "private":
        userid = message.from_user.id
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("මම ඔයාගෙ group එකේ ඉන්නවද කියල බලන්න", quote=True)
                return
        else:
            await message.reply_text("මම දැනට කිසිම group එකකට connect වෙලා නෑ", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
        st.status != "administrator"
        and st.status != "creator"
        and str(userid) not in ADMINS
    ):
        return

    texts = await get_filters(grp_id)
    count = await count_filters(grp_id)
    if count:
        filterlist = f"තියෙන සියලුම ෆිල්ටර් ගණන👉 **{title}** : {count}\n\n"

        for text in texts:
            keywords = " ×  `{}`\n".format(text)

            filterlist += keywords

        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        filterlist = f"මේ group එකේ සක්‍රීය ෆිල්ටර් එකක්වත් නෑ **{title}**"

    await message.reply_text(
        text=filterlist,
        quote=True,
        parse_mode="md"
    )
        
@Client.on_message(filters.command('del') & filters.incoming)
async def deletefilter(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ඔයා anonymous admin දාගෙන ඉන්නෙ...මගෙ private chat එකට ඇවිත් /connect ගහල channel / group  එක connect කරන්න {message.chat.id}")
    chat_type = message.chat.type

    if chat_type == "private":
        grpid  = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("මම ඔයාගෙ group එක adminේ ඉන්නවද කියල බලන්න", quote=True)
                return
        else:
            await message.reply_text("මම දැනට කිසිම group එකකට connect වෙලා නෑ", quote=True)

    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
        st.status != "administrator"
        and st.status != "creator"
        and str(userid) not in ADMINS
    ):
        return

    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>ඔයාට delete කරන්න ඕනෙ ෆිල්ටර් එකේ නම සදහන් කරන්න</i>\n\n"
            "<code>/del filtername</code>\n\n"
            "Use /viewfilters 👈මේක දෙන්න දැනට තියෙන සියලු ෆිල්ටර් බලාගන්න",
            quote=True
        )
        return

    query = text.lower()

    await delete_filter(message, query, grp_id)
        

@Client.on_message(filters.command('delall') & filters.incoming)
async def delallconfirm(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ඔයා anonymous admin දාගෙන ඉන්නෙ...මගෙ private chat එකට ඇවිත් /connect ගහල channel / group  එක connect කරන්න {message.chat.id}")
    chat_type = message.chat.type

    if chat_type == "private":
        grpid  = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("මම ඔයාගෙ group එක adminේ ඉන්නවද කියල බලන්න", quote=True)
                return
        else:
            await message.reply_text("මම දැනට කිසිම group එකකට connect වෙලා නෑ", quote=True)
            return

    elif chat_type in ["group", "supergroup"]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (st.status == "creator") or (str(userid) in ADMINS):
        await message.reply_text(
            f"මේකෙන් මේ group එකේ තියෙන සියලු ෆිල්ටර් delete කරනව '{title}'.\nඑහෙම කරන්නද?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="හා",callback_data="delallconfirm")],
                [InlineKeyboardButton(text="එපා",callback_data="delallcancel")]
            ]),
            quote=True
        )

