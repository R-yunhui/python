import dashscope
import json
from http import HTTPStatus

text = "通用多模态表征模型示例"
input = [{'text': text}]
# 调用模型接口
resp = dashscope.MultiModalEmbedding.call(
    model="multimodal-embedding-v1",
    input=input
)

if resp.status_code == HTTPStatus.OK:
    print(json.dumps(resp.output, ensure_ascii=False, indent=4))