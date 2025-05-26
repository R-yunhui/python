import requests
import json

def call_embeddings_api(data=None):
    """
    调用embeddings API接口
    
    Args:
        data (dict, optional): 请求体数据，默认为空字典
    
    Returns:
        dict: API响应结果
    """
    url = "http://192.168.2.54:9015/v1/embeddings"
    headers = {
        "Content-Type": "application/json"
    }
    
    # 默认请求数据
    default_data = {
        "input": [
            {
                "text": "你好啊？"
            },
            {
                "image": "http://192.168.2.56/storage/files/1922497691916300289.jpg"
            }
        ],
        "model": "multimodal-embedding-v1"
    }
    
    # 如果data为None，使用默认数据
    if data is None:
        data = default_data
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查响应状态
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None

if __name__ == "__main__":
    # 测试调用
    result = call_embeddings_api()
    print("API响应结果:", json.dumps(result, indent=2, ensure_ascii=False))
