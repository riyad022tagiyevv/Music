#single video
youtube-dl --cookies youtube.com_cookies.txt "URL"

#playlist
youtube-dl --yes-playlist --cookies youtube.com_cookies.txt "URL"

You can use: --playlist-start, --playlist-end, --playlist-reverse or --playlist-items to achieve this goal.

#Note: cookie should be in Netscape format

Addons
#https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid
#https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/

python.exe -m pip install --upgrade pip
pip install yt-dlp
yt-dlp --yes-playlist --playlist-start 16 --cookies cookies.txt "https://www.youtube.com/playlist?list=PL8uhW8cclMiODNMBhI6MNzw5zTudkQz4G"

curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -


-------------

Youtube-dl multiple videos download from a file.

yt-dlp.exe -a file.txt

-------------

Subtitile & Video Resolution:

yt-dlp --list-subs --cookies youtube_cookie.txt URL

yt-dlp --write-auto-sub --sub-format srt --sub-lang en --skip-download --cookies youtube_cookie.txt URL


To select the video quality, first use the -F option to list the available formats, here’s an example,

youtube-dl -F URL

The best quality is 22 so use -f 22 instead of -F to download the MP4 video with 1280x720 resolution like this:

youtube-dl -f 22 URL
