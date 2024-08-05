import asyncio
import re
import random
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError, DataInvalidError
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
    'charz1.session': ["Venusaur", "Blastoise", "Garchomp", "Dragapult", "Aaa DedM2"],
    'charz2.session': ["Venusaur", "Blastoise", "Garchomp", "Rhyperior", "Mewtwo"],
}

repeat_ball = regular_poks_repeat + legendary_poks

# Add your chat id or username in "YOUR_CHAT" section to recieve notification (I prefer using livegram connected bot for notifications)
async def send_alert(client, alert_type, message):
    try:
        sent_message = await client.send_message("@Hexa_AlertBot", f"**{alert_type} Alert:**\n\n{message}") # If using a group chat as notification centre, add username of the id you want to get notifications on, anywhere on 2nd message without replacing anything, except the one being used for auto 
        await client.pin_message("@Hexa_AlertBot", sent_message.id, notify=True)
        print(f"{alert_type} Alert sent successfully and pinned!")
    except FloodWaitError as e:
        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
        sent_message = await client.send_message("@Hexa_AlertBot", f"**{alert_type} Alert:**\n\n{message}") 
        await client.pin_message("@Hexa_AlertBot", sent_message.id, notify=True)
        print(f"{alert_type} Alert sent successfully and pinned!")
        
async def click_button(event, text=None, row=None, col=None):
    try:
        if text:
            await event.click(text=text)
        else:
            await event.click(row, col)
    except MessageIdInvalidError:
        print(f"Failed to click button {text or (row, col)}")
    except DataInvalidError:
        print(f"Pokemon already fainted or button {text or (row, col)} not found.")

def calculate_health_percentage(max_hp, current_hp):
    if max_hp <= 0:
        raise ValueError("Total health must be greater than zero.")
    if current_hp < 0 or current_hp > max_hp:
        raise ValueError("Current health must be between 0 and the total health.")
    health_percentage = round((current_hp / max_hp) * 100)
    return health_percentage

def initialize_cs_check():
    return {'cs_msg_id': None, 'cs_msg_text': None}

