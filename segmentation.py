import os
import subprocess

def split_video(video_path, segment_duration):
    # 创建保存分割视频的文件夹
    output_dir = os.path.splitext(video_path)[0] + '_segments'
    os.makedirs(output_dir, exist_ok=True)

    # 分割视频
    ffmpeg_command = f'ffmpeg -i "{video_path}" -f segment -segment_time {segment_duration} -c copy -reset_timestamps 1 "{output_dir}/output%03d.mp4"'
    subprocess.call(ffmpeg_command, shell=True)

    # 统计分割视频数量
    num_segments = len([name for name in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, name))])

    print(f'视频分割完成，共生成 {num_segments} 个分割视频。')


# 示例用法
video_path = 'path/to/video.mp4'  # 视频文件的路径
segment_duration = 5  # 分割的秒数

split_video(video_path, segment_duration)