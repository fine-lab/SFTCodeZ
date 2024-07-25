# 安装

## whisper

```bash
pip install openai-whisper
pip install zhconv
pip3 install wheel 
pip3 install torch torchvision torchaudio
```

### ffmpeg

- https://github.com/BtbN/FFmpeg-Builds/releases，下载ffmpeg-master-latest-win64-gpl.zip文件

- 解压后，找到bin文件夹下的“ffmpeg.exe”，将它复制到一个文件夹中，假设这个文件夹的路径是"D:\software\ffmpeg"，然后将"D:/software/ffmpeg"添加到系统环境变量PATH。

# 代码

```python
import whisper
# 可加载small、medium、large等
whisper_model = whisper.load_model("small")
# initial_prompt="以下是普通话的句子。"是为了确保输出为简体中文
result = whisper_model.transcribe(r"D:\aData\SFT\视频转录0719\test5.mp4", language="Chinese", initial_prompt="以下是普通话的句子。")
print(", ".join([i["text"] for i in result["segments"] if i is not None]))
```

# 参考

https://blog.csdn.net/hhy321/article/details/134897967