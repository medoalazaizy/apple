# Bot by MeDo Alazaizy
# Telegram: @Alazaizy
from typing import Any
import os,json,time,asyncio,zipfile,re,sys
from telethon.sessions import StringSession
from telethon import functions,TelegramClient
import random
import string

# ✅ استيراد مكتبة socks للبروكسي
try:
    import socks
    SOCKS_AVAILABLE = True
except ImportError:
    try:
        from python_socks import ProxyType
        SOCKS_AVAILABLE = True
    except ImportError:
        SOCKS_AVAILABLE = False
        print("[Proxy] Warning: Neither 'socks' nor 'python-socks' is installed. Proxy support may be limited.")

from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
    PhoneMigrateError,
    PeerFloodError
)
from datetime import datetime
from pyrogram import Client, idle
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from pyromod import listen
from pyromod.exceptions import ListenerTimeout
from asyncio import get_event_loop
from telethon.tl.types import MessageActionGiftCode

db_file = 'users_db.json'
countries_db_file = 'countries_db.json'
delivered_numbers_file = 'delivered_numbers.json'
leaders_db_file = 'leaders_db.json'
pending_session_deletions_file = 'pending_session_deletions.json'
users_db = {}
countries_db = {}
delivered_numbers = []
leaders_db = {}  # {leader_id: {name, channel_id, commission, wallet_address, stats: {withdrawals_count, total_withdrawn, total_commission, numbers_count}}}
maintenance=True

API_ID = 22256614
API_HASH = "4f9f53e287de541cf0ed81e12a68fa3b"
sudo = 6496424788
token = "7691740416:AAGd18MkOXOEV9ymadF7AI0skUbWMPIF5zI"
bot = Client("MeDo_Alazaizy", api_id=API_ID, api_hash=API_HASH, bot_token=token)
m="5566"#التحقق الثنائي
m2="@FiveStarsNumbers"#تلميح التحقق الثنائي
gg = "@TeleGoLFC"  # ايدي قناه اضافه الارقام الناجحه
OWNER_CHANNEL_ID = "@TeleGolFCCoin"  # id القناة
COUNTRIES_ANNOUNCEMENT_CHANNEL = "@TeleGolFCCoin"  # ✅ قناة إعلان الدول (يمكن تغييرها)

yo=1.0#اقل مبلغ للسحب

# ✅ قاموس البروكسيات لكل دولة (Datacenter Proxy routing)
# الصيغة: username:password@host:port_http:port_socks5
# port_823 = HTTP proxy, port_824 = SOCKS5 proxy
PROXY_CONFIG = {
    '+93': '9a9e1170ade3cc2409f0__cr.af:a79d5f35283ab07e@gw.dataimpulse.com:823:824',   # Afghanistan
    '+355': '9a9e1170ade3cc2409f0__cr.al:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Albania
    '+213': '9a9e1170ade3cc2409f0__cr.dz:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Algeria
    '+376': '9a9e1170ade3cc2409f0__cr.ad:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Andorra
    '+244': '9a9e1170ade3cc2409f0__cr.ao:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Angola
    '+1264': '9a9e1170ade3cc2409f0__cr.ai:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Anguilla
    '+1268': '9a9e1170ade3cc2409f0__cr.ag:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Antigua and Barbuda
    '+54': '9a9e1170ade3cc2409f0__cr.ar:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Argentina
    '+374': '9a9e1170ade3cc2409f0__cr.am:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Armenia
    '+297': '9a9e1170ade3cc2409f0__cr.aw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Aruba
    '+61': '9a9e1170ade3cc2409f0__cr.au:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Australia
    '+43': '9a9e1170ade3cc2409f0__cr.at:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Austria
    '+994': '9a9e1170ade3cc2409f0__cr.az:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Azerbaijan
    '+1242': '9a9e1170ade3cc2409f0__cr.bs:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Bahamas
    '+973': '9a9e1170ade3cc2409f0__cr.bh:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Bahrain
    '+880': '9a9e1170ade3cc2409f0__cr.bd:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Bangladesh
    '+1246': '9a9e1170ade3cc2409f0__cr.bb:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Barbados
    '+375': '9a9e1170ade3cc2409f0__cr.by:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Belarus
    '+32': '9a9e1170ade3cc2409f0__cr.be:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Belgium
    '+501': '9a9e1170ade3cc2409f0__cr.bz:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Belize
    '+229': '9a9e1170ade3cc2409f0__cr.bj:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Benin
    '+1441': '9a9e1170ade3cc2409f0__cr.bm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Bermuda
    '+975': '9a9e1170ade3cc2409f0__cr.bt:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Bhutan
    '+591': '9a9e1170ade3cc2409f0__cr.bo:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Bolivia
    '+387': '9a9e1170ade3cc2409f0__cr.ba:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Bosnia and Herzegovina
    '+267': '9a9e1170ade3cc2409f0__cr.bw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Botswana
    '+55': '9a9e1170ade3cc2409f0__cr.br:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Brazil
    '+246': '9a9e1170ade3cc2409f0__cr.io:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # British Indian Ocean Territory
    '+1284': '9a9e1170ade3cc2409f0__cr.vg:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # British Virgin Islands
    '+673': '9a9e1170ade3cc2409f0__cr.bn:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Brunei
    '+359': '9a9e1170ade3cc2409f0__cr.bg:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Bulgaria
    '+226': '9a9e1170ade3cc2409f0__cr.bf:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Burkina Faso
    '+257': '9a9e1170ade3cc2409f0__cr.bi:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Burundi
    '+855': '9a9e1170ade3cc2409f0__cr.kh:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Cambodia
    '+237': '9a9e1170ade3cc2409f0__cr.cm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Cameroon
    '+1': '9a9e1170ade3cc2409f0__cr.ca:a79d5f35283ab07e@gw.dataimpulse.com:823:824',   # Canada
    '+238': '9a9e1170ade3cc2409f0__cr.cv:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Cape Verde
    '+1345': '9a9e1170ade3cc2409f0__cr.ky:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Cayman Islands
    '+236': '9a9e1170ade3cc2409f0__cr.cf:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Central African Republic
    '+235': '9a9e1170ade3cc2409f0__cr.td:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Chad
    '+56': '9a9e1170ade3cc2409f0__cr.cl:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Chile
    '+86': '9a9e1170ade3cc2409f0__cr.cn:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # China
    '+57': '9a9e1170ade3cc2409f0__cr.co:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Colombia
    '+269': '9a9e1170ade3cc2409f0__cr.km:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Comoros
    '+242': '9a9e1170ade3cc2409f0__cr.cg:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Congo
    '+243': '9a9e1170ade3cc2409f0__cr.cd:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # DR Congo
    '+682': '9a9e1170ade3cc2409f0__cr.ck:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Cook Islands
    '+506': '9a9e1170ade3cc2409f0__cr.cr:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Costa Rica
    '+225': '9a9e1170ade3cc2409f0__cr.ci:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Côte d’Ivoire
    '+385': '9a9e1170ade3cc2409f0__cr.hr:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Croatia
    '+53': '9a9e1170ade3cc2409f0__cr.cu:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Cuba
    '+599': '9a9e1170ade3cc2409f0__cr.cw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Curaçao
    '+357': '9a9e1170ade3cc2409f0__cr.cy:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Cyprus
    '+420': '9a9e1170ade3cc2409f0__cr.cz:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Czechia
    '+45': '9a9e1170ade3cc2409f0__cr.dk:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Denmark
    '+253': '9a9e1170ade3cc2409f0__cr.dj:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Djibouti
    '+1767': '9a9e1170ade3cc2409f0__cr.dm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Dominica
    '+1809': '9a9e1170ade3cc2409f0__cr.do:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Dominican Republic
    '+593': '9a9e1170ade3cc2409f0__cr.ec:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Ecuador
    '+20': '9a9e1170ade3cc2409f0__cr.eg:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Egypt
    '+503': '9a9e1170ade3cc2409f0__cr.sv:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # El Salvador
    '+240': '9a9e1170ade3cc2409f0__cr.gq:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Equatorial Guinea
    '+291': '9a9e1170ade3cc2409f0__cr.er:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Eritrea
    '+372': '9a9e1170ade3cc2409f0__cr.ee:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Estonia
    '+251': '9a9e1170ade3cc2409f0__cr.et:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Ethiopia
    '+500': '9a9e1170ade3cc2409f0__cr.fk:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Falkland Islands
    '+298': '9a9e1170ade3cc2409f0__cr.fo:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Faroe Islands
    '+679': '9a9e1170ade3cc2409f0__cr.fj:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Fiji
    '+358': '9a9e1170ade3cc2409f0__cr.fi:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Finland
    '+33': '9a9e1170ade3cc2409f0__cr.fr:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # France
    '+594': '9a9e1170ade3cc2409f0__cr.gf:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # French Guiana
    '+689': '9a9e1170ade3cc2409f0__cr.pf:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # French Polynesia
    '+241': '9a9e1170ade3cc2409f0__cr.ga:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Gabon
    '+220': '9a9e1170ade3cc2409f0__cr.gm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Gambia
    '+995': '9a9e1170ade3cc2409f0__cr.ge:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Georgia
    '+49': '9a9e1170ade3cc2409f0__cr.de:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Germany
    '+233': '9a9e1170ade3cc2409f0__cr.gh:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Ghana
    '+350': '9a9e1170ade3cc2409f0__cr.gi:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Gibraltar
    '+30': '9a9e1170ade3cc2409f0__cr.gr:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Greece
    '+299': '9a9e1170ade3cc2409f0__cr.gl:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Greenland
    '+1473': '9a9e1170ade3cc2409f0__cr.gd:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Grenada
    '+590': '9a9e1170ade3cc2409f0__cr.gp:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Guadeloupe
    '+1671': '9a9e1170ade3cc2409f0__cr.gu:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Guam
    '+502': '9a9e1170ade3cc2409f0__cr.gt:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Guatemala
    '+441481': '9a9e1170ade3cc2409f0__cr.gg:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Guernsey
    '+224': '9a9e1170ade3cc2409f0__cr.gn:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Guinea
    '+245': '9a9e1170ade3cc2409f0__cr.gw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Guinea-Bissau
    '+592': '9a9e1170ade3cc2409f0__cr.gy:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Guyana
    '+509': '9a9e1170ade3cc2409f0__cr.ht:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Haiti
    '+504': '9a9e1170ade3cc2409f0__cr.hn:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Honduras
    '+852': '9a9e1170ade3cc2409f0__cr.hk:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Hong Kong
    '+36': '9a9e1170ade3cc2409f0__cr.hu:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Hungary
    '+354': '9a9e1170ade3cc2409f0__cr.is:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Iceland
    '+91': '9a9e1170ade3cc2409f0__cr.in:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # India
    '+62': '9a9e1170ade3cc2409f0__cr.id:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Indonesia
    '+98': '9a9e1170ade3cc2409f0__cr.ir:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Iran
    '+964': '9a9e1170ade3cc2409f0__cr.iq:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Iraq
    '+353': '9a9e1170ade3cc2409f0__cr.ie:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Ireland
    '+441624': '9a9e1170ade3cc2409f0__cr.im:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Isle of Man
    '+972': '9a9e1170ade3cc2409f0__cr.il:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Israel
    '+39': '9a9e1170ade3cc2409f0__cr.it:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Italy
    '+1876': '9a9e1170ade3cc2409f0__cr.jm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Jamaica
    '+81': '9a9e1170ade3cc2409f0__cr.jp:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Japan
    '+441534': '9a9e1170ade3cc2409f0__cr.je:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Jersey
    '+962': '9a9e1170ade3cc2409f0__cr.jo:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Jordan
    '+7': '9a9e1170ade3cc2409f0__cr.kz:a79d5f35283ab07e@gw.dataimpulse.com:823:824',   # Kazakhstan
    '+254': '9a9e1170ade3cc2409f0__cr.ke:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Kenya
    '+686': '9a9e1170ade3cc2409f0__cr.ki:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Kiribati
    '+965': '9a9e1170ade3cc2409f0__cr.kw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Kuwait
    '+996': '9a9e1170ade3cc2409f0__cr.kg:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Kyrgyzstan
    '+856': '9a9e1170ade3cc2409f0__cr.la:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Laos
    '+371': '9a9e1170ade3cc2409f0__cr.lv:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Latvia
    '+961': '9a9e1170ade3cc2409f0__cr.lb:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Lebanon
    '+266': '9a9e1170ade3cc2409f0__cr.ls:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Lesotho
    '+231': '9a9e1170ade3cc2409f0__cr.lr:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Liberia
    '+218': '9a9e1170ade3cc2409f0__cr.ly:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Libya
    '+423': '9a9e1170ade3cc2409f0__cr.li:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Liechtenstein
    '+370': '9a9e1170ade3cc2409f0__cr.lt:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Lithuania
    '+352': '9a9e1170ade3cc2409f0__cr.lu:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Luxembourg
    '+853': '9a9e1170ade3cc2409f0__cr.mo:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Macau
    '+389': '9a9e1170ade3cc2409f0__cr.mk:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # North Macedonia
    '+261': '9a9e1170ade3cc2409f0__cr.mg:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Madagascar
    '+265': '9a9e1170ade3cc2409f0__cr.mw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Malawi
    '+60': '9a9e1170ade3cc2409f0__cr.my:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Malaysia
    '+960': '9a9e1170ade3cc2409f0__cr.mv:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Maldives
    '+223': '9a9e1170ade3cc2409f0__cr.ml:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Mali
    '+356': '9a9e1170ade3cc2409f0__cr.mt:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Malta
    '+692': '9a9e1170ade3cc2409f0__cr.mh:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Marshall Islands
    '+596': '9a9e1170ade3cc2409f0__cr.mq:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Martinique
    '+222': '9a9e1170ade3cc2409f0__cr.mr:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Mauritania
    '+230': '9a9e1170ade3cc2409f0__cr.mu:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Mauritius
    '+262': '9a9e1170ade3cc2409f0__cr.yt:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Mayotte
    '+52': '9a9e1170ade3cc2409f0__cr.mx:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Mexico
    '+691': '9a9e1170ade3cc2409f0__cr.fm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Micronesia
    '+373': '9a9e1170ade3cc2409f0__cr.md:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Moldova
    '+377': '9a9e1170ade3cc2409f0__cr.mc:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Monaco
    '+976': '9a9e1170ade3cc2409f0__cr.mn:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Mongolia
    '+382': '9a9e1170ade3cc2409f0__cr.me:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Montenegro
    '+1664': '9a9e1170ade3cc2409f0__cr.ms:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Montserrat
    '+212': '9a9e1170ade3cc2409f0__cr.ma:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Morocco
    '+258': '9a9e1170ade3cc2409f0__cr.mz:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Mozambique
    '+95': '9a9e1170ade3cc2409f0__cr.mm:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Myanmar
    '+264': '9a9e1170ade3cc2409f0__cr.na:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Namibia
    '+674': '9a9e1170ade3cc2409f0__cr.nr:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Nauru
    '+977': '9a9e1170ade3cc2409f0__cr.np:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Nepal
    '+31': '9a9e1170ade3cc2409f0__cr.nl:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Netherlands
    '+687': '9a9e1170ade3cc2409f0__cr.nc:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # New Caledonia
    '+64': '9a9e1170ade3cc2409f0__cr.nz:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # New Zealand
    '+505': '9a9e1170ade3cc2409f0__cr.ni:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Nicaragua
    '+227': '9a9e1170ade3cc2409f0__cr.ne:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Niger
    '+234': '9a9e1170ade3cc2409f0__cr.ng:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Nigeria
    '+683': '9a9e1170ade3cc2409f0__cr.nu:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Niue
    '+672': '9a9e1170ade3cc2409f0__cr.nf:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Norfolk Island
    '+850': '9a9e1170ade3cc2409f0__cr.kp:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # North Korea
    '+1670': '9a9e1170ade3cc2409f0__cr.mp:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Northern Mariana Islands
    '+47': '9a9e1170ade3cc2409f0__cr.no:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Norway
    '+968': '9a9e1170ade3cc2409f0__cr.om:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Oman
    '+92': '9a9e1170ade3cc2409f0__cr.pk:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Pakistan
    '+680': '9a9e1170ade3cc2409f0__cr.pw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Palau
    '+970': '9a9e1170ade3cc2409f0__cr.ps:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Palestine
    '+507': '9a9e1170ade3cc2409f0__cr.pa:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Panama
    '+675': '9a9e1170ade3cc2409f0__cr.pg:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Papua New Guinea
    '+595': '9a9e1170ade3cc2409f0__cr.py:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Paraguay
    '+51': '9a9e1170ade3cc2409f0__cr.pe:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Peru
    '+63': '9a9e1170ade3cc2409f0__cr.ph:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Philippines
    '+48': '9a9e1170ade3cc2409f0__cr.pl:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Poland
    '+351': '9a9e1170ade3cc2409f0__cr.pt:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Portugal
    '+1787': '9a9e1170ade3cc2409f0__cr.pr:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Puerto Rico
    '+974': '9a9e1170ade3cc2409f0__cr.qa:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Qatar
    '+262': '9a9e1170ade3cc2409f0__cr.re:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Réunion
    '+40': '9a9e1170ade3cc2409f0__cr.ro:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Romania
    '+7': '9a9e1170ade3cc2409f0__cr.ru:a79d5f35283ab07e@gw.dataimpulse.com:823:824',   # Russia
    '+250': '9a9e1170ade3cc2409f0__cr.rw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Rwanda
    '+290': '9a9e1170ade3cc2409f0__cr.sh:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Saint Helena
    '+1869': '9a9e1170ade3cc2409f0__cr.kn:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Saint Kitts and Nevis
    '+1758': '9a9e1170ade3cc2409f0__cr.lc:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Saint Lucia
    '+508': '9a9e1170ade3cc2409f0__cr.pm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Saint Pierre and Miquelon
    '+1784': '9a9e1170ade3cc2409f0__cr.vc:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Saint Vincent and the Grenadines
    '+685': '9a9e1170ade3cc2409f0__cr.ws:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Samoa
    '+378': '9a9e1170ade3cc2409f0__cr.sm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # San Marino
    '+239': '9a9e1170ade3cc2409f0__cr.st:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # São Tomé and Príncipe
    '+966': '9a9e1170ade3cc2409f0__cr.sa:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Saudi Arabia
    '+221': '9a9e1170ade3cc2409f0__cr.sn:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Senegal
    '+381': '9a9e1170ade3cc2409f0__cr.rs:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Serbia
    '+248': '9a9e1170ade3cc2409f0__cr.sc:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Seychelles
    '+232': '9a9e1170ade3cc2409f0__cr.sl:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Sierra Leone
    '+65': '9a9e1170ade3cc2409f0__cr.sg:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Singapore
    '+1721': '9a9e1170ade3cc2409f0__cr.sx:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Sint Maarten
    '+421': '9a9e1170ade3cc2409f0__cr.sk:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Slovakia
    '+386': '9a9e1170ade3cc2409f0__cr.si:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Slovenia
    '+677': '9a9e1170ade3cc2409f0__cr.sb:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Solomon Islands
    '+252': '9a9e1170ade3cc2409f0__cr.so:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Somalia
    '+27': '9a9e1170ade3cc2409f0__cr.za:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # South Africa
    '+82': '9a9e1170ade3cc2409f0__cr.kr:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # South Korea
    '+211': '9a9e1170ade3cc2409f0__cr.ss:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # South Sudan
    '+34': '9a9e1170ade3cc2409f0__cr.es:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Spain
    '+94': '9a9e1170ade3cc2409f0__cr.lk:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Sri Lanka
    '+249': '9a9e1170ade3cc2409f0__cr.sd:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Sudan
    '+597': '9a9e1170ade3cc2409f0__cr.sr:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Suriname
    '+4779': '9a9e1170ade3cc2409f0__cr.sj:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Svalbard and Jan Mayen
    '+268': '9a9e1170ade3cc2409f0__cr.sz:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Eswatini
    '+46': '9a9e1170ade3cc2409f0__cr.se:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Sweden
    '+41': '9a9e1170ade3cc2409f0__cr.ch:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Switzerland
    '+963': '9a9e1170ade3cc2409f0__cr.sy:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Syria
    '+886': '9a9e1170ade3cc2409f0__cr.tw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Taiwan
    '+992': '9a9e1170ade3cc2409f0__cr.tj:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Tajikistan
    '+255': '9a9e1170ade3cc2409f0__cr.tz:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Tanzania
    '+66': '9a9e1170ade3cc2409f0__cr.th:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Thailand
    '+670': '9a9e1170ade3cc2409f0__cr.tl:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Timor-Leste
    '+228': '9a9e1170ade3cc2409f0__cr.tg:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Togo
    '+690': '9a9e1170ade3cc2409f0__cr.tk:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Tokelau
    '+676': '9a9e1170ade3cc2409f0__cr.to:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Tonga
    '+1868': '9a9e1170ade3cc2409f0__cr.tt:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Trinidad and Tobago
    '+216': '9a9e1170ade3cc2409f0__cr.tn:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Tunisia
    '+90': '9a9e1170ade3cc2409f0__cr.tr:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Turkey
    '+993': '9a9e1170ade3cc2409f0__cr.tm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Turkmenistan
    '+1649': '9a9e1170ade3cc2409f0__cr.tc:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Turks and Caicos Islands
    '+688': '9a9e1170ade3cc2409f0__cr.tv:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Tuvalu
    '+256': '9a9e1170ade3cc2409f0__cr.ug:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Uganda
    '+380': '9a9e1170ade3cc2409f0__cr.ua:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Ukraine
    '+971': '9a9e1170ade3cc2409f0__cr.ae:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # UAE
    '+44': '9a9e1170ade3cc2409f0__cr.uk:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # United Kingdom
    '+1': '9a9e1170ade3cc2409f0__cr.us:a79d5f35283ab07e@gw.dataimpulse.com:823:824',   # USA
    '+598': '9a9e1170ade3cc2409f0__cr.uy:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Uruguay
    '+998': '9a9e1170ade3cc2409f0__cr.uz:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Uzbekistan
    '+678': '9a9e1170ade3cc2409f0__cr.vu:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Vanuatu
    '+379': '9a9e1170ade3cc2409f0__cr.va:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Vatican City
    '+58': '9a9e1170ade3cc2409f0__cr.ve:a79d5f35283ab07e@gw.dataimpulse.com:823:824',  # Venezuela
    '+84': '9a9e1170ade3cc2409f0__cr.vn:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Vietnam
    '+1284': '9a9e1170ade3cc2409f0__cr.vi:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # US Virgin Islands
    '+681': '9a9e1170ade3cc2409f0__cr.wf:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Wallis and Futuna
    '+212': '9a9e1170ade3cc2409f0__cr.eh:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Western Sahara
    '+967': '9a9e1170ade3cc2409f0__cr.ye:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Yemen
    '+260': '9a9e1170ade3cc2409f0__cr.zm:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Zambia
    '+263': '9a9e1170ade3cc2409f0__cr.zw:a79d5f35283ab07e@gw.dataimpulse.com:823:824', # Zimbabwe
}

def get_proxy_for_number(number):
    """استخراج رمز الدولة من الرقم وإرجاع البروكسي المناسب"""
    if not number:
        return None
    
    # استخراج رمز الدولة من الرقم
    number = str(number).replace('+', '')
    
    # محاولة مطابقة الأرقام الطويلة أولاً (3 أرقام)
    for code_length in [3, 2, 1]:
        if len(number) >= code_length:
            country_code = '+' + number[:code_length]
            if country_code in PROXY_CONFIG:
                proxy_str = PROXY_CONFIG[country_code]
                # تحويل من username:password@host:port إلى HttpProxy للـ Telethon
                try:
                    if '@' in proxy_str:
                        auth_part, server_part = proxy_str.split('@')
                        username, password = auth_part.split(':')
                        # التحقق إذا كان هناك منفذين (HTTP:823, SOCKS5:824)
                        parts = server_part.split(':')
                        host = parts[0]
                        http_port = int(parts[1]) if len(parts) > 1 else 823
                        socks5_port = int(parts[2]) if len(parts) > 2 else 824
                        
                        # استخدام SOCKS5 proxy على المنفذ 824
                        # Telethon يتطلب استخدام مكتبة socks مع صيغة محددة
                        if SOCKS_AVAILABLE:
                            try:
                                import socks
                                # ✅ الصيغة الصحيحة لـ Telethon: (socks.SOCKS5, host, port, True, username, password)
                                # True يشير إلى أن البروكسي يتطلب مصادقة
                                proxy = (socks.SOCKS5, host, socks5_port, True, username, password)
                                return proxy
                            except ImportError:
                                try:
                                    from python_socks import ProxyType
                                    # استخدام python-socks
                                    proxy = {
                                        'proxy_type': ProxyType.SOCKS5,
                                        'addr': host,
                                        'port': socks5_port,
                                        'username': username,
                                        'password': password
                                    }
                                    return proxy
                                except ImportError:
                                    pass
                        
                        # Fallback: استخدام صيغة مع True
                        proxy = ('socks5', host, socks5_port, True, username, password)
                        return proxy
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    return None
    
    print(f"[Proxy] No proxy found for number +{number}")
    return None

def get_proxy_for_country(country_code_or_name):
    """
    الحصول على البروكسي لدولة معينة
    country_code_or_name: رمز الدولة (مثل '+48') أو اسم الدولة
    """
    proxy_str = None
    
    # البحث في PROXY_CONFIG أولاً
    if country_code_or_name in PROXY_CONFIG:
        proxy_str = PROXY_CONFIG[country_code_or_name]
    else:
        # البحث في countries_db
        found_code = None
        for name, data in countries_db.items():
            if data.get('code') == country_code_or_name or name == country_code_or_name:
                found_code = data.get('code', country_code_or_name)
                break
        
        if found_code and found_code in PROXY_CONFIG:
            proxy_str = PROXY_CONFIG[found_code]
        else:
            # محاولة استخدام generate_proxy_for_country إذا كانت موجودة
            try:
                # البحث عن generate_proxy_for_country في نفس الملف
                if 'generate_proxy_for_country' in globals():
                    proxy_str = globals()['generate_proxy_for_country'](country_code_or_name)
                else:
                    return None
            except Exception as e:
                return None
    
    if not proxy_str:
        return None
    
    # تحويل proxy_str إلى format صحيح
    try:
        if '@' in proxy_str:
            auth_part, server_part = proxy_str.split('@')
            username, password = auth_part.split(':')
            parts = server_part.split(':')
            host = parts[0]
            http_port = int(parts[1]) if len(parts) > 1 else 823
            socks5_port = int(parts[2]) if len(parts) > 2 else 824
            
            if SOCKS_AVAILABLE:
                try:
                    import socks
                    # ✅ الصيغة الصحيحة: (socks.SOCKS5, host, port, True, username, password)
                    proxy = (socks.SOCKS5, host, socks5_port, True, username, password)
                    return proxy
                except ImportError:
                    try:
                        from python_socks import ProxyType
                        proxy = {
                            'proxy_type': ProxyType.SOCKS5,
                            'addr': host,
                            'port': socks5_port,
                            'username': username,
                            'password': password
                        }
                        return proxy
                    except ImportError:
                        pass
            
            # Fallback مع True
            proxy = ('socks5', host, socks5_port, True, username, password)
            return proxy
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None
    
    return None

def normalize_proxy(proxy):
    """تحويل البروكسي من أي صيغة إلى format صحيح للـ Telethon"""
    if not proxy:
        return None
    
    # إذا كان dict (python-socks format)، إرجاعه كما هو
    if isinstance(proxy, dict):
        return proxy
    
    # إذا كان tuple بالفعل، التحقق من صيغته
    if isinstance(proxy, tuple):
        # إذا كان tuple مع 5 عناصر (socks.SOCKS5, host, port, username, password) - الصيغة الصحيحة
        if len(proxy) == 5:
            protocol, host, port, username, password = proxy
            # إذا كان protocol هو socks.SOCKS5 (من مكتبة socks)، إرجاعه كما هو
            if hasattr(protocol, '__module__') and 'socks' in str(protocol.__module__):
                return proxy
            # إذا كان string 'socks5'، تحويله إلى socks.SOCKS5
            elif protocol == 'socks5' or protocol == 'socks5h':
                if SOCKS_AVAILABLE:
                    try:
                        import socks
                        return (socks.SOCKS5, host, int(port), username, password)
                    except ImportError:
                        try:
                            from python_socks import ProxyType
                            return {
                                'proxy_type': ProxyType.SOCKS5,
                                'addr': host,
                                'port': int(port),
                                'username': username,
                                'password': password
                            }
                        except ImportError:
                            pass
                # Fallback
                return proxy
            else:
                return proxy
        # إذا كان tuple مع 6 عناصر (protocol, host, port, True, username, password)، إزالة True
        elif len(proxy) == 6:
            protocol, host, port, _, username, password = proxy[:6]
            if hasattr(protocol, '__module__') and 'socks' in str(protocol.__module__):
                return (protocol, host, int(port), username, password)
            elif protocol == 'socks5' or protocol == 'socks5h':
                if SOCKS_AVAILABLE:
                    try:
                        import socks
                        return (socks.SOCKS5, host, int(port), username, password)
                    except ImportError:
                        try:
                            from python_socks import ProxyType
                            return {
                                'proxy_type': ProxyType.SOCKS5,
                                'addr': host,
                                'port': int(port),
                                'username': username,
                                'password': password
                            }
                        except ImportError:
                            pass
                return (protocol, host, int(port), username, password)
        # إذا كان tuple مع 4 عناصر (host, port, username, password)، إضافة socks.SOCKS5
        elif len(proxy) == 4:
            host, port, username, password = proxy
            if SOCKS_AVAILABLE:
                try:
                    import socks
                    return (socks.SOCKS5, host, int(port), username, password)
                except ImportError:
                    try:
                        from python_socks import ProxyType
                        return {
                            'proxy_type': ProxyType.SOCKS5,
                            'addr': host,
                            'port': int(port),
                            'username': username,
                            'password': password
                        }
                    except ImportError:
                        pass
            return ('socks5', host, int(port), username, password)
        # إذا كان tuple مع 2 عناصر (host, port) بدون auth
        elif len(proxy) == 2:
            host, port = proxy
            if SOCKS_AVAILABLE:
                try:
                    import socks
                    return (socks.SOCKS5, host, int(port))
                except ImportError:
                    try:
                        from python_socks import ProxyType
                        return {
                            'proxy_type': ProxyType.SOCKS5,
                            'addr': host,
                            'port': int(port)
                        }
                    except ImportError:
                        pass
            return ('socks5', host, int(port))
        else:
            return None
    
    return proxy

# متغيرات عامة
total_verifications = 0
verifications_by_country = {}
pending_confirmations = {}
# ✅ متغير لتتبع الجلسات التي يجب حذفها بعد 24 ساعة
pending_session_deletions = {}  # {number: deletion_time}
# ✅ متغير لتخزين معلومات السحب مؤقتاً (لتجنب مشكلة BUTTON_DATA_INVALID)
pending_withdrawals = {}  # {withdrawal_id: {user_id, amount, wallet_address, wallet_type, leader_id, numbers_count}}

def load_db():
    global users_db, countries_db, delivered_numbers, leaders_db, pending_session_deletions
    if os.path.exists(db_file):
        with open(db_file, 'r', encoding='utf-8') as f:
            users_db = json.load(f)
    if os.path.exists(countries_db_file):
        with open(countries_db_file, 'r', encoding='utf-8') as f:
            countries_db = json.load(f)
    if os.path.exists(delivered_numbers_file):
        with open(delivered_numbers_file, 'r', encoding='utf-8') as f:
            delivered_numbers = json.load(f)
    else:
        delivered_numbers = []
    if os.path.exists(leaders_db_file):
        with open(leaders_db_file, 'r', encoding='utf-8') as f:
            leaders_db = json.load(f)
    else:
        leaders_db = {}
    # ✅ تحميل pending_session_deletions من الملف
    if os.path.exists(pending_session_deletions_file):
        with open(pending_session_deletions_file, 'r', encoding='utf-8') as f:
            pending_data = json.load(f)
            # ✅ تحويل القيم من string إلى float (لأن JSON يحفظ الأرقام كـ strings أحياناً)
            pending_session_deletions = {k: float(v) for k, v in pending_data.items()}
    else:
        pending_session_deletions = {}

