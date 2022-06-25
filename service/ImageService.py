import asyncio, aiohttp, logging, time
from typing import Dict
from PIL import Image
from config import Config
from io import BytesIO

logger = logging.getLogger("ImageService")

async def fetchImagesAsBuffer(images: Dict[str, str], output):
    async def process(output, session, url, index):
        async with session.get(url) as resp:
            data = Image.open(BytesIO(await resp.read()))
            output[index] = data

    async with aiohttp.ClientSession() as session:
        results = {}
        tasks = [process(results, session, url, i) for i, url
                 in enumerate(images)]
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
        startTime = time.time()
        await fetchImagesAsBuffer(panels, images)
        logger.info(f"Finish fetching all panels for {title}, took {time.time() - startTime}.")

        startTime = time.time()
        if len(images) > 1:
            images[0].save(url, "PDF",
                           resolution=50, save_all=True,
                           optimise=True,
                           quality=30,
                           append_images=images[1:]
                           )
            logger.info(f"Finish parsing PDF for {title}, took {time.time() - startTime}")
            return url, None
        else:
            if len(images) == 1:
                images[0].save(url, "PDF",
                               resolution=50, save_all=True,
                               optimise=True,
                               quality=30,
                               )
                logger.info(f"Finish parsing PDF for {title}, took {time.time() - startTime}")
                return url, None

            logger.warn(f"No panels found for {title}, panels: {panels}")
            return None, "No panels found for this manga and chapter(s). There might be a problem in the source or the chapter/manga you specified does not exist. Try again!"
