# -*- coding: utf-8 -*-
"""Short animated cutscenes (drawn in code, no external assets)."""
import math, random, pygame
from gfx import *

def _key(sc, x, y, t, s=1.0):
    pygame.draw.circle(sc, GOLD, (int(x), int(y)), int(7 * s), 3); pygame.draw.line(sc, GOLD, (x + 6 * s, y), (x + 22 * s, y), 3)
    pygame.draw.line(sc, GOLD, (x + 17 * s, y), (x + 17 * s, y + 6 * s), 3); pygame.draw.line(sc, GOLD, (x + 22 * s, y), (x + 22 * s, y + 5 * s), 3)
    k = .5 + .5 * math.sin(t * 8); pygame.draw.line(sc, WHITE, (x - 8, y - 8), (x - 8 + 6 * k, y - 8 - 6 * k), 2)

def _torch(sc, x, y, t):
    fl = 4 * math.sin(t * 13 + x) + 2 * math.sin(t * 31)
    gl = pygame.Surface((90, 90), pygame.SRCALPHA); pygame.draw.circle(gl, (255, 150, 40, 50), (45, 45), 44); sc.blit(gl, (x - 45, y - 50))
    pygame.draw.rect(sc, (110, 70, 40), (x - 3, y, 6, 22)); pygame.draw.circle(sc, (255, 120, 30), (x, int(y - fl / 2)), int(8 + fl / 2)); pygame.draw.circle(sc, (255, 225, 110), (x, y + 1), 5)

# ---------------------------------------------------------------- intro
def sc_city(g, sc, t):
    gradient(sc, (8, 8, 40), (90, 50, 130)); stars(sc, t, 1); moon(sc, 640, 160, t)
    skyline(sc, t, 420, 1, (34, 26, 80), 6, 110, 230, True); skyline(sc, t, 480, 2, (20, 14, 52), 14, 80, 170, True)
    pygame.draw.rect(sc, (62, 52, 96), (0, 470, W, 90))
    for i in range(0, W, 40): pygame.draw.line(sc, (45, 36, 76), (i, 470), (i, 560), 2)
    for j in (500, 530): pygame.draw.line(sc, (45, 36, 76), (0, j), (W, j), 2)
    pygame.draw.rect(sc, (62, 52, 96), (0, 462, W, 10))
    for i in range(0, W, 40): pygame.draw.rect(sc, (62, 52, 96), (i + 4, 452, 22, 12))
    g.avatar_big(150, 464, g.pal, "side", 1, False, 0, k=2)
def _room(sc, t):
    gradient(sc, (82, 48, 52), (42, 26, 38)); pygame.draw.rect(sc, (70, 42, 34), (0, 430, W, 130))
    pygame.draw.rect(sc, (22, 20, 62), (90, 130, 150, 170)); moon(sc, 165, 190, t, 22); stars(sc, t, 5, 12, 300)
    pygame.draw.rect(sc, (140, 100, 70), (90, 130, 150, 170), 6); pygame.draw.line(sc, (140, 100, 70), (165, 130), (165, 300), 5); pygame.draw.line(sc, (140, 100, 70), (90, 215), (240, 215), 5)
    fl = .75 + .25 * math.sin(t * 9) * math.sin(t * 3.7)
    gl = pygame.Surface((520, 420), pygame.SRCALPHA)
    for k in range(6): pygame.draw.circle(gl, (255, 190, 90, int(14 * fl)), (260, 210), 70 + k * 32)
    sc.blit(gl, (240, 190)); pygame.draw.rect(sc, (100, 70, 50), (560, 330, 150, 14)); pygame.draw.rect(sc, (100, 70, 50), (580, 344, 10, 90)); pygame.draw.rect(sc, (100, 70, 50), (680, 344, 10, 90))