def save_db():
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(users_db, f, indent=4, ensure_ascii=False)

def save_countries_db():
    with open(countries_db_file, 'w', encoding='utf-8') as f:
        json.dump(countries_db, f, indent=4, ensure_ascii=False)

def save_delivered_numbers():
    global delivered_numbers
    with open(delivered_numbers_file, 'w', encoding='utf-8') as f:
        json.dump(delivered_numbers, f, indent=4, ensure_ascii=False)

def save_leaders_db():
    with open(leaders_db_file, 'w', encoding='utf-8') as f:
        json.dump(leaders_db, f, indent=4, ensure_ascii=False)

def save_pending_session_deletions():
    """حفظ pending_session_deletions في ملف JSON"""
    global pending_session_deletions
    with open(pending_session_deletions_file, 'w', encoding='utf-8') as f:
        json.dump(pending_session_deletions, f, indent=4, ensure_ascii=False)

load_db()

from tttt import translations

import requests
from datetime import datetime  
import re


# ✅ قمبل من DEVICES_LIST (من كودك)
DEVICES_LIST = [
    {"name": "HP EliteBook 840 G1", "system": "Windows 7", "app": "5.15.4 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP EliteBook 840 G2", "system": "Windows 8.1", "app": "6.3.3 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP EliteBook 840 G3", "system": "Windows 10", "app": "5.8.0 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP EliteBook 840 G4", "system": "Windows 8.1", "app": "6.0.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP EliteBook 840 G5", "system": "Windows 10", "app": "5.14.1 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP EliteBook 850 G1", "system": "Windows 10", "app": "6.3.3 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP EliteBook 850 G2", "system": "Windows 7", "app": "6.0.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP EliteBook 850 G3", "system": "Windows 8.1", "app": "5.12.3 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP EliteBook 850 G4", "system": "Windows 8.1", "app": "6.2.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP EliteBook 850 G5", "system": "Windows 11", "app": "5.8.0 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Dell Latitude 5400", "system": "Windows 10", "app": "5.15.4 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Dell Latitude 5500", "system": "Windows 11", "app": "5.10.2 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Dell Latitude 7400", "system": "Windows 11", "app": "5.12.3 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Dell Latitude 7410", "system": "Windows 7", "app": "5.15.4 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Dell XPS 13 9380", "system": "Windows 8.1", "app": "5.10.2 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Dell XPS 15 7590", "system": "Windows 7", "app": "6.0.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Lenovo ThinkPad T480", "system": "Windows 11", "app": "6.2.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Lenovo ThinkPad T490", "system": "Windows 8.1", "app": "5.15.4 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Lenovo ThinkPad X1 Carbon Gen 7", "system": "Windows 10", "app": "5.9.1 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Lenovo ThinkPad X1 Carbon Gen 8", "system": "Windows 10", "app": "6.2.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Acer Aspire 5 A515", "system": "Windows 10", "app": "6.1.2 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Acer Aspire 7 A715", "system": "Windows 11", "app": "5.14.1 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Asus VivoBook 15", "system": "Windows 8.1", "app": "5.8.0 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Asus ZenBook 14", "system": "Windows 7", "app": "6.3.3 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Asus ROG Zephyrus G14", "system": "Windows 10", "app": "6.1.2 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Microsoft Surface Laptop 3", "system": "Windows 8.1", "app": "5.12.3 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Microsoft Surface Laptop 4", "system": "Windows 10", "app": "5.15.4 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Toshiba Tecra A50", "system": "Windows 11", "app": "5.9.1 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Toshiba Satellite Pro", "system": "Windows 8.1", "app": "5.14.1 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Fujitsu Lifebook U7410", "system": "Windows 11", "app": "6.3.3 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Fujitsu Lifebook U9310", "system": "Windows 7", "app": "6.2.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "MSI Modern 14", "system": "Windows 10", "app": "5.9.1 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "MSI Prestige 15", "system": "Windows 11", "app": "5.12.3 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Samsung Galaxy Book Flex", "system": "Windows 7", "app": "5.10.2 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Samsung Notebook 9 Pro", "system": "Windows 10", "app": "6.3.3 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Razer Blade 15", "system": "Windows 11", "app": "5.8.0 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Razer Book 13", "system": "Windows 8.1", "app": "6.2.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "LG Gram 14", "system": "Windows 7", "app": "6.0.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "LG Gram 17", "system": "Windows 10", "app": "5.14.1 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Google Pixelbook Go", "system": "Windows 11", "app": "5.15.4 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Huawei MateBook D15", "system": "Windows 10", "app": "6.1.2 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Huawei MateBook X Pro", "system": "Windows 7", "app": "5.10.2 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Chuwi AeroBook", "system": "Windows 8.1", "app": "5.8.0 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "VAIO SX14", "system": "Windows 11", "app": "6.2.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Panasonic Toughbook CF-54", "system": "Windows 10", "app": "6.3.3 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Panasonic Toughbook CF-33", "system": "Windows 8.1", "app": "5.12.3 x86", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP ProBook 450 G7", "system": "Windows 10", "app": "6.0.0 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP ProBook 450 G8", "system": "Windows 7", "app": "5.15.4 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP ZBook Firefly 14", "system": "Windows 11", "app": "5.9.1 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "HP Spectre x360", "system": "Windows 8.1", "app": "6.1.2 x64", "API_ID": 22001267, "API_HASH": "6b1e984d16e4d491d52193eb23760928"},
    {"name": "Samsung Galaxy S23", "system": "Android 13", "app": "10.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy S22", "system": "Android 12", "app": "9.6.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy S21", "system": "Android 11", "app": "9.2.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy Note 20", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy A72", "system": "Android 11", "app": "8.8.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy A52", "system": "Android 11", "app": "8.7.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy M31", "system": "Android 10", "app": "8.5.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy M21", "system": "Android 10", "app": "8.4.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy S20 FE", "system": "Android 11", "app": "9.0.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy Note 10", "system": "Android 10", "app": "8.3.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 7", "system": "Android 13", "app": "10.0.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 6", "system": "Android 12", "app": "9.6.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 5", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 4a", "system": "Android 11", "app": "8.9.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 3", "system": "Android 10", "app": "8.2.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Mi 11", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Mi 10", "system": "Android 10", "app": "8.5.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Redmi Note 11", "system": "Android 11", "app": "9.0.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Redmi Note 10", "system": "Android 11", "app": "8.9.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Redmi Note 9", "system": "Android 10", "app": "8.4.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus 10 Pro", "system": "Android 13", "app": "10.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus 9 Pro", "system": "Android 12", "app": "9.5.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus 8T", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus Nord 2", "system": "Android 11", "app": "8.9.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus 7T", "system": "Android 10", "app": "8.4.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Huawei P50 Pro", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Huawei Mate 40 Pro", "system": "Android 10", "app": "8.5.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Huawei Nova 9", "system": "Android 11", "app": "8.9.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Huawei P40 Lite", "system": "Android 10", "app": "8.3.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Realme GT Neo 2", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Realme 8 Pro", "system": "Android 11", "app": "8.8.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Realme Narzo 30", "system": "Android 10", "app": "8.3.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Oppo Reno6", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Oppo A74", "system": "Android 11", "app": "8.8.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Oppo Find X3 Pro", "system": "Android 11", "app": "9.1.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Vivo V23", "system": "Android 12", "app": "9.6.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Vivo Y33s", "system": "Android 11", "app": "8.9.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Vivo X60 Pro", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Motorola Edge 30", "system": "Android 12", "app": "9.6.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Motorola Moto G100", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Motorola Moto G60", "system": "Android 11", "app": "8.9.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Nokia X20", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Nokia 5.4", "system": "Android 10", "app": "8.4.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Sony Xperia 1 III", "system": "Android 11", "app": "9.1.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Sony Xperia 5 II", "system": "Android 10", "app": "8.5.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Sony Xperia 10 II", "system": "Android 10", "app": "8.4.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Infinix Zero 5G", "system": "Android 11", "app": "8.9.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Infinix Note 10", "system": "Android 11", "app": "8.8.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Tecno Camon 18", "system": "Android 11", "app": "8.8.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Tecno Spark 7", "system": "Android 10", "app": "8.3.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy S23", "system": "Android 13", "app": "10.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy S22", "system": "Android 12", "app": "9.6.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy S21", "system": "Android 11", "app": "9.2.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy Note 20", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy A72", "system": "Android 11", "app": "8.8.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy A52", "system": "Android 11", "app": "8.7.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy M31", "system": "Android 10", "app": "8.5.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy M21", "system": "Android 10", "app": "8.4.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy S20 FE", "system": "Android 11", "app": "9.0.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Samsung Galaxy Note 10", "system": "Android 10", "app": "8.3.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 7", "system": "Android 13", "app": "10.0.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 6", "system": "Android 12", "app": "9.6.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 5", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 4a", "system": "Android 11", "app": "8.9.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Google Pixel 3", "system": "Android 10", "app": "8.2.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Mi 11", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Mi 10", "system": "Android 10", "app": "8.5.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Redmi Note 11", "system": "Android 11", "app": "9.0.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Redmi Note 10", "system": "Android 11", "app": "8.9.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Xiaomi Redmi Note 9", "system": "Android 10", "app": "8.4.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus 10 Pro", "system": "Android 13", "app": "10.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus 9 Pro", "system": "Android 12", "app": "9.5.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus 8T", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus Nord 2", "system": "Android 11", "app": "8.9.1", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "OnePlus 7T", "system": "Android 10", "app": "8.4.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Huawei P50 Pro", "system": "Android 11", "app": "9.0.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Huawei Mate 40 Pro", "system": "Android 10", "app": "8.5.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Huawei Nova 9", "system": "Android 11", "app": "8.9.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},
    {"name": "Huawei P40 Lite", "system": "Android 10", "app": "8.3.0", "API_ID": 27677998, "API_HASH": "37c49149eb55b3b5a97353c2e0666587"},    
    {"name": "iPhone 15 Pro Max", "system": "iOS 17", "app": "10.1.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 15 Pro", "system": "iOS 17", "app": "10.1.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 15", "system": "iOS 17", "app": "10.1.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 14 Pro Max", "system": "iOS 16", "app": "10.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 14 Pro", "system": "iOS 16", "app": "10.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 14", "system": "iOS 16", "app": "10.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 13 Pro Max", "system": "iOS 15", "app": "9.6.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 13 Pro", "system": "iOS 15", "app": "9.6.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 13", "system": "iOS 15", "app": "9.6.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 12 Pro Max", "system": "iOS 14", "app": "9.0.1", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 12 Pro", "system": "iOS 14", "app": "9.0.1", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 12", "system": "iOS 14", "app": "9.0.1", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 11 Pro Max", "system": "iOS 13", "app": "8.9.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 11 Pro", "system": "iOS 13", "app": "8.9.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 11", "system": "iOS 13", "app": "8.9.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone XS Max", "system": "iOS 12", "app": "8.5.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone XS", "system": "iOS 12", "app": "8.5.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone XR", "system": "iOS 12", "app": "8.5.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone X", "system": "iOS 11", "app": "8.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 8 Plus", "system": "iOS 11", "app": "8.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 8", "system": "iOS 11", "app": "8.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 7 Plus", "system": "iOS 10", "app": "7.9.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 7", "system": "iOS 10", "app": "7.9.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 6s Plus", "system": "iOS 9", "app": "7.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 6s", "system": "iOS 9", "app": "7.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone SE (2022)", "system": "iOS 15", "app": "9.6.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone SE (2020)", "system": "iOS 13", "app": "8.9.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone SE", "system": "iOS 9", "app": "7.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 6", "system": "iOS 9", "app": "7.0.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
    {"name": "iPhone 5s", "system": "iOS 8", "app": "6.9.0", "API_ID": 12128209, "API_HASH": "88e710f938e10c0d93bcbae954311cc5"},
  {"name": "Chrome", "system": "Web", "app": "115", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Firefox", "system": "Web", "app": "114", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Edge", "system": "Web", "app": "114", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Safari", "system": "Web", "app": "16", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Opera", "system": "Web", "app": "100", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Brave", "system": "Web", "app": "115", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Vivaldi", "system": "Web", "app": "6", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Chromium", "system": "Web", "app": "115", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Chrome", "system": "Web", "app": "116 BETA", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Firefox", "system": "Web", "app": "102 ESR", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Chrome", "system": "Web", "app": "115", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Firefox", "system": "Web", "app": "114", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Edge", "system": "Web", "app": "114", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Safari", "system": "Web", "app": "16", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Opera", "system": "Web", "app": "100", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Brave", "system": "Web", "app": "115", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Vivaldi", "system": "Web", "app": "6", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Chromium", "system": "Web", "app": "115", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Chrome", "system": "Web", "app": "116 BETA", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Firefox", "system": "Web", "app": "102 ESR", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Chrome", "system": "Web", "app": "115", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Firefox", "system": "Web", "app": "114", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Edge", "system": "Web", "app": "114", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Safari", "system": "Web", "app": "16", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Opera", "system": "Web", "app": "100", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Brave", "system": "Web", "app": "115", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Vivaldi", "system": "Web", "app": "6", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Chromium", "system": "Web", "app": "115", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Chrome", "system": "Web", "app": "116 BETA", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},
  {"name": "Firefox", "system": "Web", "app": "102 ESR", "API_ID": 24312695, "API_HASH": "600e609eee928456a1f0677eda1e0b06"},    
]

async def check_spam(client, string_session, api_id, api_hash, device, proxy_dict=None):
    """
    فحص الاسبام للرقم بإرسال رسالة لـ @alazaizy
    Returns: (is_spam: bool, error: str or None)
    - is_spam = True: الرقم اسبام (لا يرسل رسائل)
    - is_spam = False: الرقم ليس اسبام (تم إرسال الرسالة بنجاح)
    """
    spam_check_username = "alazaizy"  # المعرف المستهدف
    test_message = "Spam Check"  # رسالة الاختبار
       
    try:
        # إنشاء client مؤقت للفحص
        temp_client = TelegramClient(
            StringSession(string_session),
            api_id,
            api_hash,
            device_model=device['name'],
            system_version=device['system'],
            app_version=device['app'],
            lang_code='en',
            system_lang_code='en-US',
            proxy=proxy_dict,
            connection_retries=1,
            auto_reconnect=False,
            timeout=20.0  # زيادة timeout للاتصال
        )
        
        try:
            # الاتصال مع timeout
            await asyncio.wait_for(temp_client.connect(), timeout=20.0)
            
            # التحقق من أن الجلسة صالحة
            if not await temp_client.is_user_authorized():
                await temp_client.disconnect()
                return True, "الجلسة غير صالحة"
            
            
            # محاولة إرسال رسالة لـ @alazaizy
            try:
                # الحصول على كيان المستخدم
                target_entity = await temp_client.get_entity(spam_check_username)
                
                # محاولة إرسال الرسالة مع timeout
                sent_message = await asyncio.wait_for(
                    temp_client.send_message(target_entity, test_message),
                    timeout=15.0
                )
                
                # ✅ تم إرسال الرسالة بنجاح - الرقم ليس اسبام
                # الآن نحذف الشات والرسالة
                try:
                    # حذف الرسالة
                    await asyncio.wait_for(
                        temp_client.delete_messages(target_entity, [sent_message.id]),
                        timeout=5.0
                    )
                except Exception as del_msg_err:
                    pass
                
                try:
                    # حذف الشات (حذف المحادثة)
                    await asyncio.wait_for(
                        temp_client.delete_dialog(target_entity),
                        timeout=5.0
                    )
                except Exception as del_chat_err:
                    pass
                
                await temp_client.disconnect()
                return False, None  # ✅ ليس اسبام
                
            except PeerFloodError as flood_err:
                # ✅ PeerFloodError - الرقم محظور من إرسال الرسائل (اسبام)
                error_msg = str(flood_err)
                # ✅ لا نطبع traceback لأن هذا خطأ متوقع عندما يكون الرقم اسبام
                
                # محاولة إغلاق الاتصال
                try:
                    await temp_client.disconnect()
                except:
                    pass
                
                return True, "الرقم محظور من إرسال الرسائل (اسبام)"
                
            except Exception as send_err:
                # فشل إرسال الرسالة - الرقم اسبام
                error_msg = str(send_err)
                error_type = type(send_err).__name__
                import traceback
                traceback.print_exc()
                
                # محاولة إغلاق الاتصال
                try:
                    await temp_client.disconnect()
                except:
                    pass
                
                # التحقق من نوع الخطأ
                if "FLOOD" in error_msg.upper() or "SPAM" in error_msg.upper() or "blocked" in error_msg.lower():
                    return True, "الرقم محظور من إرسال الرسائل (اسبام)"
                elif "PEER_FLOOD" in error_msg or "USER_PRIVACY" in error_msg or "CHAT_SEND_MEDIA_FORBIDDEN" in error_msg:
                    return True, "الرقم لا يمكنه إرسال رسائل (اسبام)"
                elif "USERNAME_NOT_OCCUPIED" in error_msg or "USERNAME_INVALID" in error_msg:
                    return True, f"المعرف @{spam_check_username} غير موجود أو غير صالح"
                else:
                    return True, f"فشل إرسال الرسالة: {error_msg}"
                    
        except asyncio.TimeoutError:
            try:
                await temp_client.disconnect()
            except:
                pass
            return True, "انتهت مهلة الاتصال"
        except Exception as conn_err:
            error_msg = str(conn_err)
            error_type = type(conn_err).__name__
            import traceback
            traceback.print_exc()
            try:
                await temp_client.disconnect()
            except:
                pass
            return True, f"خطأ في الاتصال: {error_msg}"
            
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        import traceback
        traceback.print_exc()
        return True, f"خطأ في فحص الاسبام: {error_msg}"

def get_trx_exchange_rate():
    try:
        
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "tron",  
            "vs_currencies": "usd"  
        }
        
        
        response = requests.get(url, params=params)
        response.raise_for_status()  
        
        
        data = response.json()
        
     
        trx_price = data["tron"]["usd"]
        
        return trx_price
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TRX exchange rate: {e}")
        return None

@bot.on_message(filters.command("coin") & filters.private)
async def handle_coin_request(app, message):
    global yo
    try:
        user_id = str(message.from_user.id)
        user_data = users_db.get(user_id, {})
        
        balance = user_data.get('balance', 0.0)
        num_numbers = len(user_data.get('numbers', []))  
        
        
        # ✅ استخدام الترجمة
        language = users_db.get(user_id, {}).get('language', 'ar')
        msg_translation = translations[language]
        
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request_details = (
            f"{msg_translation['new_withdrawal_request']} \n\n"
            f"🔵{msg_translation['your_balance_is']} ${balance}\n\n"
            f"{msg_translation['current_time']}: {date_time}\n\n"
            f"{msg_translation['number_of_added_numbers']}: {num_numbers}\n\n"
            f"{msg_translation['click_button_to_enter_wallet']}"
        )
                
        request_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(msg_translation['enter_wallet_address'], callback_data=f"enter_wallet_{user_id}_{balance}")]]
        )

        await message.reply(request_details, reply_markup=request_markup)

    except Exception as e:
        print(f"Error: {e}")
        # ✅ استخدام الترجمة
        language = users_db.get(user_id, {}).get('language', 'ar')
        msg_translation = translations[language]
        await message.reply(msg_translation['error_processing_request'])
        

@bot.on_callback_query(filters.regex(r"enter_wallet_(\d+)_(\d+\.\d+)"))
async def enter_wallet_address(app, query):
    global yo
    try:
        match = re.match(r"enter_wallet_(\d+)_(\d+\.\d+)", query.data)
        if not match:
            raise ValueError("Pattern did not match")

        user_id = match.group(1)
        amount = float(match.group(2))

        
        # ✅ استخدام الترجمة
        language = users_db.get(user_id, {}).get('language', 'ar')
        msg_translation = translations[language]
        
        user_data = users_db.get(user_id, {})
        balance = user_data.get('balance', 0.0)
        if balance < yo:
            await query.message.reply(msg_translation['insufficient_balance'])
            return        
        
        # عرض خيارات نوع المحفظة
        wallet_type_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("BEP20", callback_data=f"wallet_type_BEP20_{user_id}_{amount}")],
            [InlineKeyboardButton("LEADERNAME", callback_data=f"wallet_type_LEADERNAME_{user_id}_{amount}")],
            [InlineKeyboardButton("TRC20", callback_data=f"wallet_type_TRC20_{user_id}_{amount}")]
        ])
        
        await query.message.reply(f"{msg_translation['send_withdrawal_wallet']}\n\n{msg_translation['allowed_wallet_types']}", reply_markup=wallet_type_markup)
    except Exception as e:
        print(f"Error in enter_wallet_address: {e}")
        # ✅ استخدام الترجمة
        user_id_str = str(query.from_user.id)
        language = users_db.get(user_id_str, {}).get('language', 'ar')
        msg_translation = translations[language]
        await query.message.reply(msg_translation['error_processing_request'])

# دالة معالجة اختيار نوع المحفظة
@bot.on_callback_query(filters.regex(r"wallet_type_(BEP20|LEADERNAME|TRC20)_(\d+)_(\d+\.\d+)"))
async def handle_wallet_type(app, query):
    global yo
    try:
        match = re.match(r"wallet_type_(BEP20|LEADERNAME|TRC20)_(\d+)_(\d+\.\d+)", query.data)
        if not match:
            raise ValueError("Pattern did not match")

        wallet_type = match.group(1)
        user_id = match.group(2)
        amount = float(match.group(3))

        # ✅ استخدام الترجمة
        user_id_str = str(query.from_user.id)
        language = users_db.get(user_id_str, {}).get('language', 'ar')
        msg_translation = translations[language]
        
        user_data = users_db.get(user_id, {})
        balance = user_data.get('balance', 0.0)
        if balance < yo:
            await query.message.reply(msg_translation['insufficient_balance'])
            return
        
        # إذا كان LEADERNAME، طلب اسم القائد مباشرة (كتابة نصية)
        if wallet_type == "LEADERNAME":
            request_wallet_details = msg_translation.get('enter_leadername', 'Please enter the LEADERNAME')
        else:
            # إذا كان BEP20 أو TRC20، طلب عنوان المحفظة
            request_wallet_details = f"Please enter the {wallet_type} wallet address"
               
        cancel_keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton("إلغاء")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await query.message.reply(request_wallet_details, reply_markup=cancel_keyboard)

        wallet_address_msg = await app.listen(query.message.chat.id, timeout=300)
        wallet_input = wallet_address_msg.text.strip()

        if wallet_input.lower() == msg_translation.get('cancel', 'إلغاء').lower() or wallet_input.lower() == "cancellation":
            await query.message.reply(msg_translation.get('operation_cancelled', 'The operation has been cancelled'), reply_markup=ReplyKeyboardRemove())
            return

        # إذا كان LEADERNAME، البحث عن القائد بالاسم
        leader_id = None
        wallet_address = wallet_input
        
        if wallet_type == "LEADERNAME":
            # البحث عن القائد بالاسم (دعم البحث غير حساس لحالة الأحرف)
            found_leader = False
            wallet_input_lower = wallet_input.strip().lower()
            
            for lid, leader_data in leaders_db.items():
                leader_name = leader_data.get('name', '').strip()
                leader_name_lower = leader_name.lower()
                
                # البحث بعدة طرق: بالاسم، بالمعرف، باليوزر
                if (leader_name_lower == wallet_input_lower or 
                    str(lid).lower() == wallet_input_lower or 
                    str(lid) == wallet_input or
                    (wallet_input.startswith('@') and str(lid).lower() == wallet_input[1:].lower())):
                    # ✅ تحويل lid إلى string للتأكد من المطابقة
                    leader_id = str(lid)
                    wallet_address = leader_data.get('wallet_address', '')
                    found_leader = True
                    print(f"[Withdrawal] Found leader: id={leader_id} (type: {type(leader_id)}), name={leader_name}, wallet={wallet_address[:20]}...")
                    break
            
            if not found_leader or not wallet_address:
                await query.message.reply(msg_translation['leader_no_wallet'], reply_markup=ReplyKeyboardRemove())
                print(f"[Withdrawal] Leader not found for input: {wallet_input}")
                return

        # متابعة معالجة السحب
        await process_withdrawal(app, query.message, user_id, amount, wallet_address, wallet_type, leader_id)

    except Exception as e:
        print(f"Error in handle_wallet_type: {e}")
        # ✅ استخدام الترجمة
        user_id_str = str(query.from_user.id)
        language = users_db.get(user_id_str, {}).get('language', 'ar')
        msg_translation = translations[language]
        await query.message.reply(msg_translation['error_processing_request'])

# دالة معالجة اختيار القائد
@bot.on_callback_query(filters.regex(r"select_leader_(\d+)_(\d+)_(\d+\.\d+)"))
async def select_leader_for_withdrawal(app, query):
    global yo
    try:
        match = re.match(r"select_leader_(\d+)_(\d+)_(\d+\.\d+)", query.data)
        if not match:
            raise ValueError("Pattern did not match")

        leader_id = match.group(1)
        user_id = match.group(2)
        amount = float(match.group(3))

        if leader_id not in leaders_db:
            await query.message.reply("❌ القائد غير موجود.")
            return

        leader_data = leaders_db[leader_id]
        wallet_address = leader_data.get('wallet_address', '')
        
        if not wallet_address:
            await query.message.reply("❌ القائد لا يملك عنوان محفظة مسجل.")
            return

        # متابعة معالجة السحب باستخدام عنوان محفظة القائد
        await process_withdrawal(app, query.message, user_id, amount, wallet_address, "LEADERNAME", leader_id)

    except Exception as e:
        print(f"Error in select_leader_for_withdrawal: {e}")
        await query.message.reply("حدث خطأ أثناء معالجة طلبك. الرجاء المحاولة لاحقًا.")

# دالة معالجة السحب (منفصلة للاستخدام من أماكن متعددة)
async def process_withdrawal(app, message, user_id, amount, wallet_address, wallet_type="TRC20", leader_id=None):
    try:

        # ✅ استخدام الترجمة
        language = users_db.get(user_id, {}).get('language', 'ar')
        msg_translation = translations[language]

        trx_exchange_rate = get_trx_exchange_rate()
        if trx_exchange_rate is None:
            await message.reply(msg_translation['trx_exchange_error'], reply_markup=ReplyKeyboardRemove())
            return
        
        total_in_trx = amount / trx_exchange_rate
        
        user_info = await app.get_users(int(user_id))
        username = user_info.username if hasattr(user_info, 'username') else "N/A"
        name = user_info.first_name if hasattr(user_info, 'first_name') else "N/A"
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        user_data = users_db.get(user_id, {})
        
        # ✅ الحصول على بيانات القائد إذا كان LEADERNAME
        leader_name_for_simple = "N/A"
        if leader_id:
            leader_data_temp = leaders_db.get(str(leader_id), {})
            leader_name_for_simple = leader_data_temp.get('name', f'Leader {leader_id}')

        # ✅ إنشاء رسالتين منفصلتين: واحدة للأدمن وأخرى لقناة القائد
        # رسالة مفصلة (للأدمن عند BEP20/TRC20، وللقائد عند LEADERNAME)
        withdrawal_details_full = (
            f"New withdrawal request\n\n"
            f"🔵 User: @{username}\n"
            f"🟢 **Name: {name}**\n"
            f"🟡 **User ID:** `{user_id}`\n"
            f"💰**Amount: ${amount}**\n"
            f"💱 TRX Exchange Rate: {trx_exchange_rate} USD\n"
            f"💲 Total in TRX: `{total_in_trx} `TRX\n"
            f"🟠Wallet Type: {wallet_type}\n"
            f"🟠Wallet Address: `{wallet_address}`\n"
        )
        
        # رسالة مبسطة (للأدمن عند LEADERNAME)
        withdrawal_details_simple = (
            f"New withdrawal request\n\n"
            f"🔵 User: @{username}\n"
            f"🟢 **Name: {name}**\n"
            f"💰**Amount: ${amount}**\n"
            f"👤 Leader: {leader_name_for_simple}\n"
            f"📱 Numbers: {len(user_data.get('numbers', []))}\n"
            f"📅Date and Time: **{date_time}**\n"
        )
        
        if leader_id:
            leader_data = leaders_db.get(leader_id, {})
            leader_name = leader_data.get('name', f'Leader {leader_id}')
            withdrawal_details_full += f"👤 Leader: {leader_name}\n"
        
        withdrawal_details_full += (
            f"📅Date and Time: **{date_time}**\n"
            f"📱 The number of added numbers  {len(user_data.get('numbers', []))}\n"  
        )
        
        # حفظ عدد الأرقام قبل حذفها (لحساب عمولة القائد)
        numbers_count_before_delete = len(user_data.get('numbers', []))
        
        # ✅ استخدام معرّف مؤقت لتجنب مشكلة BUTTON_DATA_INVALID (64 بايت محدود)
        withdrawal_id = str(int(time.time() * 1000)) + str(user_id)[:6]  # timestamp + user_id مختصر
        # ✅ تحويل leader_id إلى string للتأكد من المطابقة
        leader_id_str_for_storage = str(leader_id).strip() if leader_id else 'NONE'
        
        pending_withdrawals[withdrawal_id] = {
            'user_id': user_id,
            'amount': amount,
            'wallet_address': wallet_address,
            'wallet_type': wallet_type,
            'leader_id': leader_id_str_for_storage,
            'numbers_count': numbers_count_before_delete
        }
        print(f"[Withdrawal] Saved withdrawal data: withdrawal_id={withdrawal_id}, leader_id={leader_id_str_for_storage} (type: {type(leader_id_str_for_storage)}), numbers_count={numbers_count_before_delete}")
        
        # ✅ استخدام الترجمة (للأدمن والقائد - رسائل داخلية)
        # ملاحظة: زر Confirm يظهر للقائد عند LEADERNAME وللأدمن عند BEP20/TRC20
        confirmation_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Confirm Withdrawal", callback_data=f"confirm_withdrawal_{withdrawal_id}")]]
        )

        # ✅ إرسال رسالة للأدمن: مفصلة مع زر Confirm إذا كان BEP20/TRC20، مفصلة بدون زر إذا كان LEADERNAME
        if wallet_type == "LEADERNAME" and leader_id:
            # رسالة مفصلة للأدمن عند استخدام LEADERNAME (بدون زر Confirm)
            await app.send_message(OWNER_CHANNEL_ID, withdrawal_details_full, reply_markup=None)
        else:
            # رسالة مفصلة للأدمن عند استخدام BEP20/TRC20 (مع زر Confirm)
            await app.send_message(OWNER_CHANNEL_ID, withdrawal_details_full, reply_markup=confirmation_markup)
        
        # ✅ إذا كان السحب من قائد، تحديث إحصائيات القائد مباشرة عند تقديم الطلب
        if leader_id and leader_id != "NONE":
            # البحث عن القائد في قاعدة البيانات
            found_leader_key = None
            leader_id_str = str(leader_id).strip()
            
            # محاولة البحث المباشر أولاً
            if leader_id_str in leaders_db:
                found_leader_key = leader_id_str
            else:
                # البحث غير حساس لحالة الأحرف
                for key in leaders_db.keys():
                    key_str = str(key).strip()
                    if key_str.lower() == leader_id_str.lower() or key_str == leader_id_str:
                        found_leader_key = key
                        break
            
            if found_leader_key:
                print(f"[Withdrawal] ✅ Updating stats immediately for leader: {found_leader_key}")
                leader_data = leaders_db[found_leader_key]
                
                if 'stats' not in leader_data:
                    leader_data['stats'] = {
                        'withdrawals_count': 0,
                        'total_withdrawn': 0.0,
                        'total_commission': 0.0,
                        'numbers_count': 0
                    }
                
                # حساب العمولة: عدد الأرقام × عمولة كل رقم
                commission_per_number = leader_data.get('commission', 0.03)
                total_commission = numbers_count_before_delete * commission_per_number
                
                # ✅ تحديث الإحصائيات مباشرة عند تقديم الطلب
                leader_data['stats']['withdrawals_count'] = leader_data['stats'].get('withdrawals_count', 0) + 1
                leader_data['stats']['total_withdrawn'] = leader_data['stats'].get('total_withdrawn', 0.0) + amount
                leader_data['stats']['total_commission'] = leader_data['stats'].get('total_commission', 0.0) + total_commission
                leader_data['stats']['numbers_count'] = leader_data['stats'].get('numbers_count', 0) + numbers_count_before_delete
                save_leaders_db()
                
                print(f"[Withdrawal] ✅ Stats updated immediately: withdrawals={leader_data['stats']['withdrawals_count']}, total_withdrawn=${leader_data['stats']['total_withdrawn']:.2f}, commission=${leader_data['stats']['total_commission']:.2f}, numbers={leader_data['stats']['numbers_count']}")
                
                # ✅ إرسال إشعار طلب السحب للقناة الخاصة بالقائد (رسالة خاصة بالقائد)
                leader_channel_id = leader_data.get('channel_id', '')
                if leader_channel_id:
                    try:
                        # حساب العمولة
                        commission_per_number = leader_data.get('commission', 0.03)
                        total_commission = numbers_count_before_delete * commission_per_number
                        total_with_commission = amount + total_commission
                        
                        # رسالة خاصة للقائد
                        leader_withdrawal_message = (
                            f"New withdrawal request\n\n"
                            f"🔵 User: @{username}\n"
                            f"🟢 **Name: {name}**\n"
                            f"🟡 **User ID:** `{user_id}`\n"
                            f"💰**Amount: ${amount}**\n"
                            f"💳 Leader Card: {leader_data.get('name', 'N/A')}\n"
                            f"💵 Commission: ${total_commission:.2f} ({commission_per_number * 100}%)\n"
                            f"💰 Total with Commission: ${total_with_commission:.2f}\n"
                            f"📅Date and Time: **{date_time}**\n"
                            f"📱 The number of added numbers {numbers_count_before_delete}"
                        )
                        
                        # ✅ إرسال رسالة للقائد مع زر Confirm Withdrawal
                        await app.send_message(leader_channel_id, leader_withdrawal_message, reply_markup=confirmation_markup)
                        print(f"[Withdrawal] Notification sent to leader channel: {leader_channel_id}")
                    except Exception as e:
                        print(f"[Withdrawal] Error sending to leader channel {leader_channel_id}: {e}")
        
        # ✅ استخدام الترجمة
        language = users_db.get(user_id, {}).get('language', 'ar')
        msg_translation = translations[language]
        
        await message.reply(msg_translation['request_sent_to_owner'], reply_markup=ReplyKeyboardRemove())
        if user_id in users_db:
            users_db[user_id]['balance'] -= amount
        users_db[user_id]['numbers'] = []
        save_db() 
        
    except Exception as e:
        print(f"Error in process_withdrawal: {e}")
        # ✅ استخدام الترجمة
        language = users_db.get(user_id, {}).get('language', 'ar')
        msg_translation = translations[language]
        await message.reply(msg_translation['error_processing_request'])
        await app.send_message(OWNER_CHANNEL_ID, f"خطأ أثناء معالجة طلب السحب: {str(e)}")

