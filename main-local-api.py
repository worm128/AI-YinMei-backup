import argparse
import datetime
import queue
import subprocess
import threading
import os
import time
import requests
import sseclient
import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from bilibili_api import live, sync, Credential
from pynput.keyboard import Key, Controller

print("=====================================================================")
print("开始启动人工智能吟美！")
print("当前AI使用最新ChatGLM3引擎开发")
print("ChatGLM3-6B：https://github.com/THUDM/ChatGLM3-6B")
print("开发作者 by Winlone")
print("=====================================================================\n")

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
QuestionList = queue.Queue(10)  # 定义问题 用户名 回复 播放列表 四个先进先出队列
QuestionName = queue.Queue(10)
AnswerList = queue.Queue()
MpvList = queue.Queue()
LogsList = queue.Queue()
history = []
is_ai_ready = True  # 定义chatglm是否转换完成标志
is_tts_ready = True  # 定义语音是否生成完成标志
is_mpv_ready = True  # 定义是否播放完成标志
AudioCount = 0
enable_history = False  # 是否启用记忆
history_count = 2  # 定义最大对话记忆轮数,请注意这个数值不包括扮演设置消耗的轮数，只有当enable_history为True时生效
enable_role = False  # 是否启用扮演模式


print("--------------------")
print("启动成功！")
print("--------------------")

#sched1 = BlockingScheduler(timezone="Asia/Shanghai")

def input_msg():
    """
     处理弹幕消息
    """
    global QuestionList
    global QuestionName
    global LogsList
    while(True):
        content = input("输入你的问题: ")
        user_name = "Winlone"
        print(f"\033[36m[{user_name}]\033[0m:{content}")  # 打印弹幕信息
        if not QuestionList.full():
            QuestionName.put(user_name)  # 将用户名放入队列
            QuestionList.put(content)  # 将弹幕消息放入队列
            time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            LogsList.put(f"[{time1}] [{user_name}]：{content}")
            print('\033[32mSystem>>\033[0m已将该条弹幕添加入问题队列')
        else:
            print('\033[32mSystem>>\033[0m队列已满，该条弹幕被丢弃')
        #执行ai回复线程
        # thread1 = threading.Thread(target=all)
        # thread1.start()
        check_answer();
        # check_tts();
        # check_mpv();

def all():
    check_answer();
    check_tts();
    check_mpv();

#mode:instruct/chat/chat-instruct  preset:Alpaca/Winlone(自定义)  character:角色卡Rengoku/Ninya  
def chat_tgw(content,character,mode,preset):
    url = "http://127.0.0.1:5000/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    history.append({"role": "user", "content": content})
    data = {
        "mode": mode,
        "character": character,
        'your_name': 'Winlone',
        'user_input': content,
        "messages": history,

        "preset":preset,
        'do_sample': True,
        'truncation_length': 4000,
        'seed': -1,
        'add_bos_token': True,
        'ban_eos_token': False,
        'skip_special_tokens': True
    }
    response = requests.post(url, headers=headers, json=data, verify=False, stream=True)
    assistant_message = response.json()['choices'][0]['message']['content']
    #history.append({"role": "assistant", "content": assistant_message})
    return assistant_message



def ai_response():
    """
    从问题队列中提取一条，生成回复并存入回复队列中
    :return:
    """
    global is_ai_ready
    global QuestionList
    global AnswerList
    global QuestionName
    global LogsList
    global history
    prompt = QuestionList.get()
    user_name = QuestionName.get()
    ques = LogsList.get()
    response=chat_tgw(prompt,"111","chat","Winlone");
    answer = f'回复{user_name}：{response}'
    #加入回复列表，并且后续合成语音
    AnswerList.put(f'{prompt}'+","+answer)
    current_question_count = QuestionList.qsize()
    print(f"\033[31m[ChatGLM]\033[0m{answer}")  # 打印AI回复信息
    print(f'\033[32mSystem>>\033[0m[{user_name}]的回复已存入队列，当前剩余问题数:{current_question_count}')
    time2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("./logs.txt", "a", encoding="utf-8") as f:  # 将问答写入logs
        f.write(f"{ques}\n[{time2}] {answer}\n========================================================\n")
    is_ai_ready = True  # 指示AI已经准备好回复下一个问题


