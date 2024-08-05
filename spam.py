import asyncio
import random
from telethon import TelegramClient, events

api_id = 21594284
api_hash = '632534e8e24d668c907870ef3639d7ff'

# List of session files for different accounts
session_files = ['account3.session', 'account4.session', 'account5.session', 'account6.session', 'account7.session']

# Username or user ID of the person to alert
alert_user = '@Hexa_AlertBot'

class Account:
    def __init__(self, session_file):
        self.client = TelegramClient(session_file, api_id, api_hash)
        self.stop_hunting = False

    async def start_hunting(self):
        async with self.client:
            bot_entity = await self.client.get_entity('@HeXamonbot')
            while not self.stop_hunting:
                last_messages = await self.client.get_messages(bot_entity, limit=2)
                shiny_found = any('✨ shiny pokemon found!' in message.message.lower() for message in last_messages)
                if shiny_found:
                    self.stop_hunting = True
                    print('Shiny Pokemon found in last messages!')
                    break

                for message in last_messages:
                    await self.handle_message(message)

                if not self.stop_hunting:
                    await self.client.send_message('@HeXamonbot', '/hunt')
                    gap = random.randint(2, 3)
                    await asyncio.sleep(gap)

    async def handle_message(self, message):
        stop_keywords = [
            "✨ Shiny Pokémon found!", "Daily hunt limit reached"
        ]
        log_keywords = [
            "Mega Stone found!", "💿 found!"
        ]

        if any(keyword in message.message for keyword in stop_keywords):
            self.stop_hunting = True
            print(f"Found stopping keyword in message: {message.message}")
            await self.alert_user(message)
        elif any(keyword in message.message for keyword in log_keywords):
            print(f"Found log keyword in message: {message.message}")
            await self.alert_user(message)
            gap = random.randint(2, 3)
            await asyncio.sleep(gap)
            await self.client.send_message('@HeXamonbot', '/hunt')
        else:
            print(f"Received message: {message.message}")

    async def alert_user(self, message):
        try:
            await self.client.send_message(alert_user, f"🚨 Alert: {message.message}")
            print(f"Alert sent to {alert_user}: {message.message}")
        except Exception as e:
            print(f"Failed to send alert: {e}")

    async def connect(self):
        await self.client.start()
        print(f"Connected client with session: {self.client.session.filename}")
        # Handle OTP and TFA code if required

    def close(self):
        self.stop_hunting = True
        self.client.disconnect()
        print(f"Disconnected client with session: {self.client.session.filename}")

async def main(session_file):
    account = Account(session_file)
    await account.connect()

    while not account.stop_hunting:
        await account.start_hunting()

    account.close()
    print(f"Script stopped for session: {session_file}")

# Run the main function for each session file
async def run_all_clients():
    tasks = []
    for session_file in session_files:
        tasks.append(main(session_file))
    await asyncio.gather(*tasks)

asyncio.run(run_all_clients())