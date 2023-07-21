import logging
import os
import telepot
from telepot.namedtuple import Update
from moviepy.editor import VideoFileClip
import tornado.ioloop
import tornado.web
import tornado.gen

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)  # Use __name__ to get the current module name

# Define the function to handle /start command
def start(chat_id):
    bot.sendMessage(chat_id, "Hello! Send me a video, and I'll compress it for you.")

# Define the function to handle video messages
def handle_video(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'video':
        # Get the file_id of the video
        file_id = msg['video']['file_id']
        
        # Get the file path of the video on Telegram's servers
        file_info = bot.getFile(file_id)
        file_path = file_info['file_path']

        # Perform video compression using MoviePy
        clip = VideoFileClip(file_path)

        # Adjust the compression settings
        compressed_file = "compressed_video.mp4"
        codec = 'libx265'  # Change the codec to 'libvpx-vp9' for VP9 compression
        bitrate = '250k'  # Adjust the bitrate as desired (e.g., '1M' for 1 Mbps)

        # Compress the video with the specified codec and bitrate
        clip.write_videofile(compressed_file, codec=codec, bitrate=bitrate)

        # Send the compressed video
        bot.sendVideo(chat_id, open(compressed_file, 'rb'))

        # Clean up the temporary files
        clip.close()
        os.remove(compressed_file)

# Tornado request handler for the Telegram bot
class TelegramBotHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        body = self.request.body.decode()
        update = telepot.glance(telepot.flavor.Tornado, body, bot_token)
        handle_video(update[2])
        self.set_status(200)
        self.write('OK')

def make_app():
    return tornado.web.Application([
        (r"/", TelegramBotHandler),
    ])

if __name__ == "__main__":
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = '6266356161:AAEd7RPG1NnYlYr6rDikURVDzZGHtyozeA8'
    bot = telepot.Bot(bot_token)

    app = make_app()
    app.listen(10000)  # Port number to listen on

    logger.info("Bot started!")
    tornado.ioloop.IOLoop.current().start()
