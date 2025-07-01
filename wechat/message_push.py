import requests

class WeComMessenger:
    def __init__(self, corp_id, corp_secret, agent_id):
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.agent_id = agent_id
        self.access_token = None
    
    def _refresh_token(self):
        """获取或刷新access_token"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corp_id}&corpsecret={self.corp_secret}"
        response = requests.get(url)
        self.access_token = response.json().get('access_token')
    
    def send_message(self, content, to_user="@all"):
        """发送文本消息"""
        if not self.access_token:
            self._refresh_token()
            
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        payload = {
            "touser": to_user,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {"content": content},
            "safe": 0
        }
        response = requests.post(url, json=payload)
        return response.json()

# 测试用例
if __name__ == "__main__":
    # 替换为你的企业微信参数
    messenger = WeComMessenger(
        corp_id="ww3ad474a1a7ee0113",
        corp_secret="OR5TfsFOgKsz-lOEforpj_9Q6hfiBcwbqL0y0bWCdt4",
        agent_id=1000002
    )
    
    while True:
        message = input("请输入要发送的消息（输入q退出）: ")
        if message.lower() == 'q':
            break
            
        result = messenger.send_message(message)
        print("发送结果:", result)
