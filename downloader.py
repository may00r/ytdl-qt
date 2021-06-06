from __future__ import unicode_literals
import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
    if d['status'] == 'downloading':
        p = d['_percent_str']
        p = p.replace('%','')
        print(d['filename'], d['_percent_str'], d['_eta_str'])

class Downloader():
    
    def download(self, url = "https://www.youtube.com/watch?v=3M016-PgLDk"):
        ydl_opts = {
            'format': 'bestvideo[ext=webm]+bestaudio[ext=m4a]',
            'merge_output_format': 'mp4',
            'logger': MyLogger(),
            'progress_hooks': [self.my_hook] if not __name__ == '__main__' else [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])




def main():
    ytDownload = Downloader()
    ytDownload.download()

if __name__ == '__main__':
    main()