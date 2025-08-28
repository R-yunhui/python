from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen2.5-vl-72b-instruct",
    api_key="NA",
    base_url="http://192.168.2.54:9015/v1/",
    max_retries=3,
    temperature=0.7,
    timeout=20,
    max_tokens=200
)

data = llm.stream("你是谁？你能帮我干什么？")

for chunk in data:
    if hasattr(chunk, 'content'):
        print(chunk.content)
    elif isinstance(chunk, dict) and 'content' in chunk:
        print(chunk['content'])
    elif isinstance(chunk, str):
        print(chunk)