def sc_father(g, sc, t):
    _room(sc, t); g.avatar_big(270, 452, FATHER, "side", 1, False, 0, k=4); g.avatar_big(520, 452, g.pal, "side", -1, False, 0, k=3)
    if t < 1.3: _key(sc, 312, 396 + 4 * math.sin(t * 4), t)
    elif t < 3.0:
        k = (t - 1.3) / 1.7; x = 312 + 172 * k; y = 396 + 8 * k - 80 * math.sin(k * math.pi); _key(sc, x, y, t)
        for i in range(6): pygame.draw.circle(sc, (255, 230, 140), (int(x - i * 8), int(y + i * 3 + math.sin(t * 20 + i) * 3)), 3 - i // 3)
    else: _key(sc, 480, 404, t, .8)
def sc_vanish(g, sc, t):
    _room(sc, t); a = 1 - clamp((t - .8) / 2.2)
    if a > 0:
        g.avatar_big(270, 452, FATHER, "side", 1, False, 0, k=4, alpha=int(255 * a))
        for i in range(24):
            ph = (t * .8 + i * .37) % 1; x = 270 + 50 * math.sin(i * 2.1 + t); y = 440 - ph * 260
            pygame.draw.circle(sc, (255, 220, 120), (int(x), int(y)), int(2 + 2 * (1 - ph)))
    g.avatar_big(520, 452, g.pal, "front", 1, False, 0, k=3)
    pygame.draw.rect(sc, (245, 240, 220), (610, 312, 46, 18), border_radius=2); _key(sc, 586, 322, t, .8)
    g.text("0", g.f_m, (60, 30, 30), (633, 321))
def sc_door(g, sc, t):
    gradient(sc, (10, 10, 24), (34, 24, 56)); pygame.draw.polygon(sc, (28, 22, 44), [(0, 560), (W, 560), (W // 2 + 120, 380), (W // 2 - 120, 380)])
    for i in range(-4, 5): pygame.draw.line(sc, (46, 36, 70), (W // 2 + i * 22, 380), (W // 2 + i * 120, 560), 2)
    _torch(sc, 90, 260, t); _torch(sc, 710, 260, t)
    op = ease_out((t - 2.8) / 1.6); dx = int(op * 80)
    pygame.draw.rect(sc, (70, 62, 96), (W // 2 - 110, 150, 220, 260), border_radius=10)
    if op > 0:
        gl = pygame.Surface((W, H), pygame.SRCALPHA); pygame.draw.polygon(gl, (255, 235, 160, 90), [(W // 2, 280), (W // 2 - 260, 560), (W // 2 + 260, 560)]); sc.blit(gl, (0, 0))
        pygame.draw.rect(sc, (255, 240, 180), (W // 2 - 80 + 0, 180, 160, 230))
    for sgn in (-1, 1):
        px = W // 2 - 80 - (dx * sgn < 0) * 0 + (0 if sgn < 0 else 80) + sgn * dx
        pygame.draw.rect(sc, (95, 84, 130), (px, 180, 80, 230)); pygame.draw.rect(sc, (60, 52, 90), (px, 180, 80, 230), 3)
    if op < 1:
        k = 1 + .08 * math.sin(t * 5); pygame.draw.circle(sc, (255, 210, 90), (W // 2, 290), int(30 * k), 4); g.text("0", g.f_xl, (255, 210, 90), (W // 2, 290))
    wx = 60 + min(1, t / 2.6) * 300; g.avatar_big(wx, 535, g.pal, "side", 1, t < 2.6, t * 12, k=3)
def sc_alarm(g, sc, t):
    gradient(sc, (20, 16, 30), (44, 24, 44)); pygame.draw.rect(sc, (50, 36, 62), (0, 440, W, 120))
    for sx in (40, 600):
        pygame.draw.rect(sc, (70, 50, 40), (sx, 130, 150, 300), border_radius=4)
        for r in range(4):
            for i in range(6): pygame.draw.rect(sc, CONFETTI[(i + r * 2) % 5], (sx + 8 + i * 23, 142 + r * 72, 18, 56))
    pygame.draw.rect(sc, (20, 22, 30), (260, 150, 280, 190), border_radius=10); pygame.draw.rect(sc, (60, 20, 24), (272, 162, 256, 160), border_radius=6)
    on = int(t * 4) % 2
    g.text("تم العثور على وريث", g.f_m, (255, 90, 90) if on else (255, 160, 160), (400, 215)); g.text("المشروع صفر", g.f_m, (255, 90, 90) if on else (255, 160, 160), (400, 265))
    ov = pygame.Surface((W, H), pygame.SRCALPHA); ov.fill((255, 0, 0, int(50 * (.5 + .5 * math.sin(t * 8))))); sc.blit(ov, (0, 0))
    g.avatar_big(250, 520, g.pal, "front", 1, False, 0, k=3)
    x = W + 60 - ease_out((t - 1.6) / 2.2) * 250
    if t > 1.6:
        gl = pygame.Surface((220, 220), pygame.SRCALPHA)
        for k in range(5): pygame.draw.circle(gl, (255, 200, 100, 22), (110, 110), 100 - k * 16)
        sc.blit(gl, (x - 140, 368)); g.avatar_big(x, 520, ORMAN, "side", -1, t < 3.8, t * 9, k=3)
        pygame.draw.circle(sc, (255, 220, 120), (int(x - 30), 480), 8)

# ---------------------------------------------------------------- ending
def sc_gate(g, sc, t):
    gradient(sc, (30, 24, 64), (90, 60, 120)); stars(sc, t, 7); pygame.draw.rect(sc, (60, 50, 90), (0, 400, W, 160))
    op = ease_out((t - .8) / 3)
    gl = pygame.Surface((W, H), pygame.SRCALPHA)
    if op > 0:
        pygame.draw.polygon(gl, (255, 240, 170, int(110 * op)), [(W // 2, 250), (W // 2 - 420, 560), (W // 2 + 420, 560)]); sc.blit(gl, (0, 0))
        pygame.draw.rect(sc, (255, 245, 200), (W // 2 - 100 + int(50 * op), 160, int(200 - 100 * op), 250))
    pygame.draw.rect(sc, (80, 70, 110), (W // 2 - 140, 130, 280, 290), border_radius=16, width=10)
    for sgn in (-1, 1):
        w = int(100 * (1 - op)); x = W // 2 - 100 if sgn < 0 else W // 2 + 100 - w
        pygame.draw.rect(sc, (100, 90, 140), (x, 160, w, 250)); pygame.draw.rect(sc, (66, 58, 96), (x, 160, w, 250), 3)
    if op < .5: g.text("0", g.f_xl, GOLD, (W // 2, 285))
    for i, p in enumerate(AVATARS): g.avatar_big(250 + i * 90, 500, p, "back", 1, False, 0, k=3)
    g.avatar_big(640, 500, KING, "side", -1, False, 0, k=3)
def sc_outside(g, sc, t):
    gradient(sc, (255, 170, 110), (130, 210, 250)); r = ease_out(t / 4)
    pygame.draw.circle(sc, (255, 240, 170), (560, int(330 - 150 * r)), 46)
    mountains(sc, 360, (110, 170, 190), 1, 80); mountains(sc, 400, (60, 150, 110), 3, 60, shift=t * .1)
    pygame.draw.rect(sc, (70, 190, 120), (0, 430, W, 130))
    for i in range(8): pygame.draw.rect(sc, (255, 220, 120) if i % 2 else (255, 255, 255), (40 + i * 20, 372 + (i % 3) * 5, 8, 14))
    for i in range(14): pygame.draw.rect(sc, (255, 240, 160), (500 + i * 14, 346 - (i * 7) % 28, 7, 24 + (i * 5) % 20))
    for i in range(5):
        bx = (t * 60 + i * 170) % (W + 100) - 50; by = 110 + i * 24 + 10 * math.sin(t * 3 + i); w = 6 * math.sin(t * 10 + i)
        pygame.draw.lines(sc, (60, 60, 90), False, [(bx - 8, by + w), (bx, by), (bx + 8, by + w)], 2)
    pygame.draw.polygon(sc, (60, 150, 220), [(0, 480), (W, 470), (W, 560), (0, 560)])
    for i, p in enumerate(AVATARS): g.avatar_big((t * 70 + 40 - i * 70) % (W + 200) - 60, 510, p, "side", 1, True, t * 11 + i, k=3)
def sc_zero(g, sc, t):
    sc.fill((8, 8, 26)); stars(sc, t, 9, 80, 560)
    k = 1 + .05 * math.sin(t * 3)
    for i in range(6): pygame.draw.circle(sc, (255, 200, 80), (W // 2, 250), int((60 + i * 22) * k), 2)
    gl = pygame.Surface((W, H), pygame.SRCALPHA)
    for i in range(7): pygame.draw.circle(gl, (255, 200, 80, 12), (W // 2, 250), 80 + i * 26)
    sc.blit(gl, (0, 0)); g.text("0", g.f_xl, GOLD, (W // 2, 250))
    for i in range(12):
        a = t * .8 + i * math.pi / 6; pygame.draw.circle(sc, CONFETTI[i % 5], (int(W // 2 + 190 * k * math.cos(a)), int(250 + 190 * k * math.sin(a))), 4)
# ---------------------------------------------------------------- november
def sc_nov(g, sc, t):
    gradient(sc, (20, 30, 80), (250, 150, 90)); r = ease_out(t / 5); pygame.draw.circle(sc, (255, 235, 160), (200, int(400 - 170 * r)), 50)
    mountains(sc, 330, (90, 80, 130), 2, 110); mountains(sc, 390, (50, 90, 80), 5, 90, shift=t * .1); mountains(sc, 450, (20, 70, 50), 8, 60)
    pygame.draw.rect(sc, (16, 60, 44), (0, 470, W, 90)); draw_flag(sc, 440, 150, 260, 170, t, 8)
    for i in range(3): pygame.draw.circle(sc, (255, 255, 255), (int((t * 30 + i * 280) % (W + 100)), 70 + i * 26), 18)

INTRO_SCENES = [
 (sc_city, 6.0, "مدينة نوفيرا… أسوار ضخمة وأبراج شاهقة، وسكان يظنون أن ما وراء الأسوار ظلام لا ينتهي."),
 (sc_father, 6.0, "كان والد كاير يقول له دائمًا: «لا تصدّق كل ما تراه يا كاير، فبعض الحقائق تُدفن حتى لا يستيقظ الناس»."),
 (sc_vanish, 5.5, "وفي ليلة مظلمة اختفى الأب… وترك مفتاحًا صغيرًا وورقة كُتب عليها رقم واحد فقط: صفر."),
 (sc_door, 5.5, "تتبّع كاير الرقم حتى وصل إلى باب قديم في الأرشيف لم يجرؤ أحد على فتحه."),
 (sc_alarm, 5.5, "وفجأة ظهر ضوء أحمر على الشاشة… ولم يكن كاير وحده في الأرشيف!"),
]
ENDING_SCENES = [
 (sc_gate, 6.0, "وضع كاير يده على الرمز، فتحرّك الحجر ببطء… وانفتحت البوابة القديمة."),
 (sc_outside, 6.5, "لم يكن وراء الأسوار ظلام أبدي… كان هناك عالم كامل: أرض خضراء ومياه صافية ومدن تتلألأ عند الأفق."),
 (sc_zero, 5.0, "«الصفر ليس نهاية العدّ، بل بدايته»."),
]
NOV_SCENES = [
 (sc_nov, 7.0, "أول نوفمبر 1954… ليلة انطلقت فيها الثورة التحريرية المجيدة، فكانت بداية الطريق نحو الحرية والاستقلال."),
]
