import os


class Config:

   API_ID = int(os.getenv("API_ID", "24548143"))
   API_HASH = os.getenv("API_HASH", "6cba049c135a0393615878ea1e3c9443")
   BOT_TOKEN = os.getenv("BOT_TOKEN", "2142897671:ghyujjhgggggggggggggfddddddddddddtttttttttttttt")
   BOT_USERNAME = os.environ.get("BOT_USERNAME", "NezrinSongBot")
   OWNER_NAME = os.environ.get("OWNER_NAME", "Thagiyev") 
   PLAYLIST_NAME = os.environ.get("PLAYLIST_NAME", "NezrinLogo")
   PLAYLIST_ID = int(os.environ.get("PLAYLIST_ID", "-1002168356385"))
   ALIVE_NAME = os.environ.get("ALIVE_NAME", "Nezrin")
   ALIVE_IMG = os.environ.get("ALIVE_IMG", "https://images.app.goo.gl/2P23ebDm6bjE68ED8") 
   START_IMG = os.environ.get("START_IMG", "https://images.app.goo.gl/2P23ebDm6bjE68ED8")    
