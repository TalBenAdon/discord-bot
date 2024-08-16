from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, File
from responses import get_video_response
from helpers import check_if_has_link, desirable_domain_check

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Message Functionality
async def send_message(message: Message, user_message:str) -> None:
    if not user_message:
        print('(Message was empty, intents were not enabled properly)')
        return
    
    url = check_if_has_link(user_message)
    
  
    if url and desirable_domain_check(url):

        file_path = await get_video_response(url)
        try:
            with open(file_path, 'rb') as f:
                await message.channel.send(file=File(f))

            os.remove(file_path)
        except Exception as e:
            print(e)
            await message.channel.send("Couldn't manage to grasp a video for you this time")
    else:
        return
    
  

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)
       


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()