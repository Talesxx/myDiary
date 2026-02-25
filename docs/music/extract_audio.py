#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量视频转音频和提取封面脚本
功能：将video目录中的所有视频文件提取音频和封面图并保存到按视频名命名的子目录中
"""

import os
import sys
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# 定义支持的视频文件扩展名
SUPPORTED_VIDEO_EXTENSIONS = (
    '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', 
    '.webm', '.m4v', '.mpeg', '.mpg', '.rmvb', '.3gp'
)

def check_ffmpeg_installed():
    """检查FFmpeg是否已安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def extract_audio_from_video(video_path, audio_output_path, quality=320):
    """
    从单个视频文件中提取音频
    
    Args:
        video_path: 视频文件路径
        audio_output_path: 音频输出路径
        quality: 音频质量（kbps）
        
    Returns:
        bool: 提取是否成功
    """
    try:
        # 构建FFmpeg命令
        command = [
            'ffmpeg',
            '-i', video_path,        # 输入文件
            '-vn',                   # 不处理视频
            '-ab', f'{quality}k',    # 音频比特率
            '-ar', '44100',          # 音频采样率
            '-y',                    # 覆盖已存在的文件
            audio_output_path        # 输出文件
        ]
        
        # 执行命令
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: 处理文件 {os.path.basename(video_path)} 失败 - {e}")
        return False

def extract_thumbnail_from_video(video_path, thumbnail_output_path):
    """
    从单个视频文件中提取封面图
    
    Args:
        video_path: 视频文件路径
        thumbnail_output_path: 封面图输出路径
        
    Returns:
        bool: 提取是否成功
    """
    try:
        # 构建FFmpeg命令，提取视频第一帧作为封面图
        command = [
            'ffmpeg',
            '-i', video_path,              # 输入文件
            '-ss', '00:00:02.000',        # 截取时间点（第2秒）
            '-vframes', '1',               # 只提取1帧
            '-y',                          # 覆盖已存在的文件
            thumbnail_output_path          # 输出文件
        ]
        
        # 执行命令
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: 提取文件 {os.path.basename(video_path)} 的封面失败 - {e}")
        return False

def get_video_files(directory):
    """
    获取目录中所有支持的视频文件
    
    Args:
        directory: 视频文件所在目录
        
    Returns:
        list: 视频文件路径列表
    """
    video_files = []
    
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"错误: 目录 {directory} 不存在")
        return []
    
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.lower().endswith(SUPPORTED_VIDEO_EXTENSIONS):
            video_files.append(os.path.join(directory, filename))
    
    return video_files

def process_video_file(video_file, output_dir, quality=320):
    """
    处理单个视频文件，提取音频和封面图并返回结果
    """
    # 获取文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    # 创建以视频名命名的子目录
    video_output_dir = os.path.join(output_dir, base_name)
    os.makedirs(video_output_dir, exist_ok=True)
    
    # 构建输出音频文件路径（使用mp3格式）
    audio_file = os.path.join(video_output_dir, f"audio.mp3")
    # 构建输出封面图文件路径（使用jpg格式）
    thumbnail_file = os.path.join(video_output_dir, f"cover.jpg")
    
    # 提取音频
    audio_success = extract_audio_from_video(video_file, audio_file, quality)
    # 提取封面图
    thumbnail_success = extract_thumbnail_from_video(video_file, thumbnail_file)
    
    return {
        'video': video_file,
        'audio': audio_file,
        'thumbnail': thumbnail_file,
        'audio_success': audio_success,
        'thumbnail_success': thumbnail_success,
        'success': audio_success and thumbnail_success  # 只有两者都成功才算成功
    }

def batch_extract_media(video_dir, output_dir, quality=320, max_workers=4):
    """
    批量提取音频和封面图
    
    Args:
        video_dir: 视频文件所在目录
        output_dir: 输出目录
        quality: 音频质量（kbps）
        max_workers: 最大并发工作线程数
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有视频文件
    video_files = get_video_files(video_dir)
    
    if not video_files:
        print(f"提示: 在 {video_dir} 中没有找到支持的视频文件")
        return
    
    print(f"找到 {len(video_files)} 个视频文件，开始提取音频和封面图...")
    
    # 跟踪成功和失败的数量
    success_count = 0
    failed_count = 0
    
    # 使用线程池并行处理视频文件
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        futures = [
            executor.submit(process_video_file, video_file, output_dir, quality)
            for video_file in video_files
        ]
        
        # 使用tqdm显示进度条
        for future in tqdm(futures, total=len(video_files), desc="处理进度"):
            result = future.result()
            if result['success']:
                success_count += 1
            else:
                failed_count += 1
    
    # 显示处理结果摘要
    print("\n处理完成！")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"处理结果已保存至: {output_dir}")

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='批量从视频文件中提取音频和封面图')
    parser.add_argument('--video-dir', default='video', help='视频文件目录')
    parser.add_argument('--output-dir', default='audio', help='输出目录（包含以视频名命名的子目录）')
    parser.add_argument('--quality', type=int, default=320, help='音频质量（kbps），默认为320kbps')
    parser.add_argument('--threads', type=int, default=4, help='并发处理线程数，默认为4')
    
    args = parser.parse_args()
    
    # 检查FFmpeg是否已安装
    if not check_ffmpeg_installed():
        print("错误: 未找到FFmpeg。请安装FFmpeg并确保它在系统PATH中。")
        print("\n安装指南:")
        print("Windows: 访问 https://ffmpeg.org/download.html 下载Windows版本，解压后将bin目录添加到系统PATH")
        print("macOS: 使用Homebrew安装: brew install ffmpeg")
        print("Linux: 使用包管理器安装: sudo apt install ffmpeg (Ubuntu/Debian) 或 sudo dnf install ffmpeg (Fedora)")
        sys.exit(1)
    
    # 获取绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    video_dir = os.path.join(script_dir, args.video_dir)
    output_dir = os.path.join(script_dir, args.output_dir)
    
    # 执行批量提取
    batch_extract_media(video_dir, output_dir, args.quality, args.threads)

if __name__ == "__main__":
    main()