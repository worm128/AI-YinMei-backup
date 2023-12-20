# **AI-YinMei**

- AI 虚拟主播 Vtuber 研发(N 卡版本)
- AI 名称：吟美
- 开发者：Winlone
- B 站频道：程序猿的退休生活
- Q 群：27831318
- 版本：1.0

## **介绍**

- 支持本地 LLM 模型 chatglm-6b 的 1 代~3 代的 AI 自然语言回复

- 支持对接 bilibili 直播间弹幕回复和进入直播间欢迎语

- 支持微软 edge-tts 语音合成

- 支持聊天记忆模式和扮演卡,可以多角色切换

- 支持 AI 训练

- 支持 Vtuber 表情控制

### 运行环境

- Python 3.11

### 调用类库

- 对应重要的 py 包<br>
  torch：2.1.0+cu121<br>
  peft：0.6.2<br>
  bilibili-api-python：16.1.1<br>
  edge-tts：6.1.9<br>
  pynput：1.7.6<br>
  APScheduler：3.10.4<br>
  transformers：4.35.2<br>

### 启动方式

1、启动应用层，在根目录

```bash
#进入虚拟环境
& 盘符:路径/pylib/aivenv/Scripts/Activate.ps1
#安装py包
pip install -r requirements.txt
#选择一、启动对接b站直播程序(此程序会对接后端text-generation-webui接口)
python bilibili-live-api.py
#选择二、启动对接b站直播程序(此程序直接在当前代码加载chatglm大语言模型+训练checkpoint)
python bilibili-live-local.py
```

2、启动 LLM 模型，进入 text-generation-webui

```bash
#进入虚拟环境
& 盘符:路径/pylib/aivenv/Scripts/Activate.ps1
#安装py包
pip install -r requirements.txt
#启动text-generation-webui程序，start.bat是我自定义的window启动脚本
./start.bat
```

3、皮肤启动，安装 steam，安装 VTube Studio<br>
这个自行下载 steam 平台，在平台里面有一个 VTube Studio 软件，它就是启动 live2D 的虚拟主播皮肤<br>

4、其他<br>
安装虚拟声卡：虚拟声卡驱动（Virtual Audio Cable）4.66 官方版<br>

此外，需要在 text-generation-webui/models 路径放入 LLM 模型，我这里放的是 chatgml2 的模型，大家可以任意选择底层 LLM 模型，例如，千问、百川、chatglm、llama 等<br>
更多详细技术细节，请看技术文档：https://note.youdao.com/s/1k0x7BLt<br>

### 目录说明

- text-generation-webui【第三方工具】：<br>
  LLM 聚合接口，可以放置 chatglm 等大语言模型，然后进行参数配置后，再输入角色卡进行角色扮演聊天<br>
  https://github.com/oobabooga/text-generation-webui<br>
- LLaMA-Factory【AI 训练】：<br>
  AI 聚合训练工具，可以界面化配置训练参数，可视化 ai 训练，相当强大<br>
  https://github.com/hiyouga/LLaMA-Factory<br>
- ChatGLM、ChatGLM2、ChatGLM3【语言模型】：<br>
  放置的是清华大学研发的自然语言模型，可以自行添加如：百川、千问、LLAMA 等其他大语言模型<br>
- SillyTavern【第三方工具】：<br>
  酒馆，强大的 AI 角色扮演，但是该项目没有公开接口调用，而且 TTS 语言合成很缓慢，暂未集成使用<br>
  https://github.com/SillyTavern/SillyTavern<br>
- output【输出路径】：<br>
  输出的文本 txt、语音 mp3 文件都在这里<br>
- ChatGLM2\ptuning【AI 训练】：<br>
  ChatGLM 官方训练例子<br>
- ChatGLM2\ptuning\zero_nlp【AI 训练】：<br>
  ai 的 lora 训练模式

### 特别鸣谢

- LLM 模型：ChatGLM<br>
  https://github.com/THUDM/ChatGLM2-6B<br>
- 聚合 LLM 调用模型：text-generation-webui<br>
  https://github.com/oobabooga/text-generation-webui<br>
- AI 虚拟主播模型：B 站的·领航员未鸟·<br>
  https://github.com/AliceNavigator/AI-Vtuber-chatglm<br>
- AI 训练模型：LLaMA-Factory<br>
  https://github.com/hiyouga/LLaMA-Factory<br>
- MPV 播放器：MPV<br>
  https://github.com/mpv-player/mpv<br>
- 其他：<br>
  Lora 训练：https://github.com/yuanzhoulvpi2017/zero_nlp<br>
  ChatGLM 训练：https://github.com/hiyouga/ChatGLM-Efficient-Tuning<br>
  SillyTavern 酒馆：https://github.com/SillyTavern/SillyTavern<br>
  LoRA 中文训练：https://github.com/super-wuliao/LoRA-ChatGLM-Chinese-Alpaca<br>
  数据集-训练语料：https://github.com/codemayq/chinese-chatbot-corpus<br>

### 更多关注

- 讨论 Q 群：27831318<br>
