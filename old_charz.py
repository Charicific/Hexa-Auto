import asyncio
import re
import random
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError
from telethon.errors.rpcerrorlist import FloodWaitError
from collections import deque

api_id = '21594284'
api_hash = '632534e8e24d668c907870ef3639d7ff'

# List of account credentials
session_files = ['charz1.session', 'charz2.session']  # Add more accounts as needed

clicked_4th_button = False

last_two_messages = deque(maxlen=2)

legendary_poks = ["Regigigas", "Giratina", "Dialga", "Mewtwo", "Ho-oh", "Palkia", "Groudon", "Kyogre", "Rayquaza", "Deoxys", "Arceus", "Reshiram", "Kyurem", "Victini", "Xerneas", "Yveltal", "Zygarde", "Necrozama", "Solgaleo", "Marshadow", "Lunala", "Pheromosa", "Cosmog", "Cosmoem", "Kartana", "Regidrago", "Regieleki", "Spectrier", "Glastrier", "Diancie", "Eternatus", "Zacian", "Zamazenta", "Enamorus", "Buzzwole"]

regular_poks_repeat = ["Venusaur", "Charizard", "Blastoise", "Alakazam", "Gengar", "Kangaskhan", "Pinsir", "Gyarados", "Aerodactyl", "Ampharos", "Scizor", "Heracross", "Houndoom", "Tyranitar", "Blaziken", "Gardevoir", "Mawile", "Aggron", "Medicham", "Manectric", "Banette", "Absol", "Garchomp", "Lucario", "Abomasnow", "Beedrill", "Pidgeot", "Slowbro", "Steelix", "Sceptile", "Swampert", "Sableye", "Sharpedo", "Camerupt", "Altaria", "Glalie", "Salamence", "Metagross", "Lopunny", "Gallade", "Audino"]

regular_ball = ["Slakoth", "Vigoroth"]

# Define separate buttons_to_click lists for each account
buttons_to_click_lists = {
    'charz1.session': ["Mewtwo", "Ho-oh", "Garchomp", "Dragapult", "Aaa DedM2"],
    'charz2.session': ["Chansey", "Krookodile", "Garchomp", "Rhyperior", "Mewtwo"],
}

repeat_ball = regular_poks_repeat + legendary_poks

# Add your chat id or username in "YOUR_CHAT" section to recieve notification (I prefer using livegram connected bot for notifications)
async def send_alert(client, alert_type, message):
    try:
        await client.send_message("@Hexa_AlertBot", f"**{alert_type} Alert:**\n\n{message}") # If using a group chat as notification centre, add username of the id you want to get notifications on, anywhere on 2nd message without replacing anything, except the one being used for auto 
        print(f"{alert_type} Alert sent successfully!")
    except FloodWaitError as e:
        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
        await client.send_message("@Hexa_AlertBot", f"**{alert_type} Alert:**\n\n{message}") # If using a group chat as notification centre, add username of the id you want to get notifications on, anywhere on 2nd message without replacing anything, except the one being used for auto 
        print(f"{alert_type} Alert sent successfully!")

async def click_button(event, text=None, row=None, col=None):
    try:
        if text:
            await event.click(text=text)
        else:
            await event.click(row, col)
    except MessageIdInvalidError:
        print(f"Failed to click button {text or (row, col)}")

def calculate_health_percentage(max_hp, current_hp):
    if max_hp <= 0:
        raise ValueError("Total health must be greater than zero.")
    if current_hp < 0 or current_hp > max_hp:
        raise ValueError("Current health must be between 0 and the total health.")
    health_percentage = round((current_hp / max_hp) * 100)
    return health_percentage

