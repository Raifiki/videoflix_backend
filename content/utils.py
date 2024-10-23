import os
import subprocess
import sys
import ffmpeg

def get_video_upload_path(instance, filename):
    """ This function returns the path where the uploaded video will be stored, depended on the uuid and the filename of the video. """
    return 'videos/' + str(instance.uuid) + '/' + filename

def get_video_thumbnail_path(instance, filename=None):
    """ This function returns the path where the thumbnail will be stored, depended on the uuid. """
    return 'videos/' + str(instance.uuid) + '/thumbnail.jpg'

def generate_and_store_thumbnail(video_file, thumbnail_file):
    """ This function generates and stores the thumbnail of the video with ffmpeg. """
    probe = ffmpeg.probe(video_file)
    time = float(0)
    width = probe['streams'][0]['width']
    try:
            (
            ffmpeg
            .input(video_file, ss=time)
            .filter('scale', width, -1)
            .output(thumbnail_file, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
            )
    except ffmpeg.Error as e:
            print('error:', e.stderr, file=sys.stderr)
                            
#def get_linux_path_from_windows_path(win_path):
#    return '/mnt/' + win_path.replace('\\', '/').replace('C:','c')
            
def convert_video_and_store(video_file, fps):
    """ This function converts the video to the desired resolution and stores it in the database. """
    new_file_name = video_file.split(".mp4")[0] + "_" + str(fps) +  "p.mp4"
    source_path = video_file
    target_path = new_file_name
    print(source_path, target_path)
    cmd_command_win = 'ffmpeg -i "{}" -s hd{} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_path,fps , target_path)
    run = subprocess.run(cmd_command_win, capture_output=True, shell=True) 


def delete_folder_content(folder):
    """ This function deletes the content of a folder. """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try: os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))