import os
import json
import pytest
from unittest.mock import Mock, patch
from src.scrape import scrape_channel, client  # Adjust import based on your module structure

# Mock data for testing
MOCK_CHANNEL = "test_channel"
MOCK_MESSAGE_DATA = {
    "id": 1,
    "date": "2025-07-15 08:00:00+00:00",
    "text": "Test message",
    "channel": MOCK_CHANNEL
}
MOCK_MEDIA_PATH = "mock_image.jpg"

@pytest.fixture
def mock_client():
    # Mock the TelegramClient
    mock_client = Mock()
    mock_entity = Mock()
    mock_entity.id = 123
    mock_client.get_entity.return_value = mock_entity

    async def mock_iter_messages(entity, limit):
        yield Mock(id=MOCK_MESSAGE_DATA["id"], date=MOCK_MESSAGE_DATA["date"], text=MOCK_MESSAGE_DATA["text"],
                   channel=MOCK_CHANNEL, photo=True, download_media=Mock(return_value=MOCK_MEDIA_PATH))
    mock_client.iter_messages = Mock(side_effect=mock_iter_messages)

    return mock_client

@pytest.mark.asyncio
async def test_scrape_channel_creates_json_file(mock_client, tmp_path):
    # Set up temporary directory for testing
    os.chdir(tmp_path)
    date_str = "2025-07-15"
    messages_dir = f"data/raw/telegram_messages/{date_str}/{MOCK_CHANNEL}"
    media_dir = f"data/raw/media/{date_str}/{MOCK_CHANNEL}"

    # Patch the client and run the function
    with patch('src.scrape.client', new=mock_client):
        await scrape_channel(MOCK_CHANNEL)

    # Verify JSON file is created
    json_file = os.path.join(messages_dir, f"{MOCK_MESSAGE_DATA['id']}.json")
    assert os.path.exists(json_file)
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data == MOCK_MESSAGE_DATA

    # Verify media file is created
    media_file = os.path.join(media_dir, f"{MOCK_CHANNEL}_{MOCK_MESSAGE_DATA['id']}.jpg")
    assert os.path.exists(media_file)

@pytest.mark.asyncio
async def test_scrape_channel_no_media(mock_client, tmp_path):
    # Modify mock to exclude media
    mock_client.iter_messages = Mock(side_effect=lambda entity, limit: [Mock(id=2, date="2025-07-15 08:01:00+00:00",
                                                                           text="No media message", channel=MOCK_CHANNEL)])

    os.chdir(tmp_path)
    date_str = "2025-07-15"
    messages_dir = f"data/raw/telegram_messages/{date_str}/{MOCK_CHANNEL}"

    with patch('src.scrape.client', new=mock_client):
        await scrape_channel(MOCK_CHANNEL)

    json_file = os.path.join(messages_dir, "2.json")
    assert os.path.exists(json_file)
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data["id"] == 2
    assert data["text"] == "No media message"
    assert not os.path.exists(f"data/raw/media/{date_str}/{MOCK_CHANNEL}/2.jpg")