# Function to create and run a client
async def main(session_file):
    client = TelegramClient(session_file, api_id, api_hash)
    stop_hunting = False
    cooldown = random.randint(3, 4)
    low_lvl = False
    buttons_to_click = buttons_to_click_lists[session_file]
    
    @client.on(events.NewMessage(from_users=572621020))
    async def daily_limit(event):
        if "Daily hunt limit reached" in event.raw_text:
            await send_alert(client, "🚨 Limit", event.raw_text)
            stop_hunting = True
            await client.disconnect()

    @client.on(events.NewMessage(from_users=572621020))
    async def hunt_or_pass(event):
        if "✨ Shiny Pokémon found!" in event.raw_text:
            await send_alert(client, "✨ Shiny", event.raw_text)
            stop_hunting = True
            await client.disconnect()
        elif "💿 found!" in event.raw_text:
            low_lvl = False
            await send_alert(client, "💿 TM", event.raw_text)
            await asyncio.sleep(cooldown)
            try:
                await client.send_message(572621020, '/hunt')
            except FloodWaitError as e:
                print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                await client.send_message(572621020, '/hunt')
        elif "Mega Stone found!" in event.raw_text:
            low_lvl = False
            await send_alert(client, "🔮 Stone", event.raw_text)
            await asyncio.sleep(cooldown)
            try:
                await client.send_message(572621020, '/hunt')
            except FloodWaitError as e:
                print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                await client.send_message(572621020, '/hunt')
        elif "A wild" in event.raw_text:
            pok_name = event.raw_text.split("wild ")[1].split(" (")[0]
            print(pok_name)
            if pok_name in regular_ball or pok_name in repeat_ball:
                await asyncio.sleep(cooldown)
                await click_button(event, row=0, col=0)
            else:
                await asyncio.sleep(cooldown)
                try:
                    await client.send_message(572621020, '/hunt')
                except FloodWaitError as e:
                    print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                    await asyncio.sleep(e.seconds)
                    await client.send_message(572621020, '/hunt')

    @client.on(events.NewMessage(from_users=572621020))
    async def battle_first(event):
        if "Battle begins!" in event.raw_text:
            wild_pokemon_name_match = re.search(r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", event.raw_text)
            if wild_pokemon_name_match:
                pok_name = wild_pokemon_name_match.group(1)
                wild_pokemon_hp_match = re.search(r"Wild .* \[.*\]\nLv\. \d+  •  HP (\d+)/(\d+)", event.raw_text)
                if wild_pokemon_hp_match:
                    wild_max_hp = int(wild_pokemon_hp_match.group(2))
                    if wild_max_hp <= 50:
                        low_lvl = True
                        print("low lvl set to true")
                        await asyncio.sleep(cooldown)
                        try:
                            await click_button(event, text="Poke Balls")
                            print("clicked on btn poke balls")
                        except MessageIdInvalidError:
                            print("Failed to click Poke Balls")
                    else:
                        await asyncio.sleep(2)
                        try:
                            await click_button(event, row=0, col=0)
                        except MessageIdInvalidError:
                            print("Failed to click the button for high-level Pokemon")

    @client.on(events.MessageEdited(from_users=572621020))
    async def battle(event):
        if "Wild" in event.raw_text:
            wild_pokemon_name_match = re.search(r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", event.raw_text)
            if wild_pokemon_name_match:
                pok_name = wild_pokemon_name_match.group(1)
                wild_pokemon_hp_match = re.search(r"Wild .* \[.*\]\nLv\. \d+  •  HP (\d+)/(\d+)", event.raw_text)
                if wild_pokemon_hp_match:
                    wild_max_hp = int(wild_pokemon_hp_match.group(2))
                    wild_current_hp = int(wild_pokemon_hp_match.group(1))
                    wild_health_percentage = calculate_health_percentage(wild_max_hp, wild_current_hp)
                    if low_lvl:
                        await asyncio.sleep(cooldown)
                        try:
                            await click_button(event, text="Poke Balls")
                            if pok_name in regular_ball:
                                await asyncio.sleep(1)
                                await click_button(event, text="Regular")
                            elif pok_name in repeat_ball:
                                await asyncio.sleep(1)
                                await click_button(event, text="Repeat")
                        except MessageIdInvalidError:
                            print(f"Failed to click Poke Balls for {pok_name}")
                    elif wild_health_percentage > 50:
                        await asyncio.sleep(1)
                        try:
                            await click_button(event, row=0, col=0)
                        except MessageIdInvalidError:
                            print(f"Failed to click the button for {pok_name} with high health")
                    elif wild_health_percentage <= 50:
                        await asyncio.sleep(1)
                        try:
                            await click_button(event, text="Poke Balls")
                            if pok_name in regular_ball:
                                await asyncio.sleep(1)
                                await click_button(event, text="Regular")
                            elif pok_name in repeat_ball:
                                await asyncio.sleep(1)
                                await click_button(event, text="Repeat")
                        except MessageIdInvalidError:
                            print(f"Failed to click Poke Balls for {pok_name} with low health")
                    print(f"{pok_name} health percentage: {wild_health_percentage}%")
                else:
                    print(f"Wild Pokemon {pok_name} HP not found in the battle description.")
            else:
                print("Wild Pokemon name not found in the battle description.")

    @client.on(events.MessageEdited(from_users=572621020))
    async def skip(event):
        if any(substring in event.raw_text for substring in ["fled", "💵", "You caught"]):
            low_lvl = False
            await asyncio.sleep(cooldown)
            try:
                await client.send_message(572621020, '/hunt')
            except FloodWaitError as e:
                print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                await client.send_message(572621020, '/hunt')

    @client.on(events.NewMessage(from_users=572621020))
    async def skip_trainer(event):
        if "An expert trainer" in event.raw_text:
            await asyncio.sleep(cooldown)
            try:
                await client.send_message(572621020, '/hunt')
            except FloodWaitError as e:
                print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                await client.send_message(572621020, '/hunt')

    @client.on(events.MessageEdited(from_users=572621020))
    async def poke_switch(event):
        if "Choose your next pokemon." in event.raw_text:
            for button in buttons_to_click:
                try:
                    await click_button(event, text=button)
                except MessageIdInvalidError:
                    print(f"Failed to click button {button}")

    await client.start()
    print(f"Connected client with session: {client.session.filename}")
    try:
        await client.send_message("@Hexa_AlertBot", "**Hexa Auto Session Started.\nClick [HERE](https://t.me/HeXamonbot?start=command_hunt) to begin if not yet.\n\n⚡ POWERED BY: @STERN_LEGION**")
    except FloodWaitError as e:
        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
        await client.send_message("@Hexa_AlertBot", "**Hexa Auto Session Started.\nClick [HERE](https://t.me/HeXamonbot?start=command_hunt) to begin if not yet.\n\n⚡ POWERED BY: @STERN_LEGION**")

    await client.run_until_disconnected()
    print(f"Disconnected client with session: {client.session.filename}")
    print(f"Script stopped for session: {session_file}")

# Function to run all clients concurrently
async def run_all_clients():
    tasks = []
    for session_file in session_files:
        tasks.append(main(session_file))
    await asyncio.gather(*tasks)

asyncio.run(run_all_clients())
