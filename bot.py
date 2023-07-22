import logging
import os
from aiogram import Bot, Dispatcher, types, executor
from moviepy.editor import VideoFileClip

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot with your token
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN_HERE'
bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot)

# Define the function to handle /start command
@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Hello! Send me a video, and I'll compress it for you.")

# Define the function to handle video messages
@dispatcher.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    video = message.video

    # Get the file path of the video on Telegram's servers
    file_path = await bot.download_file(video.file_id)

    # Perform video compression using MoviePy
    clip = VideoFileClip(file_path)

    # Adjust the compression settings
    compressed_file = "compressed_video.mp4"
    codec = 'libx265'  # Change the codec to 'libvpx-vp9' for VP9 compression
    bitrate = '250k'  # Adjust the bitrate as desired (e.g., '1M' for 1 Mbps)

    # Compress the video with the specified codec and bitrate
    clip.write_videofile(compressed_file, codec=codec, bitrate=bitrate)

    # Send the compressed video
    await message.answer_video(types.InputFile(compressed_file))

    # Clean up the temporary files
    clip.close()
    os.remove(compressed_file)

# Run the bot using the executor
if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
```