@bot.on_callback_query(filters.regex(r"confirm_withdrawal_(.+)"))
async def confirm_withdrawal(app, query):
    try:
        withdrawal_id = query.data.split('_', 2)[2]  # confirm_withdrawal_{withdrawal_id}
        
        # جلب المعلومات من pending_withdrawals
        if withdrawal_id not in pending_withdrawals:
            # محاولة نمط قديم للتوافق مع السحوبات القديمة
            match_old = re.match(r"confirm_withdrawal_(\d+)_(\d+\.\d+)_(.+)", query.data)
            if match_old:
                user_id = match_old.group(1)
                amount = float(match_old.group(2))
                wallet_encoded = match_old.group(3)
                wallet_address = wallet_encoded.replace('_', ':').replace('_PLUS_', '+').replace('_AND_', '&')
                wallet_type = "TRC20"
                leader_id = "NONE"
                numbers_count = 0
            else:
                raise ValueError("Withdrawal ID not found or invalid pattern")
        else:
            withdrawal_data = pending_withdrawals[withdrawal_id]
            user_id = withdrawal_data['user_id']
            amount = withdrawal_data['amount']
            wallet_address = withdrawal_data['wallet_address']
            wallet_type = withdrawal_data['wallet_type']
            leader_id = withdrawal_data['leader_id']
            numbers_count = withdrawal_data['numbers_count']
            
            # حذف المعلومات المؤقتة بعد الاستخدام
            del pending_withdrawals[withdrawal_id]
                                         
        original_text = query.message.text
        confirmation_text = "\n\nThe transfer has been confirmed successfully ✅"

        await query.message.edit_text(
            original_text + confirmation_text,
            reply_markup=None
        )

        # ✅ استخدام الترجمة
        language = users_db.get(user_id, {}).get('language', 'ar')
        msg_translation = translations[language]
        
        await app.send_message(user_id, msg_translation['payment_confirmed_successfully'])
        
        # ✅ الإحصائيات تم تحديثها بالفعل عند تقديم الطلب، لا حاجة لتحديثها هنا
        print(f"[Withdrawal] Withdrawal confirmed for user {user_id}, amount: ${amount}")

    except Exception as e:
        print(f"Error in confirmation: {e}")
        
@bot.on_message(filters.command("language") & filters.private)
async def change_language_callback(app, query):
    user_id = str(query.from_user.id)
    
    if user_id not in users_db:
        users_db[user_id] = {
            "language": "ar"
        }
    
    language = users_db[user_id]['language']
    
    # ✅ بناء رسالة اختيار اللغة بنفس أسلوب الصورة
    translated_text = translations[language]['select_language']
    
    # ✅ استخدام InlineKeyboardButtons مع الأعلام
    await app.send_message(
        chat_id=query.chat.id,
        text=translated_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🇮🇷 فارسی", callback_data="set_language_fa"),
                    InlineKeyboardButton("🇷🇺 Russia", callback_data="set_language_ru")
                ],
                [
                    InlineKeyboardButton("🇬🇧 English", callback_data="set_language_en"),
                    InlineKeyboardButton("🇪🇬 Arabic", callback_data="set_language_ar")
                ]
            ]
        )
    )

@bot.on_callback_query(filters.regex("gift"))
async def check_gifts(app, q: CallbackQuery):
    count=0
    user_id = str(q.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    translation = translations.get(language, translations['ar'])

    key_back = InlineKeyboardMarkup([[InlineKeyboardButton(translation.get('cancel', 'إلغاء'), callback_data='back')]])
    
    await q.edit_message_text(translation.get('please_wait', 'جاري الفحص..'), reply_markup=key_back)
    
    # جلب الأرقام من قاعدة البيانات
    from data import database
    db = database()
    xdata = db.view()
    
    for i in xdata:
        number = i[1] if len(i) > 1 else None
        string_session = i[0] if len(i) > 0 else None
        
        if not number or not string_session:
            continue
            
        try:
            device = random.choice(DEVICES_LIST)
            proxy = get_proxy_for_number(number)
            clogin = TelegramClient(
                StringSession(string_session),
                device['API_ID'],
                device['API_HASH'],
                device_model=device['name'],
                system_version=device['system'],
                app_version=device['app'],
                lang_code='en',
                system_lang_code='en-US',
                proxy=proxy,
                connection_retries=0,
                retry_delay=0,
                auto_reconnect=False
            )
            # ✅ استخدام timeout قصير للاتصال لتجنب التأخير
            try:
                await asyncio.wait_for(clogin.connect(), timeout=5.0)
            except (asyncio.TimeoutError, Exception) as e:
                await app.send_message(q.message.chat.id, f"فشل الاتصال: {str(e)}")
                try:
                    await clogin.disconnect()
                except:
                    pass
                continue
            if not await clogin.is_user_authorized():
                await app.send_message(q.message.chat.id, f"الرقم : {number} غير صالح")
                await clogin.disconnect()
            else:
                async for msg in clogin.iter_messages(777000):
                    if msg.action and isinstance(msg.action, MessageActionGiftCode):
                        count+=1
                        xmsg_view = f"https://t.me/giftcode/{msg.action.slug}\nمن رقم : {number}"
                        await app.send_message(q.message.chat.id, xmsg_view)
                await clogin.disconnect()
        except Exception as ex:
            await app.send_message(q.message.chat.id, f"حدث خطأ: {str(ex)}")
            if 'clogin' in locals():
                try:
                    await clogin.disconnect()
                except:
                    pass
    if count==0:
        return await q.edit_message_text(f"لا توجد روابط هدايا!", reply_markup=key_back)
    else:
        return await app.send_message(q.message.chat.id, f"تم العثور على ({count}) رابط هدية", reply_markup=key_back)

def load_countries_db():
    global countries_db
    try:
        with open('countries_db.json', 'r', encoding='utf-8') as f:
            countries_db = json.load(f)
            return countries_db
    except FileNotFoundError:
        countries_db = {}
        return {}


def count_numbers_by_country():
    """عد الأرقام المتوفرة لكل دولة من مجلد numbers"""
    numbers_folder = "numbers"  
    country_count = {}
    
    if not os.path.exists(numbers_folder):
        os.makedirs(numbers_folder)
        return country_count
   
    for filename in os.listdir(numbers_folder):
        if filename.endswith(".session"):
            # استخراج رمز الدولة من اسم الملف (مثل +1234567890.session)
            number_str = filename.replace(".session", "")
            
            # البحث عن رمز الدولة المطابق من countries_db
            matched_code = None
            for country_name, country_data in countries_db.items():
                code = country_data.get("code", "")
                if number_str.startswith(code):
                    matched_code = code
                    break
            
            if matched_code:
                if matched_code in country_count:
                    country_count[matched_code] += 1
                else:
                    country_count[matched_code] = 1

    return country_count

async def generate_country_buttons():
    """إنشاء أزرار الدول مع عدد الأرقام المتوفرة من ملفات .session + علم الدولة"""
    # ✅ حساب عدد الأرقام من ملفات .session في مجلد numbers
    numbers_by_country = count_numbers_by_country()
    buttons = []

    for country_name, country_data in countries_db.items():
        code = country_data.get("code", "")
        price = country_data.get("price", 0.0)
        
        # ✅ عدد الأرقام المتوفرة من ملفات .session في مجلد numbers
        num_available = numbers_by_country.get(code, 0)
        
        # ✅ الحصول على علم الدولة
        flag = get_country_flag(code)
        
        # ✅ إضافة علم الدولة بجانب الاسم
        name_button = InlineKeyboardButton(f"{flag} {country_name} ({num_available})", callback_data=f"view_{country_name}")
        price_button = InlineKeyboardButton(f"{price}$", callback_data=f"price_{country_name}")

        buttons.append([name_button, price_button])

    return InlineKeyboardMarkup(buttons)

@bot.on_callback_query(filters.regex("show_countries"))
async def show_countries_callback(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    translation = translations.get(language, translations['ar'])
    
    buttons = await generate_country_buttons()
    text = translation.get('show_countries', 'الدول المسجلة:')
    if not countries_db:
        text = translation.get('no_countries', 'لا توجد دول مسجلة حالياً.')
    await query.message.edit_text(text, reply_markup=buttons)

@bot.on_callback_query(filters.regex("unban_user"))
async def handle_unban_user(client, callback_query):
    user_id = str(callback_query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    translation = translations.get(language, translations['ar'])
    
    if callback_query.from_user.id != sudo:
        await callback_query.answer(translation['no_permission'], show_alert=True)
        return
    
    await callback_query.message.reply(translation['send_user_id_unban'])
    
    @bot.on_message(filters.private)
    async def receive_user_id(client, message):
            user_id = message.text.strip()
            msg_user_id = str(message.from_user.id)
            msg_language = users_db.get(msg_user_id, {}).get('language', 'ar')
            msg_translation = translations.get(msg_language, translations['ar'])
            
            if unban_user(user_id):
                await message.reply(msg_translation['user_unbanned_success'].format(user_id=user_id))
            else:
                await message.reply(msg_translation['user_not_banned'].format(user_id=user_id))

def create_keyboards(bot, msg, language, is_sudo):
    global sudo
    if is_sudo:
        key_not = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(translations[language]['add_country'], callback_data='add_country'),
                 InlineKeyboardButton(translations[language]['delete_country'], callback_data='delete_country')],
                [InlineKeyboardButton(translations[language]['show_countries'], callback_data='show_countries')],
                [InlineKeyboardButton(translations[language]['ban_user_button'], callback_data='ban_user'),
                 InlineKeyboardButton(translations[language]['unban_user_button'], callback_data='unban_user')],
                [InlineKeyboardButton(translations[language]['send_country_numbers'], callback_data='send_country_numbers')],
                [InlineKeyboardButton(translations[language]['maintenance_True'], callback_data='enable_maintenance'),
                 InlineKeyboardButton(translations[language]['maintenance_False'], callback_data='disable_maintenance')],
                [InlineKeyboardButton(translations[language]['ax'], callback_data='add_balance'),
                 InlineKeyboardButton(translations[language]['idbc'], callback_data='deduct_balance')],
                [InlineKeyboardButton(translations[language]['gift'], callback_data='gift')],
                [InlineKeyboardButton(translations[language]['add_leader'], callback_data='add_leader'),
                 InlineKeyboardButton(translations[language]['edit_leader'], callback_data='edit_leader')],
                [InlineKeyboardButton(translations[language]['delete_leader'], callback_data='delete_leader'),
                 InlineKeyboardButton(translations[language]['show_leader_stats'], callback_data='show_leader_stats')],
                [InlineKeyboardButton(translations[language]['encrypt_leader_stats'], callback_data='encrypt_leader_stats')],
            ]
        )
    else:
        key_not = None
    
    return key_not

# ============= دوال إدارة القادة =============

