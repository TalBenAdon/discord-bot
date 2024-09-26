from random import choice, randint
from helpers import extract_blob, create_file_path
 
 # // after extracting the blob and creating a file path using it, we're returning the final file path.
async def get_video_response(url_to_extract:str) -> str:
    try:

        blob_url = await extract_blob(url_to_extract)
        
        file_path = create_file_path(blob_url)
        print(file_path)
        return file_path
    except Exception as e:
        print(f"Error at get_video_response, error: {e}")