def check_answer():
    """
    如果AI没有在生成回复且队列中还有问题 则创建一个生成的线程
    :return:
    """
    global is_ai_ready
    global QuestionList
    global AnswerList
    if not QuestionList.empty() and is_ai_ready:
        is_ai_ready = False
        answers_thread = threading.Thread(target=ai_response())
        answers_thread.start()


def check_tts():
    """
    如果语音已经放完且队列中还有回复 则创建一个生成并播放TTS的线程
    :return:
    """
    global is_tts_ready
    if not AnswerList.empty() and is_tts_ready:
        is_tts_ready = False
        tts_thread = threading.Thread(target=tts_generate())
        tts_thread.start()


def tts_generate():
    """
    从回复队列中提取一条，通过edge-tts生成语音对应AudioCount编号语音
    :return:
    """
    global is_tts_ready
    global AnswerList
    global MpvList
    global AudioCount
    response = AnswerList.get()
    with open("./output/output.txt", "w", encoding="utf-8") as f:
        f.write(f"{response}")  # 将要读的回复写入临时文件
    subprocess.run(f'edge-tts --voice zh-CN-XiaoyiNeural --f .\output\output.txt --write-media .\output\output{AudioCount}.mp3 2>nul', shell=True)  # 执行命令行指令
    begin_name = response.find('回复')
    end_name = response.find("：")
    name = response[begin_name+2:end_name]
    print(f'\033[32mSystem>>\033[0m对[{name}]的回复已成功转换为语音并缓存为output{AudioCount}.mp3')

    #表情加入:使用键盘控制VTube
    # emote_thread = threading.Thread(target=emote_show(response))
    # emote_thread.start()
    
    #加入音频播放列表
    MpvList.put(AudioCount)
    AudioCount += 1
    is_tts_ready = True  # 指示TTS已经准备好回复下一个问题

def emote_show(response):
    #表情加入:使用键盘控制VTube
    keyboard = Controller()
    good = ["好", "不错", "哈" , "开心"]
    if is_array_contain_string(good,response) == True:
       keyboard.press("1")
       time.sleep(5)
       keyboard.release("1")

def is_array_contain_string(string_array, target_string):
    for s in string_array:
        if s in target_string:
            return True
    return False

def check_mpv():
    """
    若mpv已经播放完毕且播放列表中有数据 则创建一个播放音频的线程
    :return:
    """
    global is_mpv_ready
    global MpvList
    if not MpvList.empty() and is_mpv_ready:
        is_mpv_ready = False
        tts_thread = threading.Thread(target=mpv_read())
        tts_thread.start()


def mpv_read():
    """
    按照MpvList内的名单播放音频直到播放完毕
    :return:
    """
    global MpvList
    global is_mpv_ready
    while not MpvList.empty():
        temp1 = MpvList.get()
        current_mpvlist_count = MpvList.qsize()
        print(f'\033[32mSystem>>\033[0m开始播放output{temp1}.mp3，当前待播语音数：{current_mpvlist_count}')
        subprocess.run(f'mpv.exe -vo null .\output\output{temp1}.mp3 1>nul', shell=True)  # 执行命令行指令
        subprocess.run(f'del /f .\output\output{temp1}.mp3 1>nul', shell=True)
    is_mpv_ready = True


def main():
    # sched1.add_job(check_answer, 'interval', seconds=1, id=f'answer', max_instances=4)
    # sched1.add_job(check_tts, 'interval', seconds=1, id=f'tts', max_instances=4)
    # sched1.add_job(check_mpv, 'interval', seconds=1, id=f'mpv', max_instances=4)
    # sched1.start()
    input_msg()  #输入框


if __name__ == '__main__':
    main()
