from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, File
from responses import get_video_response
from helpers import check_if_has_link, desirable_domain_check

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN2') #Extracting the discord token from ENV


# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
standby_message: str = "Hold on, trying to get that video out for you"

# Message Functionality
async def handle_received_message(message: Message, user_message:str) -> None:
    if not user_message:
        print('(Message was empty, intents were not enabled properly)') # // not sure about this, if an video is uploaded, user_message is considered 'empty'. //
        return
    
    url = check_if_has_link(user_message) # // Checks for web URL patterns. //
    
  
    if url and desirable_domain_check(url): # // Checks if url contains the domains we're imposing extractions from (Instagram, reddit, so on..). //

        try:
            await message.channel.send(standby_message) # // personal choice of message to show the bot is trying to initiate extraction. //
            file_path = await get_video_response(url) # // Getting final file path //
            with open(file_path, 'rb') as f:
                    await message.channel.send(file=File(f)) # // sending file to channel. //

            os.remove(file_path) # // removing the file from system. //
        except TimeoutError as e: # // if it took the bot too much time identifying the video, returns an error //
             print(f"Timeout error occured {e}")
             await message.channel.send("Error, it took me too long to look for the video :(")
        except Exception as e:
                print(e)
                await message.channel.send("Couldn't manage to grasp a video for you this time")
    else:
        return
    
  
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

# // could be simplified by returning none if 'check_if_has_link' returns falls, but we're gathering message information for later usage if needed. //
@client.event
async def on_message(message: Message) -> None: 
    if message.author == client.user: 
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    channel_id: str = str(message.channel.id)
    print(channel_id)
    print(f'[{channel}] {username}: "{user_message}"') # // just prints every message in chat. //
    await handle_received_message(message, user_message)
       


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()