# إضافة قائد
@bot.on_callback_query(filters.regex("add_leader"))
async def add_leader_handler(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    msg_translation = translations[language]
    
    if query.from_user.id != sudo:
        await query.answer(msg_translation.get('no_permission', '❌ ليس لديك صلاحية'), show_alert=True)
        return
    
    await query.message.reply(msg_translation['enter_leader_id'])
    
    try:
        leader_identifier_msg = await app.listen(query.message.chat.id, timeout=300)
        leader_identifier = leader_identifier_msg.text.strip()
        
        # تنظيف المعرف (إزالة @ إذا كان يوزر)
        if leader_identifier.startswith('@'):
            leader_id = leader_identifier[1:]
        else:
            leader_id = leader_identifier
        
        await query.message.reply(msg_translation['enter_leader_channel'])
        channel_msg = await app.listen(query.message.chat.id, timeout=300)
        channel_id = channel_msg.text.strip()
        
        await query.message.reply(msg_translation['enter_leader_name'])
        name_msg = await app.listen(query.message.chat.id, timeout=300)
        leader_name = name_msg.text.strip()
        
        await query.message.reply(msg_translation['enter_leader_commission'])
        commission_msg = await app.listen(query.message.chat.id, timeout=300)
        try:
            commission = float(commission_msg.text.strip())
        except ValueError:
            await query.message.reply(msg_translation['invalid_commission'])
            return
        
        await query.message.reply(msg_translation['enter_leader_wallet'])
        wallet_msg = await app.listen(query.message.chat.id, timeout=300)
        wallet_address = wallet_msg.text.strip()
        
        # إضافة القائد إلى قاعدة البيانات
        leaders_db[leader_id] = {
            'name': leader_name,
            'channel_id': channel_id,
            'commission': commission,
            'wallet_address': wallet_address,
            'stats': {
                'withdrawals_count': 0,
                'total_withdrawn': 0.0,
                'total_commission': 0.0,
                'numbers_count': 0
            }
        }
        save_leaders_db()
        
        await query.message.reply(msg_translation['leader_added_success'].format(name=leader_name))
        
    except asyncio.TimeoutError:
        await query.message.reply(msg_translation.get('timeout', '⏱ انتهت مهلة الإدخال'))
    except Exception as e:
        await query.message.reply(f"❌ {msg_translation.get('unknown_error', 'حدث خطأ')}: {str(e)}")

# تعديل قائد
@bot.on_callback_query(filters.regex("edit_leader"))
async def edit_leader_handler(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    msg_translation = translations[language]
    
    if query.from_user.id != sudo:
        await query.answer(msg_translation.get('no_permission', '❌ ليس لديك صلاحية'), show_alert=True)
        return
    
    if not leaders_db:
        await query.message.reply(msg_translation['no_leaders'])
        return
    
    # عرض قائمة القادة
    buttons = []
    for leader_id, leader_data in leaders_db.items():
        leader_name = leader_data.get('name', f'Leader {leader_id}')
        # ✅ استخدام معرّف فريد لتجنب التكرار
        buttons.append([InlineKeyboardButton(leader_name, callback_data=f"edit_ldr_{leader_id}")])
    
    markup = InlineKeyboardMarkup(buttons)
    try:
        await query.message.edit_text(msg_translation['choose_leader_to_edit'], reply_markup=markup)
    except Exception as e:
        # إذا فشل edit_text (ربما نفس المحتوى)، استخدم reply
        print(f"[Edit Leader] Error editing message: {e}")
        await query.message.reply(msg_translation['choose_leader_to_edit'], reply_markup=markup)

@bot.on_callback_query(filters.regex(r"edit_ldr_(.+)"))
async def edit_leader_details(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    msg_translation = translations[language]
    
    if query.from_user.id != sudo:
        await query.answer(msg_translation.get('no_permission', '❌ ليس لديك صلاحية'), show_alert=True)
        return
    
    # استخراج leader_id من callback_data: edit_ldr_{leader_id}
    leader_id = query.data.replace('edit_ldr_', '', 1)
    
    print(f"[Edit Leader] Extracted leader_id: '{leader_id}' from callback_data: '{query.data}'")
    print(f"[Edit Leader] Available leader IDs: {list(leaders_db.keys())}")
    
    if leader_id not in leaders_db:
        await query.answer(msg_translation['leader_not_found'], show_alert=True)
        try:
            await query.message.edit_text(msg_translation['leader_not_found'], reply_markup=None)
        except Exception as e:
            print(f"[Edit Leader] Error editing message: {e}")
            await query.message.reply(msg_translation['leader_not_found'])
        return
    
    await query.answer("✅", show_alert=False)
    try:
        await query.message.edit_text(msg_translation['enter_new_leader_data'], reply_markup=None)
    except Exception as e:
        print(f"[Edit Leader] Error editing message: {e}")
        await query.message.reply(msg_translation['enter_new_leader_data'])
    
    try:
        data_msg = await app.listen(query.message.chat.id, timeout=300)
        lines = data_msg.text.strip().split('\n')
        
        if len(lines) >= 4:
            leader_name = lines[0].strip()
            channel_id = lines[1].strip()
            commission = float(lines[2].strip())
            wallet_address = lines[3].strip()
            
            # الحفاظ على الإحصائيات الحالية
            old_stats = leaders_db[leader_id].get('stats', {
                'withdrawals_count': 0,
                'total_withdrawn': 0.0,
                'total_commission': 0.0,
                'numbers_count': 0
            })
            
            leaders_db[leader_id] = {
                'name': leader_name,
                'channel_id': channel_id,
                'commission': commission,
                'wallet_address': wallet_address,
                'stats': old_stats
            }
            save_leaders_db()
            
            await query.message.reply(msg_translation['leader_edited_success'])
        else:
            await query.message.reply(msg_translation['incomplete_data'])
    except ValueError:
        await query.message.reply(msg_translation['invalid_commission'])
    except asyncio.TimeoutError:
        await query.message.reply(msg_translation.get('timeout', '⏱ انتهت مهلة الإدخال'))
    except Exception as e:
        await query.message.reply(f"❌ {msg_translation.get('unknown_error', 'حدث خطأ')}: {str(e)}")

# حذف قائد
@bot.on_callback_query(filters.regex("delete_leader"))
async def delete_leader_handler(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    msg_translation = translations[language]
    
    if query.from_user.id != sudo:
        await query.answer(msg_translation.get('no_permission', '❌ ليس لديك صلاحية'), show_alert=True)
        return
    
    if not leaders_db:
        await query.message.reply(msg_translation['no_leaders'])
        return
    
    buttons = []
    for leader_id, leader_data in leaders_db.items():
        leader_name = leader_data.get('name', f'Leader {leader_id}')
        # ✅ استخدام معرّف فريد لتجنب التكرار
        buttons.append([InlineKeyboardButton(leader_name, callback_data=f"del_leader_{leader_id}")])
    
    markup = InlineKeyboardMarkup(buttons)
    try:
        await query.message.edit_text(msg_translation['choose_leader_to_delete'], reply_markup=markup)
    except Exception as e:
        # إذا فشل edit_text (ربما نفس المحتوى)، استخدم reply
        print(f"[Delete Leader] Error editing message: {e}")
        await query.message.reply(msg_translation['choose_leader_to_delete'], reply_markup=markup)

@bot.on_callback_query(filters.regex(r"del_leader_(.+)"))
async def delete_leader_confirm(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    msg_translation = translations[language]
    
    if query.from_user.id != sudo:
        await query.answer(msg_translation.get('no_permission', '❌ ليس لديك صلاحية'), show_alert=True)
        return
    
    # استخراج leader_id من callback_data: del_leader_{leader_id}
    leader_id = query.data.replace('del_leader_', '', 1)
    
    print(f"[Delete Leader] Extracted leader_id: '{leader_id}' from callback_data: '{query.data}'")
    print(f"[Delete Leader] Available leader IDs: {list(leaders_db.keys())}")
    
    if leader_id in leaders_db:
        leader_name = leaders_db[leader_id].get('name', f'Leader {leader_id}')
        del leaders_db[leader_id]
        save_leaders_db()
        await query.answer(msg_translation['leader_deleted_success'].format(name=leader_name), show_alert=True)
        try:
            await query.message.edit_text(msg_translation['leader_deleted_success'].format(name=leader_name), reply_markup=None)
        except Exception as e:
            print(f"[Delete Leader] Error editing message: {e}")
            await query.message.reply(msg_translation['leader_deleted_success'].format(name=leader_name))
    else:
        await query.answer(msg_translation['leader_not_found'], show_alert=True)
        try:
            await query.message.edit_text(msg_translation['leader_not_found'], reply_markup=None)
        except Exception as e:
            print(f"[Delete Leader] Error editing message: {e}")
            await query.message.reply(msg_translation['leader_not_found'])

# إحصائيات قائد
@bot.on_callback_query(filters.regex("show_leader_stats"))
async def show_leader_stats_handler(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    msg_translation = translations[language]
    
    if query.from_user.id != sudo:
        await query.answer(msg_translation.get('no_permission', '❌ ليس لديك صلاحية'), show_alert=True)
        return
    
    if not leaders_db:
        await query.message.reply(msg_translation['no_leaders'])
        return
    
    buttons = []
    for leader_id, leader_data in leaders_db.items():
        leader_name = leader_data.get('name', f'Leader {leader_id}')
        buttons.append([InlineKeyboardButton(leader_name, callback_data=f"show_stats_{leader_id}")])
    
    markup = InlineKeyboardMarkup(buttons)
    try:
        await query.message.edit_text(msg_translation['choose_leader_to_show_stats'], reply_markup=markup)
    except Exception as e:
        print(f"[Show Stats] Error editing message: {e}")
        await query.message.reply(msg_translation['choose_leader_to_show_stats'], reply_markup=markup)

@bot.on_callback_query(filters.regex(r"show_stats_(.+)"))
async def show_leader_stats(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    msg_translation = translations[language]
    
    # استخراج leader_id من callback_data (يدعم أرقام وحروف)
    leader_id = query.data.split('_', 2)[2] if '_' in query.data and query.data.count('_') >= 2 else query.data.replace('show_stats_', '')
    if leader_id not in leaders_db:
        await query.message.reply(msg_translation['leader_not_found'])
        return
    
    leader_data = leaders_db[leader_id]
    stats = leader_data.get('stats', {
        'withdrawals_count': 0,
        'total_withdrawn': 0.0,
        'total_commission': 0.0,
        'numbers_count': 0
    })
    
    stats_text = f"""{msg_translation['leader_stats_title'].format(name=leader_data.get('name', 'N/A'))}

{msg_translation['leader_withdrawals_count'].format(count=stats.get('withdrawals_count', 0))}
{msg_translation['leader_total_withdrawn'].format(amount=stats.get('total_withdrawn', 0.0))}
{msg_translation['leader_total_commission'].format(amount=stats.get('total_commission', 0.0))}
{msg_translation['leader_numbers_count'].format(count=stats.get('numbers_count', 0))}
"""
    
    await query.message.reply(stats_text)

# تشفير إحصائيات القائد (إعادة تعيين)
@bot.on_callback_query(filters.regex("encrypt_leader_stats"))
async def encrypt_leader_stats_handler(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    msg_translation = translations[language]
    
    if query.from_user.id != sudo:
        await query.answer(msg_translation.get('no_permission', '❌ ليس لديك صلاحية'), show_alert=True)
        return
    
    if not leaders_db:
        await query.message.reply(msg_translation['no_leaders'])
        return
    
    buttons = []
    for leader_id, leader_data in leaders_db.items():
        leader_name = leader_data.get('name', f'Leader {leader_id}')
        buttons.append([InlineKeyboardButton(leader_name, callback_data=f"encrypt_stats_{leader_id}")])
    
    markup = InlineKeyboardMarkup(buttons)
    try:
        await query.message.edit_text(msg_translation['choose_leader_to_encrypt'], reply_markup=markup)
    except Exception as e:
        print(f"[Encrypt Stats] Error editing message: {e}")
        await query.message.reply(msg_translation['choose_leader_to_encrypt'], reply_markup=markup)

@bot.on_callback_query(filters.regex(r"encrypt_stats_(.+)"))
async def encrypt_leader_stats(app, query):
    user_id = str(query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    msg_translation = translations[language]
    
    if query.from_user.id != sudo:
        await query.answer(msg_translation.get('no_permission', '❌ ليس لديك صلاحية'), show_alert=True)
        return
    
    # استخراج leader_id من callback_data (يدعم أرقام وحروف)
    leader_id = query.data.split('_', 2)[2] if '_' in query.data and query.data.count('_') >= 2 else query.data.replace('encrypt_stats_', '')
    if leader_id in leaders_db:
        leaders_db[leader_id]['stats'] = {
            'withdrawals_count': 0,
            'total_withdrawn': 0.0,
            'total_commission': 0.0,
            'numbers_count': 0
        }
        save_leaders_db()
        leader_name = leaders_db[leader_id].get('name', 'N/A')
        await query.answer(msg_translation['leader_stats_reset'].format(name=leader_name), show_alert=True)
        try:
            await query.message.edit_text(msg_translation['leader_stats_reset'].format(name=leader_name), reply_markup=None)
        except Exception as e:
            print(f"[Encrypt Stats] Error editing message: {e}")
            await query.message.reply(msg_translation['leader_stats_reset'].format(name=leader_name))
    else:
        await query.answer(msg_translation['leader_not_found'], show_alert=True)
        try:
            await query.message.edit_text(msg_translation['leader_not_found'], reply_markup=None)
        except Exception as e:
            print(f"[Encrypt Stats] Error editing message: {e}")
            await query.message.reply(msg_translation['leader_not_found'])

# تم نقل الدالة إلى الأسفل مع /start
@bot.on_callback_query(filters.regex("disable_maintenance"))
async def disable_maintenance(app, msg):
    global maintenance
    user_id = str(msg.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    translation = translations.get(language, translations['ar'])
    
    if maintenance == False: 
        return await app.send_message(msg.message.chat.id, translation['maintenance_mode_already_disabled'])
    maintenance = False
    await app.send_message(msg.message.chat.id, translation['maintenance_mode_disabled'])

    

@bot.on_callback_query(filters.regex("enable_maintenance"))
async def work_maintenance(app, msg):
    global maintenance
    user_id = str(msg.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    translation = translations.get(language, translations['ar'])
    
    if maintenance == True: 
        return await app.send_message(msg.message.chat.id, translation['maintenance_mode_already_enabled'])
    maintenance = True
    await app.send_message(msg.message.chat.id, translation['maintenance_mode_enabled'])

   



user_country_code = {}
user_requested_quantity = {}  # لتخزين الكمية المطلوبة لكل مستخدم

def create_number_json(number, device_data, string_session):
    """إنشاء ملف JSON للرقم بنفس التنسيق المطلوب"""
    # استخراج معلومات من device_data
    api_id = device_data.get('API_ID', 2040)
    api_hash = device_data.get('API_HASH', 'b18441a1ff607e10a989891a5462e627')
    device_name = device_data.get('name', 'MX8734')
    device_system = device_data.get('system', 'Windows 11')
    device_app = device_data.get('app', '6.3.4 x64')
    
    # الحصول على twofa_password - التحقق من وجوده وقيمته
    twofa_password = device_data.get('twofa_password') or device_data.get('2fa_password')
    if twofa_password and twofa_password.strip():
        twofa_value = twofa_password
    else:
        twofa_value = None
    
    # الحصول على معلومات إضافية من device_data إذا كانت موجودة
    user_info = device_data.get('user_info', {})
    first_name = user_info.get('first_name') if user_info else None
    last_name = user_info.get('last_name') if user_info else None
    username = user_info.get('username') if user_info else None
    user_id = user_info.get('id') if user_info else None
    
    # إنشاء ملف JSON
    json_data = {
        "session_file": number.replace('+', ''),
        "phone": number.replace('+', ''),
        "api_id": api_id,
        "api_hash": api_hash,
        "sdk": device_system,
        "system_version": device_system,
        "app_version": device_app,
        "device": device_name,
        "device_model": device_name,
        "lang_pack": "tdesktop",
        "system_lang_pack": "en-US",
        "username": username,
        "ipv6": False,
        "first_name": first_name,
        "last_name": last_name,
        "register_time": int(time.time()),
        "sex": None,
        "last_check_time": int(time.time()),
        "lang_code": "en",
        "avatar": "img/default.png",
        "proxy": None,
        "twoFA": twofa_value,
        "password": twofa_value,
        "block": False,
        "system_lang_code": "en-US",
        "id": user_id,
        "string_session": string_session if string_session else None
    }
    
    return json_data

@bot.on_callback_query(filters.regex("send_country_numbers"))
async def send_country_numbers(app, query):
    user_id = str(query.from_user.id)
    language = users_db[user_id]['language']
    
    # طلب الدولة أولاً
    await query.message.reply("أرسل اسم الدولة أو رمز الدولة:")
    
    try:
        country_msg = await app.listen(query.message.chat.id, timeout=300)
        country_input = country_msg.text.strip()
        
        # البحث عن الدولة في countries_db
        country_code = None
        country_name = None
        for name, data in countries_db.items():
            if name.lower() == country_input.lower() or data.get('code', '') == country_input:
                country_code = data.get('code', '')
                country_name = name
                break
        
        if not country_code:
            await query.message.reply("❌ لم يتم العثور على الدولة. أعد المحاولة.")
            return
        
        # طلب الكمية
        await query.message.reply(f"أرسل الكمية المطلوبة للأرقام من {country_name}:")
        quantity_msg = await app.listen(query.message.chat.id, timeout=300)
        
        try:
            quantity = int(quantity_msg.text.strip())
            if quantity <= 0:
                await query.message.reply("❌ الكمية يجب أن تكون أكبر من 0.")
                return
        except ValueError:
            await query.message.reply("❌ الكمية غير صحيحة. يجب أن تكون رقماً.")
            return
        
        # ✅ البحث عن الأرقام المؤكدة - نبدأ بملفات .session (أسرع)
        confirmed_numbers = []
        added_numbers = set()  # ✅ لتتبع الأرقام التي تم إضافتها بالفعل (تجنب التكرار)
        
        # ✅ البحث عن ملفات .session أولاً (أسرع)
        session_files = []
        for filename in os.listdir("numbers"):
            if filename.endswith(".session"):
                number = filename.replace(".session", "")
                if number.startswith(country_code):
                    # ✅ التحقق من أن الرقم ليس في وضع التأكيد
                    if number in pending_session_deletions:
                        continue  # تخطي الأرقام التي في وضع التأكيد
                    session_files.append({
                        'number': number,
                        'filename': filename,
                        'source': 'session_file'
                    })
        
        print(f"[Send Numbers] Found {len(session_files)} session files for country {country_code}")
        
        # ✅ معالجة ملفات .session أولاً (أسرع)
        if session_files:
            
            # استخدام ملفات .session
            print(f"[Send Numbers] Processing {len(session_files)} session files...")
            for idx, session_info in enumerate(session_files, 1):
                number = session_info['number']
                filename = session_info['filename']
                
                # ✅ التحقق من أن الرقم ليس في وضع التأكيد (pending_session_deletions)
                # إذا كانت الجلسة في فترة التأكيد، لا نرسلها
                if number in pending_session_deletions:
                    print(f"[Send Numbers] Skipping {number} - still pending verification (in pending_session_deletions)")
                    continue  # تخطي الأرقام التي في وضع التأكيد
                
                # ✅ السماح بإرسال ملفات .session المؤكدة حتى لو كانت في delivered_numbers
                # (يمكن إعادة إرسال الجلسات المؤكدة من ملفات .session)
                
                print(f"[Send Numbers] Processing file {idx}/{len(session_files)}: {filename}")
                
                # البحث عن device_data في users_db إذا كانت موجودة
                device_data = None
                user_id_found = None
                for uid, user_data in users_db.items():
                    if 'devices' in user_data and number in user_data['devices']:
                        device_data = user_data['devices'][number]
                        user_id_found = uid
                        break
                
                # إذا لم توجد device_data، استخدام بيانات افتراضية
                if not device_data:
                    device_data = {
                        'API_ID': 2040,
                        'API_HASH': 'b18441a1ff607e10a989891a5462e627',
                        'name': 'MX8734',
                        'system': 'Windows 11',
                        'app': '6.3.4 x64'
                    }
                
                # قراءة string_session من ملف .session
                session_filepath = os.path.join("numbers", filename)
                string_session = None
                try:
                    # محاولة قراءة الملف كنص أولاً (إذا كان StringSession)
                    try:
                        with open(session_filepath, 'r', encoding='utf-8') as f:
                            string_session = f.read().strip()
                        # التحقق من أن المحتوى يبدو كـ StringSession (يبدأ بـ 1)
                        if string_session and len(string_session) > 10 and string_session[0] == '1':
                            print(f"[Send Numbers] Read StringSession from {filename}, length: {len(string_session)}")
                        else:
                            # إذا لم يكن StringSession، نجرب قراءته كملف SQLite
                            string_session = None
                            raise ValueError("Not a StringSession file")
                    except (UnicodeDecodeError, ValueError):
                        # إذا فشلت القراءة كنص، نجرب كملف SQLite من Telethon
                        print(f"[Send Numbers] File {filename} is not text, trying as SQLite session file...")
                        api_id = device_data.get('API_ID', 2040)
                        api_hash = device_data.get('API_HASH', 'b18441a1ff607e10a989891a5462e627')
                        device_name = device_data.get('name', 'MX8734')
                        device_system = device_data.get('system', 'Windows 11')
                        device_app = device_data.get('app', '6.3.4 x64')
                        
                        # إنشاء client مؤقت من ملف .session
                        # TelegramClient يحتاج إلى مسار بدون .session
                        session_path_without_ext = session_filepath.replace('.session', '')
                        proxy = get_proxy_for_number(number)
                        temp_client = TelegramClient(
                            session_path_without_ext,
                            api_id,
                            api_hash,
                            device_model=device_name,
                            system_version=device_system,
                            app_version=device_app,
                            proxy=proxy
                        )
                        # إضافة timeout للاتصال
                        await asyncio.wait_for(temp_client.connect(), timeout=10.0)
                        if await temp_client.is_user_authorized():
                            # تحويل إلى StringSession
                            string_session = StringSession.save(temp_client.session)
                            print(f"[Send Numbers] Converted SQLite session file {filename} to string_session, length: {len(string_session)}")
                        await temp_client.disconnect()
                except asyncio.TimeoutError:
                    print(f"[Send Numbers] Timeout connecting to {filename}, skipping")
                    continue
                except Exception as e:
                    print(f"[Send Numbers] Error reading/converting session file {filename}: {e}")
                    continue
                
                if string_session and len(string_session) > 0:
                    # ✅ التحقق من أن الرقم لم يتم إضافته من قبل (تجنب التكرار)
                    if number in added_numbers:
                        print(f"[Send Numbers] Skipping {number} - already added to confirmed_numbers")
                        continue
                    
                    device_data['string_session'] = string_session
                    confirmed_numbers.append({
                        'number': number,
                        'device_data': device_data,
                        'user_id': user_id_found,
                        'source': 'session_file',
                        'session_filepath': session_filepath
                    })
                    added_numbers.add(number)  # ✅ إضافة الرقم إلى المجموعة
                    print(f"[Send Numbers] Added number {number} to confirmed_numbers. Total: {len(confirmed_numbers)}")
                    
                    # ✅ إذا وصلنا للعدد المطلوب، نتوقف (تسريع العملية)
                    if len(confirmed_numbers) >= quantity:
                        print(f"[Send Numbers] Reached requested quantity ({quantity}), stopping search")
                        break
                else:
                    print(f"[Send Numbers] Skipping {number} - empty or invalid string_session")
        
        # ✅ إذا لم نصل للعدد المطلوب، نبحث في users_db
        if len(confirmed_numbers) < quantity:
            print(f"[Send Numbers] Only found {len(confirmed_numbers)} sessions, searching in users_db...")
            for uid, user_data in users_db.items():
                if 'numbers' in user_data:
                    for num in user_data['numbers']:
                        # ✅ إذا وصلنا للعدد المطلوب، نتوقف
                        if len(confirmed_numbers) >= quantity:
                            break
                        
                        # ✅ التحقق من أن الرقم لم يتم إضافته من قبل
                        if num in added_numbers:
                            continue
                        
                        # ✅ التحقق من أن الرقم ليس في وضع التأكيد
                        if num in pending_session_deletions:
                            continue
                        
                        # التحقق من أن الرقم يبدأ برمز الدولة
                        if num.startswith(country_code):
                            if 'devices' in user_data and num in user_data['devices']:
                                device_data = user_data['devices'][num]
                                if 'string_session' in device_data and device_data['string_session']:
                                    confirmed_numbers.append({
                                        'number': num,
                                        'device_data': device_data,
                                        'user_id': uid,
                                        'source': 'confirmed'
                                    })
                                    added_numbers.add(num)
                                    print(f"[Send Numbers] Added confirmed number: {num}")
        
        if not confirmed_numbers:
            await query.message.reply(f"❌ لا توجد أرقام متوفرة للدولة {country_name}.")
            return
        
        # تحديد الكمية المطلوبة (لا تتجاوز المتوفرة)
        print(f"[Send Numbers] Requested quantity: {quantity}, Available: {len(confirmed_numbers)}")
        quantity = min(quantity, len(confirmed_numbers))
        selected_numbers = confirmed_numbers[:quantity]
        print(f"[Send Numbers] Selected {len(selected_numbers)} numbers for zip file")
        
        # إنشاء ملف zip للجلسات الصالحة
        zip_filename = f"{country_code}_{quantity}_numbers.zip"
        zip_filepath = os.path.join("numbers", zip_filename)
        
        # ✅ إنشاء ملف zip منفصل للجلسات التي لا تعمل
        invalid_zip_filename = f"{country_code}_invalid_sessions.zip"
        invalid_zip_filepath = os.path.join("numbers", invalid_zip_filename)
        
        # قوائم لتتبع الجلسات الصالحة وغير الصالحة
        valid_sessions = []
        invalid_sessions = []
        
        with zipfile.ZipFile(zip_filepath, 'w') as zipf, zipfile.ZipFile(invalid_zip_filepath, 'w') as invalid_zipf:
            processed_count = 0
            for num_info in selected_numbers:
                number = num_info['number']
                device_data = num_info['device_data']
                uid = num_info['user_id']
                
                print(f"[Send Numbers] Processing number {processed_count + 1}/{len(selected_numbers)}: {number}")
                
                # ✅ التحقق من أن الرقم ليس في وضع التأكيد (pending_session_deletions)
                if number in pending_session_deletions:
                    print(f"[Send Numbers] Skipping {number} - still pending verification (in pending_session_deletions)")
                    processed_count += 1
                    continue  # تخطي الأرقام التي في وضع التأكيد
                
                # ✅ البحث عن ملف .session في مجلد numbers
                session_filename = f"{number}.session"
                original_session_filepath = os.path.join("numbers", session_filename)
                
                # ✅ إذا كان source هو 'session_file'، استخدم المسار المحفوظ
                if num_info.get('source') == 'session_file' and 'session_filepath' in num_info:
                    original_session_filepath = num_info['session_filepath']
                
                # ✅ التحقق من وجود ملف .session الأصلي
                if not os.path.exists(original_session_filepath):
                    print(f"[Send Numbers] Warning: Session file not found for {number}: {original_session_filepath}")
                    # ✅ إضافة إلى قائمة الجلسات غير الصالحة
                    invalid_sessions.append(number)
                    processed_count += 1
                    continue
                
                # ✅ فحص الجلسة عن طريق الاتصال فقط
                session_valid = False
                string_session = device_data.get('string_session')
                
                if string_session:
                    try:
                        api_id = device_data.get('API_ID', 2040)
                        api_hash = device_data.get('API_HASH', 'b18441a1ff607e10a989891a5462e627')
                        device_name = device_data.get('name', 'MX8734')
                        device_system = device_data.get('system', 'Windows 11')
                        device_app = device_data.get('app', '6.3.4 x64')
                        
                        proxy = get_proxy_for_number(number)
                        
                        # ✅ فحص الجلسة عن طريق الاتصال فقط
                        temp_client = TelegramClient(
                            StringSession(string_session),
                            api_id,
                            api_hash,
                            device_model=device_name,
                            system_version=device_system,
                            app_version=device_app,
                            lang_code='en',
                            system_lang_code='en-US',
                            proxy=proxy,
                            connection_retries=0,
                            auto_reconnect=False
                        )
                        
                        # ✅ محاولة الاتصال فقط (لا نحتاج get_me)
                        await asyncio.wait_for(temp_client.connect(), timeout=10.0)
                        session_valid = True  # ✅ إذا اتصل بنجاح، الجلسة تعمل
                        await temp_client.disconnect()
                        print(f"[Send Numbers] ✅ Session valid for {number} (connection successful)")
                    
                    except asyncio.TimeoutError:
                        print(f"[Send Numbers] ❌ Timeout connecting to {number} - session invalid")
                        session_valid = False
                    except Exception as e:
                        print(f"[Send Numbers] ❌ Error connecting to {number}: {e} - session invalid")
                        session_valid = False
                else:
                    print(f"[Send Numbers] ❌ No string_session for {number} - session invalid")
                    session_valid = False
                
                # ✅ إذا كانت الجلسة غير صالحة، إضافتها إلى ملف منفصل
                if not session_valid:
                    print(f"[Send Numbers] Adding invalid session {number} to separate file")
                    invalid_sessions.append(number)
                    # ✅ نسخ ملف .session الأصلي إلى ملف ZIP للجلسات غير الصالحة
                    if os.path.exists(original_session_filepath):
                        invalid_zipf.write(original_session_filepath, session_filename)
                        print(f"[Send Numbers] Copied invalid session file for {number}")
                    processed_count += 1
                    continue
                
                # ✅ إذا كانت الجلسة صالحة، نسخ ملف .session الأصلي إلى zip الصالح
                if os.path.exists(original_session_filepath):
                    zipf.write(original_session_filepath, session_filename)
                    file_size = os.path.getsize(original_session_filepath)
                    print(f"[Send Numbers] Copied valid session file for {number} ({file_size} bytes)")
                
                # استخدام الكلمة الثابتة (m) إذا كان الرقم مؤكداً
                is_confirmed = number in users_db.get(uid, {}).get('numbers', [])
                if is_confirmed:
                    device_data_for_json = device_data.copy()
                    device_data_for_json['twofa_password'] = m
                else:
                    device_data_for_json = device_data
                
                # ✅ جلب معلومات المستخدم (اختياري)
                user_info = {}
                if session_valid and string_session:
                    try:
                        api_id = device_data.get('API_ID', 2040)
                        api_hash = device_data.get('API_HASH', 'b18441a1ff607e10a989891a5462e627')
                        device_name = device_data.get('name', 'MX8734')
                        device_system = device_data.get('system', 'Windows 11')
                        device_app = device_data.get('app', '6.3.4 x64')
                        proxy = get_proxy_for_number(number)
                        async with TelegramClient(
                            StringSession(string_session),
                            api_id, api_hash,
                            device_model=device_name,
                            system_version=device_system,
                            app_version=device_app,
                            lang_code='en',
                            system_lang_code='en-US',
                            proxy=proxy,
                            connection_retries=0,
                            auto_reconnect=False
                        ) as temp_client:
                            await asyncio.wait_for(temp_client.connect(), timeout=10.0)
                            if await temp_client.is_user_authorized():
                                try:
                                    me = await asyncio.wait_for(temp_client.get_me(), timeout=5.0)
                                    user_info = {
                                        'first_name': getattr(me, 'first_name', None),
                                        'last_name': getattr(me, 'last_name', None),
                                        'username': getattr(me, 'username', None),
                                        'id': getattr(me, 'id', None)
                                    }
                                except:
                                    pass
                    except:
                        pass
                
                if user_info:
                    device_data_for_json['user_info'] = user_info
                
                # إنشاء ملف JSON
                json_data = create_number_json(number, device_data_for_json, string_session)
                json_filename = f"{number}.json"
                json_filepath = os.path.join("numbers", json_filename)
                with open(json_filepath, 'w', encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, ensure_ascii=False, indent=4)
                
                zipf.write(json_filepath, json_filename)
                os.remove(json_filepath)
                
                valid_sessions.append(number)
                if number not in delivered_numbers:
                    delivered_numbers.append(number)
                    save_delivered_numbers()
                
                processed_count += 1
                print(f"[Send Numbers] Successfully processed {number} ({processed_count}/{len(selected_numbers)})")
                
                # حذف الرقم من users_db أو من ملف .session بعد الجلب
                if num_info.get('source') == 'confirmed' and uid:
                    # حذف من users_db
                    if uid in users_db and 'numbers' in users_db[uid]:
                        if number in users_db[uid]['numbers']:
                            users_db[uid]['numbers'].remove(number)
                    if uid in users_db and 'devices' in users_db[uid]:
                        if number in users_db[uid]['devices']:
                            del users_db[uid]['devices'][number]
                    save_db()
                elif num_info.get('source') == 'session_file':
                    # حذف ملف .session
                    session_filepath = num_info.get('session_filepath')
                    if session_filepath and os.path.exists(session_filepath):
                        os.remove(session_filepath)
        
        # ✅ إرسال ملف zip للجلسات الصالحة
        actual_sent = len(valid_sessions)
        print(f"[Send Numbers] Sending zip file with {actual_sent} valid numbers")
        try:
            if actual_sent > 0:
                await app.send_document(query.message.chat.id, zip_filepath)
                print(f"[Send Numbers] Successfully sent zip file with {actual_sent} valid numbers")
            else:
                await query.message.reply(f"❌ لا توجد جلسات صالحة لإرسالها.")
        except Exception as e:
            print(f"[Send Numbers] Error sending zip file: {e}")
            await query.message.reply(f"❌ حدث خطأ أثناء إرسال الملف: {str(e)}")
            # حذف ملف zip في حالة الخطأ
            if os.path.exists(zip_filepath):
                os.remove(zip_filepath)
            return
        
        # ✅ إرسال ملف zip منفصل للجلسات غير الصالحة (إذا كانت موجودة)
        if len(invalid_sessions) > 0:
            try:
                # ✅ الحصول على معلومات المستخدم لإرسالها مع الملف
                user_info_for_message = await app.get_users(int(user_id))
                username = user_info_for_message.username if hasattr(user_info_for_message, 'username') else "N/A"
                user_name = user_info_for_message.first_name if hasattr(user_info_for_message, 'first_name') else "N/A"
                
                # ✅ إرسال ملف ZIP للجلسات غير الصالحة مع معلومات المستخدم
                invalid_count = len(invalid_sessions)
                message_text = (
                    f"📁 **اسم الملف:** `{invalid_zip_filename}`\n"
                    f"👤 **المستخدم:** {user_name} (@{username})\n"
                    f"🆔 **معرف المستخدم:** `{user_id}`\n"
                    f"❌ **عدد الجلسات التي لا تعمل:** {invalid_count}\n"
                    f"📋 **الأرقام:** {', '.join(invalid_sessions[:10])}{'...' if len(invalid_sessions) > 10 else ''}"
                )
                
                await app.send_document(
                    query.message.chat.id,
                    invalid_zip_filepath,
                    caption=message_text
                )
                print(f"[Send Numbers] Successfully sent invalid sessions file with {invalid_count} numbers")
            except Exception as e:
                print(f"[Send Numbers] Error sending invalid sessions file: {e}")
                await query.message.reply(f"❌ حدث خطأ أثناء إرسال ملف الجلسات غير الصالحة: {str(e)}")
        
        # ✅ حذف ملفات zip بعد الإرسال
        if os.path.exists(zip_filepath):
            os.remove(zip_filepath)
        if os.path.exists(invalid_zip_filepath):
            os.remove(invalid_zip_filepath)
        
        # حفظ معلومات الطلب
        user_country_code[user_id] = country_code
        user_requested_quantity[user_id] = quantity
        
        # حذف ملف zip
        if os.path.exists(zip_filepath):
            os.remove(zip_filepath)
        
        await query.message.reply(f"✅ تم إرسال {actual_sent} رقم من {country_name}.\nتم حذف الملفات من المجلد تلقائياً.")
        
        # حذف ملف zip
        if os.path.exists(zip_filepath):
            os.remove(zip_filepath)
    
    except asyncio.TimeoutError:
        await query.message.reply(translations[language]['operation_cancelled'])

@bot.on_callback_query(filters.regex("delete_fetched_files"))
async def delete_fetched_files(app, query):
    user_id = str(query.from_user.id)
    language = users_db[user_id]['language']
    
    # تم حذف الملفات تلقائياً عند الإرسال، لذا هذه الدالة لم تعد ضرورية
    await query.message.reply("✅ تم حذف الملفات تلقائياً عند الإرسال.")
    
    # تنظيف المتغيرات
    user_country_code.pop(user_id, None)
    user_requested_quantity.pop(user_id, None)




    
@bot.on_callback_query(filters.regex("change_language"))
async def change_language_callback(app, query):
    user_id = str(query.from_user.id)
    language = users_db[user_id]['language']
    
    translated_text = translations[language]['select_language']
    
  
    await query.message.edit_text(
        text=translated_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🇮🇷 فارسی", callback_data="set_language_fa"),
                    InlineKeyboardButton("🇷🇺 Russia", callback_data="set_language_ru")
                ],
                [
                    InlineKeyboardButton("🇬🇧 English", callback_data="set_language_en"),
                    InlineKeyboardButton("🇪🇬 Arabic", callback_data="set_language_ar")
                ]
            ]
        )
    )



@bot.on_callback_query(filters.regex("add_balance"))
async def add_balance(app, query):
    user_id = str(query.from_user.id)
    language = users_db[user_id]['language']
    
    await query.message.reply(translations[language]['send_number'])
    
    try:
       
        user_id_msg = await app.listen(query.message.chat.id, timeout=300)
        target_user_id = user_id_msg.text.strip()
        
        if target_user_id not in users_db:
            await query.message.reply(translations[language]['invalid_number'])
            return
        
        await app.send_message(query.message.chat.id, translations[language]['enter_balance_to_add'])
        balance_msg = await app.listen(query.message.chat.id, timeout=300)
        
        try:
            balance_to_add = float(balance_msg.text.strip())
        except ValueError:
            await app.send_message(query.message.chat.id, translations[language]['invalid_amount'])
            return
        
        users_db[target_user_id]['balance'] += balance_to_add
        save_db()
        
        
        await app.send_message(query.message.chat.id, translations[language]['balance_added_success'].format(amount=balance_to_add, user_id=target_user_id))
        
        target_language = users_db[target_user_id].get('language', 'en')
        target_translation = translations.get(target_language, translations['en'])
        await app.send_message(target_user_id, f"{target_translation['balance']} +{balance_to_add}$ {target_translation['balance_added_by_owner']}")
    
    except TimeoutError:
        await query.message.reply(translations[language]['operaion_canelled'])
# تم دمج الدالة أعلاه


@bot.on_callback_query(filters.regex("deduct_balance"))
async def deduct_balance(app, query):
    user_id = str(query.from_user.id)
    language = users_db[user_id]['language']
    
    await query.message.reply(translations[language]['send_number'])
    
    try:
        
        user_id_msg = await app.listen(query.message.chat.id, timeout=300)
        target_user_id = user_id_msg.text.strip()
        
        if target_user_id not in users_db:
            await query.message.reply(translations[language]['invalid_number'])
            return
        
        await app.send_message(query.message.chat.id, translations[language]['enter_balance_to_deduct'])
        balance_msg = await app.listen(query.message.chat.id, timeout=300)
        
        try:
            balance_to_deduct = float(balance_msg.text.strip())
        except ValueError:
            await app.send_message(query.message.chat.id, translations[language]['invalid_amount'])
            return
        
        users_db[target_user_id]['balance'] -= balance_to_deduct
        save_db()
        
        
        await app.send_message(query.message.chat.id, translations[language]['balance_deducted_success'].format(amount=balance_to_deduct, user_id=target_user_id))
        
        
        target_language = users_db[target_user_id].get('language', 'en')
        target_translation = translations.get(target_language, translations['en'])
        await app.send_message(target_user_id, f"{target_translation['balance']} -{balance_to_deduct}$ {target_translation['balance_added_by_owner']}")
    
    except TimeoutError:
        await query.message.reply(translations[language]['operaion_canelled'])

    
    
    
    
    
    
# تم تعريف load_db و save_db في الأعلى

def ban_user(user_id):
    user_id = str(user_id)
    if "banned_users" not in users_db:
        users_db["banned_users"] = []
    if user_id not in users_db["banned_users"]:
        users_db["banned_users"].append(user_id)
        save_db()
        return True  
    return False  

def is_banned(user_id):
    user_id = str(user_id)
    return "banned_users" in users_db and user_id in users_db["banned_users"]

def unban_user(user_id):
    user_id = str(user_id)
    if "banned_users" in users_db and user_id in users_db["banned_users"]:
        users_db["banned_users"].remove(user_id)
        save_db()
        return True
    return False

@bot.on_callback_query(filters.regex("ban_user"))
async def handle_ban_user(app, callback_query):
    user_id = str(callback_query.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    translation = translations.get(language, translations['ar'])
    
    if callback_query.from_user.id != sudo:
        await callback_query.answer(translation['no_permission'], show_alert=True)
        return
        
    await callback_query.message.reply(translation['send_user_id_ban'])
    
    try:
        user_id_msg = await app.listen(callback_query.message.chat.id, timeout=300)
        target_user_id = user_id_msg.text.strip()
        if ban_user(target_user_id):
            await app.send_message(callback_query.message.chat.id, translation['user_banned_success'].format(user_id=target_user_id))
        else:
            await app.send_message(callback_query.message.chat.id, translation['user_already_banned'].format(user_id=target_user_id))
    except asyncio.TimeoutError:
        await app.send_message(callback_query.message.chat.id, translation.get('timeout_error', 'انتهت المهلة.'))


@bot.on_callback_query(filters.regex("delete_country"))
async def delete_country(app, query):
    user_id = str(query.from_user.id)
    language = users_db[user_id]['language']

    
    if query.from_user.id != sudo:
        await query.answer(translations[language]['country_not_supported'], show_alert=True)
        return

   
    if not countries_db:
        await query.message.edit_text(translations[language]['no_countries'])
        return

  
    buttons = []
    for country_name in countries_db.keys():
        buttons.append([InlineKeyboardButton(country_name, callback_data=f"confirm_delete_{country_name}")])

    
    await query.message.edit_text(translations[language]['choose_country_to_delete'], reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex(r"confirm_delete_(.+)"))
async def confirm_delete(app, query):
    country_name = query.data.split("_", 2)[2]
    language = users_db[str(query.from_user.id)]['language']

   
    buttons = [
        [InlineKeyboardButton(translations[language]['yes'], callback_data=f"delete_confirmed_{country_name}")],
        [InlineKeyboardButton(translations[language]['no'], callback_data="cancel_delete")]
    ]
    await query.message.edit_text(translations[language]['confirm_delete'].format(country_name=country_name), reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex(r"delete_confirmed_(.+)"))
async def delete_confirmed(app, query):
    country_name = query.data.split("_", 2)[2]
    language = users_db[str(query.from_user.id)]['language']

    
    if country_name in countries_db:
        del countries_db[country_name]
        with open('countries_db.json', 'w') as f:
            json.dump(countries_db, f)

    await query.message.edit_text(translations[language]['country_deleted'].format(country_name=country_name))

@bot.on_callback_query(filters.regex("cancel_delete"))
async def cancel_delete(app, query):
    language = users_db[str(query.from_user.id)]['language']
    await query.message.edit_text(translations[language]['delete_cancelled'])

    
    
    
@bot.on_callback_query(filters.regex("view_pending_numbers"))
async def view_pending_numbers(app, query):
    user_id = str(query.from_user.id)
    language = users_db[user_id]['language']
    
    pending_numbers = []
    for country_name, country_data in countries_db.items():
        for number in country_data.get('registered_numbers', []):
            if number['user_id'] == user_id:
                remaining_time = country_data['seconds'] - (time.time() - number['timestamp'])
                pending_numbers.append(f"{number['number']} - {remaining_time} seconds remaining")

    if pending_numbers:
        await query.message.edit_text("\n".join(pending_numbers))
    else:
        await query.message.edit_text(translations[language]['no_pending_numbers'])





@bot.on_message(filters.command("cancel") & filters.private)
async def cancel_command(app, message):
    """معالجة أمر /cancel في أي وقت"""
    user_language = users_db.get(str(message.from_user.id), {}).get('language', 'ar')
    translation = translations.get(user_language, translations['ar'])
    
    await app.send_message(
        message.chat.id,
        f"✅ {translation.get('operation_cancelled', 'تم إلغاء العملية!')}\n\n{translation.get('continue_help', 'للمتابعة، أرسل رقم الحساب الافتراضي أو أرسل /help للحصول على الإرشادات.')}",
        reply_markup=ReplyKeyboardRemove()
    )

@bot.on_message(filters.command("start") & filters.private)
async def start_bot(app, msg):
    user_id = str(msg.from_user.id)
    
    if is_banned(user_id):
        return  
    users_numbers = []
        

    if user_id not in users_db:
        users_db[user_id] = {
            "language": users_db.get(user_id, {}).get('language', 'ar'),
            "balance": users_db.get(user_id, {}).get('balance', 0),
            "numbers": users_numbers,
            "countries_registered": users_db.get(user_id, {}).get('countries_registered', {})
        }

        save_db()
        await msg.reply(translations['en']['select_language'], reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🇮🇷 فارسی", callback_data="set_language_fa"),
                    InlineKeyboardButton("🇷🇺 Russia", callback_data="set_language_ru")
                ],
                [
                    InlineKeyboardButton("🇬🇧 English", callback_data="set_language_en"),
                    InlineKeyboardButton("🇪🇬 Arabic", callback_data="set_language_ar")
                ]
            ]
        ))
    else:
        language = users_db[user_id].get('language', 'en')
        is_sudo = msg.from_user.id == sudo
        balance = users_db[user_id].get('balance', 0.0)
        
        # التحقق إذا كان المستخدم قائد
        is_leader = False
        leader_id = None
        for lid, leader_data in leaders_db.items():
            # التحقق من user_id أو username
            if lid == user_id or (msg.from_user.username and lid == f"@{msg.from_user.username}"):
                is_leader = True
                leader_id = lid
                break
        
        key_not = create_keyboards(bot, msg, language, is_sudo)
        
        welcome_message = f"{translations[language]['welcome']} :( {msg.from_user.mention} )\n{translations[language]['balance']}: {balance} $\n /help"  
        
        # إذا كان قائد، إضافة الإحصائيات
        if is_leader and leader_id:
            leader_data = leaders_db[leader_id]
            stats = leader_data.get('stats', {
                'withdrawals_count': 0,
                'total_withdrawn': 0.0,
                'total_commission': 0.0,
                'numbers_count': 0
            })
            
            stats_text = f"""
{translations[language]['leader_stats_your_title']}

{translations[language]['leader_withdrawals_count'].format(count=stats.get('withdrawals_count', 0))}
{translations[language]['leader_total_withdrawn'].format(amount=stats.get('total_withdrawn', 0.0))}
{translations[language]['leader_total_commission'].format(amount=stats.get('total_commission', 0.0))}
{translations[language]['leader_numbers_count'].format(count=stats.get('numbers_count', 0))}
"""
            welcome_message += stats_text
        
        await msg.reply(welcome_message, reply_markup=key_not)





@bot.on_callback_query(filters.regex(r"set_language_(ar|en|fa|ru)"))
async def set_language(app, query):
    user_id = str(query.from_user.id)
    language_code = query.data.split("_")[2]
    
    users_db[user_id]['language'] = language_code
    save_db()
   
    is_sudo = query.from_user.id == sudo
    
    key_not = create_keyboards(bot, query.message, language_code, is_sudo)
  
    await query.message.edit_text(translations[language_code]['language_set'])



@bot.on_callback_query(filters.regex("add_country"))
async def add_country(app, query):
    user_id = str(query.from_user.id)
    language = users_db[user_id]['language']
    global m, m2, data

    if query.from_user.id != sudo:
        await query.answer(translations[language]['country_not_supported'], show_alert=True)
        return

    await query.message.delete()
    await query.message.reply(translations[language]['enter_country_name'])

    try:
        
        country_name_msg = await app.listen(query.message.chat.id, timeout=300)
        country_name = country_name_msg.text

        
        await app.send_message(query.message.chat.id, translations[language]['enter_country_code'])
        country_code_msg = await app.listen(query.message.chat.id, timeout=300)
        country_code = country_code_msg.text

        
        await app.send_message(query.message.chat.id, translations[language]['enter_country_price'])
        country_price_msg = await app.listen(query.message.chat.id, timeout=300)
        try:
            country_price = float(country_price_msg.text)
        except ValueError:
            await app.send_message(query.message.chat.id, translations[language]['invalid_price'])
            return

        
        await app.send_message(query.message.chat.id, translations[language]['enter_time_format'])
        time_msg = await app.listen(query.message.chat.id, timeout=300)
        
        try:
            time_pattern = re.compile(r"(\d+)\s*\n(\d+)\s*\n(\d+)")
            match = time_pattern.search(time_msg.text)
            
            if match:
                hours = int(match.group(1))
                minutes = int(match.group(2))
                seconds = int(match.group(3))
                total_seconds = (hours * 3600) + (minutes * 60) + seconds
            else:
                await app.send_message(query.message.chat.id, translations[language]['invalid_format'])
                return
            
        except ValueError:
            await app.send_message(query.message.chat.id, translations[language]['invalid_input'])
            return
        
        
        await app.send_message(query.message.chat.id, translations[language]['enter_max_numbers'])
        max_numbers_msg = await app.listen(query.message.chat.id, timeout=300)
        
        try:
            max_numbers = int(max_numbers_msg.text)
        except ValueError:
            await app.send_message(query.message.chat.id, translations[language]['invalid_input'])
            return
        
        # ✅ سؤال عن فحص الاسبام
        await app.send_message(query.message.chat.id, translations[language]['enable_spam_check'])
        spam_check_msg = await app.listen(query.message.chat.id, timeout=300)
        spam_check = spam_check_msg.text.strip().lower()
        # ✅ دعم جميع اللغات الأربع
        yes_responses = ['نعم', 'yes', 'y', '1', 'true', 'да', 'بله', 'بلی']
        spam_check_enabled = spam_check in yes_responses
        
        countries_db[country_name] = {
            'code': country_code,
            'price': country_price,
            'seconds': total_seconds,
            'max_numbers': max_numbers,
            'spam_check': spam_check_enabled,  # ✅ إضافة حقل فحص الاسبام
            'registered_numbers': []
        }
        save_countries_db()

        await app.send_message(query.message.chat.id, translations[language]['country_added'])
        
        # ✅ إرسال رسالة في قناة إعلان الدول بنفس الشكل المطلوب
        try:
            country_flag = get_country_flag(country_code)
            
            # ✅ الحصول على معلومات البوت لإنشاء رابط البوت
            bot_info = await app.get_me()
            bot_username = bot_info.username
            bot_link = f"https://t.me/{bot_username}" if bot_username else None
            
            # ✅ بناء الرسالة بنفس الشكل الموجود في الصورة (داخل Quote)
            # ✅ جعل أول حرف من اسم الدولة كبير
            country_name_capitalized = country_name.capitalize()
            
            # ✅ استخدام HTML مع blockquote لعمل Quote بشكل صحيح (مثل الصورة الثانية)
            announcement_message = (
                f"<blockquote>"
                f"{country_name_capitalized} [{country_flag} - {country_code} ] Open now.\n\n"
                f"[ ${country_price} | Quantity: +{max_numbers} ]\n\n"
                f"Confirmation Time: [ {total_seconds} ] seconds.\n\n"
                f"It will be updated here if the price changes."
                f"</blockquote>"
            )
            
            # ✅ إنشاء زر لتحويل المستخدم إلى البوت
            buttons = []
            if bot_link:
                buttons.append([InlineKeyboardButton("🔗 Start Bot", url=bot_link)])
            
            reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
            
            await app.send_message(
                COUNTRIES_ANNOUNCEMENT_CHANNEL, 
                announcement_message,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            print(f"[Add Country] Sent announcement to channel: {COUNTRIES_ANNOUNCEMENT_CHANNEL}")
        except Exception as e:
            print(f"[Add Country] Error sending announcement to channel: {e}")
    
    except asyncio.TimeoutError:
        await app.send_message(query.message.chat.id, translations[language]['timeout'])
             
        
        
        
@bot.on_message(filters.command("help") & filters.private)
async def yyy(app, message):
    user_id = str(message.from_user.id)
    language = users_db.get(user_id, {}).get('language', 'ar')
    translation = translations.get(language, translations['ar'])
    
    await app.send_message(
        chat_id=message.chat.id, 
        text=translation['help_message']
    )
    
    
def get_country_flag(country_code):
    """إرجاع علم الدولة بناءً على رمز الدولة"""
    flag_map = {
        # أمريكا الشمالية والكاريبـي (+1)
        '+1242': '🇧🇸',  # جزر البهاما
        '+1246': '🇧🇧',  # بربادوس
        '+1264': '🇦🇮',  # أنغويلا
        '+1268': '🇦🇬',  # أنتيغوا وبربودا
        '+1284': '🇻🇬',  # جزر فرجن البريطانية
        '+1340': '🇻🇮',  # جزر فرجن الأمريكية
        '+1345': '🇰🇾',  # جزر كايمان
        '+1441': '🇧🇲',  # برمودا
        '+1473': '🇬🇩',  # غرينادا
        '+1649': '🇹🇨',  # جزر تركس وكايكوس
        '+1664': '🇲🇸',  # مونتسرات
        '+1670': '🇲🇵',  # جزر ماريانا الشمالية
        '+1671': '🇬🇺',  # غوام
        '+1684': '🇦🇸',  # ساموا الأمريكية
        '+1721': '🇸🇽',  # سينت مارتن
        '+1758': '🇱🇨',  # سانت لوسيا
        '+1767': '🇩🇲',  # دومينيكا
        '+1784': '🇻🇨',  # سانت فنسنت والغرينادين
        '+1809': '🇩🇴',  # جمهورية الدومينيكان
        '+1829': '🇩🇴',  # جمهورية الدومينيكان (بديل)
        '+1849': '🇩🇴',  # جمهورية الدومينيكان (بديل)
        '+1868': '🇹🇹',  # ترينيداد وتوباغو
        '+1869': '🇰🇳',  # سانت كيتس ونيفيس
        '+1876': '🇯🇲',  # جامايكا
        '+1939': '🇵🇷',  # بورتوريكو
        '+1': '🇺🇸',     # الولايات المتحدة (الأساسي)

        # كندا (يُفضل فصلها رغم أنها +1)
        '+1204': '🇨🇦',  # مانيتوبا
        '+1226': '🇨🇦',  # أونتاريو
        '+1236': '🇨🇦',  # كولومبيا البريطانية
        '+1249': '🇨🇦',  # أونتاريو
        '+1250': '🇨🇦',  # كولومبيا البريطانية
        '+1289': '🇨🇦',  # أونتاريو
        '+1306': '🇨🇦',  # ساسكاتشوان
        '+1343': '🇨🇦',  # أونتاريو
        '+1365': '🇨🇦',  # أونتاريو
        '+1403': '🇨🇦',  # ألبرتا
        '+1416': '🇨🇦',  # أونتاريو
        '+1418': '🇨🇦',  # كيبيك
        '+1431': '🇨🇦',  # مانيتوبا
        '+1437': '🇨🇦',  # أونتاريو
        '+1438': '🇨🇦',  # كيبيك
        '+1450': '🇨🇦',  # كيبيك
        '+1506': '🇨🇦',  # نيو برونزويك
        '+1514': '🇨🇦',  # كيبيك
        '+1519': '🇨🇦',  # أونتاريو
        '+1548': '🇨🇦',  # أونتاريو
        '+1579': '🇨🇦',  # كيبيك
        '+1581': '🇨🇦',  # كيبيك
        '+1587': '🇨🇦',  # ألبرتا
        '+1604': '🇨🇦',  # كولومبيا البريطانية
        '+1613': '🇨🇦',  # أونتاريو
        '+1639': '🇨🇦',  # ساسكاتشوان
        '+1647': '🇨🇦',  # أونتاريو
        '+1705': '🇨🇦',  # أونتاريو
        '+1709': '🇨🇦',  # نيوفاوندلاند ولابرادور
        '+1778': '🇨🇦',  # كولومبيا البريطانية
        '+1780': '🇨🇦',  # ألبرتا
        '+1782': '🇨🇦',  # نوفا سكوشا / جزيرة الأمير إدوارد
        '+1807': '🇨🇦',  # أونتاريو
        '+1819': '🇨🇦',  # كيبيك
        '+1825': '🇨🇦',  # ألبرتا
        '+1867': '🇨🇦',  # الأقاليم الشمالية
        '+1873': '🇨🇦',  # كيبيك
        '+1902': '🇨🇦',  # نوفا سكوشا / جزيرة الأمير إدوارد
        '+1905': '🇨🇦',  # أونتاريو

        # باقي دول العالم
        '+7': '🇷🇺',      # روسيا / كازاخستان (يُستخدم لكليهما، لكن غالبًا روسيا)
        '+76': '🇰🇿',     # كازاخستان (اختياري، لكن +7 مشترك)
        '+77': '🇰🇿',     # كازاخستان
        '+20': '🇪🇬',     # مصر
        '+27': '🇿🇦',     # جنوب أفريقيا
        '+30': '🇬🇷',     # اليونان
        '+31': '🇳🇱',     # هولندا
        '+32': '🇧🇪',     # بلجيكا
        '+33': '🇫🇷',     # فرنسا
        '+34': '🇪🇸',     # إسبانيا
        '+36': '🇭🇺',     # المجر
        '+39': '🇮🇹',     # إيطاليا
        '+40': '🇷🇴',     # رومانيا
        '+41': '🇨🇭',     # سويسرا
        '+43': '🇦🇹',     # النمسا
        '+44': '🇬🇧',     # المملكة المتحدة
        '+45': '🇩🇰',     # الدنمارك
        '+46': '🇸🇪',     # السويد
        '+47': '🇳🇴',     # النرويج
        '+48': '🇵🇱',     # بولندا
        '+49': '🇩🇪',     # ألمانيا
        '+51': '🇵🇪',     # بيرو
        '+52': '🇲🇽',     # المكسيك
        '+53': '🇨🇺',     # كوبا
        '+54': '🇦🇷',     # الأرجنتين
        '+55': '🇧🇷',     # البرازيل
        '+56': '🇨🇱',     # تشيلي
        '+57': '🇨🇴',     # كولومبيا
        '+58': '🇻🇪',     # فنزويلا
        '+591': '🇧🇴',    # بوليفيا
        '+592': '🇬🇾',    # غيانا
        '+593': '🇪🇨',    # الإكوادور
        '+594': '🇬🇫',    # غويانا الفرنسية
        '+595': '🇵🇾',    # باراغواي
        '+596': '🇲🇶',    # مارتينيك
        '+597': '🇸🇷',    # سورينام
        '+598': '🇺🇾',    # الأوروغواي
        '+599': '🇨🇼',    # كوراساو
        '+60': '🇲🇾',     # ماليزيا
        '+61': '🇦🇺',     # أستراليا
        '+62': '🇮🇩',     # إندونيسيا
        '+63': '🇵🇭',     # الفلبين
        '+64': '🇳🇿',     # نيوزيلندا
        '+65': '🇸🇬',     # سنغافورة
        '+66': '🇹🇭',     # تايلاند
        '+670': '🇹🇱',    # تيمور الشرقية
        '+672': '🇦🇶',    # القطب الجنوبي (أو جزر خارجية لأستراليا)
        '+673': '🇧🇳',    # بروناي
        '+674': '🇳🇷',    # ناورو
        '+675': '🇵🇬',    # بابوا غينيا الجديدة
        '+676': '🇹🇴',    # تونغا
        '+677': '🇸🇧',    # جزر سليمان
        '+678': '🇻🇺',    # فانواتو
        '+679': '🇫🇯',    # فيجي
        '+680': '🇵🇼',    # بالاو
        '+681': '🇼🇫',    # والس وفوتونا
        '+682': '🇨🇰',    # جزر كوك
        '+683': '🇳🇺',    # نيوي
        '+685': '🇼🇸',    # ساموا
        '+686': '🇰🇮',    # كيريباتي
        '+687': '🇳🇨',    # كاليدونيا الجديدة
        '+688': '🇹🇻',    # توفالو
        '+689': '🇵🇫',    # بولينيزيا الفرنسية
        '+690': '🇹🇰',    # توكيلاو
        '+691': '🇫🇲',    # ولايات ميكرونيسيا المتحدة
        '+692': '🇲🇭',    # جزر مارشال
        '+81': '🇯🇵',     # اليابان
        '+82': '🇰🇷',     # كوريا الجنوبية
        '+84': '🇻🇳',     # فيتنام
        '+850': '🇰🇵',    # كوريا الشمالية
        '+852': '🇭🇰',    # هونغ كونغ
        '+853': '🇲🇴',    # ماكاو
        '+855': '🇰🇭',    # كمبوديا
        '+856': '🇱🇦',    # لاوس
        '+880': '🇧🇩',    # بنغلاديش
        '+886': '🇹🇼',    # تايوان
        '+90': '🇹🇷',     # تركيا
        '+91': '🇮🇳',     # الهند
        '+92': '🇵🇰',     # باكستان
        '+93': '🇦🇫',     # أفغانستان
        '+94': '🇱🇰',     # سريلانكا
        '+95': '🇲🇲',     # ميانمار
        '+960': '🇲🇻',    # جزر المالديف
        '+961': '🇱🇧',    # لبنان
        '+962': '🇯🇴',    # الأردن
        '+963': '🇸🇾',    # سوريا
        '+964': '🇮🇶',    # العراق
        '+965': '🇰🇼',    # الكويت
        '+966': '🇸🇦',    # السعودية
        '+967': '🇾🇪',    # اليمن
        '+968': '🇴🇲',    # عُمان
        '+970': '🇵🇸',    # فلسطين
        '+971': '🇦🇪',    # الإمارات
        '+972': '🇮🇱',    # إسرائيل
        '+973': '🇧🇭',    # البحرين
        '+974': '🇶🇦',    # قطر
        '+975': '🇧🇹',    # بوتان
        '+976': '🇲🇳',    # منغوليا
        '+977': '🇳🇵',    # نيبال
        '+992': '🇹🇯',    # طاجيكستان
        '+993': '🇹🇲',    # تركمانستان
        '+994': '🇦🇿',    # أذربيجان
        '+995': '🇬🇪',    # جورجيا
        '+996': '🇰🇬',    # قيرغيزستان
        '+998': '🇺🇿',    # أوزبكستان

        # دول أوروبية وأفريقية إضافية
        '+212': '🇲🇦',    # المغرب
        '+213': '🇩🇿',    # الجزائر
        '+216': '🇹🇳',    # تونس
        '+218': '🇱🇾',    # ليبيا
        '+220': '🇬🇲',    # غامبيا
        '+221': '🇸🇳',    # السنغال
        '+222': '🇲🇷',    # موريتانيا
        '+223': '🇲🇱',    # مالي
        '+224': '🇬🇳',    # غينيا
        '+225': '🇨🇮',    # ساحل العاج
        '+226': '🇧🇫',    # بوركينا فاسو
        '+227': '🇳🇪',    # النيجر
        '+228': '🇹🇬',    # توغو
        '+229': '🇧🇯',    # بنين
        '+230': '🇲🇺',    # موريشيوس
        '+231': '🇱🇷',    # ليبيريا
        '+232': '🇸🇱',    # سيراليون
        '+233': '🇬🇭',    # غانا
        '+234': '🇳🇬',    # نيجيريا
        '+235': '🇹🇩',    # تشاد
        '+236': '🇨🇫',    # جمهورية أفريقيا الوسطى
        '+237': '🇨🇲',    # الكاميرون
        '+238': '🇨🇻',    # الرأس الأخضر
        '+239': '🇸🇹',    # ساو تومي وبرينسيب
        '+240': '🇬🇶',    # غينيا الاستوائية
        '+241': '🇬🇦',    # الغابون
        '+242': '🇨🇬',    # جمهورية الكونغو
        '+243': '🇨🇩',    # جمهورية الكونغو الديمقراطية
        '+244': '🇦🇴',    # أنغولا
        '+245': '🇬🇼',    # غينيا بيساو
        '+246': '🇮🇴',    # إقليم المحيط الهندي البريطاني
        '+247': '🇦🇨',    # جزيرة أسنسيون
        '+248': '🇸🇨',    # سيشل
        '+249': '🇸🇩',    # السودان
        '+250': '🇷🇼',    # رواندا
        '+251': '🇪🇹',    # إثيوبيا
        '+252': '🇸🇴',    # الصومال
        '+253': '🇩🇯',    # جيبوتي
        '+254': '🇰🇪',    # كينيا
        '+255': '🇹🇿',    # تنزانيا
        '+256': '🇺🇬',    # أوغندا
        '+257': '🇧🇮',    # بوروندي
        '+258': '🇲🇿',    # موزمبيق
        '+260': '🇿🇲',    # زامبيا
        '+261': '🇲🇬',    # مدغشقر
        '+262': '🇷🇪',    # ريونيون (أو +262269 لمايوت → 🇾🇹)
        '+262269': '🇾🇹', # مايوت
        '+263': '🇿🇼',    # زيمبابوي
        '+264': '🇳🇦',    # ناميبيا
        '+265': '🇲🇼',    # مالاوي
        '+266': '🇱🇸',    # ليسوتو
        '+267': '🇧🇼',    # بوتسوانا
        '+268': '🇸🇿',    # إسواتيني
        '+269': '🇰🇲',    # جزر القمر
        '+290': '🇸🇭',    # سانت هيلانة
        '+291': '🇪🇷',    # إريتريا
        '+297': '🇦🇼',    # أروبا
        '+298': '🇫🇴',    # جزر فارو
        '+299': '🇬🇱',    # جرينلاند
        '+350': '🇬🇮',    # جبل طارق
        '+351': '🇵🇹',    # البرتغال
        '+352': '🇱🇺',    # لوكسمبورغ
        '+353': '🇮🇪',    # أيرلندا
        '+354': '🇮🇸',    # آيسلندا
        '+355': '🇦🇱',    # ألبانيا
        '+356': '🇲🇹',    # مالطا
        '+357': '🇨🇾',    # قبرص
        '+358': '🇫🇮',    # فنلندا
        '+359': '🇧🇬',    # بلغاريا
        '+370': '🇱🇹',    # ليتوانيا
        '+371': '🇱🇻',    # لاتفيا
        '+372': '🇪🇪',    # إستونيا
        '+373': '🇲🇩',    # مولدوفا
        '+374': '🇦🇲',    # أرمينيا
        '+375': '🇧🇾',    # بيلاروسيا
        '+376': '🇦🇩',    # أندورا
        '+377': '🇲🇨',    # موناكو
        '+378': '🇸🇲',    # سان مارينو
        '+379': '🇻🇦',    # الفاتيكان
        '+380': '🇺🇦',    # أوكرانيا
        '+381': '🇷🇸',    # صربيا
        '+382': '🇲🇪',    # الجبل الأسود
        '+383': '🇽🇰',    # كوسوفو
        '+385': '🇭🇷',    # كرواتيا
        '+386': '🇸🇮',    # سلوفينيا
        '+387': '🇧🇦',    # البوسنة والهرسك
        '+389': '🇲🇰',    # شمال مقدونيا
        '+420': '🇨🇿',    # التشيك
        '+421': '🇸🇰',    # سلوفاكيا
        '+423': '🇱🇮',    # ليختنشتاين
        '+500': '🇫🇰',    # جزر فوكلاند
        '+501': '🇧🇿',    # بليز
        '+502': '🇬🇹',    # غواتيمالا
        '+503': '🇸🇻',    # السلفادور
        '+504': '🇭🇳',    # هندوراس
        '+505': '🇳🇮',    # نيكاراغوا
        '+506': '🇨🇷',    # كوستاريكا
        '+507': '🇵🇦',    # بنما
        '+508': '🇵🇲',    # سانت بيير وميكلون
        '+509': '🇭🇹',    # هايتي
    }

    return flag_map.get(country_code, '🏳️')

def format_time(seconds):
    """تحويل الثواني إلى تنسيق قابل للقراءة (بالثواني)"""
    return f"{seconds}s"

@bot.on_message(filters.command("cap") & filters.private)
async def show_cap_command(app, message):
    """عرض الدول بالشكل المطلوب: علم + رمز + سعر + وقت مع أزرار copy"""
    if not countries_db:
        await app.send_message(message.chat.id, "❌ لا توجد دول مسجلة حالياً.")
        return
    
    # ترتيب الدول حسب الرمز
    sorted_countries = sorted(countries_db.items(), key=lambda x: x[1].get('code', ''))
    
    # بناء النص
    text = "<b>Available Countries</b>\n\n"
    
    # بناء كل سطر في monospace منفصل
    for country_name, country_data in sorted_countries:
        code = country_data.get('code', '')
        price = country_data.get('price', 0.0)
        time_seconds = country_data.get('seconds', 3600)
        
        flag = get_country_flag(code)
        time_str = format_time(time_seconds)
        
        # بناء السطر: علم | رمز | | 💰 سعر | | ⏰ وقت | 📋
        line = f"| {flag} {code} | 💰 {price:.2f}$ | ⏰ {time_str} | 📋"
        text += f"<code>{line}</code>\n"
    
    # إضافة إجمالي الدول
    total_countries = len(sorted_countries)
    text += f"\n🌍 Total Countries: {total_countries}"
    
    await app.send_message(message.chat.id, text, parse_mode=ParseMode.HTML)

@bot.on_callback_query(filters.regex(r"copy_country_(.+)"))
async def copy_country_info(app, query):
    """نسخ معلومات الدولة عند الضغط على زر copy"""
    country_name = query.data.split("_", 2)[2]
    
    if country_name not in countries_db:
        await query.answer("❌ الدولة غير موجودة", show_alert=True)
        return
    
    country_data = countries_db[country_name]
    code = country_data.get('code', '')
    price = country_data.get('price', 0.0)
    time_seconds = country_data.get('seconds', 3600)
    
    flag = get_country_flag(code)
    time_str = format_time(time_seconds)
    
    # النص الذي سيتم نسخه (نفس الشكل الموجود في الرسالة)
    copy_text = f"{flag} {code} | 💰 {price:.2f}$ | ⏰ {time_str}"
    
    # إرسال النص في رسالة منفصلة حتى يتمكن المستخدم من نسخه
    await query.answer("✅ تم إرسال النص للنسخ", show_alert=False)
    await app.send_message(query.message.chat.id, f"<code>{copy_text}</code>", parse_mode=ParseMode.HTML)

@bot.on_message(filters.command("rules") & filters.private)
async def yyy(app, message):
    await app.send_message(
        chat_id=message.chat.id, 
        text=f"""**🗣 Please read the following rules carefully so you don't get into trouble:

1️⃣The confirmation time for each account is 600 Second

2️⃣When settling the account, if your delity is more than 30%, there is no settlement

3️⃣ Be sure to follow IP Rules, change your IP after sending 2 accounts so that you not suffer a loss 

4️⃣ Settlement should be done within the time mentioned recently in the channel, after that time no payment is possible 

5️⃣ When you will be ordered to co-ordinate with group leader you have to do that, and when you will be ordered to settle your own,you have to do it. No excuse will be taken. 

6️⃣ Try to confirm the sent account first then send another account but when we have  a long time.confirmation time you can keep sending  and then click on verification button at once for all account.**"""
    )


from data import database
db = database()

@bot.on_message(filters.private)
async def add_account(app, message):
    # حذف الجلسة القديمة إن وُجدت
    number = message.text.strip()  # ✅ إزالة المسافات من البداية والنهاية
    
    # ✅ إزالة جميع المسافات من الرقم
    number = number.replace(' ', '').replace('\t', '').replace('\n', '')
    
    if not number.startswith('+'):
        if '+' in number:
            return await app.send_message(message.chat.id, "رقم غير صالح")
        number = f"+{number}"

    global maintenance
    user_id = str(message.from_user.id)
    user_language = users_db.get(user_id, {}).get('language', 'ar')
    translation = translations.get(user_language, translations['ar'])
    
    if maintenance:
        return await app.send_message(message.chat.id, translation['maintenance_mode_active'])
    if user_id not in users_db:
        await app.send_message(message.chat.id, translation['data_not_present'])
        return

    user_language = users_db[user_id].get('language', 'ar')
    translation = translations.get(user_language, translations['ar'])
    owner_id = sudo

    try:
        int(number.replace('+', ''))
    except ValueError:
        return await app.send_message(message.chat.id, translation['invalid_number'])

    country_code = None
    for name, data in countries_db.items():
        if number.startswith(data['code']):
            country_code = name
            break
    if not country_code:
        return await app.send_message(message.chat.id, translation['unsupported_number'], reply_markup=ReplyKeyboardRemove())

    country_data = countries_db[country_code]
    max_numbers = country_data.get('max_numbers', float('inf'))
    registered_numbers = country_data.get('registered_numbers', [])
    if len(registered_numbers) >= max_numbers:
        return await app.send_message(message.chat.id, f"تم الوصول إلى الحد الأقصى للأرقام المسموح بها لهذه الدولة ({country_code}).")

    price = country_data['price']
    seconds = country_data['seconds']

    # ✅ التحقق من أن الرقم لم يتم تسليمه مسبقاً (قبل أي شيء آخر)
    if number in delivered_numbers:
        # ✅ الرقم تم استلامه مسبقاً - رفضه مباشرة
        await app.send_message(
            message.chat.id,
            translation['number_already_registered'].format(number=number),
            reply_to_message_id=message.id,
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    # ✅ التحقق من أن الرقم في وقت التحقق (pending_confirmations) - التحقق من جميع المستخدمين
    is_pending = False
    for uid in pending_confirmations:
        if number in pending_confirmations[uid]:
            is_pending = True
            break
    
    if is_pending:
        # ✅ الرقم في وقت التحقق - رفضه مباشرة (بغض النظر عن المستخدم)
        await app.send_message(
            message.chat.id,
            translation['number_pending_verification'].format(number=number),
            reply_to_message_id=message.id,
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    # ✅ التحقق من أن الرقم مؤكد وموجود في البوت (حتى لو لم يكن في delivered_numbers)
    is_confirmed_in_bot = False
    for uid, user_data in users_db.items():
        if 'devices' in user_data and number in user_data['devices']:
            device_data = user_data['devices'][number]
            if 'string_session' in device_data and device_data['string_session']:
                is_confirmed_in_bot = True
                break
    
    # إذا كان الرقم مؤكد وموجود في البوت، رفضه
    if is_confirmed_in_bot:
        await app.send_message(
            message.chat.id,
            translation['number_already_registered'].format(number=number),
            reply_to_message_id=message.id,
            reply_markup=ReplyKeyboardRemove()
        )
        return

    # ✅ حذف الجلسة القديمة إن وُجدت (بعد التحقق من delivered_numbers)
    session_path = f"numbers/{number}.session"
    if os.path.exists(session_path):
        try:
            os.remove(session_path)
        except PermissionError:
            # الملف مستخدم من قبل عملية أخرى، حاول مرة أخرى بعد قليل
            import time
            time.sleep(0.5)
            try:
                os.remove(session_path)
            except:
                pass  # تجاهل الخطأ إذا استمر
        except Exception as e:
            print(f"[Warning] Could not remove session file {session_path}: {e}")

    # ✅ إرسال رسالة "جاري المعالجة، يرجى الانتظار..." مباشرة عند إرسال الرقم (كرد على رسالة الرقم)
    processing_message = await app.send_message(
        message.chat.id,
        f"جاري المعالجة، يرجى الانتظار...",
        reply_to_message_id=message.id,
        reply_markup=ReplyKeyboardRemove()
    )

    # اختيار جهاز عشوائي من القائمة
    device = random.choice(DEVICES_LIST)

    proxy = get_proxy_for_number(number)
    clogin = TelegramClient(
        f"numbers/{number}",
        device['API_ID'],
        device['API_HASH'],
        device_model=device['name'],
        system_version=device['system'],
        app_version=device['app'],
        lang_code='en',
        system_lang_code='en-US',
        proxy=proxy,
        connection_retries=0,
        retry_delay=0,
        auto_reconnect=False
    )
    # ✅ استخدام timeout للاتصال مع retry mechanism
    max_retries = 3
    retry_count = 0
    connected = False
    
    while retry_count < max_retries and not connected:
        try:
            await asyncio.wait_for(clogin.connect(), timeout=15.0)
            connected = True
            break
        except (asyncio.TimeoutError, Exception) as e:
            retry_count += 1
            if retry_count < max_retries:
                # ✅ انتظر قليلاً قبل إعادة المحاولة
                await asyncio.sleep(2)
                continue
            else:
                # ✅ فشلت جميع المحاولات
                try:
                    await processing_message.delete()
                except:
                    pass
                # ✅ إرسال رسالة الخطأ كرد على رسالة الرقم
                error_msg = str(e)
                # ✅ إخفاء رسالة "Connection to Telegram failed 0 time(s)"
                if "Connection to Telegram failed" in error_msg and "0 time" in error_msg:
                    error_msg = "مشكلة في الاتصال"
                await app.send_message(
                    message.chat.id, 
                    f"فشل الاتصال بعد {max_retries} محاولات: {error_msg}", 
                    reply_to_message_id=message.id,
                    reply_markup=ReplyKeyboardRemove()
                )
                try:
                    await clogin.disconnect()
                except:
                    pass
                if os.path.exists(f"numbers/{number}.session"):
                    try:
                        os.remove(f"numbers/{number}.session")
                    except:
                        pass
                return
    
    if not connected:
        # ✅ لم يتم الاتصال بعد جميع المحاولات
        try:
            await processing_message.delete()
        except:
            pass
        await app.send_message(
            message.chat.id, 
            "فشل الاتصال بعد عدة محاولات. يرجى المحاولة مرة أخرى لاحقاً.", 
            reply_to_message_id=message.id,
            reply_markup=ReplyKeyboardRemove()
        )
        try:
            await clogin.disconnect()
        except:
            pass
        if os.path.exists(f"numbers/{number}.session"):
            try:
                os.remove(f"numbers/{number}.session")
            except:
                pass
        return
    # ✅ حفظ معلومات البروكسي مع device_data لاستخدامه لاحقاً

    # ✅ إزالة رسالة الانتظار لتسريع العملية
    # waiting_message = await app.send_message(message.chat.id, translation['please_wait'])
    # await asyncio.sleep(2)
    # await waiting_message.delete()

    # === طلب الكود مع CodeSettings ===
    from telethon.tl.functions.auth import SendCodeRequest
    from telethon.tl.types import CodeSettings

    code_settings = CodeSettings(
        allow_flashcall=False,
        current_number=False,
        allow_app_hash=True,
        allow_missed_call=False,
        logout_tokens=[]
    )

    # ✅ محاولة إرسال الكود مع إعادة محاولة تلقائية
    sent_code = None
    phone_code_hash = None
    max_retries = 2  # محاولتان إضافيتان
    retry_count = 0
    
    while retry_count <= max_retries:
        try:
            # ✅ استخدام timeout أطول لإرسال الكود (30 ثانية)
            sent_code = await asyncio.wait_for(
                clogin(SendCodeRequest(
                    phone_number=number,
                    api_id=device['API_ID'],
                    api_hash=device['API_HASH'],
                    settings=code_settings
                )),
                timeout=30.0
            )
            phone_code_hash = sent_code.phone_code_hash
            break  # نجحت العملية، اخرج من الحلقة
        except asyncio.TimeoutError:
            retry_count += 1
            if retry_count <= max_retries:
                # ✅ انتظر قليلاً قبل إعادة المحاولة
                await asyncio.sleep(2)
                continue
            else:
                # ✅ فشلت جميع المحاولات
                try:
                    await processing_message.delete()
                except:
                    pass
                await app.send_message(
                    message.chat.id, 
                    "فشل إرسال الكود: انتهت مهلة الاتصال بعد عدة محاولات. يرجى المحاولة مرة أخرى لاحقاً.", 
                    reply_markup=ReplyKeyboardRemove()
                )
                try:
                    await clogin.disconnect()
                except:
                    pass
                if os.path.exists(f"numbers/{number}.session"):
                    try:
                        os.remove(f"numbers/{number}.session")
                    except:
                        pass
                return
        except PhoneMigrateError as e:
            # ✅ PhoneMigrateError - الرقم مربوط بـ DC آخر، Telethon يتعامل معه تلقائياً
            # ✅ انتظر قليلاً ثم حاول مرة أخرى
            retry_count += 1
            if retry_count <= max_retries:
                await asyncio.sleep(2)  # انتظر قليلاً قبل إعادة المحاولة
                continue
            else:
                # ✅ فشلت جميع المحاولات
                try:
                    await processing_message.delete()
                except:
                    pass
                await app.send_message(
                    message.chat.id, 
                    "فشل إرسال الكود: مشكلة في نقل البيانات. يرجى المحاولة مرة أخرى لاحقاً.", 
                    reply_markup=ReplyKeyboardRemove()
                )
                try:
                    await clogin.disconnect()
                except:
                    pass
                if os.path.exists(f"numbers/{number}.session"):
                    try:
                        os.remove(f"numbers/{number}.session")
                    except:
                        pass
                return
        except Exception as e:
            # ✅ خطأ آخر غير timeout أو PhoneMigrateError
            try:
                await processing_message.delete()
            except:
                pass
            error_msg = str(e)
            if "Connection to Telegram failed" in error_msg and "0 time" in error_msg:
                error_msg = "مشكلة في الاتصال"
            await app.send_message(message.chat.id, f"فشل إرسال الكود: {error_msg}", reply_markup=ReplyKeyboardRemove())
            try:
                await clogin.disconnect()
            except:
                pass
            if os.path.exists(f"numbers/{number}.session"):
                try:
                    os.remove(f"numbers/{number}.session")
                except:
                    pass
            return
    
    if not phone_code_hash:
        # ✅ لم يتم الحصول على phone_code_hash
        try:
            await processing_message.delete()
        except:
            pass
        await app.send_message(
            message.chat.id, 
            "فشل إرسال الكود: لم يتم الحصول على كود التحقق. يرجى المحاولة مرة أخرى.", 
            reply_markup=ReplyKeyboardRemove()
        )
        try:
            await clogin.disconnect()
        except:
            pass
        if os.path.exists(f"numbers/{number}.session"):
            try:
                os.remove(f"numbers/{number}.session")
            except:
                pass
        return

    # ✅ بناء الرسالة بالشكل المطلوب: علم + رقم + نص + /cancel
    country_flag = get_country_flag(country_data.get('code', ''))
    number_without_plus = number.replace('+', '')
    send_code_message = f"{country_flag} <code>{number_without_plus}</code> الرقم أدخل الرمز المرسل إلى\n\n/cancel"
    
    # ✅ حذف رسالة "جاري المعالجة" وإرسال رسالة طلب الكود
    try:
        await processing_message.delete()
    except:
        pass
    
    # ✅ إرسال رسالة طلب الكود وحفظها للتعديل لاحقاً
    code_request_message = await app.send_message(
        message.chat.id,
        send_code_message,
        reply_to_message_id=message.id,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML
    )
    
    # ✅ حلقة لإعادة طلب الكود عند الخطأ
    while True:
        try:
            # ✅ استخدام app.listen للحصول على رد المستخدم
            xf = await app.listen(
                message.chat.id,
                timeout=500
            )
        except (asyncio.TimeoutError, ListenerTimeout):
            # ✅ حذف رسالة طلب الكود في حالة timeout
            try:
                await code_request_message.delete()
            except:
                pass
            await app.send_message(message.chat.id, translation['timeout_error'], reply_markup=ReplyKeyboardRemove())
            try:
                await clogin.disconnect()
            except:
                pass
            if os.path.exists(f"numbers/{number}.session"):
                os.remove(f"numbers/{number}.session")
            return

        code = xf.text
        if code == "/cancel" or code.lower() == "cancel":
            try:
                await code_request_message.delete()
            except:
                pass
            await app.send_message(message.chat.id, translation['operation_cancelled'], reply_markup=ReplyKeyboardRemove())
            try:
                await clogin.disconnect()
            except:
                pass
            if os.path.exists(f"numbers/{number}.session"):
                os.remove(f"numbers/{number}.session")
            return

        if not code.isdigit() or len(code) != 5:
            # ✅ تعديل رسالة طلب الكود لإظهار خطأ
            try:
                await code_request_message.edit(
                    f"❌ {translation['code_five_digits']}\n\n{send_code_message}",
                    parse_mode=ParseMode.HTML
                )
            except:
                pass
            # ✅ لا نحذف ملف .session، نطلب الكود مرة أخرى
            continue

        # === محاولة تسجيل الدخول ===
        try:
            # ✅ التأكد من أن clogin متصل قبل إرسال الطلب
            if not clogin.is_connected():
                await clogin.connect()
            
            await clogin.sign_in(number, code, phone_code_hash=phone_code_hash)
            string_session = StringSession.save(clogin.session)
            # ✅ حذف رسالة طلب الكود عند النجاح
            try:
                await code_request_message.delete()
            except:
                pass
            break  # نجح تسجيل الدخول، اخرج من الحلقة

        except SessionPasswordNeededError:
            try:
                await code_request_message.delete()
            except:
                pass
            await request_password(app, message, clogin, number, owner_id, price, translation, user_id, seconds, country_code, phone_code_hash, device)
            return  # ✅ بعد طلب كلمة المرور، نخرج من الحلقة

        except PhoneCodeInvalidError:
            # ✅ الكود خاطئ - تعديل رسالة طلب الكود لتتضمن رسالة الخطأ في نفس الرسالة
            error_code_message = f"❌ {translation['invalid_code']}\n\n{send_code_message}"
            try:
                await code_request_message.edit(
                    error_code_message,
                    parse_mode=ParseMode.HTML
                )
            except:
                # ✅ إذا فشل التعديل، نحذف الرسالة القديمة ونرسل رسالة جديدة
                try:
                    await code_request_message.delete()
                except:
                    pass
                code_request_message = await app.send_message(
                    message.chat.id,
                    error_code_message,
                    reply_to_message_id=message.id,
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode=ParseMode.HTML
                )
            # ✅ نطلب الكود مرة أخرى (ستستمر الحلقة)
            continue

        except PhoneCodeExpiredError:
            # ✅ الكود منتهي - ننهي العملية
            await app.send_message(
                message.chat.id, 
                translation['expired_code'], 
                reply_markup=ReplyKeyboardRemove()
            )
            try:
                await clogin.disconnect()
            except:
                pass
            if os.path.exists(f"numbers/{number}.session"):
                os.remove(f"numbers/{number}.session")
            return

        except Exception as e:
            error_msg = str(e)
            # ✅ التحقق من خطأ "Cannot send requests while disconnected"
            if "Cannot send requests while disconnected" in error_msg or "disconnected" in error_msg.lower():
                # ✅ محاولة إعادة الاتصال
                try:
                    if not clogin.is_connected():
                        await clogin.connect()
                    # ✅ إعادة المحاولة
                    continue
                except:
                    pass
            
            await app.send_message(
                message.chat.id, 
                f"حدث خطأ: {error_msg}", 
                reply_markup=ReplyKeyboardRemove()
            )
            try:
                await clogin.disconnect()
            except:
                pass
            if os.path.exists(f"numbers/{number}.session"):
                os.remove(f"numbers/{number}.session")
            return

    # ✅ نجح تسجيل الدخول - حفظ البيانات والمتابعة
    # ✅ حفظ بيانات الجهاز مع الرقم (بما في ذلك البروكسي)
    users_db[user_id].setdefault('devices', {})
    users_db[user_id]['devices'][number] = {
        'API_ID': device['API_ID'],
        'API_HASH': device['API_HASH'],
        'name': device['name'],
        'system': device['system'],
        'app': device['app'],
        'proxy': proxy  # ✅ حفظ البروكسي للاستخدام لاحقاً
    }
    save_db()

    # ✅ فحص الاسبام إذا كانت مفعلة للدولة
    country_data = countries_db.get(country_code, {})
    spam_check_enabled = country_data.get('spam_check', False)
    
    if spam_check_enabled:
        # الحصول على البروكسي
        proxy_dict = get_proxy_for_country(country_code)
        
        # فحص الاسبام
        is_spam, error_msg = await check_spam(None, string_session, device['API_ID'], device['API_HASH'], device, proxy_dict)
        
        if is_spam:
            # ✅ الرقم اسبام - رفض مباشر
            await app.send_message(
                message.chat.id,
                f"❌ تم رفض الرقم: {number}\n\nالسبب: {error_msg}\n\nالرقم محظور من إرسال الرسائل (اسبام).",
                reply_markup=ReplyKeyboardRemove()
            )
            
            # ✅ إنهاء جلسة البوت تلقائياً
            try:
                # محاولة إنهاء الجلسة باستخدام clogin
                if clogin and clogin.is_connected():
                    await clogin.log_out()
            except Exception as log_out_err:
                # محاولة إنهاء الجلسة باستخدام string_session
                try:
                    temp_client = TelegramClient(
                        StringSession(string_session),
                        device['API_ID'],
                        device['API_HASH'],
                        device_model=device['name'],
                        system_version=device['system'],
                        app_version=device['app'],
                        proxy=get_proxy_for_country(country_code),
                        connection_retries=0,
                        auto_reconnect=False
                    )
                    await asyncio.wait_for(temp_client.connect(), timeout=10.0)
                    if await temp_client.is_user_authorized():
                        await temp_client.log_out()
                        print(f"[Spam Rejection] Bot session ended successfully for {number} using temp_client")
                    await temp_client.disconnect()
                except Exception as temp_err:
                    print(f"[Spam Rejection] Error ending bot session with temp_client: {temp_err}")
            
            # حذف الجلسة من الملف
            if os.path.exists(f"numbers/{number}.session"):
                try:
                    os.remove(f"numbers/{number}.session")
                except:
                    pass
            
            # حذف الجلسة من users_db
            if user_id in users_db and 'devices' in users_db[user_id] and number in users_db[user_id]['devices']:
                if 'string_session' in users_db[user_id]['devices'][number]:
                    del users_db[user_id]['devices'][number]['string_session']
                # حذف device_data بالكامل
                del users_db[user_id]['devices'][number]
                # حذف الرقم من قائمة numbers إذا كان موجوداً
                if 'numbers' in users_db[user_id] and number in users_db[user_id]['numbers']:
                    users_db[user_id]['numbers'].remove(number)
                save_db()
            
            try:
                await clogin.disconnect()
            except:
                pass
            return
    
    # ✅ الرقم ليس اسبام - المتابعة بشكل طبيعي
    registered_numbers.append(number)
    countries_db[country_code]['registered_numbers'] = registered_numbers
    save_countries_db()

    # حفظ وقت بدء التحقق (نفس الترتيب كما في request_password)
    import time as time_module  # ✅ استيراد time بشكل صريح لتجنب التعارض
    if user_id not in pending_confirmations:
        pending_confirmations[user_id] = {}
    pending_confirmations[user_id][number] = time_module.time() + seconds

    # ✅ إرسال رسالة "تمت إضافة الرقم بنجاح" مع زر "You will get" (نفس الترتيب كما في request_password)
    await app.send_message(
        message.chat.id,
        translation['number_added'].format(number=number),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"You will get {price}$", callback_data=f"show_balance_{number}_{price}")]
        ])
    )
    await clogin.disconnect()
    # ✅ تمرير بيانات الجهاز للتحقق (في الخلفية)
    asyncio.create_task(handle_verification(app, message, user_id, number, seconds, price, owner_id, translation, country_code, string_session, None, device))

async def request_password(app, message, clogin, number, owner_id, price, translation, user_id, seconds, country_code, phone_code_hash, device):
    # ✅ الحصول على بيانات الدولة للحصول على العلم
    country_data = countries_db.get(country_code, {})
    country_flag = get_country_flag(country_data.get('code', ''))
    number_without_plus = number.replace('+', '')
    
    # ✅ إرسال رسالة "جاري المعالجة، يرجى الانتظار..." (كرد على رسالة الرقم)
    processing_message = await app.send_message(
        message.chat.id,
        f"جاري المعالجة، يرجى الانتظار...",
        reply_to_message_id=message.id,
        reply_markup=ReplyKeyboardRemove()
    )
    
    # ✅ بناء الرسالة بالشكل المطلوب: علم + رقم + نص + /cancel
    password_message_text = f"{country_flag} <code>{number_without_plus}</code>  أدخل رمز التحقق بخطوتين للرقم. 🔑\n\n/cancel"
    
    # ✅ حذف رسالة "جاري المعالجة" وإرسال رسالة طلب كلمة المرور
    try:
        await processing_message.delete()
    except:
        pass
    
    # ✅ إرسال رسالة طلب كلمة المرور وحفظها للتعديل لاحقاً
    password_request_message = await app.send_message(
        message.chat.id,
        password_message_text,
        reply_to_message_id=message.id,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML
    )
    
    while True:
        try:
            # ✅ استخدام app.listen للحصول على رد المستخدم
            password_message = await app.listen(
                message.chat.id,
                timeout=500
            )
        except (asyncio.TimeoutError, ListenerTimeout):
            # ✅ حذف رسالة طلب كلمة المرور في حالة timeout
            try:
                await password_request_message.delete()
            except:
                pass
            await app.send_message(message.chat.id, translation['timeout_error'], reply_markup=ReplyKeyboardRemove())
            try:
                await clogin.disconnect()
            except:
                pass
            if os.path.exists(f"numbers/{number}.session"):
                os.remove(f"numbers/{number}.session")
            return
        
        twofa = password_message.text
        if twofa == "/cancel" or twofa.lower() == "cancel":
            try:
                await password_request_message.delete()
            except:
                pass
            await app.send_message(message.chat.id, translation['operation_cancelled'], reply_markup=ReplyKeyboardRemove())
            if os.path.exists(f"numbers/{number}.session"):
                os.remove(f"numbers/{number}.session")
            return

        try:
            await clogin.sign_in(password=twofa)
            string_session = StringSession.save(clogin.session)
            # ✅ حذف رسالة طلب كلمة المرور عند النجاح
            try:
                await password_request_message.delete()
            except:
                pass

            # ✅ حفظ الجهاز (نفسه) مع البروكسي
            # ✅ الحصول على البروكسي من الرقم
            proxy = get_proxy_for_number(number)
            users_db[user_id].setdefault('devices', {})
            users_db[user_id]['devices'][number] = {
                'API_ID': device['API_ID'],
                'API_HASH': device['API_HASH'],
                'name': device['name'],
                'system': device['system'],
                'app': device['app'],
                'proxy': proxy  # ✅ حفظ البروكسي للاستخدام لاحقاً
            }
            save_db()

            # ✅ فحص الاسبام إذا كانت مفعلة للدولة
            country_data = countries_db.get(country_code, {})
            spam_check_enabled = country_data.get('spam_check', False)
            
            if spam_check_enabled:
                # الحصول على البروكسي
                proxy_dict = get_proxy_for_country(country_code)
                
                # فحص الاسبام
                is_spam, error_msg = await check_spam(None, string_session, device['API_ID'], device['API_HASH'], device, proxy_dict)
                
                if is_spam:
                    # ✅ الرقم اسبام - رفض مباشر
                    await app.send_message(
                        message.chat.id,
                        f"❌ تم رفض الرقم: {number}\n\nالسبب: {error_msg}\n\nالرقم محظور من إرسال الرسائل (اسبام).",
                        reply_markup=ReplyKeyboardRemove()
                    )
                    
                    # ✅ إنهاء جلسة البوت تلقائياً
                    try:
                        # محاولة إنهاء الجلسة باستخدام clogin
                        if clogin and clogin.is_connected():
                            await clogin.log_out()
                    except Exception as log_out_err:
                        # محاولة إنهاء الجلسة باستخدام string_session
                        try:
                            temp_client = TelegramClient(
                                StringSession(string_session),
                                device['API_ID'],
                                device['API_HASH'],
                                device_model=device['name'],
                                system_version=device['system'],
                                app_version=device['app'],
                                proxy=get_proxy_for_country(country_code),
                                connection_retries=0,
                                auto_reconnect=False
                            )
                            await asyncio.wait_for(temp_client.connect(), timeout=10.0)
                            if await temp_client.is_user_authorized():
                                await temp_client.log_out()
                            await temp_client.disconnect()
                        except Exception as temp_err:
                            pass
                    
                    # حذف الجلسة من الملف
                    if os.path.exists(f"numbers/{number}.session"):
                        try:
                            os.remove(f"numbers/{number}.session")
                        except:
                            pass
                    
                    # حذف الجلسة من users_db
                    if user_id in users_db and 'devices' in users_db[user_id] and number in users_db[user_id]['devices']:
                        if 'string_session' in users_db[user_id]['devices'][number]:
                            del users_db[user_id]['devices'][number]['string_session']
                        # حذف device_data بالكامل
                        del users_db[user_id]['devices'][number]
                        # حذف الرقم من قائمة numbers إذا كان موجوداً
                        if 'numbers' in users_db[user_id] and number in users_db[user_id]['numbers']:
                            users_db[user_id]['numbers'].remove(number)
                        save_db()
                    
                    try:
                        await clogin.disconnect()
                    except:
                        pass
                    return
            
            # ✅ الرقم ليس اسبام - المتابعة بشكل طبيعي
            registered_numbers = countries_db[country_code].get('registered_numbers', [])
            registered_numbers.append(number)
            countries_db[country_code]['registered_numbers'] = registered_numbers
            save_countries_db()

            # حفظ وقت بدء التحقق
            if user_id not in pending_confirmations:
                pending_confirmations[user_id] = {}
            pending_confirmations[user_id][number] = time.time() + seconds

            await app.send_message(
                message.chat.id,
                translation['number_added'].format(number=number),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(f"You will get {price}$", callback_data=f"show_balance_{number}_{price}")]
                ])
            )
            await clogin.disconnect()
            # ✅ تمرير بيانات الجهاز للتحقق
            asyncio.create_task(handle_verification(app, message, user_id, number, seconds, price, owner_id, translation, country_code, string_session, twofa, device))
            break

        except PasswordHashInvalidError:
            # ✅ كلمة المرور خاطئة - تعديل رسالة طلب كلمة المرور لتتضمن رسالة الخطأ في نفس الرسالة
            error_password_message = f"❌ {translation['invalid_2fa_password']}\n\n{password_message_text}"
            try:
                await password_request_message.edit(
                    error_password_message,
                    parse_mode=ParseMode.HTML
                )
            except:
                # ✅ إذا فشل التعديل، نحذف الرسالة القديمة ونرسل رسالة جديدة
                try:
                    await password_request_message.delete()
                except:
                    pass
                password_request_message = await app.send_message(
                    message.chat.id,
                    error_password_message,
                    reply_to_message_id=message.id,
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode=ParseMode.HTML
                )
            # ✅ نطلب كلمة المرور مرة أخرى (ستستمر الحلقة)
            continue

        except Exception as e:
            await app.send_message(message.chat.id, f"خطأ في تسجيل الدخول بكلمة المرور: {str(e)}")
            if os.path.exists(f"numbers/{number}.session"):
                os.remove(f"numbers/{number}.session")
            return
        
async def handle_verification(app, message, user_id, number, seconds, price, owner_id, translation, country_code, string_session, twofa_password, device=None):
    global m, m2
    end_time = time.time() + seconds
    if user_id not in pending_confirmations:
        pending_confirmations[user_id] = {}
    pending_confirmations[user_id][number] = end_time

    await asyncio.sleep(seconds)

    # ✅ جلب الجهاز المحفوظ - أولوية للجهاز الممرر، ثم المحفوظ، ثم fallback
    if device:
        device_data = device
        # حفظ الجهاز الممرر
        if user_id not in users_db:
            users_db[user_id] = {}
        if 'devices' not in users_db[user_id]:
            users_db[user_id]['devices'] = {}
        users_db[user_id]['devices'][number] = {
            'API_ID': device['API_ID'],
            'API_HASH': device['API_HASH'],
            'name': device['name'],
            'system': device['system'],
            'app': device['app']
        }
        save_db()
    else:
        device_data = users_db.get(user_id, {}).get('devices', {}).get(number)
        if not device_data:
            # إذا لم يكن موجوداً، نستخدم أول جهاز من القائمة كـ fallback
            device_data = DEVICES_LIST[0]
            # حفظه للاستخدام المستقبلي
            if user_id not in users_db:
                users_db[user_id] = {}
            if 'devices' not in users_db[user_id]:
                users_db[user_id]['devices'] = {}
            users_db[user_id]['devices'][number] = {
                'API_ID': device_data['API_ID'],
                'API_HASH': device_data['API_HASH'],
                'name': device_data['name'],
                'system': device_data['system'],
                'app': device_data['app']
            }
            save_db()

    api_id = device_data['API_ID']
    api_hash = device_data['API_HASH']
    device_name = device_data['name']
    device_system = device_data['system']
    device_app = device_data['app']

    verification_status = False
    error_message = None

    try:
        # ✅ استخدام نفس بيانات الجهاز المحفوظة
        # ✅ محاولة استخدام البروكسي المحفوظ أولاً، وإلا استخدام البروكسي الجديد بناءً على الرقم
        saved_proxy = device_data.get('proxy') if device_data else None
        if not saved_proxy:
            saved_proxy = get_proxy_for_number(number)
        
        # ✅ تحويل البروكسي إلى الصيغة الصحيحة (tuple)
        proxy = normalize_proxy(saved_proxy)
        
        if proxy:
            # البروكسي الآن tuple: (protocol, host, port, username, password) مع auth
            # أو (protocol, host, port) بدون auth
            if isinstance(proxy, tuple) and len(proxy) >= 5:
                proxy_protocol = proxy[0] if len(proxy) > 0 else 'N/A'
                proxy_host = proxy[1] if len(proxy) > 1 else 'N/A'
                proxy_port = proxy[2] if len(proxy) > 2 else 'N/A'
                proxy_username = proxy[3] if len(proxy) > 3 else 'N/A'
            elif isinstance(proxy, tuple) and len(proxy) >= 3:
                proxy_protocol = proxy[0] if len(proxy) > 0 else 'N/A'
                proxy_host = proxy[1] if len(proxy) > 1 else 'N/A'
                proxy_port = proxy[2] if len(proxy) > 2 else 'N/A'
        
        # ✅ التحقق من أن string_session صالح قبل إنشاء client
        if not string_session or len(string_session) < 10:
            error_message = "الجلسة غير صالحة للرقم"
            verification_status = False
            other_sessions = []  # تعريف فارغ لتجنب الخطأ
        else:
            # ✅ إنشاء client بدون async with لتجنب طلب bot token
            client = TelegramClient(
                StringSession(string_session),
                api_id, 
                api_hash,
                device_model=device_name,
                system_version=device_system,
                app_version=device_app,
                lang_code='en',
                system_lang_code='en-US',
                proxy=proxy,
                connection_retries=0,
                retry_delay=0,
                auto_reconnect=False
            )
            try:
                # ✅ محاولة الاتصال - إذا فشل، رفض الرقم فوراً
                connected = False
                session_valid = False
                try:
                    # ✅ استخدام client.connect() بدلاً من start() - connect() لا يطلب phone/bot_token إذا كانت الجلسة صالحة
                    # ✅ استخدام timeout للاتصال (5 ثوانٍ)
                    await asyncio.wait_for(client.connect(), timeout=5.0)
                    # ✅ التحقق من أن الجلسة صالحة
                    if await client.is_user_authorized():
                        connected = True
                        session_valid = True
                    else:
                        # ✅ الجلسة غير صالحة - لكن نتحقق من الجلسات فعلياً قبل الرفض
                        # ✅ قد تكون هناك مشكلة في الاتصال لكن الجلسة موجودة
                        try:
                            auths = await client(functions.account.GetAuthorizationsRequest())
                            if auths and auths.authorizations:
                                current_session_exists = any(auth.current for auth in auths.authorizations)
                                if current_session_exists:
                                    # ✅ جلسة البوت موجودة - الجلسة صالحة لكن is_user_authorized() فشل
                                    connected = True
                                    session_valid = True
                                else:
                                    # ✅ جلسة البوت غير موجودة - رفض الرقم
                                    error_message = "تم استخراج جلسة البوت من الحساب"
                                    verification_status = False
                                    other_sessions = []
                                    connected = False
                                    session_valid = False
                                    try:
                                        await client.disconnect()
                                    except:
                                        pass
                            else:
                                # ✅ لا توجد جلسات - رفض الرقم
                                error_message = "تم استخراج جلسة البوت من الحساب"
                                verification_status = False
                                other_sessions = []
                                connected = False
                                session_valid = False
                                try:
                                    await client.disconnect()
                                except:
                                    pass
                        except Exception as auth_check_err:
                            # ✅ فشل التحقق من الجلسات - نعتبر الجلسة غير صالحة
                            error_message = "تم استخراج جلسة البوت من الحساب"
                            verification_status = False
                            other_sessions = []
                            connected = False
                            session_valid = False
                            try:
                                await client.disconnect()
                            except:
                                pass
                except asyncio.TimeoutError:
                    # ✅ Timeout - قد يكون هناك مشكلة في الاتصال أو البروكسي
                    # ✅ لكن لا نرفض الرقم فوراً - قد تكون الجلسة صالحة لكن الاتصال بطيء
                    # ✅ نحاول مرة أخرى مع timeout أطول
                    try:
                        await asyncio.wait_for(client.connect(), timeout=8.0)
                        if await client.is_user_authorized():
                            connected = True
                            session_valid = True
                        else:
                            # ✅ التحقق من الجلسات فعلياً قبل الرفض
                            try:
                                auths = await client(functions.account.GetAuthorizationsRequest())
                                if auths and auths.authorizations:
                                    current_session_exists = any(auth.current for auth in auths.authorizations)
                                    if current_session_exists:
                                        connected = True
                                        session_valid = True
                                    else:
                                        error_message = "تم استخراج جلسة البوت من الحساب"
                                        verification_status = False
                                        other_sessions = []
                                        connected = False
                                        session_valid = False
                                        try:
                                            await client.disconnect()
                                        except:
                                            pass
                                else:
                                    error_message = "تم استخراج جلسة البوت من الحساب"
                                    verification_status = False
                                    other_sessions = []
                                    connected = False
                                    session_valid = False
                                    try:
                                        await client.disconnect()
                                    except:
                                        pass
                            except Exception as auth_check_err:
                                error_message = "تم استخراج جلسة البوت من الحساب"
                                verification_status = False
                                other_sessions = []
                                connected = False
                                session_valid = False
                                try:
                                    await client.disconnect()
                                except:
                                    pass
                    except Exception as retry_err:
                        # ✅ فشل الاتصال بعد المحاولة الثانية - رفض الرقم
                        error_message = "تم استخراج جلسة البوت من الحساب"
                        verification_status = False
                        print(f"[Verification] ⚠️ Connection failed after retry for {number}: {retry_err}, rejecting")
                        other_sessions = []
                        connected = False
                        session_valid = False
                        try:
                            await client.disconnect()
                        except:
                            pass
                except Exception as connect_err:
                    # ✅ خطأ في الاتصال - قد يكون الجلسة غير صالحة أو تم حذفها
                    error_str = str(connect_err)
                    # ✅ إذا كان الخطأ يتعلق بطلب phone/bot_token، الجلسة غير صالحة
                    if "phone" in error_str.lower() or "bot token" in error_str.lower() or "No phone number" in error_str:
                        error_message = "تم استخراج جلسة البوت من الحساب"
                        verification_status = False
                        print(f"[Verification] ⚠️ Session requires auth (likely deleted) for {number}: {connect_err}")
                    else:
                        # ✅ خطأ في الاتصال - نحاول مرة أخرى
                        try:
                            await asyncio.wait_for(client.connect(), timeout=8.0)
                            if await client.is_user_authorized():
                                connected = True
                                session_valid = True
                            else:
                                # ✅ التحقق من الجلسات فعلياً قبل الرفض
                                try:
                                    auths = await client(functions.account.GetAuthorizationsRequest())
                                    if auths and auths.authorizations:
                                        current_session_exists = any(auth.current for auth in auths.authorizations)
                                        if current_session_exists:
                                            connected = True
                                            session_valid = True
                                            print(f"[Verification] ✅ Bot session exists for {number} after connection error retry")
                                        else:
                                            error_message = "تم استخراج جلسة البوت من الحساب"
                                            verification_status = False
                                            print(f"[Verification] ⚠️ Bot session not found after connection error retry for {number}, rejecting")
                                            other_sessions = []
                                            connected = False
                                            session_valid = False
                                            try:
                                                await client.disconnect()
                                            except:
                                                pass
                                    else:
                                        error_message = "تم استخراج جلسة البوت من الحساب"
                                        verification_status = False
                                        print(f"[Verification] ⚠️ No sessions found after connection error retry for {number}, rejecting")
                                        other_sessions = []
                                        connected = False
                                        session_valid = False
                                        try:
                                            await client.disconnect()
                                        except:
                                            pass
                                except Exception as auth_check_err:
                                    error_message = "تم استخراج جلسة البوت من الحساب"
                                    verification_status = False
                                    print(f"[Verification] ⚠️ Failed to check authorizations after connection error retry for {number}: {auth_check_err}, rejecting")
                                    other_sessions = []
                                    connected = False
                                    session_valid = False
                                    try:
                                        await client.disconnect()
                                    except:
                                        pass
                        except Exception as retry_err2:
                            error_message = "تم استخراج جلسة البوت من الحساب"
                            verification_status = False
                            print(f"[Verification] ⚠️ Connection failed for {number}: {retry_err2}, rejecting")
                            other_sessions = []
                            connected = False
                            session_valid = False
                            try:
                                await client.disconnect()
                            except:
                                pass
                
                if not connected or not session_valid:
                    # ✅ إذا لم يتصل أو الجلسة غير صالحة، نرفض الرقم ونتابع إلى قسم الرفض
                    # ✅ error_message و verification_status تم تعيينهما بالفعل في except blocks
                    pass
                else:
                        # ✅ الاتصال نجح - التحقق من الجلسة
                        if not await client.is_user_authorized():
                            error_message = f"الجلسة غير صالحة للرقم {number}"
                            verification_status = False
                            print(f"[Verification] ⚠️ Session not authorized for {number}, rejecting immediately")
                            other_sessions = []  # تعريف فارغ لتجنب الخطأ
                        else:
                            try:
                                auths = await client(functions.account.GetAuthorizationsRequest())
                                # ✅ التحقق من جلسة البوت - إذا تم حذفها، رفض الرقم فوراً
                                if not auths or not auths.authorizations:
                                    error_message = "لا توجد جلسات في الحساب"
                                    verification_status = False
                                    print(f"[Verification] ⚠️ No authorizations found for {number}, rejecting immediately")
                                    other_sessions = []  # تعريف فارغ لتجنب الخطأ
                                else:
                                    # ✅ التحقق من جلسة البوت بشكل أدق
                                    current_session_exists = any(auth.current for auth in auths.authorizations)
                                    print(f"[Verification] Checking bot session for {number}: current_session_exists={current_session_exists}, total_sessions={len(auths.authorizations)}")
                                    
                                    if not current_session_exists:
                                        # ✅ تحقق مرة أخرى - قد يكون هناك تأخير في التحديث
                                        await asyncio.sleep(1)
                                        auths_check = await client(functions.account.GetAuthorizationsRequest())
                                        current_session_exists_recheck = any(auth.current for auth in auths_check.authorizations)
                                        print(f"[Verification] Rechecking bot session for {number}: current_session_exists_recheck={current_session_exists_recheck}")
                                        
                                        if not current_session_exists_recheck:
                                            # ✅ تم حذف جلسة البوت - رفض الرقم فوراً
                                            error_message = "تم استخراج جلسة البوت من الحساب"
                                            verification_status = False
                                            print(f"[Verification] ⚠️ Bot session was deleted for {number}, rejecting immediately")
                                            # ✅ إنهاء الاتصال فوراً دون محاولة حذف جلسات أخرى
                                            try:
                                                await client.disconnect()
                                            except:
                                                pass
                                            # ✅ الانتقال مباشرة لإرسال رسالة الرفض - تخطي باقي الكود
                                            other_sessions = []  # تعريف فارغ لتجنب الخطأ
                                        else:
                                            # ✅ الجلسة موجودة بعد إعادة التحقق - متابعة العملية
                                            print(f"[Verification] ✅ Bot session exists after recheck for {number}, continuing verification")
                                            auths = auths_check
                                    else:
                                        # ✅ الجلسة موجودة - متابعة العملية
                                        print(f"[Verification] ✅ Bot session exists for {number}, continuing verification")
                                    
                                    # ✅ التحقق من أن الجلسة موجودة فعلياً قبل المتابعة
                                    final_check = current_session_exists
                                    if not current_session_exists and 'current_session_exists_recheck' in locals():
                                        final_check = current_session_exists_recheck
                                        if final_check:
                                            auths = auths_check
                                    
                                    if final_check:
                                        # ✅ الجلسة موجودة - متابعة التحقق
                                        # ✅ التحقق من الجلسات - إذا كان هناك جلسات أخرى غير جلسة البوت
                                        other_sessions = [auth for auth in auths.authorizations if not auth.current]
                                        
                                        # ✅ بعد انتهاء الوقت الأصلي - التحقق من الجلسات مرة أخرى إذا كان الرقم في قائمة الانتظار
                                        if number in pending_session_deletions:
                                            deletion_time = pending_session_deletions[number]
                                            current_time = time.time()
                                        
                                            # ✅ إذا لم تمر 24 ساعة بعد، تحقق من الجلسات مرة أخرى (ربما تم حذفها من قبل المستخدم)
                                            if current_time < deletion_time:
                                                # ✅ التحقق من الجلسات مرة أخرى
                                                await asyncio.sleep(2)
                                                auths_recheck = await client(functions.account.GetAuthorizationsRequest())
                                                other_sessions_recheck = [auth for auth in auths_recheck.authorizations if not auth.current]
                                                
                                                if len(other_sessions_recheck) == 0:
                                                    # ✅ لا توجد جلسات أخرى الآن - تأكيد الرقم مباشرة
                                                    verification_status = True
                                                    # حذف الرقم من قائمة الانتظار
                                                    del pending_session_deletions[number]
                                                    save_pending_session_deletions()  # ✅ حفظ في الملف
                                                    # ✅ حذف الرقم من pending_confirmations أيضاً
                                                    if user_id in pending_confirmations and number in pending_confirmations[user_id]:
                                                        del pending_confirmations[user_id][number]
                                                        if len(pending_confirmations[user_id]) == 0:
                                                            del pending_confirmations[user_id]
                                                    # ✅ استخدام other_sessions للكود التالي
                                                    other_sessions = []
                                                    # ✅ إضافة الرصيد وإرسال الإشعارات مباشرة
                                                    if user_id not in users_db:
                                                        users_db[user_id] = {"balance": 0, "numbers": [], "language": "ar"}
                                                    if number not in users_db[user_id]['numbers']:
                                                        users_db[user_id]['numbers'].append(number)
                                                    users_db[user_id]['balance'] += price
                                                    save_db()
                                                    # ✅ إضافة الرقم إلى delivered_numbers عند التأكيد
                                                    if number not in delivered_numbers:
                                                        delivered_numbers.append(number)
                                                        save_delivered_numbers()
                                                        print(f"[Verification] Added {number} to delivered_numbers after successful verification")
                                                    
                                                    # ✅ تغيير كلمة المرور إلى الكلمة الثابتة بعد التأكيد
                                                    # ✅ إذا فشل تغيير كلمة المرور بسبب "Cannot send requests while disconnected"، لا نرفض الرقم
                                                    try:
                                                        # ✅ التأكد من أن العميل متصل قبل محاولة تغيير كلمة المرور
                                                        if not client.is_connected():
                                                            await client.connect()
                                                        
                                                        print(f"[Password Change] Attempting to change password for {number} to fixed password: {m}")
                                                        if twofa_password:
                                                            try:
                                                                await client.edit_2fa(current_password=twofa_password, new_password=m, hint=m2)
                                                                print(f"Password changed to fixed password for {number} (after confirmation)")
                                                            except Exception as e1:
                                                                error_str = str(e1)
                                                                if "Cannot send requests while disconnected" in error_str or "disconnected" in error_str.lower():
                                                                    # ✅ محاولة إعادة الاتصال
                                                                    try:
                                                                        if not client.is_connected():
                                                                            await client.connect()
                                                                        await client.edit_2fa(current_password=twofa_password, new_password=m, hint=m2)
                                                                        print(f"Password changed to fixed password for {number} (after reconnection)")
                                                                    except:
                                                                        print(f"Error changing password with old password for {number} (after confirmation): {e1}")
                                                                else:
                                                                    print(f"Error changing password with old password for {number} (after confirmation): {e1}")
                                                                    try:
                                                                        await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                                        print(f"Password set to fixed password for {number} (after confirmation)")
                                                                    except Exception as e2:
                                                                        print(f"Error setting password for {number} (after confirmation): {e2}")
                                                        else:
                                                            try:
                                                                await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                                print(f"Password set to fixed password for {number} (after confirmation)")
                                                            except Exception as e:
                                                                error_str = str(e)
                                                                if "Cannot send requests while disconnected" in error_str or "disconnected" in error_str.lower():
                                                                    # ✅ محاولة إعادة الاتصال
                                                                    try:
                                                                        if not client.is_connected():
                                                                            await client.connect()
                                                                        await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                                        print(f"Password set to fixed password for {number} (after reconnection)")
                                                                    except:
                                                                        print(f"Error setting password for {number} (after confirmation): {e}")
                                                                else:
                                                                    print(f"Error setting password for {number} (after confirmation): {e}")
                                                    except Exception as e:
                                                        error_str = str(e)
                                                        if "Cannot send requests while disconnected" in error_str or "disconnected" in error_str.lower():
                                                            # ✅ محاولة إعادة الاتصال
                                                            try:
                                                                if not client.is_connected():
                                                                    await client.connect()
                                                                # ✅ إعادة المحاولة
                                                                if twofa_password:
                                                                    try:
                                                                        await client.edit_2fa(current_password=twofa_password, new_password=m, hint=m2)
                                                                        print(f"Password changed to fixed password for {number} (after reconnection)")
                                                                    except:
                                                                        await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                                        print(f"Password set to fixed password for {number} (after reconnection)")
                                                                else:
                                                                    await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                                    print(f"Password set to fixed password for {number} (after reconnection)")
                                                            except:
                                                                print(f"Error in password change process for {number} (after confirmation): {e}")
                                                        else:
                                                            print(f"Error in password change process for {number} (after confirmation): {e}")
                                                    
                                                    # ✅ رسالة للقناة
                                                    user_name = message.from_user.first_name
                                                    user_uname = message.from_user.username or "N/A"
                                                    me = await client.get_me()
                                                    first_name = getattr(me, 'first_name', 'N/A')
                                                    last_name = getattr(me, 'last_name', 'N/A')
                                                    username = getattr(me, 'username', 'N/A')
                                                    
                                                    msg = f"""✅ تم التحقق بنجاح (بعد حذف الجلسات)

المستخدم: {user_name} (@{user_uname})
ID المستخدم: {user_id}
اسم الحساب: {first_name} {last_name}
Username: @{username if username != 'N/A' else 'N/A'}
الرقم: {number}
السعر: {price} $
الرصيد الجديد: {users_db[user_id]['balance']:.2f} $
الدولة: {country_code}
الجهاز: {device_name} ({device_system})
التاريخ والوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                                                    try:
                                                        try:
                                                            chat = await app.get_chat(gg)
                                                            await app.send_message(chat.id, msg)
                                                        except:
                                                            await app.send_message(gg, msg)
                                                    except Exception as e:
                                                        print(f"Error sending to channel: {e}")
                                                    
                                                    # ✅ إشعار للمستخدم
                                                    user_language = users_db[user_id].get('language', 'ar')
                                                    user_translation = translations.get(user_language, translations['ar'])
                                                    success_message = user_translation.get('balance_added', '🎉 تم إضافة الرقم بنجاح {number}\n\nتم إضافة {price} $ إلى رصيدك\nالرصيد الحالي: {balance} $').format(
                                                        number=number,
                                                        price=price,
                                                        balance=users_db[user_id]['balance']
                                                    )
                                                    try:
                                                        await app.send_message(int(user_id), success_message)
                                                    except:
                                                        pass
                                                    
                                                    # ✅ إنهاء الدالة بعد التأكيد
                                                    return
                                            else:
                                                # ✅ لا تزال هناك جلسات - استخدام الجلسات الجديدة
                                                other_sessions = other_sessions_recheck
                                    
                                    # ✅ التحقق من الجلسات الأخرى إذا كانت موجودة
                                    if len(other_sessions) > 0:
                                        # ✅ محاولة حذف الجلسات الأخرى مباشرة في المرحلة الأولى
                                        deleted_count = 0
                                        for auth in other_sessions:
                                            try:
                                                await client(functions.account.ResetAuthorizationRequest(hash=auth.hash))
                                                deleted_count += 1
                                            except Exception as e:
                                                print(f"Error deleting session {auth.hash} for {number}: {e}")
                                        
                                        # ✅ التحقق مرة أخرى بعد الحذف
                                        await asyncio.sleep(2)  # انتظار قليل للتأكد من الحذف
                                        auths_after = await client(functions.account.GetAuthorizationsRequest())
                                        other_sessions_after = [auth for auth in auths_after.authorizations if not auth.current]
                                        
                                        # ✅ إذا تم حذف جميع الجلسات في المرحلة الأولى، متابعة التحقق
                                        if len(other_sessions_after) == 0:
                                            verification_status = True
                                            # حذف الرقم من قائمة الانتظار إذا كان موجوداً
                                            if number in pending_session_deletions:
                                                del pending_session_deletions[number]
                                                save_pending_session_deletions()  # ✅ حفظ في الملف
                                            # ✅ حذف الرقم من pending_confirmations أيضاً
                                            if user_id in pending_confirmations and number in pending_confirmations[user_id]:
                                                del pending_confirmations[user_id][number]
                                                if len(pending_confirmations[user_id]) == 0:
                                                    del pending_confirmations[user_id]
                                            # ✅ إضافة الرصيد وإرسال الإشعارات مباشرة
                                            if user_id not in users_db:
                                                users_db[user_id] = {"balance": 0, "numbers": [], "language": "ar"}
                                            if number not in users_db[user_id]['numbers']:
                                                users_db[user_id]['numbers'].append(number)
                                            users_db[user_id]['balance'] += price
                                            save_db()
                                            # ✅ إضافة الرقم إلى delivered_numbers عند التأكيد
                                            if number not in delivered_numbers:
                                                delivered_numbers.append(number)
                                                save_delivered_numbers()
                                                print(f"[Verification] Added {number} to delivered_numbers after successful verification")
                                            
                                            # ✅ تغيير كلمة المرور إلى الكلمة الثابتة بعد التأكيد
                                            # ✅ إذا فشل تغيير كلمة المرور بسبب "Cannot send requests while disconnected"، لا نرفض الرقم
                                            try:
                                                # ✅ التأكد من أن العميل متصل قبل محاولة تغيير كلمة المرور
                                                if not client.is_connected():
                                                    await client.connect()
                                                
                                                print(f"[Password Change] Attempting to change password for {number} to fixed password: {m}")
                                                if twofa_password:
                                                    try:
                                                        await client.edit_2fa(current_password=twofa_password, new_password=m, hint=m2)
                                                        print(f"Password changed to fixed password for {number} (after confirmation)")
                                                    except Exception as e1:
                                                        error_str = str(e1)
                                                        if "Cannot send requests while disconnected" in error_str or "disconnected" in error_str.lower():
                                                            # ✅ محاولة إعادة الاتصال
                                                            try:
                                                                if not client.is_connected():
                                                                    await client.connect()
                                                                await client.edit_2fa(current_password=twofa_password, new_password=m, hint=m2)
                                                                print(f"Password changed to fixed password for {number} (after reconnection)")
                                                            except:
                                                                print(f"Error changing password with old password for {number} (after confirmation): {e1}")
                                                        else:
                                                            print(f"Error changing password with old password for {number} (after confirmation): {e1}")
                                                            try:
                                                                await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                                print(f"Password set to fixed password for {number} (after confirmation)")
                                                            except Exception as e2:
                                                                print(f"Error setting password for {number} (after confirmation): {e2}")
                                                else:
                                                    try:
                                                        await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                        print(f"Password set to fixed password for {number} (after confirmation)")
                                                    except Exception as e:
                                                        error_str = str(e)
                                                        if "Cannot send requests while disconnected" in error_str or "disconnected" in error_str.lower():
                                                            # ✅ محاولة إعادة الاتصال
                                                            try:
                                                                if not client.is_connected():
                                                                    await client.connect()
                                                                await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                                print(f"Password set to fixed password for {number} (after reconnection)")
                                                            except:
                                                                print(f"Error setting password for {number} (after confirmation): {e}")
                                                        else:
                                                            print(f"Error setting password for {number} (after confirmation): {e}")
                                            except Exception as e:
                                                error_str = str(e)
                                                if "Cannot send requests while disconnected" in error_str or "disconnected" in error_str.lower():
                                                    # ✅ محاولة إعادة الاتصال
                                                    try:
                                                        if not client.is_connected():
                                                            await client.connect()
                                                        # ✅ إعادة المحاولة
                                                        if twofa_password:
                                                            try:
                                                                await client.edit_2fa(current_password=twofa_password, new_password=m, hint=m2)
                                                                print(f"Password changed to fixed password for {number} (after reconnection)")
                                                            except:
                                                                await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                                print(f"Password set to fixed password for {number} (after reconnection)")
                                                        else:
                                                            await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                            print(f"Password set to fixed password for {number} (after reconnection)")
                                                    except:
                                                        print(f"Error in password change process for {number} (after confirmation): {e}")
                                                else:
                                                    print(f"Error in password change process for {number} (after confirmation): {e}")
                                            
                                            # ✅ رسالة للقناة
                                            user_name = message.from_user.first_name
                                            user_uname = message.from_user.username or "N/A"
                                            me = await client.get_me()
                                            first_name = getattr(me, 'first_name', 'N/A')
                                            last_name = getattr(me, 'last_name', 'N/A')
                                            username = getattr(me, 'username', 'N/A')
                                            
                                            msg = f"""✅ تم التحقق بنجاح (بعد حذف الجلسات)

المستخدم: {user_name} (@{user_uname})
ID المستخدم: {user_id}
اسم الحساب: {first_name} {last_name}
Username: @{username if username != 'N/A' else 'N/A'}
الرقم: {number}
السعر: {price} $
الرصيد الجديد: {users_db[user_id]['balance']:.2f} $
الدولة: {country_code}
الجهاز: {device_name} ({device_system})
التاريخ والوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                                            try:
                                                try:
                                                    chat = await app.get_chat(gg)
                                                    await app.send_message(chat.id, msg)
                                                except:
                                                    await app.send_message(gg, msg)
                                            except Exception as e:
                                                print(f"Error sending to channel: {e}")
                                            
                                            # ✅ إشعار للمستخدم
                                            user_language = users_db[user_id].get('language', 'ar')
                                            user_translation = translations.get(user_language, translations['ar'])
                                            success_message = user_translation.get('balance_added', '🎉 تم إضافة الرقم بنجاح {number}\n\nتم إضافة {price} $ إلى رصيدك\nالرصيد الحالي: {balance} $').format(
                                                number=number,
                                                price=price,
                                                balance=users_db[user_id]['balance']
                                            )
                                            try:
                                                await app.send_message(int(user_id), success_message)
                                            except:
                                                pass
                                            
                                            # ✅ إنهاء الدالة بعد التأكيد
                                            return
                                        else:
                                            # ✅ لم يتم حذف جميع الجلسات في المرحلة الأولى
                                            # ✅ إضافة الرقم لقائمة الانتظار لمدة 24 ساعة لمحاولة الحذف مرة أخرى
                                            deletion_time = time.time() + (24 * 3600)  # 24 ساعة
                                            pending_session_deletions[number] = deletion_time
                                            save_pending_session_deletions()  # ✅ حفظ في الملف
                                            # ✅ حفظ string_session و twofa_password في device_data
                                            if user_id not in users_db:
                                                users_db[user_id] = {}
                                            if 'devices' not in users_db[user_id]:
                                                users_db[user_id]['devices'] = {}
                                            if number not in users_db[user_id]['devices']:
                                                users_db[user_id]['devices'][number] = {}
                                            users_db[user_id]['devices'][number]['string_session'] = string_session
                                            # ✅ حفظ twofa_password إذا كان موجوداً
                                            if twofa_password:
                                                users_db[user_id]['devices'][number]['twofa_password'] = twofa_password
                                            save_db()
                                            # ✅ حساب الوقت المتبقي (24 ساعة)
                                            remaining_seconds = int(deletion_time - time.time())
                                            remaining_hours = remaining_seconds // 3600
                                            remaining_minutes = (remaining_seconds % 3600) // 60
                                            remaining_secs = remaining_seconds % 60
                                            
                                            time_str = f"{remaining_hours:02d}:{remaining_minutes:02d}:{remaining_secs:02d}"
                                            error_message = f"يوجد جلسات أخرى ({len(other_sessions_after)} جلسة). لم يتم حذفها مباشرة. سيتم محاولة حذفها تلقائياً بعد:\n⏰ الوقت المتبقي: {time_str}\nيرجى المحاولة مرة أخرى بعد انتهاء الوقت"
                                            verification_status = False
                                            # ✅ إنهاء الدالة - عدم التأكيد (سيتم التحقق من الجلسات بعد 24 ساعة في check_pending_deletions)
                                            try:
                                                await client.disconnect()
                                            except:
                                                pass
                                            return
                            except Exception as e:
                                verification_status = False
                                error_message = f"خطأ في التحقق: {str(e)}"
                                print(f"Verification error for {number}: {e}")
                            finally:
                                # ✅ إغلاق العميل بشكل صحيح في جميع الحالات
                                try:
                                    if 'client' in locals():
                                        await client.disconnect()
                                except:
                                    pass
                        # ✅ إذا لم يكن هناك جلسات أخرى في البداية - تأكيد الرقم فقط عندما لا توجد جلسات أخرى
                        if 'other_sessions' not in locals():
                            other_sessions = []
                        # ✅ التحقق النهائي: لا يتم التأكيد إلا إذا كانت جلسة البوت وحده (لا توجد جلسات أخرى)
                        if len(other_sessions) == 0:
                            # ✅ لا توجد جلسات أخرى - تأكيد الرقم تلقائياً
                            verification_status = True
                        else:
                            # ✅ لا يزال هناك جلسات أخرى - عدم التأكيد (يجب أن يتم التعامل معها في الكود أعلاه)
                            verification_status = False
                            error_message = f"يوجد جلسات أخرى ({len(other_sessions)} جلسة)، لا يمكن تأكيد الرقم"
                        # ✅ حذف الرقم من pending_confirmations
                        if user_id in pending_confirmations and number in pending_confirmations[user_id]:
                            del pending_confirmations[user_id][number]
                            if len(pending_confirmations[user_id]) == 0:
                                del pending_confirmations[user_id]
                        # ✅ إضافة الرصيد للمستخدم تلقائياً
                        if user_id not in users_db:
                            users_db[user_id] = {"balance": 0, "numbers": [], "language": "ar"}
                        if number not in users_db[user_id]['numbers']:
                            users_db[user_id]['numbers'].append(number)
                        users_db[user_id]['balance'] += price
                        save_db()
                        # ✅ إضافة الرقم إلى delivered_numbers عند التأكيد
                        if number not in delivered_numbers:
                            delivered_numbers.append(number)
                            save_delivered_numbers()
                            print(f"[Verification] Added {number} to delivered_numbers after successful verification")
                        
                        # ✅ تغيير كلمة المرور إلى الكلمة الثابتة
                        # ✅ إذا فشل تغيير كلمة المرور بسبب "Cannot send requests while disconnected"، لا نرفض الرقم
                        try:
                            # ✅ التأكد من أن العميل متصل قبل محاولة تغيير كلمة المرور
                            if not client.is_connected():
                                await client.connect()
                            
                            print(f"[Password Change] Attempting to change password for {number} to fixed password: {m}")
                            if twofa_password:
                                try:
                                    await client.edit_2fa(current_password=twofa_password, new_password=m, hint=m2)
                                    print(f"Password changed to fixed password for {number}")
                                except Exception as e1:
                                    error_str = str(e1)
                                    if "Cannot send requests while disconnected" in error_str or "disconnected" in error_str.lower():
                                        # ✅ محاولة إعادة الاتصال
                                        try:
                                            if not client.is_connected():
                                                await client.connect()
                                            await client.edit_2fa(current_password=twofa_password, new_password=m, hint=m2)
                                            print(f"Password changed to fixed password for {number} (after reconnection)")
                                        except:
                                            print(f"Error changing password with old password for {number}: {e1}")
                                    else:
                                        print(f"Error changing password with old password for {number}: {e1}")
                                        try:
                                            await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                            print(f"Password set to fixed password for {number}")
                                        except Exception as e2:
                                            print(f"Error setting password for {number}: {e2}")
                            else:
                                try:
                                    await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                    print(f"Password set to fixed password for {number}")
                                except Exception as e:
                                    error_str = str(e)
                                    if "Cannot send requests while disconnected" in error_str or "disconnected" in error_str.lower():
                                        # ✅ محاولة إعادة الاتصال
                                        try:
                                            if not client.is_connected():
                                                await client.connect()
                                            await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                            print(f"Password set to fixed password for {number} (after reconnection)")
                                        except:
                                            print(f"Error setting password for {number}: {e}")
                                    else:
                                        print(f"Error setting password for {number}: {e}")
                        except Exception as e:
                            error_str = str(e)
                            if "Cannot send requests while disconnected" in error_str or "disconnected" in error_str.lower():
                                # ✅ محاولة إعادة الاتصال
                                try:
                                    if not client.is_connected():
                                        await client.connect()
                                    # ✅ إعادة المحاولة
                                    if twofa_password:
                                        try:
                                            await client.edit_2fa(current_password=twofa_password, new_password=m, hint=m2)
                                            print(f"Password changed to fixed password for {number} (after reconnection)")
                                        except:
                                            await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                            print(f"Password set to fixed password for {number} (after reconnection)")
                                    else:
                                        await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                        print(f"Password set to fixed password for {number} (after reconnection)")
                                except:
                                    print(f"Error in password change process for {number}: {e}")
                            else:
                                print(f"Error in password change process for {number}: {e}")

                        # ✅ رسالة للقناة - استخدام معرف القناة الصحيح
                        user_name = message.from_user.first_name
                        user_uname = message.from_user.username or "N/A"
                        me = await client.get_me()
                        first_name = getattr(me, 'first_name', 'N/A')
                        last_name = getattr(me, 'last_name', 'N/A')
                        username = getattr(me, 'username', 'N/A')
                        
                        msg = f"""✅ تم التحقق بنجاح
        
المستخدم: {user_name} (@{user_uname})
ID المستخدم: {user_id}
اسم الحساب: {first_name} {last_name}
Username: @{username if username != 'N/A' else 'N/A'}
        الرقم: {number}
السعر: {price} $
الرصيد الجديد: {users_db[user_id]['balance']:.2f} $
الدولة: {country_code}
الجهاز: {device_name} ({device_system})
التاريخ والوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                        # ✅ محاولة إرسال للقناة
                        channel_sent = False
                        try:
                            try:
                                chat = await app.get_chat(gg)
                                await app.send_message(chat.id, msg)
                                channel_sent = True
                            except Exception as e_chat:
                                await app.send_message(gg, msg)
                                channel_sent = True
                        except Exception as e1:
                            error_str = str(e1).lower()
                            print(f"Error sending to channel {gg}: {e1}")
                            try:
                                chat = await app.get_chat(gg)
                                if hasattr(chat, 'username') and chat.username:
                                    await app.send_message(f"@{chat.username}", msg)
                                    channel_sent = True
                                else:
                                    raise e1
                            except Exception as e2:
                                try:
                                    error_details = f"""⚠️ خطأ في إرسال رسالة للقناة

معرف القناة: {gg}
الخطأ: {str(e1)}

🔧 الحلول الممكنة:
1. تأكد أن البوت عضو في القناة (أضف البوت كعضو وليس فقط أدمن)
2. تأكد أن البوت لديه صلاحية "Post Messages" في القناة
3. تأكد من صحة معرف القناة
4. جرب استخدام username القناة بدلاً من ID

الرسالة:
{msg}"""
                                    await app.send_message(owner_id, error_details)
                                except:
                                    pass

                        # ✅ إشعار للمستخدم بالتأكيد
                        user_language = users_db[user_id].get('language', 'ar')
                        user_translation = translations.get(user_language, translations['ar'])
                        success_message = user_translation.get('balance_added', '🎉 تم إضافة الرقم بنجاح {number}\n\nتم إضافة {price} $ إلى رصيدك\nالرصيد الحالي: {balance} $').format(
                            number=number,
                            price=price,
                            balance=users_db[user_id]['balance']
                        )
                        try:
                            await app.send_message(int(user_id), success_message)
                        except:
                            pass
            except Exception as e:
                verification_status = False
                error_message = f"خطأ في التحقق: {str(e)}"
                print(f"Verification error for {number}: {e}")
                # ✅ إغلاق العميل في حالة الخطأ
                try:
                    if 'client' in locals():
                        await client.disconnect()
                except:
                    pass
            finally:
                # ✅ إغلاق العميل بشكل صحيح في جميع الحالات
                try:
                    if 'client' in locals():
                        await client.disconnect()
                except:
                    pass
    except Exception as e:
        verification_status = False
        error_message = f"خطأ في الاتصال: {str(e)}"
        print(f"Connection error for {number}: {e}")

    # ✅ إرسال إشعار الرفض للمستخدم في حالة الفشل
    if not verification_status:
        # ✅ التحقق إذا كان الرقم في قائمة الانتظار ولم تمر 24 ساعة - لا نرفضه ولا نحذف جلسة البوت
        should_reject = True
        if number in pending_session_deletions:
            deletion_time = pending_session_deletions[number]
            current_time = time.time()
            if current_time < deletion_time:
                # ✅ الرقم في قائمة الانتظار ولم تمر 24 ساعة - لا نرفضه ولا نحذف جلسة البوت
                should_reject = False
                print(f"[Verification] Number {number} is in pending deletions, not rejecting yet. Remaining time: {int(deletion_time - current_time)} seconds")
        
        if not should_reject:
            # ✅ الرقم في قائمة الانتظار، لا نرفضه ولا ننشئ كلمة مرور ولا نحذف جلسة البوت
            return
        
        # ✅ إنشاء كلمة مرور عشوائية
        def generate_random_password(length=8):
            """إنشاء كلمة مرور عشوائية"""
            characters = string.ascii_letters + string.digits
            return ''.join(random.choice(characters) for _ in range(length))
        
        random_password = generate_random_password()
        
        # ✅ إنهاء جلسة البوت فقط وإنشاء كلمة مرور
        # ✅ إذا كانت رسالة الخطأ "تم استخراج جلسة البوت من الحساب"، لا نحاول الاتصال مرة أخرى
        if error_message and "تم استخراج جلسة البوت من الحساب" in error_message:
            print(f"[Rejection] Skipping connection attempt for {number} - bot session already deleted")
        else:
            try:
                proxy = get_proxy_for_number(number)
                async with TelegramClient(
                    StringSession(string_session), 
                    api_id, 
                    api_hash,
                    device_model=device_name,
                    system_version=device_system,
                    app_version=device_app,
                    lang_code='en',
                    system_lang_code='en-US',
                    proxy=proxy
                ) as client:
                    try:
                        # ✅ استخدام timeout لمنع انتظار bot token
                        await asyncio.wait_for(client.connect(), timeout=10.0)
                    except (asyncio.TimeoutError, Exception) as connect_err:
                        print(f"[Rejection] Connection failed/timeout for {number} during rejection: {connect_err}")
                        # ✅ إذا فشل الاتصال، نتابع بدون تغيير كلمة المرور أو إنهاء الجلسة
                    else:
                        if await client.is_user_authorized():
                            # ✅ إنشاء كلمة مرور عشوائية للرقم المرفوض أولاً (قبل إنهاء الجلسة)
                            try:
                                if twofa_password:
                                    try:
                                        await client.edit_2fa(current_password=twofa_password, new_password=random_password, hint=m2)
                                        print(f"Password changed successfully for {number}")
                                    except Exception as e1:
                                        print(f"Error changing password with old password for {number}: {e1}")
                                        try:
                                            await client.edit_2fa(current_password=None, new_password=random_password, hint=m2)
                                        except Exception as e2:
                                            print(f"Error changing password without old password for {number}: {e2}")
                                else:
                                    try:
                                        await client.edit_2fa(current_password=None, new_password=random_password, hint=m2)
                                        print(f"Password created successfully for {number}")
                                    except Exception as e:
                                        print(f"Error creating password for {number}: {e}")
                            except Exception as e:
                                print(f"Error in password process for {number}: {e}")
                            
                            # ✅ إنهاء جلسة البوت فقط (Logout) - بعد تغيير كلمة المرور
                            try:
                                await client.log_out()
                                print(f"Bot session ended successfully for {number}")
                            except Exception as e:
                                print(f"Error ending bot session for {number}: {e}")
                            try:
                                await client.disconnect()
                            except:
                                pass
                        else:
                            # ✅ الجلسة غير صالحة - لا نحاول تغيير كلمة المرور
                            print(f"[Rejection] Session not authorized for {number}, skipping password change")
                            try:
                                await client.disconnect()
                            except:
                                pass
            except Exception as e:
                print(f"Error in reject process for {number}: {e}")
        
        user_language = users_db.get(user_id, {}).get('language', 'ar')
        user_translation = translations.get(user_language, translations['ar'])
        
        # تحديد إذا كان السبب متعلقًا بعدم وجود جلسة البوت
        bot_session_missing = (
            error_message and (
                "تم استخراج جلسة البوت من الحساب" in error_message or
                "لا توجد جلسات في الحساب" in error_message
            )
        )

        if bot_session_missing:
            reject_message = f"""❌ تم رفض الرقم {number}

        السبب: {error_message if error_message else 'فشل التحقق من الحساب'}

        الرجاء المحاولة مرة أخرى."""
        else:
            reject_message = f"""❌ تم رفض الرقم {number}
        السبب: {error_message if error_message else 'فشل التحقق من الحساب'}
        🔑 كلمة المرور الجديدة: `{random_password}`
        ⚠️ تم إنهاء جلسة البوت تلقائياً
        الرجاء المحاولة مرة أخرى."""     
               
        try:
            await app.send_message(int(user_id), reject_message)
        except:
            pass
        
        # ✅ رسالة للقناة - رفض الرقم
        user_name = message.from_user.first_name
        user_uname = message.from_user.username or "N/A"
        reject_channel_msg = f"""❌ تم رفض الرقم

المستخدم: {user_name} (@{user_uname})
ID المستخدم: {user_id}
الرقم: {number}
السبب: {error_message if error_message else 'فشل التحقق من الحساب'}
كلمة المرور الجديدة: {random_password}
التاريخ والوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        try:
            try:
                chat = await app.get_chat(gg)
                await app.send_message(chat.id, reject_channel_msg)
            except:
                await app.send_message(gg, reject_channel_msg)
        except Exception as e:
            print(f"Error sending rejection to channel: {e}")


# ✅ Callback handler لزر "You will get"
@bot.on_callback_query(filters.regex(r"show_balance_(.+)_(.+)"))
async def show_remaining_time(client, callback_query):
    import re
    user_id = str(callback_query.from_user.id)
    match = re.match(r"show_balance_(.+)_(.+)", callback_query.data)
    if not match:
        return
    
    number = match.group(1)
    price = match.group(2)
    
    user_language = users_db.get(user_id, {}).get('language', 'ar')
    translation = translations.get(user_language, translations['ar'])

    # ✅ التحقق من الوقت المتبقي لحذف الجلسات أولاً (أولوية أعلى)
    if number in pending_session_deletions:
        deletion_time = pending_session_deletions[number]
        current_time = time.time()
        remaining_seconds = int(deletion_time - current_time)
        if remaining_seconds > 0:
            # ✅ تنسيق الوقت المتبقي
            hours = remaining_seconds // 3600
            minutes = (remaining_seconds % 3600) // 60
            secs = remaining_seconds % 60
            time_str = f"{hours:02d}:{minutes:02d}:{secs:02d}"
            await client.answer_callback_query(
                callback_query.id,
                f"⏰ الوقت المتبقي لحذف الجلسات: {time_str}",
                show_alert=True
            )
        else:
            # ✅ انتهى وقت الانتظار - التحقق من التأكيد
            if user_id in users_db and 'numbers' in users_db[user_id] and number in users_db[user_id]['numbers']:
                await client.answer_callback_query(
                    callback_query.id,
                    translation.get('number_confirmed', '✅ تم تأكيد الرقم بنجاح'),
                    show_alert=True
                )
            else:
                await client.answer_callback_query(
                    callback_query.id,
                    "⏰ انتهى وقت الانتظار. يمكنك المحاولة مرة أخرى الآن.",
                    show_alert=True
                )
    # ✅ التحقق من الوقت المتبقي للتحقق من الرقم (فقط إذا لم يكن في قائمة الانتظار لحذف الجلسات)
    elif user_id in pending_confirmations and number in pending_confirmations[user_id]:
        end_time = pending_confirmations[user_id][number]
        current_time = time.time()
        remaining_seconds = int(end_time - current_time)
        if remaining_seconds > 0:
            # ✅ تنسيق الوقت المتبقي
            hours = remaining_seconds // 3600
            minutes = (remaining_seconds % 3600) // 60
            secs = remaining_seconds % 60
            time_str = f"{hours:02d}:{minutes:02d}:{secs:02d}"
            await client.answer_callback_query(
                callback_query.id, 
                translation.get('remaining_time', 'الوقت المتبقي: {time}').format(time=time_str),
                show_alert=True
            )
        else:
            # ✅ إذا انتهى وقت التحقق، نتحقق أولاً من أن الرقم تم تأكيده
            if user_id in users_db and 'numbers' in users_db[user_id] and number in users_db[user_id]['numbers']:
                # ✅ الرقم تم تأكيده - عرض رسالة النجاح
                await client.answer_callback_query(
                    callback_query.id, 
                    translation.get('number_confirmed', '✅ تم تأكيد الرقم بنجاح'),
                    show_alert=True
                )
            # ✅ إذا لم يتم التأكيد بعد، نتحقق من قائمة الانتظار لحذف الجلسات
            elif number in pending_session_deletions:
                deletion_time = pending_session_deletions[number]
                remaining_seconds_session = int(deletion_time - current_time)
                if remaining_seconds_session > 0:
                    hours = remaining_seconds_session // 3600
                    minutes = (remaining_seconds_session % 3600) // 60
                    secs = remaining_seconds_session % 60
                    time_str = f"{hours:02d}:{minutes:02d}:{secs:02d}"
                    await client.answer_callback_query(
                        callback_query.id,
                        f"⏰ الوقت المتبقي لحذف الجلسات: {time_str}",
                        show_alert=True
                    )
                else:
                    # ✅ انتهى وقت الانتظار - التحقق من التأكيد مرة أخرى
                    if user_id in users_db and 'numbers' in users_db[user_id] and number in users_db[user_id]['numbers']:
                        await client.answer_callback_query(
                            callback_query.id, 
                            translation.get('number_confirmed', '✅ تم تأكيد الرقم بنجاح'),
                            show_alert=True
                        )
                    else:
                        await client.answer_callback_query(
                            callback_query.id,
                            "⏰ انتهى وقت الانتظار. يمكنك المحاولة مرة أخرى الآن.",
                            show_alert=True
                        )
            else:
                # ✅ التحقق من التأكيد مرة أخرى قبل عرض "انتهى الوقت"
                if user_id in users_db and 'numbers' in users_db[user_id] and number in users_db[user_id]['numbers']:
                    await client.answer_callback_query(
                        callback_query.id, 
                        translation.get('number_confirmed', '✅ تم تأكيد الرقم بنجاح'),
                        show_alert=True
                    )
                else:
                    await client.answer_callback_query(
                        callback_query.id, 
                        translation.get('time_elapsed', 'انتهى الوقت'),
                        show_alert=True
                    )
    else:
        # ✅ إذا لم يكن الرقم في أي من القوائم، حساب الوقت المتبقي من بيانات الدولة
        country_code = None
        for name, data in countries_db.items():
            if number.startswith(data.get('code', '')):
                country_code = name
                break
        
        if country_code:
            seconds = countries_db[country_code].get('seconds', 0)
            await client.answer_callback_query(
                callback_query.id, 
                translation.get('balance_info', 'سيتم إضافة {balance} إلى رصيدك لهذا الرقم').format(balance=price),
                show_alert=True
            )
        else:
            await client.answer_callback_query(
                callback_query.id, 
                translation.get('no_pending_confirmation', 'لا توجد عملية تأكيد قيد الانتظار لهذا الرقم.'),
                show_alert=True
            )


# ✅ دالة لإنشاء كلمة مرور عشوائية
def generate_random_password(length=8):
    """إنشاء كلمة مرور عشوائية"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# ✅ Background task للتحقق من pending_session_deletions
async def check_pending_deletions():
    """التحقق من الأرقام المعلقة ومحاولة حذف جلساتها بعد انتهاء الوقت"""
    global m, m2
    while True:
        try:
            await asyncio.sleep(60)  # التحقق كل دقيقة
            current_time = time.time()
            numbers_to_check = list(pending_session_deletions.keys())
            
            for number in numbers_to_check:
                if number not in pending_session_deletions:
                    continue
                deletion_time = pending_session_deletions[number]
                
                # إذا انتهى الوقت (24 ساعة)، حاول حذف الجلسات
                if current_time >= deletion_time:
                    print(f"[Pending Deletion] Checking {number} after waiting period (24 hours)")
                    
                    # البحث عن معلومات الرقم في users_db
                    user_id = None
                    for uid, user_data in users_db.items():
                        if 'devices' in user_data and number in user_data['devices']:
                            user_id = uid
                            break
                    
                    if not user_id:
                        print(f"[Pending Deletion] User ID not found for {number}, removing from list")
                        del pending_session_deletions[number]
                        save_pending_session_deletions()  # ✅ حفظ في الملف
                        continue
                    
                    print(f"[Pending Deletion] Found user_id: {user_id} for {number}")
                    
                    # جلب بيانات الجهاز والجلسة
                    device_data = users_db[user_id]['devices'].get(number)
                    if not device_data:
                        print(f"[Pending Deletion] Device data not found for {number}, rejecting")
                        del pending_session_deletions[number]
                        save_pending_session_deletions()  # ✅ حفظ في الملف
                        # رفض الرقم مع كلمة مرور عشوائية
                        await reject_number_after_24h(bot, user_id, number, "بيانات الجهاز غير موجودة")
                        continue
                    
                    string_session = device_data.get('string_session')
                    if not string_session:
                        print(f"[Pending Deletion] String session not found for {number}, rejecting")
                        del pending_session_deletions[number]
                        save_pending_session_deletions()  # ✅ حفظ في الملف
                        # رفض الرقم مع كلمة مرور عشوائية
                        await reject_number_after_24h(bot, user_id, number, "الجلسة غير موجودة")
                        continue
                    
                    api_id = device_data['API_ID']
                    api_hash = device_data['API_HASH']
                    device_name = device_data['name']
                    device_system = device_data['system']
                    device_app = device_data['app']
                    
                    print(f"[Pending Deletion] Attempting to delete sessions for {number}")
                    
                    # محاولة حذف الجلسات
                    try:
                        proxy = get_proxy_for_number(number)
                        # ✅ إنشاء client بدون async with لتجنب طلب bot token
                        client = TelegramClient(
                            StringSession(string_session),
                            api_id,
                            api_hash,
                            device_model=device_name,
                            system_version=device_system,
                            app_version=device_app,
                            lang_code='en',
                            system_lang_code='en-US',
                            proxy=proxy,
                            connection_retries=0,
                            retry_delay=0,
                            auto_reconnect=False
                        )
                        try:
                            print(f"[Pending Deletion] Connecting to Telegram for {number}")
                            # ✅ استخدام timeout للاتصال لمنع طلب bot token (5 ثوانٍ)
                            await asyncio.wait_for(client.connect(), timeout=5.0)
                            print(f"[Pending Deletion] Connected to Telegram for {number}")
                            
                            # ✅ التحقق من أن الجلسة صالحة
                            is_authorized = await client.is_user_authorized()
                            if not is_authorized:
                                # ✅ فحص أعمق باستخدام GetAuthorizationsRequest للتأكد من وجود جلسة البوت
                                try:
                                    auths = await client(functions.account.GetAuthorizationsRequest())
                                    current_session_exists = auths.current is not None
                                    if not current_session_exists:
                                        print(f"[Pending Deletion] Bot session not found for {number}, rejecting")
                                        del pending_session_deletions[number]
                                        save_pending_session_deletions()  # ✅ حفظ في الملف
                                        await client.disconnect()
                                        await reject_number_after_24h(bot, user_id, number, "تم استخراج جلسة البوت من الحساب")
                                        continue
                                    else:
                                        print(f"[Pending Deletion] Bot session exists for {number} (despite is_user_authorized=False), continuing")
                                        is_authorized = True
                                except Exception as auth_check_err:
                                    print(f"[Pending Deletion] Error checking authorizations for {number}: {auth_check_err}")
                                    await client.disconnect()
                                    del pending_session_deletions[number]
                                    save_pending_session_deletions()  # ✅ حفظ في الملف
                                    await reject_number_after_24h(bot, user_id, number, "فشل التحقق من الجلسة")
                                    continue
                            
                            if is_authorized:
                                print(f"[Pending Deletion] User authorized for {number}, checking sessions")
                                auths = await client(functions.account.GetAuthorizationsRequest())
                                other_sessions = [auth for auth in auths.authorizations if not auth.current]
                                
                                print(f"[Pending Deletion] Found {len(other_sessions)} other sessions for {number}")
                                
                                if len(other_sessions) > 0:
                                    # محاولة حذف الجلسات
                                    deleted_count = 0
                                    for auth in other_sessions:
                                        try:
                                            await client(functions.account.ResetAuthorizationRequest(hash=auth.hash))
                                            deleted_count += 1
                                            print(f"[Pending Deletion] Deleted session {auth.hash} for {number}")
                                        except Exception as e:
                                            print(f"[Pending Deletion] Error deleting session {auth.hash} for {number}: {e}")
                                    
                                    await asyncio.sleep(2)
                                    auths_final = await client(functions.account.GetAuthorizationsRequest())
                                    other_sessions_final = [auth for auth in auths_final.authorizations if not auth.current]
                                    
                                    print(f"[Pending Deletion] After deletion attempt: {len(other_sessions_final)} sessions remaining for {number}")
                                    
                                    if len(other_sessions_final) == 0:
                                        # نجح الحذف - تأكيد الرقم تلقائياً
                                        del pending_session_deletions[number]
                                        save_pending_session_deletions()  # ✅ حفظ في الملف
                                        # ✅ حذف الرقم من pending_confirmations أيضاً
                                        if user_id in pending_confirmations and number in pending_confirmations[user_id]:
                                            del pending_confirmations[user_id][number]
                                            # إذا لم يعد هناك أرقام معلقة للمستخدم، حذف المستخدم من القائمة
                                            if len(pending_confirmations[user_id]) == 0:
                                                del pending_confirmations[user_id]
                                        print(f"[Pending Deletion] Successfully deleted all sessions for {number}, confirming number")
                                        
                                        # ✅ إضافة الرصيد للمستخدم تلقائياً
                                        if user_id not in users_db:
                                            users_db[user_id] = {"balance": 0, "numbers": [], "language": "ar"}
                                        if number not in users_db[user_id]['numbers']:
                                            users_db[user_id]['numbers'].append(number)
                                        
                                        # جلب السعر من countries_db
                                        price = 0
                                        country_code = None
                                        for name, data in countries_db.items():
                                            if number.startswith(data.get('code', '')):
                                                country_code = name
                                                price = data.get('price', 0)
                                                break
                                        
                                        users_db[user_id]['balance'] += price
                                        save_db()
                                        # ✅ إضافة الرقم إلى delivered_numbers عند التأكيد
                                        if number not in delivered_numbers:
                                            delivered_numbers.append(number)
                                            save_delivered_numbers()
                                            print(f"[Pending Deletion] Added {number} to delivered_numbers after successful verification")
                                        
                                        # ✅ تغيير كلمة المرور إلى الكلمة الثابتة بعد التأكيد
                                        try:
                                            print(f"[Pending Deletion] Attempting to change password for {number} to fixed password: {m}")
                                            # محاولة الحصول على كلمة المرور القديمة من device_data إذا كانت موجودة
                                            old_password = device_data.get('twofa_password') or device_data.get('2fa_password')
                                            
                                            print(f"[Pending Deletion] Old password found in device_data: {bool(old_password)}")
                                            
                                            if old_password:
                                                try:
                                                    await client.edit_2fa(current_password=old_password, new_password=m, hint=m2)
                                                    print(f"[Pending Deletion] Password changed to fixed password for {number} (after 24h confirmation)")
                                                except Exception as e1:
                                                    print(f"[Pending Deletion] Error changing password with old password for {number} (after 24h confirmation): {e1}")
                                                    # محاولة بدون كلمة المرور القديمة (ربما تم تغييرها)
                                                    try:
                                                        await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                        print(f"[Pending Deletion] Password set to fixed password for {number} (after 24h confirmation) - without old password")
                                                    except Exception as e2:
                                                        print(f"[Pending Deletion] Error setting password for {number} (after 24h confirmation): {e2}")
                                            else:
                                                # محاولة تغيير كلمة المرور بدون كلمة المرور القديمة (لا توجد كلمة مرور حالية)
                                                try:
                                                    await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                    print(f"[Pending Deletion] Password set to fixed password for {number} (after 24h confirmation) - no old password")
                                                except Exception as e1:
                                                    print(f"[Pending Deletion] Error setting password without old password for {number} (after 24h confirmation): {e1}")
                                                    # إذا فشل، قد يكون هناك كلمة مرور موجودة بالفعل - نحاول مع كلمة المرور الثابتة الحالية
                                                    try:
                                                        await client.edit_2fa(current_password=m, new_password=m, hint=m2)
                                                        print(f"[Pending Deletion] Password already set to fixed password for {number} (after 24h confirmation)")
                                                    except Exception as e2:
                                                        print(f"[Pending Deletion] Could not change password for {number} (after 24h confirmation): {e2}")
                                        except Exception as e:
                                            print(f"[Pending Deletion] Error in password change process for {number} (after 24h confirmation): {e}")
                                        
                                        # ✅ إرسال إشعار النجاح للمستخدم
                                        user_language = users_db.get(user_id, {}).get('language', 'ar')
                                        user_translation = translations.get(user_language, translations['ar'])
                                        success_message = user_translation.get('balance_added', '🎉 تم إضافة الرقم بنجاح {number}\n\nتم إضافة {price} $ إلى رصيدك\nالرصيد الحالي: {balance} $').format(
                                            number=number,
                                            price=price,
                                            balance=users_db[user_id]['balance']
                                        )
                                        try:
                                            await bot.send_message(int(user_id), success_message)
                                            print(f"[Pending Deletion] Success message sent to user {user_id} for {number}")
                                        except Exception as e:
                                            print(f"[Pending Deletion] Error sending success message to user {user_id} for {number}: {e}")
                                        
                                        # ✅ إرسال إشعار للقناة
                                        try:
                                            me = await client.get_me()
                                            first_name = getattr(me, 'first_name', 'N/A')
                                            last_name = getattr(me, 'last_name', 'N/A')
                                            username = getattr(me, 'username', 'N/A')
                                            
                                            user_data = users_db.get(user_id, {})
                                            user_name = user_data.get('name', 'N/A')
                                            user_uname = user_data.get('username', 'N/A')
                                            
                                            msg = f"""✅ تم التحقق بنجاح (بعد 24 ساعة)

المستخدم: {user_id}
الرقم: {number}
السعر: {price} $
الرصيد الجديد: {users_db[user_id]['balance']:.2f} $
الدولة: {country_code if country_code else 'N/A'}
الجهاز: {device_name} ({device_system})
التاريخ والوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                                            
                                            try:
                                                chat = await bot.get_chat(gg)
                                                await bot.send_message(chat.id, msg)
                                            except:
                                                await bot.send_message(gg, msg)
                                            print(f"[Pending Deletion] Success message sent to channel for {number}")
                                        except Exception as e:
                                            print(f"[Pending Deletion] Error sending success to channel for {number}: {e}")
                                    else:
                                        # فشل الحذف - رفض الرقم
                                        print(f"[Pending Deletion] Failed to delete all sessions for {number}, rejecting")
                                        del pending_session_deletions[number]
                                        save_pending_session_deletions()  # ✅ حفظ في الملف
                                        await reject_number_after_24h(bot, user_id, number, f"لا تزال هناك جلسات متبقية ({len(other_sessions_final)} جلسة)", client, device_name, device_system, device_app, api_id, api_hash, string_session)
                                else:
                                    # لا توجد جلسات أخرى - تأكيد الرقم تلقائياً
                                    del pending_session_deletions[number]
                                    save_pending_session_deletions()  # ✅ حفظ في الملف
                                    # ✅ حذف الرقم من pending_confirmations أيضاً
                                    if user_id in pending_confirmations and number in pending_confirmations[user_id]:
                                        del pending_confirmations[user_id][number]
                                        if len(pending_confirmations[user_id]) == 0:
                                            del pending_confirmations[user_id]
                                    print(f"[Pending Deletion] No other sessions for {number}, confirming number")
                                    
                                    # ✅ إضافة الرصيد للمستخدم تلقائياً
                                    if user_id not in users_db:
                                        users_db[user_id] = {"balance": 0, "numbers": [], "language": "ar"}
                                    if number not in users_db[user_id]['numbers']:
                                        users_db[user_id]['numbers'].append(number)
                                    
                                    # جلب السعر من countries_db
                                    price = 0
                                    country_code = None
                                    for name, data in countries_db.items():
                                        if number.startswith(data.get('code', '')):
                                            country_code = name
                                            price = data.get('price', 0)
                                            break
                                    
                                    users_db[user_id]['balance'] += price
                                    save_db()
                                    
                                    # ✅ تغيير كلمة المرور إلى الكلمة الثابتة بعد التأكيد
                                    try:
                                        print(f"[Pending Deletion] Attempting to change password for {number} to fixed password: {m}")
                                        old_password = device_data.get('twofa_password') or device_data.get('2fa_password')
                                        print(f"[Pending Deletion] Old password found in device_data: {bool(old_password)}")
                                        
                                        if old_password:
                                            try:
                                                await client.edit_2fa(current_password=old_password, new_password=m, hint=m2)
                                                print(f"[Pending Deletion] Password changed to fixed password for {number} (after 24h confirmation - no sessions)")
                                            except Exception as e1:
                                                print(f"[Pending Deletion] Error changing password with old password for {number} (after 24h confirmation - no sessions): {e1}")
                                                try:
                                                    await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                    print(f"[Pending Deletion] Password set to fixed password for {number} (after 24h confirmation - no sessions) - without old password")
                                                except Exception as e2:
                                                    print(f"[Pending Deletion] Error setting password for {number} (after 24h confirmation - no sessions): {e2}")
                                        else:
                                            try:
                                                await client.edit_2fa(current_password=None, new_password=m, hint=m2)
                                                print(f"[Pending Deletion] Password set to fixed password for {number} (after 24h confirmation - no sessions) - no old password")
                                            except Exception as e1:
                                                print(f"[Pending Deletion] Error setting password without old password for {number} (after 24h confirmation - no sessions): {e1}")
                                                try:
                                                    await client.edit_2fa(current_password=m, new_password=m, hint=m2)
                                                    print(f"[Pending Deletion] Password already set to fixed password for {number} (after 24h confirmation - no sessions)")
                                                except Exception as e2:
                                                    print(f"[Pending Deletion] Could not change password for {number} (after 24h confirmation - no sessions): {e2}")
                                    except Exception as e:
                                        print(f"[Pending Deletion] Error in password change process for {number} (after 24h confirmation - no sessions): {e}")
                                    
                                    # ✅ إرسال إشعار النجاح للمستخدم
                                    user_language = users_db.get(user_id, {}).get('language', 'ar')
                                    user_translation = translations.get(user_language, translations['ar'])
                                    success_message = user_translation.get('balance_added', '🎉 تم إضافة الرقم بنجاح {number}\n\nتم إضافة {price} $ إلى رصيدك\nالرصيد الحالي: {balance} $').format(
                                        number=number,
                                        price=price,
                                        balance=users_db[user_id]['balance']
                                    )
                                    try:
                                        await bot.send_message(int(user_id), success_message)
                                        print(f"[Pending Deletion] Success message sent to user {user_id} for {number} (no sessions)")
                                    except Exception as e:
                                        print(f"[Pending Deletion] Error sending success message to user {user_id} for {number} (no sessions): {e}")
                                    
                                    # ✅ إرسال إشعار للقناة
                                    try:
                                        me = await client.get_me()
                                        first_name = getattr(me, 'first_name', 'N/A')
                                        last_name = getattr(me, 'last_name', 'N/A')
                                        username = getattr(me, 'username', 'N/A')
                                        
                                        user_data = users_db.get(user_id, {})
                                        user_name = user_data.get('name', 'N/A')
                                        user_uname = user_data.get('username', 'N/A')
                                        
                                        msg = f"""✅ تم التحقق بنجاح (بعد 24 ساعة - لا توجد جلسات أخرى)
المستخدم: {user_id}
الرقم: {number}
السعر: {price} $
الرصيد الجديد: {users_db[user_id]['balance']:.2f} $
الدولة: {country_code if country_code else 'N/A'}
الجهاز: {device_name} ({device_system})
التاريخ والوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                                        
                                        try:
                                            chat = await bot.get_chat(gg)
                                            await bot.send_message(chat.id, msg)
                                        except:
                                            await bot.send_message(gg, msg)
                                        print(f"[Pending Deletion] Success message sent to channel for {number} (no sessions)")
                                    except Exception as e:
                                        print(f"[Pending Deletion] Error sending success to channel for {number} (no sessions): {e}")
                            else:
                                print(f"[Pending Deletion] User not authorized for {number}, rejecting")
                                del pending_session_deletions[number]
                                save_pending_session_deletions()  # ✅ حفظ في الملف
                                await client.disconnect()
                                await reject_number_after_24h(bot, user_id, number, "الجلسة غير صالحة")
                        finally:
                            # ✅ إغلاق العميل بشكل صحيح في جميع الحالات
                            try:
                                if client.is_connected():
                                    await client.disconnect()
                            except:
                                pass
                    except asyncio.TimeoutError:
                        print(f"[Pending Deletion] Connection timeout for {number}, rejecting")
                        del pending_session_deletions[number]
                        save_pending_session_deletions()  # ✅ حفظ في الملف
                        try:
                            await client.disconnect()
                        except:
                            pass
                        if user_id:
                            await reject_number_after_24h(bot, user_id, number, "انتهت مهلة الاتصال")
                    except Exception as e:
                        print(f"[Pending Deletion] Error checking {number}: {e}")
                        import traceback
                        traceback.print_exc()
                        # رفض الرقم في حالة الخطأ
                        try:
                            await client.disconnect()
                        except:
                            pass
                        if user_id:
                            del pending_session_deletions[number]
                            save_pending_session_deletions()  # ✅ حفظ في الملف
                            await reject_number_after_24h(bot, user_id, number, f"خطأ في التحقق من الجلسات: {str(e)}")
        except Exception as e:
            print(f"[Pending Deletion Task] Error: {e}")


# ✅ دالة لرفض الرقم بعد 24 ساعة (مع حذف جلسة البوت وتغيير كلمة المرور)
async def reject_number_after_24h(app, user_id, number, reason, client=None, device_name=None, device_system=None, device_app=None, api_id=None, api_hash=None, string_session=None):
    """رفض الرقم بعد 24 ساعة مع حذف جلسة البوت وتغيير كلمة المرور"""
    random_password = generate_random_password()
    
    # جلب بيانات الجهاز إذا لم تكن موجودة
    if not device_name:
        device_data = users_db.get(user_id, {}).get('devices', {}).get(number)
        if device_data:
            device_name = device_data['name']
            device_system = device_data['system']
            device_app = device_data['app']
            api_id = device_data['API_ID']
            api_hash = device_data['API_HASH']
            string_session = device_data.get('string_session')
        else:
            device_name = DEVICES_LIST[0]['name']
            device_system = DEVICES_LIST[0]['system']
            device_app = DEVICES_LIST[0]['app']
            api_id = DEVICES_LIST[0]['API_ID']
            api_hash = DEVICES_LIST[0]['API_HASH']
    
    # إنهاء جلسة البوت وتغيير كلمة المرور
    if client:
        try:
            is_authorized = await client.is_user_authorized()
            if is_authorized:
                # استخدام الـ client الموجود
                try:
                    # محاولة الحصول على كلمة المرور القديمة من device_data
                    device_data = users_db.get(user_id, {}).get('devices', {}).get(number)
                    old_password = None
                    if device_data:
                        old_password = device_data.get('twofa_password') or device_data.get('2fa_password')
                    
                    # محاولة تغيير كلمة المرور
                    password_changed = False
                    if old_password:
                        try:
                            await client.edit_2fa(current_password=old_password, new_password=random_password, hint=m2)
                            print(f"Password changed successfully for {number} (24h rejection) with old password")
                            password_changed = True
                        except Exception as e1:
                            print(f"Error changing password with old password for {number} (24h rejection): {e1}")
                            # محاولة بدون كلمة المرور القديمة
                            try:
                                await client.edit_2fa(current_password=None, new_password=random_password, hint=m2)
                                print(f"Password changed successfully for {number} (24h rejection) without old password")
                                password_changed = True
                            except Exception as e2:
                                print(f"Error changing password without old password for {number} (24h rejection): {e2}")
                    else:
                        try:
                            await client.edit_2fa(current_password=None, new_password=random_password, hint=m2)
                            print(f"Password changed successfully for {number} (24h rejection)")
                            password_changed = True
                        except Exception as e:
                            print(f"Error changing password for {number} (24h rejection): {e}")
                    
                    # إنهاء جلسة البوت
                    try:
                        await client.log_out()
                        print(f"Bot session ended successfully for {number} (24h rejection)")
                    except Exception as e:
                        print(f"Error ending bot session for {number} (24h rejection): {e}")
                except Exception as e:
                    print(f"Error in reject process for {number} (24h rejection): {e}")
                else:
                    print(f"[Pending Deletion] Client not authorized for {number} in reject_number_after_24h")
        except Exception as e:
            print(f"Error checking client authorization for {number} in reject_number_after_24h: {e}")
    elif string_session:
        # ✅ إنشاء client جديد بدون async with لتجنب طلب bot token
        proxy = get_proxy_for_number(number)
        new_client = TelegramClient(
            StringSession(string_session),
            api_id,
            api_hash,
            device_model=device_name,
            system_version=device_system,
            app_version=device_app,
            lang_code='en',
            system_lang_code='en-US',
            proxy=proxy,
            connection_retries=0,
            retry_delay=0,
            auto_reconnect=False
        )
        try:
            # ✅ استخدام timeout للاتصال لمنع طلب bot token (5 ثوانٍ)
            await asyncio.wait_for(new_client.connect(), timeout=5.0)
            if await new_client.is_user_authorized():
                try:
                    # محاولة الحصول على كلمة المرور القديمة من device_data
                    device_data = users_db.get(user_id, {}).get('devices', {}).get(number)
                    old_password = None
                    if device_data:
                        old_password = device_data.get('twofa_password') or device_data.get('2fa_password')
                    
                    # محاولة تغيير كلمة المرور
                    password_changed = False
                    if old_password:
                        try:
                            await new_client.edit_2fa(current_password=old_password, new_password=random_password, hint=m2)
                            print(f"Password changed successfully for {number} (24h rejection) with old password")
                            password_changed = True
                        except Exception as e1:
                            print(f"Error changing password with old password for {number} (24h rejection): {e1}")
                            # محاولة بدون كلمة المرور القديمة
                            try:
                                await new_client.edit_2fa(current_password=None, new_password=random_password, hint=m2)
                                print(f"Password changed successfully for {number} (24h rejection) without old password")
                                password_changed = True
                            except Exception as e2:
                                print(f"Error changing password without old password for {number} (24h rejection): {e2}")
                    else:
                        try:
                            await new_client.edit_2fa(current_password=None, new_password=random_password, hint=m2)
                            print(f"Password changed successfully for {number} (24h rejection)")
                            password_changed = True
                        except Exception as e:
                            print(f"Error changing password for {number} (24h rejection): {e}")
                    
                    try:
                        await new_client.log_out()
                        print(f"Bot session ended successfully for {number} (24h rejection)")
                    except Exception as e:
                        print(f"Error ending bot session for {number} (24h rejection): {e}")
                except Exception as e:
                    print(f"Error in reject process for {number} (24h rejection): {e}")
            else:
                print(f"[Pending Deletion] User not authorized for {number} in reject_number_after_24h")
        except asyncio.TimeoutError:
            print(f"[Pending Deletion] Connection timeout for {number} in reject_number_after_24h")
        except Exception as e:
            print(f"Error connecting to {number} in reject_number_after_24h: {e}")
        finally:
            # ✅ إغلاق العميل بشكل صحيح
            try:
                if new_client.is_connected():
                    await new_client.disconnect()
            except:
                pass
    else:
        print(f"[Pending Deletion] No client or string_session provided for {number} in reject_number_after_24h")
    
    # إرسال إشعار للمستخدم
    user_language = users_db.get(user_id, {}).get('language', 'ar')
    user_translation = translations.get(user_language, translations['ar'])
    
        # تحديد إذا كان السبب متعلقًا بعدم وجود جلسة البوت
    bot_session_missing = (
            reason and (
                "تم استخراج جلسة البوت من الحساب" in reason or
                "لا توجد جلسات في الحساب" in reason
            )
        )

    if bot_session_missing:
            reject_message = f"""❌ تم رفض الرقم {number}

        السبب: {reason}

        الرجاء المحاولة مرة أخرى."""
    else:
            reject_message = f"""❌ تم رفض الرقم {number}
        السبب: {reason}
        🔑 كلمة المرور الجديدة: `{random_password}`
        ⚠️ تم إنهاء جلسة البوت تلقائياً
        الرجاء المحاولة مرة أخرى."""    
    try:
        await app.send_message(int(user_id), reject_message)
        print(f"[Pending Deletion] Rejection message sent to user {user_id} for {number}")
    except Exception as e:
        print(f"[Pending Deletion] Error sending rejection message to user {user_id} for {number}: {e}")
    
    # ✅ رسالة للقناة - رفض الرقم
    try:
        user_data = users_db.get(user_id, {})
        user_name = user_data.get('name', 'N/A')
        user_uname = user_data.get('username', 'N/A')
        
        reject_channel_msg = f"""❌ تم رفض الرقم (بعد 24 ساعة)
المستخدم: {user_id}
الرقم: {number}
السبب: {reason}
كلمة المرور الجديدة: {random_password}
التاريخ والوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        try:
            chat = await app.get_chat(gg)
            await app.send_message(chat.id, reject_channel_msg)
        except:
            await app.send_message(gg, reject_channel_msg)
        print(f"[Pending Deletion] Rejection message sent to channel for {number}")
    except Exception as e:
        print(f"[Pending Deletion] Error sending rejection to channel for {number}: {e}")


async def Run():
    try:
        print("[Starting Bot..]")
        await bot.start()
        print(f"[Running...] [Name : {bot.me.first_name}] [User : {bot.me.username}]")
        
        # ✅ Start background task for pending deletions
        asyncio.create_task(check_pending_deletions())
        print("[Background Task] Pending deletions checker started")
        
    except Exception as e:
        print(e)
    await idle()

if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(Run())   