class script(object):
    START_TXT = """𝙷𝙴𝙻𝙾 {},
𝙼𝚈 𝙽𝙰𝙼𝙴 𝙸𝚂 <a href=https://t.me/{}>{}</a>, මට පුලුවන් ඔයාලට සින්හල මූවිස් දෙන්න....
මගෙ Main group එක : @sinhalafilmsgo
මාව group එකකට add කරල admin දෙන්න... එච්චරයි...ඔයාල දාන නමට ෆිල්ම් තිබ්බොත් මම දෙන්නම්"""
    HELP_TXT = """හායි {}
මේ තියෙන්නෙ මගෙ commands වලට අදාල සප් එක"""
    ABOUT_TXT = """✯ මගෙ නම: {}
✯ 𝙲𝚁𝙴𝙰𝚃𝙾𝚁: <a href=https://t.me/sinhalafilmsgo>SL Media Network ( Infine Pictures )</a>
✯ 𝙻𝙸𝙱𝚁𝙰𝚁𝚈: 𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼
✯ 𝙻𝙰𝙽𝙶𝚄𝙰𝙶𝙴: 𝙿𝚈𝚃𝙷𝙾𝙽 𝟹
✯ 𝙳𝙰𝚃𝙰 𝙱𝙰𝚂𝙴: 𝙼𝙾𝙽𝙶𝙾 𝙳𝙱
✯ 𝙱𝙾𝚃 𝚂𝙴𝚁𝚅𝙴𝚁: 𝙷𝙴𝚁𝙾𝙺𝚄
✯ 𝙱𝚄𝙸𝙻𝙳 𝚂𝚃𝙰𝚃𝚄𝚂: v1.0.1 [ 𝙱𝙴𝚃𝙰 ]"""
    SOURCE_TXT = """<b>NOTE:</b>
- Credits - EvaMaria Developer"""
    
    MANUELFILTER_TXT = """උදවු: <b>ෆිල්ටර්</b>

- මේකෙන් ඔයාලට පුලුවන් user කෙනෙක් දාන message එකකට auto reply වෙන්න හදන්න

<b>NOTE:</b>
1. බොට්ට ඇඩ්මින් දෙන්න ඕනෙ
2. ඇඩ්මින්ලට විතරයි ෆිල්ටර් දාන්න පුලුවන්
3. Alert එකක් අකුරු 64 යි දාන්න පුලුවන්

<b>විධාන හා භාවිතයන්:</b>
• /filter - <code>Group එකට filter එකක් add කිරීමට</code>
• /filters - <code>Group එකක ඇති සියලු ෆිල්ටර් පෙන්වීමට</code>
• /del - <code>යම් ෆිල්ටර් එකක් delete කිරීමට</code>
• /delall - <code>සියලුම ෆිල්ටර් කිරීමට ( මේක කරන්න පුලුවන් group එකේ Ownerට විතරයි )</code>"""
    BUTTON_TXT = """උදවු: <b>Buttons</b>

-මෙයා Url and Inline කියන බටන් වර්ග දෙකටම support කරනව

<b>URL buttons:</b>
<code>[Button Text](buttonurl:https://t.me/sinhalafilmsgo)</code>

<b>Alert buttons:</b>
<code>[Button Text](buttonalert:මෙතන ඔයාගෙ alert message එක)</code>"""
    AUTOFILTER_TXT = """උදවු: <b>Auto Filter</b>

<b>NOTE:</b>
1. මාව channel එකේ ඇඩ්මින් කරන්න
2. ඔයාගෙ channel එක පිරිසිදු ෆයිල් තියෙන channel එකක් විය යුතුයි ( වැරදි format වගේ, Invalid extentions තියෙන්න බෑ)
3. මට ඔයා ඒ channel එකට දාපු අන්තිම message එක එවන්න
මම සේරම ෆයිල් ටික මගෙ DB එකට add කරගන්නම්"""
    CONNECTION_TXT = """උදවු: <b>Connections</b>

- ෆිල්ටර් කරන්න බොට්ව PM එකට connect කරන එක තමයි මේකෙන් කරන්නෙ
- Grou[ වල spam ගහන එක වළක්වා ගන්න පුලුවන් මේකෙන්

<b>NOTE:</b>
1. Connection එකක් add කරන්න පුලුවන් admin කෙනෙක් ට විතරයි
2. එවන්න මේ විදිහට👉 <code>/connect</code> ඔයාගෙ group එක connect කරන්න ඕනෙනම්

<b>විධාන හා භාවිතයන්:</b>
• /connect  - <code>යම් chat එකක් ඔයාගෙ PM එකට connect කරනව</code>
• /disconnect  - <code>යම් chat එකක් disconnect කරනව්</code>
• /connections - <code>ඔයාගෙ සියලුම connections ටික ලිස්ට් එකකින් පෙන්නනව</code>"""
    EXTRAMOD_TXT = """Help: <b>අමතර ගැජමැටික් ටිකක්</b>
    
<b>විධාන හා භාවිතයන්:</b>
• /id - <code>යම් user කෙනෙක්ගෙ id එක ගන්න</code>
• /info  - <code>යම් user කෙනෙක් ගැන තොරතුරු ගන්න</code>
• /imdb  - <code>IMDb එකෙන් ෆිල්ම් එක ගැන තොරතුරු ගන්න</code>
• /search  - <code>තවත් විවිධ මූලාශ්‍ර වලින් ෆිල්ම් එක ගැන තොරතුරු ගන්න</code>"""
    ADMIN_TXT = """උදවු: <b>මගෙ ඇඩ්මින්ලට දීල තියෙන ගැජමැටික්ස්</b>
    
-------මේක ඔයාලට වැදගත් නෑ👇👇👇👇👇 ----------
<b>Commands and Usage:</b>
• /logs - <code>to get the rescent errors</code>
• /stats - <code>to get status of files in db.</code>
• /delete - <code>to delete a specific file from db.</code>
• /users - <code>to get list of my users and ids.</code>
• /chats - <code>to get list of the my chats and ids </code>
• /leave  - <code>to leave from a chat.</code>
• /disable  -  <code>do disable a chat.</code>
• /ban  - <code>to ban a user.</code>
• /unban  - <code>to unban a user.</code>
• /channel - <code>to get list of total connected channels</code>
• /broadcast - <code>to broadcast a message to all users</code>"""
    STATUS_TXT = """★ 𝚃𝙾𝚃𝙰𝙻 𝙵𝙸𝙻𝙴𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝙲𝙷𝙰𝚃𝚂: <code>{}</code>
★ 𝚄𝚂𝙴𝙳 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱
★ 𝙵𝚁𝙴𝙴 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱"""
    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
"""
    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}
"""
