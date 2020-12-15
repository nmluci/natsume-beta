data = ['https://imgur.com/a/kjksjhkds',
        'https://i.imgur.com/aksfls',
        'https://redgifts.com/watch/90280859',
        'https://www.pornhub.com/view_video.php?viewkey=ph5fb6a5797a557',
        'https://i.redd.it/b8lo21426r261.png']

import youtube_dl.YoutubeDL as ytdl


for url in data:
    filename = url.split('/')[len(url.split('/'))-1]
    print(filename)