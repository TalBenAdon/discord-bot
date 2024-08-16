from random import choice, randint
from helpers import extract_blob, create_file_path
def get_response(user_input:str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awufully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    

async def get_video_response(url_to_extract:str) -> str:
    blob_url = await extract_blob(url_to_extract)
    file_path = create_file_path(blob_url)
    print(file_path)
    return file_path

