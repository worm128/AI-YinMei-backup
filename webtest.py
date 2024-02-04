from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

content=1
# 聊天回复弹框处理
@app.route("/chatreply", methods=["GET"])
def chatreply():
    global content
    CallBackForTest=request.args.get('CallBack')
    print(CallBackForTest)
    content=content+1
    temp = "({\"status\": \"成功\",\"content\": \""+str(content)+"画画鬼灭之刃的美女似懂非懂是否第三方的身份画画鬼灭之刃的美女似懂非懂是否第三方的身份画画鬼灭之刃的美女似懂非懂是否第三方的身份画画鬼灭之刃的美女似懂非懂是否第三方的身份画画鬼灭之刃的美女似懂非懂是否第三方的身份画画鬼灭之刃的美女似懂非懂是否第三方的身份画画鬼灭之刃的美女似懂非懂是否第三方的身份画画鬼灭之刃的美女似懂非懂是否第三方的身份\"})"
    if CallBackForTest is not None:
       temp=CallBackForTest+temp
    return temp

if __name__ == "__main__":
    # 开启web
    app.run(host="0.0.0.0", port=1800)