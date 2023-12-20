from bilibili_api import live, sync, Credential

cred = Credential(
    sessdata="e0a77b8b,1712479559,b0ada*a2CjA_tzquQm9z8KRIPNPQaWGck1LsiRbDk4xA7MKyOCd5CQ-hVVyb-8XTVqu5baVpzBISVnE2MVdRSE1FRDE0TDFpVVVKMFg5UFl3bWthZHpuNEh2TUhSNnAyVXJJeHVKRGFFRkRQVGNGQzFQM2NkMFU1Sk5TU0RUa3lYbXphLXlZcnREWGI4NzlRIIEC",
    buvid3="0A13475A-402F-CB81-5E03-E1E992C5FF7C86303infoc",
)
room = live.LiveDanmaku("3033646", credential=cred)

@room.on('DANMU_MSG')
async def on_danmaku(event):
    # 收到弹幕
    print(event)

@room.on('SEND_GIFT')
async def on_gift(event):
    # 收到礼物
    print(event)

sync(room.connect())