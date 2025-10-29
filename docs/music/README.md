# 批量视频转音频工具

这个目录包含两个版本的批量视频转音频脚本，可以将`video`目录中的所有视频文件提取音频并保存到`audio`目录。

## 可用的脚本

1. **Python版本**: `extract_audio.py`
2. **Node.js版本**: `extract_audio.js` (备选方案)

## Python版本使用说明

### 依赖安装

1. **安装Python**:
   - 从 [Python官网](https://www.python.org/downloads/) 下载并安装Python 3.7或更高版本
   - 确保在安装过程中勾选"Add Python to PATH"

2. **安装Python依赖**:
   ```bash
   # 进入脚本所在目录
   cd d:\MyWork\myDiary\docs\music
   
   # 安装依赖
   pip install -r requirements.txt
   ```

3. **安装FFmpeg** (必须):
   - **Windows**: 
     1. 从 [FFmpeg官网](https://ffmpeg.org/download.html) 下载Windows版本
     2. 解压下载的文件
     3. 将解压目录中的`bin`文件夹添加到系统PATH环境变量
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) 或 `sudo dnf install ffmpeg` (Fedora)

### 使用方法

1. 将视频文件放入`video`目录
2. 运行脚本:

   ```bash
   # 基本用法
   python extract_audio.py
   
   # 自定义线程数 (提高处理速度)
   python extract_audio.py --threads 8
   
   # 自定义音频质量 (较低质量，较小文件)
   python extract_audio.py --quality 192
   
   # 自定义视频和输出目录
   python extract_audio.py --video-dir "your/video/path" --output-dir "your/audio/path"
   ```

## Node.js版本使用说明

如果您的环境中已安装Node.js但没有Python，可以使用此版本。

### 依赖安装

1. **安装Node.js**:
   - 从 [Node.js官网](https://nodejs.org/) 下载并安装Node.js 12或更高版本

2. **安装FFmpeg** (必须):
   - 同上Python版本的FFmpeg安装步骤

### 使用方法

1. 将视频文件放入`video`目录
2. 运行脚本:

   ```bash
   # 基本用法
   node extract_audio.js
   
   # 自定义线程数
   node extract_audio.js --threads 8
   
   # 自定义音频质量
   node extract_audio.js --quality 192
   
   # 自定义视频和输出目录
   node extract_audio.js --video-dir "your/video/path" --output-dir "your/audio/path"
   ```

## 功能特点

- 支持多种视频格式：mp4、avi、mov、wmv、flv、mkv、webm等
- 批量处理：自动扫描video目录中的所有视频文件
- 并行处理：多线程加速转换
- 可自定义音频质量：默认320kbps高品质MP3
- 详细的进度显示和结果统计
- 自动创建输出目录

## 注意事项

- 音频文件将以MP3格式输出，保留原视频文件名
- 处理大型视频文件可能需要较长时间，取决于您的计算机性能
- 确保有足够的磁盘空间存储生成的音频文件

## 故障排除

- **错误: 未找到FFmpeg**: 请确保FFmpeg已正确安装并添加到系统PATH
- **错误: 权限不足**: 以管理员权限运行命令提示符或终端
- **转换失败**: 检查视频文件是否损坏或受DRM保护

## 示例

假设您有以下视频文件在`video`目录中:
- `video1.mp4`
- `video2.mkv`

运行脚本后，您将在`audio`目录中得到:
- `video1.mp3`
- `video2.mp3`