import asyncio
import json
import logging
import os
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('scrape.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# List of channels to scrape
channels = [
    'CheMed123',  # Replace with actual username if known
    'lobelia4cosmetics',
    'tikvahpharma'
]
# Additional channels can be added from https://et.tgstat.com/medicine

async def scrape_channel(channel):
    try:
        logger.info(f"Starting scrape for channel: {channel}")
        target_channel = await client.get_entity(channel)
        date_str = datetime.now().strftime('%Y-%m-%d')
        messages_dir = f"data/raw/telegram_messages/{date_str}/{channel}"
        media_dir = f"data/raw/media/{date_str}/{channel}"

        os.makedirs(messages_dir, exist_ok=True)
        os.makedirs(media_dir, exist_ok=True)

        async for message in client.iter_messages(target_channel, limit=100):  # Adjust limit as needed
            message_data = {
                'id': message.id,
                'date': str(message.date),
                'text': message.text if message.text else None,
                'channel': channel
            }
            filename = f"{messages_dir}/{message.id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(message_data, f, ensure_ascii=False, indent=4)
            logger.info(f"Saved message {message.id} from {channel}")

            if message.photo or message.document:
                media_file = await client.download_media(message, file=media_dir)
                if media_file:
                    new_filename = f"{media_dir}/{channel}_{message.id}.jpg"
                    os.rename(media_file, new_filename)
                    logger.info(f"Saved image {message.id} from {channel}")

    except Exception as e:
        logger.error(f"Error scraping {channel}: {str(e)}")

async def main():
    await client.start(phone)
    for channel in channels:
        await scrape_channel(channel)
    await client.disconnect()
    logger.info("Scraping completed")

if __name__ == "__main__":
    asyncio.run(main())