import re
import requests
import tempfile
from playwright.async_api import async_playwright
domain_list = ["reddit", "instagram","twitter","tiktok"]
#// self explanatory, uses regular expression for web url patterns
def check_if_has_link(user_input:str):

    url_pattern = re.compile(r'https?://\S+|www\.\S+')

    url_match = url_pattern.search(user_input)

    if url_match:
        url = url_match.group(0)
        return url
        
    else:
        
        return None

#// locating the first video tag and copying its src after receiving url
async def extract_blob(url:str) -> str:
 
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" # Wasn't sure what webkit was best, kept on testing around.
        )
        try:
            page = await context.new_page()
            
            await page.goto(url)
            video_element = await page.wait_for_selector("video")
            blob_url = str(await video_element.get_attribute("src"))
            if blob_url:
                print("extracted url: ", blob_url)
                return blob_url
            else:
                raise "Video did not extract properly"
        finally:
            await context.close()
            await browser.close()

# //Writing the video blob into the file-path the was created.
def save_blob_to_file(blob_url, file_path) -> None:
    response = requests.get(blob_url, stream=True)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

# //Creating the path to the dowloaded file within the machine running the bot. Defaulted for mp4.
def create_file_path(blob_url:str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        file_path = temp_file.name
    save_blob_to_file(blob_url, file_path)
    return file_path
    

#//simple definition for checking if the url contains a domain we want to impose video extraction if provided with a link
def desirable_domain_check(url) -> bool:
    for domain in domain_list:
        if domain in url:
            return True