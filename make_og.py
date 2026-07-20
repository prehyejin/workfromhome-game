"""카톡/SNS 링크 미리보기용 썸네일(og-image.png) 생성.

게임 화면과 같은 팔레트를 쓴다. 문구를 바꾸려면 아래 상수만 고치고 다시 실행:
    python make_og.py
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

BG_TOP = (255, 249, 238)     # #FFF9EE
BG_BOT = (231, 244, 240)     # #E7F4F0
INK = (34, 48, 60)           # #22303c
TEAL = (15, 168, 148)        # #0FA894
RED = (232, 80, 58)          # #E8503A
GRAY = (120, 133, 143)

BOLD = "C:/Windows/Fonts/malgunbd.ttf"
REG = "C:/Windows/Fonts/malgun.ttf"

TITLE1 = "재택 하루에 월급 3%,"
TITLE2 = "당신은 며칠까지?"
SUB = "30초 밸런스 게임으로 알아보는 나의 재택 가격"
FOOT = "서울대 대학원 연구 프로젝트 · 익명 응답"


def font(path, size):
    return ImageFont.truetype(path, size)


def center(d, y, text, f, fill):
    w = d.textbbox((0, 0), text, font=f)[2]
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


img = Image.new("RGB", (W, H), BG_TOP)
d = ImageDraw.Draw(img)

# 세로 그라데이션 (게임 배경과 동일한 느낌)
for y in range(H):
    t = y / H
    d.line(
        [(0, y), (W, y)],
        fill=tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)),
    )

center(d, 92, "🏠  ⚖️  🏢".replace("🏠", "집").replace("⚖️", "vs").replace("🏢", "회사"),
       font(BOLD, 34), GRAY)

center(d, 168, TITLE1, font(BOLD, 74), INK)
center(d, 258, TITLE2, font(BOLD, 74), TEAL)

center(d, 372, SUB, font(REG, 34), (91, 103, 112))

# 요일 칩 — 재택 3일 예시 (게임의 week() 시각화를 단순화)
chips = [("월", 0), ("화", 1), ("수", 0), ("목", 1), ("금", 0)]
cw, ch, gap = 104, 76, 18
total = len(chips) * cw + (len(chips) - 1) * gap
x0 = (W - total) / 2
y0 = 440
fchip = font(BOLD, 34)
for i, (day, home) in enumerate(chips):
    x = x0 + i * (cw + gap)
    fill = (222, 244, 239) if home else (255, 255, 255)
    edge = TEAL if home else (214, 222, 228)
    d.rounded_rectangle([x, y0, x + cw, y0 + ch], radius=18, fill=fill, outline=edge, width=3)
    tw = d.textbbox((0, 0), day, font=fchip)[2]
    d.text((x + (cw - tw) / 2, y0 + 18), day, font=fchip, fill=TEAL if home else GRAY)

center(d, 556, FOOT, font(REG, 26), GRAY)

# 우상단 포인트 배지
badge = "-3%/일"
fb = font(BOLD, 32)
bw = d.textbbox((0, 0), badge, font=fb)[2]
d.rounded_rectangle([W - bw - 92, 52, W - 44, 112], radius=30, fill=RED)
d.text((W - bw - 68, 64), badge, font=fb, fill=(255, 255, 255))

img.save("og-image.png", "PNG", optimize=True)
print("og-image.png 생성 완료", img.size)
