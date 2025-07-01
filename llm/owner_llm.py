import random

class PoetryLLM:
    def __init__(self, model_path='llm/ci.txt'):
        self.model_path = model_path
        self.chars = []
        self.vocab_size = 0
        self.stoi = {}
        self.itos = {}
        self.transition = []
        self.is_trained = False
        
    def load_data(self):
        try:
            with open(self.model_path, 'r', encoding='utf-8') as f:
                text = f.read()
            if not text:
                raise ValueError("训练文件为空")
            return text
        except FileNotFoundError:
            print(f"错误：找不到训练文件 '{self.model_path}'")
            return None
        except Exception as e:
            print(f"错误：读取文件时发生错误 - {str(e)}")
            return None

    def train(self):
        print("正在训练模型...")
        text = self.load_data()
        if not text:
            return False

        self.chars = sorted(list(set(text)))
        self.vocab_size = len(self.chars)
        self.stoi = {ch: i for i, ch in enumerate(self.chars)}
        self.itos = {i: ch for i, ch in enumerate(self.chars)}

        # 使用滑动窗口来构建转移矩阵，考虑更多上下文
        window_size = 2
        self.transition = [[0 for _ in range(self.vocab_size)] for _ in range(self.vocab_size)]
        
        for i in range(len(text) - window_size):
            current_token_id = self.encode(text[i])[0]
            next_token_id = self.encode(text[i + 1])[0]
            self.transition[current_token_id][next_token_id] += 1

        self.is_trained = True
        print(f"训练完成！词汇表大小：{self.vocab_size}")
        return True

    def encode(self, s):
        """将文本转换为数字序列，处理未知字符"""
        result = []
        for c in s:
            if c in self.stoi:
                result.append(self.stoi[c])
            else:
                # 对于未知字符，随机选择一个已知字符
                result.append(random.randint(0, self.vocab_size - 1))
        return result

    def decode(self, l):
        return ''.join([self.itos[i] for i in l])

    def generate(self, prompt, max_length=50, temperature=0.8):
        if not self.is_trained:
            print("错误：模型尚未训练")
            return None

        if not prompt:
            print("错误：请输入有效的起始词")
            return None

        print(f"正在生成诗词，起始词：{prompt}", end="")
        
        # 检查提示词中的未知字符
        unknown_chars = [c for c in prompt if c not in self.chars]
        if unknown_chars:
            print(f"\n注意：以下字符不在训练数据中，将使用随机字符替代：{', '.join(unknown_chars)}")
        
        generated_token = self.encode(prompt)
        
        for i in range(max_length - 1):
            current_token_id = generated_token[-1]
            logits = self.transition[current_token_id]
            total = sum(logits)
            
            if total == 0:
                next_token_id = random.randint(0, self.vocab_size - 1)
            else:
                logits = [logit / total for logit in logits]
                if temperature != 1.0:
                    logits = [logit ** (1/temperature) for logit in logits]
                    total = sum(logits)
                    logits = [logit / total for logit in logits]
                
                next_token_id = random.choices(range(self.vocab_size), weights=logits, k=1)[0]
            
            generated_token.append(next_token_id)
            if i % 5 == 0:
                print(".", end="", flush=True)
        
        print("\n生成完成！")
        return self.decode(generated_token)

def main():
    model = PoetryLLM()
    if not model.train():
        return

    while True:
        print("\n" + "="*30)
        print("诗词生成器")
        print("="*30)
        
        prompt = input("\n请输入起始词（输入'q'退出）：")
        if prompt.lower() == 'q':
            break
            
        try:
            max_length = int(input("请输入要生成的字符数量（建议30-50）："))
            if max_length <= 0:
                print("请输入大于0的数字！")
                continue
                
            temperature = float(input("请输入温度参数（0.1-1.0，越小越稳定）："))
            if not 0.1 <= temperature <= 1.0:
                print("温度参数应在0.1到1.0之间！")
                continue
                
            result = model.generate(prompt, max_length, temperature)
            if result:
                print("\n生成的诗词：")
                print("-"*30)
                print(result)
                print("-"*30)
                print()
                
        except ValueError:
            print("输入无效，请重试！")
            continue

if __name__ == "__main__":
    main()