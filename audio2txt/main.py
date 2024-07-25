import whisper
whisper_model = whisper.load_model("small")
result = whisper_model.transcribe(r"D:\aData\SFT\视频转录0719\test5.mp4", language="Chinese", initial_prompt="以下是普通话的句子。")
print(", ".join([i["text"] for i in result["segments"] if i is not None]))
