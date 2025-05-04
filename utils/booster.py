import random
import httpx
import tls_client
import json
import base64
import threading
import os
from utils.logger import setup_logger
from utils.captcha import CaptchaSolver

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {config_path}")

class Booster:
    def __init__(self):
        self.config = load_config()
        self.proxy = self.get_proxy()
        self.chrome_v = f'Chrome_{random.randint(110, 118)}'
        self.client = tls_client.Session(
            client_identifier=self.chrome_v,
            random_tls_extension_order=True
        )
        self.locale = random.choice(["en-US", "en-GB", "fr-FR", "de-DE"])
        self.useragent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) {self.chrome_v}.0.0.0 Safari/537.36'
        self.failed = []
        self.success = []
        self.captcha = []
        self.get_x()
        self.fingerprints()
        self.logger = setup_logger()
        self.captcha_solver = CaptchaSolver()

    def get_proxy(self):
        try:
            proxy = random.choice(open("data/proxies.txt", "r").read().splitlines())
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        except:
            return None

    def get_x(self):
        properties = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": self.locale,
            "browser_user_agent": self.useragent,
            "browser_version": f"{self.chrome_v}.0.0.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": 236850,
            "client_event_source": None
        }
        self.x = base64.b64encode(json.dumps(properties, separators=(',', ':')).encode("utf-8")).decode()

    def fingerprints(self):
        headers = {
            "authority": "discord.com",
            "method": "GET",
            "path": "/api/v9/experiments",
            "scheme": "https",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": f"{self.locale},en;q=0.9",
            "User-Agent": self.useragent
        }
        for _ in range(10):
            try:
                r = httpx.get('https://discord.com/api/v9/experiments', headers=headers)
                self.fp = r.json()['fingerprint']
                self.ckis = f'locale={self.locale}; __dcfduid={r.cookies.get("__dcfduid")}; __sdcfduid={r.cookies.get("__sdcfduid")}; __cfruid={r.cookies.get("__cfruid")}; _cfuvid={r.cookies.get("_cfuvid")}'
                return
            except:
                continue
        self.logger.error("Failed to fetch fingerprints after 10 attempts")

    def boost(self, token, invite, guild):
        headers = {
            "authority": "discord.com",
            "scheme": "https",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": f"{self.locale},en;q=0.9",
            "Authorization": str(token),
            "Content-Type": "application/json",
            "Cookie": str(self.ckis),
            "Origin": "https://discord.com",
            "User-Agent": self.useragent,
            "X-Fingerprint": self.fp,
            "X-Super-Properties": self.x
        }
        slots = self.client.get(
            "https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots",
            headers=headers
        )
        slot_json = slots.json()
        if slots.status_code != 200 or len(slot_json) == 0:
            self.logger.error(f"Invalid/No-Nitro: {token}")
            self.failed.append(token)
            return

        r = self.client.post(
            f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={}
        )
        if r.status_code == 429:
            captcha_solution = self.captcha_solver.solve_captcha()
            if captcha_solution:
                headers["X-Captcha-Key"] = captcha_solution
                r = self.client.post(
                    f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={}
                )
            else:
                self.captcha.append(token)
                with open("data/output/captcha.txt", "a") as file:
                    file.write(f"{token}\n")
                return

        if r.status_code == 200:
            self.guild_id = r.json()["guild"]["id"]
            boosts_list = [boost["id"] for boost in slot_json]
            payload = {"user_premium_guild_subscription_slot_ids": boosts_list}
            boosted = self.client.put(
                f"https://discord.com/api/v9/guilds/{guild}/premium/subscriptions",
                json=payload,
                headers=headers
            )
            if boosted.status_code == 201:
                self.success.append(token)
                with open("data/output/success.txt", "a") as file:
                    file.write(f"{token}\n")
            else:
                self.failed.append(token)
                with open("data/output/failed_boosts.txt", "a") as file:
                    file.write(f"{token}\n")
        else:
            self.captcha.append(token)
            with open("data/output/captcha.txt", "a") as file:
                file.write(f"{token}\n")

    def humanizer(self, token):
        headers = {
            "authority": "discord.com",
            "scheme": "https",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": f"{self.locale},en;q=0.9",
            "Authorization": str(token),
            "Content-Type": "application/json",
            "Cookie": str(self.ckis),
            "Origin": "https://discord.com",
            "User-Agent": self.useragent,
            "X-Fingerprint": self.fp,
            "X-Super-Properties": self.x
        }
        applied = []
        if self.config["customization"]["bio"]:
            self.client.patch(
                "https://discord.com/api/v9/users/@me/profile",
                headers=headers,
                json={"bio": self.config["customization"]["bio"]}
            )
            applied.append("bio")
        if self.config["customization"]["nickname"]:
            self.client.patch(
                f"https://discord.com/api/v9/guilds/{self.guild_id}/members/@me",
                headers=headers,
                json={"nick": self.config["customization"]["nickname"]}
            )
            applied.append("nickname")
        if applied:
            self.logger.info(f"Humanized token: {applied}")

    def humanizerthread(self, tokens):
        threads = [threading.Thread(target=self.humanizer, args=(token,)) for token in tokens]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def thread(self, invite, tokens, guild):
        threads = [threading.Thread(target=self.boost, args=(token, invite, guild)) for token in tokens]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return {
            "success": self.success,
            "failed": self.failed,
            "captcha": self.captcha
        }