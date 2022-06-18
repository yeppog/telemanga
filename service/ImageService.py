from typing import Dict
from PIL import Image
from config import Config
import asyncio
import aiohttp
from io import BytesIO


async def fetchImagesAsBuffer(images: Dict[str, str], output):
    async def process(output, session, url, index):
        async with session.get(url) as resp:
            data = Image.open(BytesIO(await resp.read()))
            output[index] = data

    async with aiohttp.ClientSession() as session:
        results = {}
        tasks = [process(results, session, url, i) for i, (key, url)
                 in enumerate(images.items())]
        await asyncio.gather(*tasks)
    for i in range(len(images)):
        output.append(results[i])


"""
The image service parses URLS and transform them into temporary images or PDFS,
according to what is required.
"""


class ImageService:

    @classmethod
    async def parsePDF(self, panels: Dict[int, str], title: str):
        url = f"{Config.outputFolder}/{title}.pdf"
        images = []
        await fetchImagesAsBuffer(panels, images)
        images[0].save(url, "PDF",
                       resolution=100.0, save_all=True,
                       append_images=images[1:])
        return url
