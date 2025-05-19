from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

# 定义一个简单的加法工具
@tool
def add_tool(a: float, b: float) -> str:
    """返回两个数的和。"""
    return json.dumps({"result": a + b})

def simple_function_call():
    llm = ChatOpenAI(
        model="qwen2.5-vl-72b-instruct",
        api_key="NA",
        base_url="http://192.168.2.54:9015/v1/",
        max_retries=3,
        temperature=0.7,
        timeout=20
    )
    tools = [add_tool]
    llm_with_tools = llm.bind_tools(tools)

    print("请输入加法问题，例如：'2加3等于多少' 或 '5.5加7'（输入 'exit' 退出）")
    while True:
        user_prompt = input("用户: ")
        if user_prompt.lower() == 'exit':
            print("程序退出。"); break

        messages = [HumanMessage(content=user_prompt)]
        ai_response: AIMessage = llm_with_tools.invoke(messages)
        messages.append(ai_response)

        if ai_response.tool_calls and len(ai_response.tool_calls) > 0:
            for tool_call in ai_response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_call_id = tool_call["id"]

                if tool_name == "add_tool":
                    try:
                        tool_output_str = add_tool.invoke(tool_args)
                        tool_output = json.loads(tool_output_str)
                        print(f"工具输出: {tool_output}")
                    except Exception as e:
                        tool_output = {"error": str(e)}

                    messages.append(ToolMessage(content=json.dumps(tool_output), tool_call_id=tool_call_id))

                    # 再次调用 LLM 生成最终回复
                    messages = [
                        HumanMessage(content=user_prompt),
                        ToolMessage(content=json.dumps(tool_output), tool_call_id=tool_call_id)
                    ]
                    try:
                        final_response: AIMessage = llm_with_tools.invoke(messages)
                        print(f"模型回复: {final_response.content}")
                    except Exception as e:
                        print("LLM 原始响应：", e)
                        raise
                else:
                    print(f"未知工具: {tool_name}")
        else:
            print(f"模型回复: {ai_response.content}")

if __name__ == "__main__":
    simple_function_call()
