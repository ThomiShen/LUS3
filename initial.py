from  evaluation import Evaluator

api_key = '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'
# 读取你的提示prompt
a=Evaluator(api_key)
with open('/Users/thomi/Desktop/1.txt', "r") as f:
    prompt = f.read()
k=a.get_evaluation(prompt)
print(k)