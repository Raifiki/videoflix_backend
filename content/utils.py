import os
import subprocess
import sys
import ffmpeg


def get_video_upload_path(instance, filename):
    return 'videos/' + str(instance.uuid) + '/' + filename

def get_video_thumbnail_path(instance, filename=None):
    return 'videos/' + str(instance.uuid) + '/thumbnail.jpg'

def generate_and_store_thumbnail(video_file, thumbnail_file):
        probe = ffmpeg.probe(video_file)
        time = float(0)
        width = probe['streams'][0]['width']
        print('saved to: ', thumbnail_file)
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
                            
            
def convert_video_and_store(video_file, fps):
    new_file_name = video_file.split(".mp4")[0] + "_" + str(fps) +  "p.mp4"
    cmd_command = 'ffmpeg -i "{}" -s hd{} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(video_file,fps , new_file_name)
    run = subprocess.run(cmd_command, capture_output=True)
    
def delete_folder_content(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try: os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))