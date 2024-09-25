import sys
import ffmpeg

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
    