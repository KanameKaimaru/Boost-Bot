import json
import random
import threading
import time
import os
from utils.logger import setup_logger
from enum import Enum
import websockets
import asyncio

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {config_path}")

class Status(Enum):
    ONLINE = "online"
    DND = "dnd"
    IDLE = "idle"
    INVISIBLE = "invisible"

class Activity(Enum):
    GAME = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4
    COMPETING = 5

class OPCodes(Enum):
    Heartbeat = 1
    Identify = 2
    PresenceUpdate = 3
    HeartbeatACK = 11

class DiscordIntents(int, Enum):
    GUILDS = 1 << 0
    GUILD_MESSAGES = 1 << 9

class Presence:
    def __init__(self, online_status: Status):
        self.online_status = online_status
        self.activities = []

    def add_activity(self, name: str, activity_type: Activity, url: str = None):
        self.activities.append({
            "name": name,
            "type": activity_type.value,
            "url": url if activity_type == Activity.STREAMING else None
        })

class DiscordWebSocket:
    def __init__(self, token):
        self.token = token
        self.logger = setup_logger()
        self.heartbeat_interval = None
        self.last_heartbeat = None
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(
                "wss://gateway.discord.gg/?v=10&encoding=json",
                extra_headers={"User-Agent": "DiscordBot"}
            )
            await self.get_heartbeat_interval()
            await self.authenticate()
            await self.run()
        except Exception as e:
            self.logger.error(f"Websocket error: {e}")

    async def get_heartbeat_interval(self):
        resp = json.loads(await self.websocket.recv())
        self.heartbeat_interval = resp["d"]["heartbeat_interval"]

    async def authenticate(self):
        config = load_config().get("onliner", {})
        activity_types = [Activity[x.upper()] for x in config["choose_random_activity_type_from"]]
        online_statuses = [Status[x.upper()] for x in config["choose_random_online_status_from"]]
        
        online_status = random.choice(online_statuses)
        activity_type = random.choice(activity_types)
        
        activity_name = random.choice(config[activity_type.name.lower()]["choose_random_name_from"])
        activity_url = random.choice(config["streaming"]["choose_random_url_from"]) if activity_type == Activity.STREAMING else None
        
        presence = Presence(online_status)
        presence.add_activity(activity_name, activity_type, activity_url)
        
        await self.websocket.send(json.dumps({
            "op": OPCodes.Identify.value,
            "d": {
                "token": self.token,
                "intents": DiscordIntents.GUILDS | DiscordIntents.GUILD_MESSAGES,
                "properties": {
                    "os": "linux",
                    "browser": "Brave",
                    "device": "Desktop"
                },
                "presence": {
                    "activities": presence.activities,
                    "status": presence.online_status.value,
                    "since": int(time.time()),
                    "afk": false
                }
            }
        }))
        self.last_heartbeat = time.time()

    async def send_heartbeat(self):
        await self.websocket.send(json.dumps({
            "op": OPCodes.Heartbeat.value,
            "d": None
        }))
        self.last_heartbeat = time.time()

    async def run(self):
        while True:
            if time.time() - self.last_heartbeat >= (self.heartbeat_interval / 1000) - 5:
                await self.send_heartbeat()
            await asyncio.sleep(0.5)

async def onliner():
    config = load_config().get("onliner", {})
    tokens = set()
    
    for path in config["onliner_paths"]:
        with open(path, "r") as file:
            for line in file.read().splitlines():
                token = line.split(":")[2] if ":" in line else line
                tokens.add(token)
    
    tasks = [DiscordWebSocket(token).connect() for token in tokens]
    await asyncio.gather(*tasks)