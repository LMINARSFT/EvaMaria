from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from info import ADMINS
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(client,message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ඔයා anonymous admin දාගෙන ඉන්නෙ.... මගෙ Private Chat එකට ඇවිත් /connect ගහල channel එක connect කරන්න {message.chat.id}")
    chat_type = message.chat.type

    if chat_type == "private":
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "<b>නිවැරදි අනුපිළිවෙල භාවිත කරන්න</b>\n\n"
                "<code>/connect groupid</code>\n\n"
                "<i>Gඔයාගෙ group එකෙ id ගන්න මේ බොට් ඔයාගෙ එකට  add කරන්න  <code>/id</code></i>",
                quote=True
            )
            return

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
        ):
            await message.reply_text("ඔයා මේ දුන්න group එකේ admin ඉන්න ඕනෙ අනිවාරෙන්", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "Group Id එක වැරදි\n\nඑහෙමත් නැත්නම් මම ඒ group එකේ නෑ.. මාව Group එකට add කරල උත්සාහ කරන්න",
            quote=True,
        )

        return
    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == "administrator":
            ttl = await client.get_chat(group_id)
            title = ttl.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(
                    f"Sucessfully connected to **{title}**\nදැන් ඔයාට ඔයාගෙ group එක මේ private chat එකේ ඉදන් පාලනය කරන්න පුලුවන්",
                    quote=True,
                    parse_mode="md"
                )
                if chat_type in ["group", "supergroup"]:
                    await client.send_message(
                        userid,
                        f"මේකට connect වුනා👉 **{title}** !",
                        parse_mode="md"
                    )
            else:
                await message.reply_text(
                    "මේකට කලින්ම connect කරල තිබිල තියෙන්නෙ🤗",
                    quote=True
                )
        else:
            await message.reply_text("මාව group එකේ admin කරන්න", quote=True)
    except Exception as e:
        logger.exception(e)
        await message.reply_text('අවුලක් වුනා.. ටික වෙලාවකින් නැවත උත්සාහ කරන්න', quote=True)
        return


@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client,message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ඔයා anonymous admin දාගෙන ඉන්නෙ මගෙ private chat එකට ඇවිත් /connect ගහල group එක connect කරන්න {message.chat.id} ")
    chat_type = message.chat.type

    if chat_type == "private":
        await message.reply_text("මාව groupp එකකින් disconnect කරන්නයි දැනට connect වෙලා තියෙන grou /channel ටික බලාගන්නයි /connections දෙන්න​", quote=True)

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

        st = await client.get_chat_member(group_id, userid)
        if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text("මේ chat එකෙන් disconnect කරා, quote=True)
        else:
            await message.reply_text("මේක මට කලින් connect කරල තිබ්බ එකක් නෙවේ..\nConnect කරන්න ඕනනම් /connect දෙන්න", quote=True)



@Client.on_message(filters.private & filters.command(["connections"]))
async def connections(client,message):
    userid = message.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        await message.reply_text(
            "කිසිම group/channel එකකට connect කරලා නෑ.. ඔයා මුලින්ම මාව group / channel එකකට  connect කරලා ඉන්න",
            quote=True
        )
        return
    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                    )
                ]
            )
        except:
            pass
    if buttons:
        await message.reply_text(
            "දැනට තියෙන Connections ;\n\n",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply_text(
            "කිසිම group / channel එකකට connect කරලා නෑ.. ඔයා මුලින්ම මාව group / channel එකකට connect කරලා ඉන්න",
            quote=True
        )
