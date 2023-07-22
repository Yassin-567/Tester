import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling
from moviepy.editor import VideoFileClip

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the function to handle /start command
async def start(message: types.Message):
    await message.reply("Hello! Send me a video, and I'll compress it for you.")

# Define the function to handle video messages
async def handle_video(message: types.Message):
    video = message.video

    if isinstance(video, types.Video):
        # Get the file path of the video on Telegram's servers
        file_path = await message.get_video()

        # Perform video compression using MoviePy
        clip = VideoFileClip(file_path)

        # Adjust the compression settings
        compressed_file = "compressed_video.mp4"
        codec = 'libx265'  # Change the codec to 'libvpx-vp9' for VP9 compression
        bitrate = '250k'  # Adjust the bitrate as desired (e.g., '1M' for 1 Mbps)

        # Compress the video with the specified codec and bitrate
        clip.write_videofile(compressed_file, codec=codec, bitrate=bitrate)

        # Send the compressed video
        await message.reply_video(open(compressed_file, 'rb'))

        # Clean up the temporary files
        clip.close()
        os.remove(compressed_file)
    else:
        await message.reply("Please send a video file.")

# Set up the Telegram bot
bot = Bot(token='5877188485:AAH2kX8z5iprNjEDLORGzZ9B_fR9XOx_xXc')
dp = Dispatcher(bot)

# Add command handlers
dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.video, handle_video))

# Start the bot
start_polling(dp)