# Function to create and run a client
async def main(session_file):
    client = TelegramClient(session_file, api_id, api_hash)
    stop_hunting = False
    cooldown = random.randint(1, 2)
    low_lvl = False
    buttons_to_click = buttons_to_click_lists[session_file]
    cs_check = initialize_cs_check()
    
    @client.on(events.NewMessage(from_users=572621020))
    async def daily_limit(event):
        nonlocal stop_hunting
        if "Daily hunt limit reached" in event.raw_text:
            await send_alert(client, "🚨 Limit", event.raw_text)
            stop_hunting = True
            await client.disconnect()

    @client.on(events.NewMessage(from_users=572621020))
    async def hunt_or_pass(event):
        if "✨ Shiny Pokémon found!" in event.raw_text:
            await send_alert(client, "✨ Shiny", event.raw_text)
            await asyncio.sleep(1805)
            try:
                await client.send_message(572621020, '/hunt')
            except FloodWaitError as e:
                print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                await client.send_message(572621020, '/hunt')
        elif "💿 found!" in event.raw_text:
            await send_alert(client, "💿 TM", event.raw_text)
            await asyncio.sleep(cooldown)
            try:
                await client.send_message(572621020, '/hunt')
            except FloodWaitError as e:
                print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                await client.send_message(572621020, '/hunt')
        elif "Mega Stone found!" in event.raw_text:
            await send_alert(client, "🔮 Stone", event.raw_text)
            await asyncio.sleep(cooldown)
            try:
                await client.send_message(572621020, '/hunt')
            except FloodWaitError as e:
                print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                await client.send_message(572621020, '/hunt')
        elif "You noticed a strange object located outside of an abandoned Day Care Center.  Upon closer inspection, this appears to be a Pokémon Egg... some trainers must have been breeding Pokémon here and forgot one of their Eggs when the Day Care Center was shut down.... 1 Pokémon Egg 🥚 has been added to your inventory.  Looks like it is up to you to care for the Pokémon that will hatch from this Egg" in event.raw_text:
            await send_alert(client, "🥚 Egg", event.raw_text)
            await asyncio.sleep(cooldown)
            try:
                await client.send_message(572621020, '/hunt')
            except FloodWaitError as e:
                print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                await client.send_message(572621020, '/hunt')
        elif "A wild" in event.raw_text:
            pok_name = event.raw_text.split("wild ")[1].split(" (")[0]
            print(f"{pok_name} spawned!")
            if "✨" in event.raw_text:
                await asyncio.sleep(1620)
                await click_button(event, row=0, col=0)
            elif (regular_ball and pok_name in regular_ball) or (repeat_ball and pok_name in repeat_ball):
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
        nonlocal low_lvl, cs_check
        if "Battle begins!" in event.raw_text:
            bot = await client.get_entity('@HeXamonbot')
            last_messages = await client.get_messages(bot, limit=3)
            btl_msg_id = event.message.id
            cs_msg = None
            for msg in last_messages:
                if msg.id == btl_msg_id:
                    continue
                cs_msg = msg
                break
            if cs_msg:
                cs_check['cs_msg_id'] = cs_msg.id
                cs_check['cs_msg_text'] = cs_msg.message                
            wild_pokemon_name_match = re.search(r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", event.raw_text)
            if cs_msg and '✨' in cs_msg.message.lower():
                low_lvl = True
                print("low lvl set to true")
                await asyncio.sleep(cooldown)
                try:
                    await click_button(event, text="Poke Balls")
                    print("clicked on btn poke balls")
                except MessageIdInvalidError:
                    print("Failed to click Poke Balls button for ✨ Shiny Pokemon")
            elif wild_pokemon_name_match:
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
        nonlocal low_lvl, cs_check
        cs_msg_id = cs_check.get('cs_msg_id')
        cs_msg_text = cs_check.get('cs_msg_text')
        if "Wild" in event.raw_text:
            wild_pokemon_name_match = re.search(r"Wild (\w+) \[.*\]\nLv\. \d+  •  HP \d+/\d+", event.raw_text)
            if cs_msg_text and '✨' in cs_msg_text.lower():
                await asyncio.sleep(cooldown)
                try:
                    await click_button(event, text="Poke Balls")
                    if "☆" in cs_msg_text.lower():
                        await asyncio.sleep(1)
                        await click_button(event, text="Repeat")
                    else:
                        await asyncio.sleep(1)
                        await click_button(event, text="Ultra")
                except MessageIdInvalidError:
                    print(f"Failed to click Poke Balls for {pok_name}")
            elif wild_pokemon_name_match:
                pok_name = wild_pokemon_name_match.group(1)
                wild_pokemon_hp_match = re.search(r"Wild .* \[.*\]\nLv\. \d+  •  HP (\d+)/(\d+)", event.raw_text)
                if wild_pokemon_hp_match:
                    wild_max_hp = int(wild_pokemon_hp_match.group(2))
                    wild_current_hp = int(wild_pokemon_hp_match.group(1))
                    wild_health_percentage = calculate_health_percentage(wild_max_hp, wild_current_hp)
                    if low_lvl == True:
                        await asyncio.sleep(cooldown)
                        try:
                            await click_button(event, text="Poke Balls")
                            if regular_ball and pok_name in regular_ball:
                                await asyncio.sleep(1)
                                await click_button(event, text="Regular")
                            elif repeat_ball and pok_name in repeat_ball:
                                if cs_msg_text and "☆" in cs_msg_text.lower():
                                    await asyncio.sleep(1)
                                    await click_button(event, text="Repeat")
                                else:
                                    await asyncio.sleep(1)
                                    await click_button(event, text="Ultra")
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
                            if regular_ball and pok_name in regular_ball:
                                await asyncio.sleep(1)
                                await click_button(event, text="Regular")
                            elif repeat_ball and pok_name in repeat_ball:
                                if cs_msg_text and "☆" in cs_msg_text.lower():
                                    await asyncio.sleep(1)
                                    await click_button(event, text="Repeat")
                                else:
                                    await asyncio.sleep(1)
                                    await click_button(event, text="Ultra")
                        except MessageIdInvalidError:
                            print(f"Failed to click Poke Balls for {pok_name} with low health")
                    print(f"{pok_name} health percentage: {wild_health_percentage}%")
                else:
                    print(f"Wild Pokemon {pok_name} HP not found in the battle description.")
            else:
                print("Wild Pokemon name not found in the battle description.")

    @client.on(events.MessageEdited(from_users=572621020))
    async def after_fled_or_catch_noti(event):
        nonlocal low_lvl, cs_check
        cs_msg_id = cs_check.get('cs_msg_id')
        cs_msg_text = cs_check.get('cs_msg_text')
        if "You caught a wild" in event.raw_text:
            catch_match = re.search(r'You caught a wild (.*?)\.', event.raw_text)
            if catch_match:
                caught_poke = catch_match.group(1)
                if caught_poke in legendary_poks:
                    print(f"Caught {caught_poke}!")
                    await send_alert(client, "🐲 6L", event.raw_text)
                    await asyncio.sleep(cooldown)
                    try:
                        await client.send_message(572621020, '/hunt')
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                        await asyncio.sleep(e.seconds)
                        await client.send_message(572621020, '/hunt')
                elif cs_msg_text and '✨' in cs_msg_text.lower():
                    print(f"Caught {caught_poke}!")
                    await send_alert(client, "✨ Shiny Catch", event.raw_text)
                    await asyncio.sleep(cooldown)
                    try:
                        await client.send_message(572621020, '/hunt')
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                        await asyncio.sleep(e.seconds)
                        await client.send_message(572621020, '/hunt')
                else:
                    low_lvl = False
                    print(f"Caught {caught_poke}!")
                    await asyncio.sleep(cooldown)
                    try:
                        await client.send_message(572621020, '/hunt')
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                        await asyncio.sleep(e.seconds)
                        await client.send_message(572621020, '/hunt')
        elif "ball failed and the wild" in event.raw_text:
            flee_match = re.search(r'Your .* ball failed and the wild (.*?) fled\.', event.raw_text)
            if flee_match:
                fled_poke = flee_match.group(1)
                print(f"{fled_poke} fled!")
                if "As you walk away filled with sadness, you decide to sit down and rest at a nearby rock. Next to this simple rock, you discover a dusty master ball. It seems this master ball has been sitting here a long time..." in event.raw_text:
                    await send_alert(client, "💮 Master Ball", event.raw_text)
                    await asyncio.sleep(cooldown)
                    try:
                        await client.send_message(572621020, '/hunt')
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                        await asyncio.sleep(e.seconds)
                        await client.send_message(572621020, '/hunt')
                elif "You also stumbled upon" in event.raw_text:
                    await send_alert(client, "🚶🏻‍♂️ Stumble", event.raw_text)
                    await asyncio.sleep(cooldown)
                    try:
                        await client.send_message(572621020, '/hunt')
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                        await asyncio.sleep(e.seconds)
                        await client.send_message(572621020, '/hunt')
                elif "A kind stranger felt sorry for you and gifted you" in event.raw_text:
                    await send_alert(client, "🎁 Gift", event.raw_text)
                    await asyncio.sleep(cooldown)
                    try:
                        await client.send_message(572621020, '/hunt')
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                        await asyncio.sleep(e.seconds)
                        await client.send_message(572621020, '/hunt')
                elif "After strolling around a dark cave for hours, completely lost, you stumble upon a pot of candy. It seems someone hid their treasure and forgot about it.... now where is the exit..." in event.raw_text:
                    await send_alert(client, "🍬 Candy Pot", event.raw_text)
                    await asyncio.sleep(cooldown)
                    try:
                        await client.send_message(572621020, '/hunt')
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                        await asyncio.sleep(e.seconds)
                        await client.send_message(572621020, '/hunt')
                else:
                    await asyncio.sleep(cooldown)
                    try:
                        await client.send_message(572621020, '/hunt')
                    except FloodWaitError as e:
                        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                        await asyncio.sleep(e.seconds)
                        await client.send_message(572621020, '/hunt')
        elif "💵" in event.raw_text:
            fainted_poke = event.raw_text.split("wild ")[1].split(" fainted.")[0]
            print(f"{fainted_poke} got defeated by team and fainted!")
            await asyncio.sleep(cooldown)
            try:
                await client.send_message(572621020, '/hunt')
            except FloodWaitError as e:
                print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
                await client.send_message(572621020, '/hunt')
        elif "Your entire team has fainted and the wild" in event.raw_text:
            foe_poke = event.raw_text.split("wild ")[1].split(" has")[0]
            print(f"{foe_poke} defeated whole team and fled!")
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
                await click_button(event, text=button)

    await client.start()
    print(f"Connected client with session: {client.session.filename}")
    try:
        await client.send_message("@Hexa_AlertBot", "**Hexa Auto Session Started.\nClick [HERE](https://t.me/HeXamonbot?start=command_hunt) to begin if not yet.\n\n⚡ POWERED BY: @STERN_LEGION**")
    except FloodWaitError as e:
        print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
        await client.send_message("@Hexa_AlertBot", "**Hexa Auto Session Started.\nClick [HERE](https://t.me/HeXamonbot?start=command_hunt) to begin if not yet.\n\n⚡ POWERED BY: @STERN_LEGION**")

    bot_entity = await client.get_entity('@HeXamonbot')
    last_messages = await client.get_messages(bot_entity, limit=2)
    shiny_found = any('✨ Shiny Pokémon found!' in message.message.lower() for message in last_messages)
    if shiny_found:
        try:
            await client.send_message("@Hexa_AlertBot", '✨ Shiny found before start.\n\nSend [/hunt](https://t.me/HeXamonbot?start=command_hunt) manually if stopped.')
        except FloodWaitError as e:
            print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
            await asyncio.sleep(e.seconds)
            await client.send_message("@Hexa_AlertBot", '✨ Shiny found before start.\n\nSend [/hunt](https://t.me/HeXamonbot?start=command_hunt) manually if stopped.')
        stop_hunting = True
        print('Shiny Pokemon found in last messages!')
    else:
        try:
            await client.send_message(572621020, '/hunt')
        except FloodWaitError as e:
            print(f"⚠️ FloodWait Enforced. Waiting for {e.seconds} seconds.")
            await asyncio.sleep(e.seconds)
            await client.send_message(572621020, '/hunt')

    await client.run_until_disconnected()
    print(f"Disconnected client with session: {client.session.filename}")
    print(f"Script stopped for session: {session_file}")

# Function to run all clients concurrently
async def run_all_clients():
    tasks = []
    for session_file in session_files:
        tasks.append(main(session_file))
    await asyncio.gather(*tasks)

try:
    asyncio.run(run_all_clients())
except KeyboardInterrupt:
    print("Script interrupted by user.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Perform any necessary cleanup here, if needed.
    print("Cleaning up resources...")
