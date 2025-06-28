import os
import random
import subprocess
import uuid


def get_video_duration(path):
    """
    Returns video duration in seconds using ffprobe.
    """
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        return float(result.stdout)
    except Exception as e:
        raise RuntimeError(f"Could not get duration: {e}")


def generate_clips(input_path, num_clips, min_dur, max_dur, output_dir):
    total_duration = get_video_duration(input_path)
    result_paths = []

    for _ in range(num_clips):
        clip_dur = random.uniform(min_dur, max_dur)
        start_max = total_duration - clip_dur
        if start_max <= 0:
            break

        start_time = random.uniform(0, start_max)
        unique_name = uuid.uuid4().hex
        output_path = os.path.join(output_dir, f"clip_{unique_name}.mp4")

        cmd = [
            'ffmpeg', '-y',
            '-ss', f"{start_time:.2f}",
            '-i', input_path,
            '-t', f"{clip_dur:.2f}",
            '-c:v', 'libx264',
            '-c:a', 'aac',
            output_path
        ]

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        result_paths.append(output_path)

    return result_paths
