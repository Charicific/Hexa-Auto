import asyncio
import re
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError

api_id = 21594284
api_hash = '632534e8e24d668c907870ef3639d7ff'

async def main():
    client = TelegramClient('charz2', api_id, api_hash)
    await client.start()

    print('''
          Acoount Logged in
                                 ~ @STERN_LEGION  ''')
    

    await client.run_until_disconnected()

asyncio.run(main())
