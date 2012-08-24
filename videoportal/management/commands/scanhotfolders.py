from django.core.management.base import BaseCommand, CommandError
from videoportal.models import *
import videoportal.appsettings as settings
import djangotasks
import datetime
import shutil

class Command(BaseCommand):
    args = ''
    help = 'Gets new videos out of hotfolders'

    def handle(self, *args, **options):
        hotfolders = Hotfolder.objects.filter(activated=True)
        for folder in hotfolders:
            self.stdout.write('This is folder "%s"\n' % folder.folderName)
            os.chdir(settings.HOTFOLDER_BASE_DIR + folder.folderName)
            for file in os.listdir("."):
                if file.endswith(".mov") or file.endswoth(".mp4") or file.endswoth(".avi") or file.endswoth(".ogv") or file.endswoth(".m4v") or file.endswoth(".mp3") or file.endswoth(".ogg"):
                    self.stdout.write('Using file %s\n' % file) 
                    video = Video(title=folder.defaultName,date=datetime.date.today(),description=folder.description,kind=folder.kind,channel=folder.channel)
                    video.save()
                    shutil.move(settings.HOTFOLDER_BASE_DIR + folder.folderName + '/' + file, settings.HOTFOLDER_MOVE_TO_DIR)
                    video.originalFile = settings.HOTFOLDER_MOVE_TO_DIR + file
                    video.save()
                    djangotasks.register_task(video.encode_media, "Encode the files using ffmpeg")
                    encoding_task = djangotasks.task_for_object(video.encode_media)
                    djangotasks.run_task(encoding_task)
                    if settings.USE_BITTORRENT:
                        djangotasks.register_task(video.create_bittorrent, "Create Bittorrent file for video and serve via Bittorrent")
                        torrent_task = djangotasks.task_for_object(video.create_bittorrent)
                        djangotasks.run_task(torrent_task)
