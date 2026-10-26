# -*- coding: utf-8 -*-
"""ما وراء الصفر  |  Beyond Zero  -  educational adventure game (pygame)
Controls: arrows/WASD move - 1..4 or mouse answer - Esc pause - F11 fullscreen - M mute"""
import os, sys, math, random, json, array, datetime
import pygame
from gfx import *
import cutscene as cs
from questions import POOLS, SUBJECTS

BASE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
ANDROID = "ANDROID_ARGUMENT" in os.environ
TOUCH = ANDROID or "--touch" in sys.argv          # on-screen d-pad for phones/tablets
SAVE = os.path.join(os.environ["ANDROID_PRIVATE"], "save.json") if "ANDROID_PRIVATE" in os.environ else os.path.expanduser("~/.beyond_zero_save.json")
T, COLS, ROWS, HUD = 40, 20, 12, 80
PS = 24

def lv(**k): return k
LEVELS = [
 lv(name="المستوى 1: الأرشيف", short="الأرشيف", theme="archive", kind="guard", pools=["M1", "ZERO"], walls=[7, 14], doors={7: 5, 14: 6},
    pillars=[(3,2),(3,3),(4,8),(4,9),(10,2),(10,3),(11,8),(11,9),(16,3),(16,8)],
    coins=[(2,1),(5,10),(2,10),(5,1),(9,5),(12,1),(12,10),(9,10),(16,1),(17,10),(16,5)],
    enemies=[(9,6,'v',80),(17,3,'v',90)], pickups=[("heart",12,5)], dark=88,
    floor=((70,150,185),(80,162,198)), wallc=[(222,92,112),(84,152,232),(250,182,62),(102,202,142),(162,102,212)], sky=((20,90,150),(100,210,190)),
    card=["الأرشيف", "ظهر ضوء أحمر على الشاشة القديمة: «تم العثور على وريث المشروع صفر».", "أبواب الأرشيف لا تُفتح إلا بالمعرفة: أولويات العمليات وسلاسل الجمع والطرح."]),
 lv(name="المستوى 2: النفق", short="النفق", theme="tunnel", kind="guard", pools=["M2"], walls=[5, 10, 15], doors={5: 3, 10: 8, 15: 5},
    pillars=[(2,2),(3,2),(2,8),(3,8),(7,3),(8,3),(7,8),(8,8),(12,3),(13,3),(12,8),(13,8),(17,3),(17,8)],
    coins=[(1,1),(4,10),(1,10),(6,1),(9,1),(6,10),(9,5),(11,1),(14,1),(11,10),(14,10),(16,1),(18,10),(18,1)],
    enemies=[(3,5,'v',90),(7,5,'h',110),(12,6,'h',110),(16,2,'v',120)], pickups=[("heart",8,6),("ice",13,5)], dark=96,
    floor=((208,152,92),(218,164,104)), wallc=[(152,92,202),(222,112,72),(62,172,172),(232,172,62)], sky=((120,40,110),(250,160,70)),
    card=["النفق", "قال أورمان بصوت خافت: «الأسوار لم تُبنَ لحمايتكم، بل لحماية السرّ من سكانها».", "اهرب عبر النفق القديم… وأبوابه تسأل عن الأقواس وخاصية توزيع الضرب."]),
 lv(name="المستوى 3: المكتبة", short="المكتبة", theme="library", kind="guard", pools=["AR", "FR"], walls=[6, 12], doors={6: 3, 12: 8},
    pillars=[(3,2),(3,3),(3,8),(3,9),(9,2),(9,3),(9,8),(9,9),(15,2),(16,2),(15,9),(16,9)],
    coins=[(1,1),(5,10),(1,10),(5,1),(8,5),(11,1),(8,10),(11,10),(14,1),(18,10),(14,10),(18,1),(5,5)],
    enemies=[(2,5,'v',90),(9,5,'v',110),(16,5,'v',120)], pickups=[("heart",11,5),("ice",14,5)], dark=80,
    floor=((176,124,84),(188,136,94)), wallc=[(180,70,70),(70,120,180),(210,160,60),(90,150,100),(130,80,160)], sky=((90,50,30),(230,170,90)),
    card=["مكتبة نوفيرا", "وجد كاير في المكتبة كتبًا ممنوعة تتحدث عن العالم الخارجي.", "لغتك العربية وحسابك على الكسور هما المفتاح!"]),
 lv(name="المستوى 4: قاعة الحاسوب", short="الحاسوب", theme="computer", kind="robot", pools=["INFO"], walls=[4, 9, 14], doors={4: 8, 9: 3, 14: 6},
    pillars=[(2,2),(2,3),(2,9),(6,2),(7,2),(6,9),(7,9),(11,4),(12,4),(11,7),(12,7),(16,2),(17,2),(16,9),(17,9)],
    coins=[(1,1),(3,10),(1,10),(3,1),(5,5),(8,5),(6,6),(10,1),(13,1),(10,10),(13,10),(11,5),(15,5),(18,1),(18,10),(16,6)],
    enemies=[(2,5,'v',100),(6,5,'h',110),(12,5,'h',120),(16,5,'v',120)], pickups=[("heart",7,6),("ice",13,6)], dark=90,
    floor=((66,86,126),(74,96,138)), wallc=[(40,70,120),(60,110,200),(50,150,160),(110,90,200)], sky=((10,40,90),(60,200,220)),
    card=["قاعة الحاسوب", "في القاعة ملفات مشفّرة عن المشروع صفر، والروبوتات تحرسها!", "افتح الأبواب بمعلوماتك عن الجداول في معالج النصوص {Word}."]),
 lv(name="المستوى 5: المخبر", short="المخبر", theme="lab", kind="slime", pools=["SCI", "DIV"], walls=[5, 10, 15], doors={5: 6, 10: 4, 15: 7},
    pillars=[(2,3),(3,3),(2,8),(3,8),(7,2),(7,3),(8,9),(8,8),(12,3),(13,3),(12,9),(13,9),(17,3),(17,8)],
    coins=[(1,1),(4,10),(1,10),(4,1),(6,1),(9,1),(6,10),(9,5),(11,1),(14,1),(11,10),(14,10),(16,1),(18,10),(18,1),(6,5)],
    enemies=[(3,5,'v',110),(7,6,'h',120),(12,6,'h',130),(16,4,'v',130)], pickups=[("ice",8,6),("heart",13,5)], dark=55,
    floor=((120,200,170),(132,212,182)), wallc=[(236,240,250),(200,225,245),(250,215,225)], sky=((20,110,100),(170,240,200)),
    card=["المخبر", "في المخبر أجهزة غريبة وكائنات هلامية خضراء تحرس الممر!", "أسئلة العلوم والقسمة الإقليدية والعشرية. جمّد الأعداء بالبلّورة الزرقاء!"]),
 lv(name="المستوى 6: البوابة", short="البوابة", theme="gate", kind="guard", pools=["M1", "M2", "DIV", "FR", "AR", "INFO", "SCI", "ZERO"], final=True, walls=[6, 13], doors={6: 5, 13: 6},
    pillars=[(3,3),(3,8),(9,2),(9,3),(10,8),(10,9),(16,3),(16,8)],
    coins=[(1,1),(5,10),(1,10),(5,1),(8,5),(11,1),(8,10),(11,10),(15,1),(18,10),(15,10),(18,1)],
    enemies=[(4,2,'v',120),(8,5,'v',140),(12,3,'v',140),(16,5,'v',150),(2,9,'v',110)], pickups=[("heart",11,5),("ice",14,6)], dark=100,
    floor=((98,72,152),(108,84,164)), wallc=[(72,202,222),(242,112,182),(250,212,92),(132,112,242)], sky=((40,30,120),(200,90,200)),
    card=["البوابة", "وقف الملك زيركان أمام البوابة الحجرية: «ابتعد عن البوابة يا كاير!»", "أجب عن ثلاثة أسئلة من كل المواد لتفتح البوابة. كل خطأ يكلّفك قلبًا!"]),
 lv(name="ذكرى أول نوفمبر 1954", short="أول نوفمبر", theme="nov", kind="dust", pools=["NOV"], nov=True, walls=[7, 14], doors={7: 4, 14: 7},
    pillars=[(3,2),(4,2),(3,9),(4,9),(10,3),(11,3),(10,8),(11,8),(16,2),(17,2),(16,9),(17,9)],
    coins=[(1,1),(5,10),(1,10),(5,1),(9,5),(9,6),(12,1),(12,10),(16,5),(17,10),(17,1),(2,5)],
    enemies=[(9,2,'v',100),(12,5,'h',110),(17,4,'v',100)], pickups=[("heart",9,9)], dark=30,
    floor=((246,246,240),(222,240,228)), wallc=[(0,125,62),(245,245,245)], sky=((0,90,50),(150,30,40)),
    card=["أول نوفمبر 1954", "اندلعت الثورة التحريرية ليلة أول نوفمبر 1954 بقيادة جبهة التحرير الوطني.", "اجمع النجوم وأجب عن أسئلة التاريخ والحساب، ثم ارفع العلم الوطني!"]),
]

def make_sounds():
    snd = {}
    try: pygame.mixer.init(frequency=22050, size=-16, channels=1)
    except Exception: return snd
    def tone(freqs, dur, vol=.35):
        n = int(22050 * dur); b = array.array("h")
        for i in range(n):
            f = freqs[min(len(freqs) - 1, int(i / n * len(freqs)))]
            b.append(int(32767 * vol * (1 - i / n) * math.sin(2 * math.pi * f * i / 22050)))
        return b
    def mk(f, d, v=.35): return pygame.mixer.Sound(buffer=tone(f, d, v).tobytes())
    snd["coin"] = mk([988, 1319], .12); snd["ok"] = mk([523, 659, 784], .35); snd["bad"] = mk([220, 160], .35)
    snd["hit"] = mk([140, 90], .4); snd["door"] = mk([330, 440, 554], .3); snd["win"] = mk([523, 659, 784, 1047, 1319], 1.0)
    snd["pick"] = mk([660, 880, 1100], .25); snd["ice"] = mk([1500, 1100, 800], .4); snd["star"] = mk([784, 1047], .2)
    def song(notes, nd=.5, v=.12):
        b = array.array("h")
        for f in notes: b.extend(tone([f], nd, v))
        return pygame.mixer.Sound(buffer=b.tobytes())
    snd["music"] = song([220, 262, 330, 262, 196, 247, 294, 247, 175, 220, 262, 220, 196, 247, 294, 392])
    return snd

class Particle:
    def __init__(s, x, y, col, g=0, scr=False, speed=(40, 160), life=(.4, .9), size=4, spread=None):
        a = random.uniform(0, 6.28) if spread is None else random.uniform(*spread); v = random.uniform(*speed)
        s.x, s.y, s.vx, s.vy = x, y, math.cos(a) * v, math.sin(a) * v
        s.life = s.max = random.uniform(*life); s.col, s.g, s.scr, s.size = col, g, scr, size

class Game:
    def __init__(s):
        pygame.init()
        s.touch = TOUCH
        try: s.screen = pygame.display.set_mode((W, H), (pygame.SCALED | pygame.FULLSCREEN) if ANDROID else (pygame.SCALED | pygame.RESIZABLE))   # resizable window, auto-scaling
        except Exception: s.screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
        pygame.display.set_caption("ما وراء الصفر - Beyond Zero")
        ic = pygame.Surface((32, 32), pygame.SRCALPHA); pygame.draw.circle(ic, (50, 20, 110), (16, 16), 16); pygame.draw.circle(ic, GOLD, (16, 16), 11, 4); pygame.display.set_icon(ic)
        s.clock = pygame.time.Clock()
        f = os.path.join(BASE, "assets", "DejaVuSans.ttf"); fb = os.path.join(BASE, "assets", "DejaVuSans-Bold.ttf")
        s.f_s, s.f_m, s.f_b = pygame.font.Font(f, 19), pygame.font.Font(f, 24), pygame.font.Font(fb, 34)
        s.f_xl = pygame.font.Font(fb, 78); s.f_t = pygame.font.Font(fb, 62)
        s.snd = make_sounds(); s.mute = False
        if "music" in s.snd: s.snd["music"].set_volume(.3); s.snd["music"].play(-1)
        s.data = dict(high=0, unlocked=0, stars=[0] * 7, nov=0)
        try: s.data.update(json.load(open(SAVE)))
        except Exception: pass
        s.t = 0; s.st = 0; s.fa = 255; s.prev = None; s.state = "menu"; s.parts = []; s.pops = []
        s.shake = 0; s.flash = 0; s.disp = 0; s.bump = 0; s.last_score = 0; s.score = 0; s.score0 = 0; s.lives = 3
        s.level = 0; s.time = 0; s.px = s.py = 0; s.wp = 0; s.face = 1; s.view = "side"; s.moving = False; s.dust_t = 0
        s.sel = 0; s.pal = AVATARS[0]; s.lsel = 0; s.mi = 0; s.qt = 0; s.at = 0; s.door_anim = {}; s.freeze = 0
        s.deck = []; s.cs = []; s.csi = 0; s.cst = 0; s.cs_after = None; s.hov = [0] * 5; s.pending = "campaign"
        s.got = 0; s.total_coins = 1; s.gate_ok = 0; s.stars_got = 0; s.bonus = 0; s.nov_t = 0
        s.zeros = [[random.uniform(0, W), random.uniform(0, H), random.uniform(24, 70), random.uniform(10, 30)] for _ in range(22)]
        zi = s.f_xl.render("0", True, (255, 255, 255)); s.zero_tints = []
        for c in CONFETTI: im = zi.copy(); im.fill((*c, 255), special_flags=pygame.BLEND_RGBA_MULT); s.zero_tints.append(im)
        s.dark_base = pygame.Surface((W, ROWS * T), pygame.SRCALPHA)
        big = pygame.Surface((560, 560), pygame.SRCALPHA)
        for r in range(280, 0, -4): pygame.draw.circle(big, (0, 0, 0, int(150 * (1 - r / 280) ** .8)), (280, 280), r)
        s.mask_big = big; s.mask_small = pygame.transform.smoothscale(big, (190, 190))
        s.qs = pygame.Surface((W, H), pygame.SRCALPHA); s.blob = pygame.Surface((W, H), pygame.SRCALPHA)
        s.motes = [[random.uniform(20, W - 20), random.uniform(20, ROWS * T - 20), random.uniform(-14, 14), random.uniform(-14, 14), random.choice(CONFETTI), random.uniform(0, 6)] for _ in range(28)]
        s.grid = [["."] * COLS for _ in range(ROWS)]; s.opened = set(); s.coins = []; s.enemies = []; s.pickups = []
        s.ex = (18, 5); s.inv = 0; s.q = None; s.ctx = None

    # ------------------------------------------------------------ helpers
    def save(s):
        try: json.dump(s.data, open(SAVE, "w"))
        except Exception: pass
    def sound(s, k):
        if k in s.snd and not s.mute: s.snd[k].play()
    def toggle_mute(s):
        s.mute = not s.mute
        if "music" in s.snd: s.snd["music"].set_volume(0 if s.mute else .3)
    def text(s, t, font, col, pos, anchor="center", shadow=False):
        img = font.render(shape(t), True, col); r = img.get_rect(); setattr(r, anchor, pos)
        if shadow:
            sh = font.render(shape(t), True, (0, 0, 0)); sh.set_alpha(120); s.screen.blit(sh, r.move(2, 3))
        s.screen.blit(img, r); return r
    def wrap(s, t, font, maxw):
        out = []
        for para in protect(t).split("\n"):
            cur = ""
            for w in para.split(" "):
                c = (cur + " " + w).strip()
                if font.size(shape(c))[0] <= maxw: cur = c
                else: out.append(cur); cur = w
            out.append(cur)
        return out
    def para(s, t, font, col, cx, y, maxw, lh):
        for ln in s.wrap(t, font, maxw): s.text(ln, font, col, (cx, y), "midtop"); y += lh
        return y
    def para_fx(s, t, font, col, cx, y, maxw, lh, delay=.55, start=0, tm=None):
        tm = s.st if tm is None else tm
        for i, ln in enumerate(s.wrap(t, font, maxw)):
            k = clamp((tm - start - delay * i) / .6)
            if k > 0 and ln:
                img = font.render(shape(ln), True, col); img.set_alpha(int(255 * k)); s.screen.blit(img, img.get_rect(midtop=(cx, y + (1 - k) * 14)))
            y += lh
        return y
    def fade_text(s, t, font, col, pos, delay=0, anchor="center"):
        k = clamp((s.st - delay) / .6)
        if k <= 0: return
        img = font.render(shape(t), True, col); img.set_alpha(int(255 * k)); r = img.get_rect(); setattr(r, anchor, pos); s.screen.blit(img, r)
    def text_pop(s, t, font, col, pos, delay=0):
        k = clamp((s.st - delay) / .5)
        if k <= 0: return
        img = font.render(shape(t), True, col); sc = 1 + .6 * (1 - ease_back(k))
        img = pygame.transform.smoothscale(img, (max(1, int(img.get_width() * sc)), max(1, int(img.get_height() * sc)))); img.set_alpha(int(255 * clamp(k * 2)))
        sh = pygame.transform.smoothscale(font.render(shape(t), True, (0, 0, 0)), img.get_size()); sh.set_alpha(int(110 * clamp(k * 2)))
        s.screen.blit(sh, sh.get_rect(center=(pos[0] + 2, pos[1] + 3))); s.screen.blit(img, img.get_rect(center=pos))
    def avatar_big(s, cx, feet_y, pal, view, face, moving, phase, k=3, alpha=255):
        tmp = pygame.Surface((70, 80), pygame.SRCALPHA); draw_avatar(tmp, s.t, 35, 48, pal, view, face, moving, phase)
        img = pygame.transform.smoothscale(tmp, (70 * k, 80 * k))
        if alpha < 255: img.set_alpha(alpha)
        s.screen.blit(img, img.get_rect(center=(int(cx), int(feet_y - 23 * k))))
    def burst(s, x, y, n=40, scr=True):
        c = random.choice(CONFETTI)
        for _ in range(n): s.parts.append(Particle(x, y, lt(c, random.random() * .5), g=160, scr=scr, speed=(60, 240), life=(.8, 1.5), size=4))
    def draw_parts(s, scr, ox=0, oy=0):
        for p in s.parts:
            if p.scr == scr: pygame.draw.circle(s.screen, p.col, (int(p.x + ox), int(p.y + oy)), max(1, int(p.size * p.life / p.max)))
    def nov_info(s):
        today = datetime.date.today(); tgt = datetime.date(today.year, 11, 1)
        if today > tgt: tgt = datetime.date(today.year + 1, 11, 1)
        return (tgt - today).days, tgt.year - 1954

    # ------------------------------------------------------------ flow
    def go_card(s, i):
        s.level = i; s.score0 = s.score; s.state = "card"
    def start_cs(s, scenes, after):
        s.cs = scenes; s.csi = 0; s.cst = 0; s.cs_after = after; s.state = "cutscene"
    def new_campaign(s): s.score = 0; s.pending = "campaign"; s.state = "select"
    def confirm_avatar(s):
        s.pal = AVATARS[s.sel]; s.score = 0
        s.start_cs(cs.INTRO_SCENES, lambda: s.go_card(0))
    def start_level_from_menu(s, i):
        s.score = 0
        if LEVELS[i].get("nov"): s.start_cs(cs.NOV_SCENES, lambda: s.go_card(i))
        else: s.go_card(i)
    def menu_action(s, a):
        if a == "start": s.new_campaign()
        elif a == "levels": s.state = "levels"
        elif a == "nov": s.start_level_from_menu(6)
        elif a == "help": s.state = "help"
        elif a == "quit": return False
        return True
    def load_level(s):
        L = LEVELS[s.level]
        s.grid = [["#" if x in (0, COLS - 1) or y in (0, ROWS - 1) else "." for x in range(COLS)] for y in range(ROWS)]
        for wx in L["walls"]:
            for y in range(1, ROWS - 1): s.grid[y][wx] = "#"
            s.grid[L["doors"][wx]][wx] = "D"
        for (x, y) in L["pillars"]: s.grid[y][x] = "#"
        s.opened = set(); s.door_anim = {}; s.pops = []; s.coins = [list(c) for c in L["coins"]]; s.total_coins = len(s.coins); s.got = 0
        s.enemies = [dict(x=ex * T + 20, y=ey * T + 20, d=d, sp=sp, dir=1) for ex, ey, d, sp in L["enemies"]]
        s.pickups = [dict(k=k, x=x, y=y) for k, x, y in L["pickups"]]
        s.px, s.py = 1 * T + 20, 5 * T + 20; s.ex = (18, 5); s.inv = 0; s.time = 0; s.freeze = 0
        s.parts = []; s.gate_ok = 0; s.lives = 3; s.deck = []; s.view = "side"; s.face = 1; s.score = s.score0; s.disp = s.score0
        s.state = "play"
    def retry(s): s.score = s.score0; s.load_level()
    def build_deck(s):
        s.deck = [(q, p) for p in LEVELS[s.level]["pools"] for q in POOLS[p]]; random.shuffle(s.deck)
    def next_q(s):
        if not s.deck: s.build_deck()
        (q, opts, c, ex), p = s.deck.pop(); order = list(range(4)); random.shuffle(order)
        s.q = dict(q=q, opts=[opts[i] for i in order], c=order.index(c), ex=ex, sel=None, pool=p)
    def start_quiz(s, ctx): s.next_q(); s.ctx = ctx; s.state = "quiz"; s.qt = 0; s.at = 0
    def answer(s, i):
        q = s.q
        if q["sel"] is not None: return
        q["sel"] = i; s.at = 0
        if i == q["c"]:
            s.sound("ok"); s.score += 150 if s.ctx == "gate" else 100
            for _ in range(45): s.parts.append(Particle(W // 2, 330, random.choice(CONFETTI), g=520, scr=True, speed=(150, 480), life=(1, 1.7), size=5, spread=(-2.6, -.55)))
        else:
            s.sound("bad"); s.flash = .3
            if s.ctx == "gate": s.lives -= 1
            else: s.score = max(0, s.score - 50)
    def quiz_done(s):
        q = s.q; ok = q["sel"] == q["c"]
        if s.ctx == "gate":
            if s.lives <= 0: return s.end(False)
            if ok: s.gate_ok += 1
            if s.gate_ok >= 3: return s.level_complete()
            return s.start_quiz("gate")
        if ok:
            s.opened.add(s.ctx); s.sound("door"); s.door_anim[s.ctx] = 0
            s.pops.append(dict(x=s.ctx[0] * T + 20, y=s.ctx[1] * T + 10, t="+100", col=GREEN, life=1.2, big=True))
            for _ in range(25): s.parts.append(Particle(s.ctx[0] * T + 20, s.ctx[1] * T + 20, GOLD))
        s.state = "play"
    def end(s, win):
        if s.score > s.data["high"]: s.data["high"] = s.score
        s.save(); s.state = "over"
    def level_complete(s):
        L = LEVELS[s.level]; s.bonus = max(0, 500 - 5 * int(s.time)); s.score += s.bonus
        r = s.got / max(1, s.total_coins); s.stars_got = 1 + (r >= .6) + (r >= .9)
        i = s.level; s.data["stars"][i] = max(s.data["stars"][i], s.stars_got)
        if not L.get("nov"): s.data["unlocked"] = max(s.data["unlocked"], min(i + 1, 5))
        if s.score > s.data["high"]: s.data["high"] = s.score
        s.save(); s.sound("win"); s.state = "nov_end" if L.get("nov") else "levelup"
        if L.get("nov"): s.nov_t = 0

    # ------------------------------------------------------------ update
    def solid(s, r):
        for ty in range(r.top // T, (r.bottom - 1) // T + 1):
            for tx in range(r.left // T, (r.right - 1) // T + 1):
                if not (0 <= tx < COLS and 0 <= ty < ROWS): return True
                c = s.grid[ty][tx]
                if c == "#" or (c == "D" and (tx, ty) not in s.opened): return True
        return False
    def prect(s): r = pygame.Rect(0, 0, PS, PS); r.center = (int(s.px), int(s.py)); return r
    def update(s, dt):
        s.t += dt; s.st += dt
        grp = ("play", "quiz", "pause")
        if s.state != s.prev:
            s.st = 0
            if not (s.prev in grp and s.state in grp) and s.state != "cutscene": s.fa = 255
            s.prev = s.state
        s.fa = max(0, s.fa - 700 * dt); s.flash = max(0, s.flash - dt)
        for z in s.zeros: z[1] -= z[3] * dt; z[1] = z[1] if z[1] > -80 else H + 80
        for p in s.parts: p.vy += p.g * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.life -= dt
        s.parts = [p for p in s.parts if p.life > 0]
        for p in s.pops: p["y"] -= 42 * dt; p["life"] -= dt
        s.pops = [p for p in s.pops if p["life"] > 0]
        for k in list(s.door_anim):
            s.door_anim[k] += dt
            if s.door_anim[k] > .7: del s.door_anim[k]
        for m in s.motes: m[0] = (m[0] + m[2] * dt) % W; m[1] = (m[1] + m[3] * dt) % (ROWS * T)
        s.shake = max(0, s.shake - dt); s.disp += (s.score - s.disp) * min(1, 9 * dt)
        if s.score > s.last_score: s.bump = 1
        s.last_score = s.score; s.bump = max(0, s.bump - 3 * dt)
        if s.state in ("win", "levelup") and random.random() < dt * 45:
            s.parts.append(Particle(random.uniform(0, W), -10, random.choice(CONFETTI), g=140, scr=True, speed=(30, 120), life=(3, 4), size=5, spread=(1.2, 1.9)))
        if s.state in ("nov_end",):
            s.nov_t += dt
            if random.random() < dt * 1.6: s.burst(random.uniform(120, W - 120), random.uniform(60, 260), 36)
        if s.state == "menu":
            for i, r in enumerate(s.menu_rects()): s.hov[i] += ((1 if r.collidepoint(pygame.mouse.get_pos()) or s.mi == i else 0) - s.hov[i]) * min(1, 12 * dt)
        if s.state == "cutscene":
            s.cst += dt
            if s.cst >= s.cs[s.csi][1]:
                s.csi += 1; s.cst = 0
                if s.csi >= len(s.cs): s.cs_after()
        if s.state == "quiz":
            s.qt += dt
            if s.q["sel"] is not None: s.at += dt
        if s.state == "play": s.update_play(dt)
    def update_play(s, dt):
        L = LEVELS[s.level]
        s.time += dt; s.inv = max(0, s.inv - dt); s.freeze = max(0, s.freeze - dt)
        k = pygame.key.get_pressed()
        dx = (k[pygame.K_RIGHT] or k[pygame.K_d]) - (k[pygame.K_LEFT] or k[pygame.K_a])
        dy = (k[pygame.K_DOWN] or k[pygame.K_s]) - (k[pygame.K_UP] or k[pygame.K_w])
        if s.touch and pygame.mouse.get_pressed()[0]:
            vx, vy = pygame.mouse.get_pos(); vx -= 105; vy -= H - 105
            if vx * vx + vy * vy < 130 * 130:
                if abs(vx) > 22: dx = 1 if vx > 0 else -1
                if abs(vy) > 22: dy = 1 if vy > 0 else -1
        s.moving = bool(dx or dy)
        if dx: s.face = 1 if dx > 0 else -1; s.view = "side"
        elif dy: s.view = "front" if dy > 0 else "back"
        if s.moving:
            s.wp += 14 * dt; s.dust_t -= dt
            if s.dust_t <= 0: s.dust_t = .07; s.parts.append(Particle(s.px - s.face * 6, s.py + 11, (150, 150, 165), speed=(5, 28), life=(.25, .5), size=3))
        if dx and dy: dx *= .7071; dy *= .7071
        for ax, ay in ((dx * 190 * dt, 0), (0, dy * 190 * dt)):
            ox, oy = s.px, s.py; s.px += ax; s.py += ay
            if s.solid(s.prect()): s.px, s.py = ox, oy
        pr = s.prect()
        for c in s.coins[:]:
            if pr.colliderect(pygame.Rect(c[0] * T + 8, c[1] * T + 8, 24, 24)):
                s.coins.remove(c); s.score += 10; s.got += 1; s.sound("star" if L["theme"] == "nov" else "coin")
                s.pops.append(dict(x=c[0] * T + 20, y=c[1] * T + 6, t="+10", col=GOLD, life=.8, big=False))
                for _ in range(8): s.parts.append(Particle(c[0] * T + 20, c[1] * T + 20, GOLD))
        for p in s.pickups[:]:
            if pr.colliderect(pygame.Rect(p["x"] * T + 6, p["y"] * T + 6, 28, 28)):
                s.pickups.remove(p)
                if p["k"] == "heart":
                    if s.lives < 3: s.lives += 1; txt = "+1"
                    else: s.score += 50; txt = "+50"
                    s.sound("pick"); s.pops.append(dict(x=p["x"] * T + 20, y=p["y"] * T + 6, t=txt, col=(255, 120, 150), life=1, big=True))
                else:
                    s.freeze = 4.5; s.sound("ice"); s.pops.append(dict(x=p["x"] * T + 20, y=p["y"] * T + 6, t="❄", col=(160, 230, 255), life=1.2, big=True))
                for _ in range(16): s.parts.append(Particle(p["x"] * T + 20, p["y"] * T + 20, (255, 255, 255) if p["k"] == "ice" else (255, 120, 150)))
        near = None
        for y in range(ROWS):
            for x in range(COLS):
                if s.grid[y][x] == "D" and (x, y) not in s.opened and pr.inflate(8, 8).colliderect(pygame.Rect(x * T, y * T, T, T)): near = (x, y)
        if near is None: s.door_lock = None
        elif near != getattr(s, "door_lock", None): s.door_lock = near; return s.start_quiz(near)
        for e in s.enemies:
            if s.freeze <= 0:
                nx = e["x"] + (e["dir"] * e["sp"] * dt if e["d"] == "h" else 0); ny = e["y"] + (e["dir"] * e["sp"] * dt if e["d"] == "v" else 0)
                r = pygame.Rect(0, 0, 26, 26); r.center = (int(nx), int(ny))
                if s.solid(r): e["dir"] *= -1
                else: e["x"], e["y"] = nx, ny
                gr = pygame.Rect(0, 0, 26, 26); gr.center = (int(e["x"]), int(e["y"]))
                if s.inv <= 0 and gr.colliderect(pr.inflate(-6, -6)):
                    s.lives -= 1; s.sound("hit"); s.shake = .3; s.inv = 1.6; s.flash = .3
                    for _ in range(20): s.parts.append(Particle(s.px, s.py, RED))
                    if s.lives <= 0: return s.end(False)
                    s.px, s.py = 1 * T + 20, 5 * T + 20
        if pr.colliderect(pygame.Rect(s.ex[0] * T + 4, s.ex[1] * T + 4, T - 8, T - 8)):
            if L.get("final"): s.start_quiz("gate"); s.px -= 14
            else: s.level_complete()

    # ------------------------------------------------------------ events
    def menu_items(s): return [("ابدأ المغامرة", "start"), ("اختيار المرحلة", "levels"), ("ذكرى أول نوفمبر 1954", "nov"), ("كيف تلعب؟", "help"), ("خروج", "quit")]
    def menu_rects(s): return [pygame.Rect(W // 2 - 190, 238 + i * 56, 380, 46) for i in range(5)]
    def select_rects(s): return [pygame.Rect(0, 0, 220, 360).move(int(W - (i + .5) * W / 3 - 110), 110) for i in range(len(AVATARS))]
    def level_rect(s, i):
        row, col = divmod(i, 4); n = 4 if row == 0 else len(LEVELS) - 4; tot = n * 170 + (n - 1) * 20
        return pygame.Rect((W - tot) // 2 + (n - 1 - col) * 190, 100 + row * 200, 170, 180)
    def opt_rects(s): return [pygame.Rect(70, 190 + i * 62, 660, 52) for i in range(4)]
    def events(s):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                st = s.state; go = e.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER)
                if e.key == pygame.K_F11: pygame.display.toggle_fullscreen(); continue
                if e.key == pygame.K_m: s.toggle_mute(); continue
                if e.key in (pygame.K_ESCAPE, getattr(pygame, "K_AC_BACK", -1)):
                    if st == "menu": return False
                    if st == "play": s.state = "pause"
                    elif st == "pause": s.state = "play"
                    elif st == "cutscene": s.cs_after()
                    elif st == "quiz": pass
                    else: s.state = "menu"
                    continue
                if st == "menu":
                    if e.key in (pygame.K_DOWN, pygame.K_s): s.mi = (s.mi + 1) % 5
                    elif e.key in (pygame.K_UP, pygame.K_w): s.mi = (s.mi - 1) % 5
                    elif go:
                        if not s.menu_action(s.menu_items()[s.mi][1]): return False
                    elif e.key == pygame.K_h: s.state = "help"
                elif st == "select":
                    if e.key == pygame.K_RIGHT: s.sel = max(0, s.sel - 1)
                    elif e.key == pygame.K_LEFT: s.sel = min(len(AVATARS) - 1, s.sel + 1)
                    elif go: s.confirm_avatar()
                elif st == "levels":
                    n = len(LEVELS)
                    if e.key == pygame.K_RIGHT: s.lsel = max(0, s.lsel - 1)
                    elif e.key == pygame.K_LEFT: s.lsel = min(n - 1, s.lsel + 1)
                    elif e.key == pygame.K_UP and s.lsel >= 4: s.lsel -= 4
                    elif e.key == pygame.K_DOWN and s.lsel < 4: s.lsel = min(n - 1, s.lsel + 4)
                    elif go and s.level_open(s.lsel): s.start_level_from_menu(s.lsel)
                elif st == "help" and go: s.state = "menu"
                elif st == "cutscene" and go: s.cs_after()
                elif st == "card" and go: s.load_level()
                elif st == "levelup" and go: s.go_card(s.level + 1) if not LEVELS[s.level].get("final") else s.start_cs(cs.ENDING_SCENES, s.to_win)
                elif st == "win" and go: s.state = "menu"
                elif st == "nov_end" and go: s.state = "menu"
                elif st == "over" and go: s.retry()
                elif st == "pause" and (go or e.key == pygame.K_p): s.state = "play"
                elif st == "pause" and e.key == pygame.K_q: s.state = "menu"
                elif st == "play" and e.key == pygame.K_p: s.state = "pause"
                elif st == "quiz":
                    if s.q["sel"] is None and pygame.K_1 <= e.key <= pygame.K_4: s.answer(e.key - pygame.K_1)
                    elif s.q["sel"] is not None and go: s.quiz_done()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                st = s.state
                if st == "menu":
                    for i, r in enumerate(s.menu_rects()):
                        if r.collidepoint(e.pos):
                            if not s.menu_action(s.menu_items()[i][1]): return False
                elif st == "select":
                    for i, r in enumerate(s.select_rects()):
                        if r.collidepoint(e.pos):
                            if s.sel == i: s.confirm_avatar()
                            else: s.sel = i
                elif st == "levels":
                    for i in range(len(LEVELS)):
                        if s.level_rect(i).collidepoint(e.pos):
                            if s.lsel == i and s.level_open(i): s.start_level_from_menu(i)
                            else: s.lsel = i
                elif st == "quiz":
                    if s.q["sel"] is None:
                        for i, r in enumerate(s.opt_rects()):
                            if r.collidepoint(e.pos): s.answer(i)
                    else: s.quiz_done()
                elif st == "play" and s.touch and s.pause_rect().collidepoint(e.pos): s.state = "pause"
                elif st == "pause": s.state = "play"
                elif st == "cutscene" and s.cst > .4: s.cs_after()
                elif st in ("card", "levelup", "over", "win", "nov_end", "help") and s.st > .5:
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        return True
    def pause_rect(s): return pygame.Rect(W - 62, HUD + 8, 50, 50)
    def level_open(s, i): return i == 6 or i <= s.data["unlocked"]
    def to_win(s):
        s.state = "win"; s.sound("win")

    # ------------------------------------------------------------ drawing: backgrounds
    def bg(s, top=(50, 25, 110), bot=(240, 110, 100)):
        gradient(s.screen, top, bot)
        s.blob.fill((0, 0, 0, 0))
        for k in range(4):
            cx = W / 2 + 330 * math.sin(s.t * .25 + k * 1.7); cy = H / 2 + 200 * math.cos(s.t * .2 + k * 2.3)
            pygame.draw.circle(s.blob, (*CONFETTI[k], 34), (int(cx), int(cy)), 190); pygame.draw.circle(s.blob, (*CONFETTI[k], 30), (int(cx), int(cy)), 120)
        s.screen.blit(s.blob, (0, 0))
        for i, (x, y, sz, _) in enumerate(s.zeros):
            img = pygame.transform.smoothscale(s.zero_tints[i % 5], (int(sz), int(sz * 1.3))); img.set_alpha(70); s.screen.blit(img, (x + 12 * math.sin(s.t * .8 + i), y))
    def menu_bg(s):
        sc = s.screen; gradient(sc, (12, 10, 52), (170, 70, 130)); stars(sc, s.t, 11, 70, 330); moon(sc, 725, 120, s.t)
        skyline(sc, s.t, 420, 21, (70, 38, 110), 5, 100, 220, True); skyline(sc, s.t, 480, 22, (34, 20, 70), 12, 70, 150, True)
        pygame.draw.rect(sc, (22, 14, 48), (0, 478, W, 90))
        for i, (x, y, sz, _) in enumerate(s.zeros[:10]):
            img = pygame.transform.smoothscale(s.zero_tints[i % 5], (int(sz * .8), int(sz))); img.set_alpha(45); sc.blit(img, (x, y))
        for m in s.motes:
            a = .5 + .5 * math.sin(s.t * 2 + m[5]); gl = pygame.Surface((14, 14), pygame.SRCALPHA); pygame.draw.circle(gl, (*m[4], int(70 * a)), (7, 7), 7); pygame.draw.circle(gl, (255, 255, 255, int(200 * a)), (7, 7), 2); sc.blit(gl, (m[0] - 7, m[1] + 80))

    # ------------------------------------------------------------ drawing: screens
    def draw(s):
        sc = s.screen; st = s.state
        if st == "menu":
            s.menu_bg()
            pul = (.5 + .5 * math.sin(s.t * 2)); col = mix(GOLD, (255, 250, 200), pul * .6)
            img = s.f_t.render(shape("ما وراء الصفر"), True, col); k = 1 + .03 * math.sin(s.t * 2); img = pygame.transform.smoothscale(img, (int(img.get_width() * k), int(img.get_height() * k)))
            sh = pygame.transform.smoothscale(s.f_t.render(shape("ما وراء الصفر"), True, (30, 10, 60)), img.get_size()); cy = 70 + int(6 * math.sin(s.t * 1.6))
            sc.blit(sh, sh.get_rect(center=(W // 2 + 3, cy + 4))); sc.blit(img, img.get_rect(center=(W // 2, cy)))
            s.text("Beyond Zero  -  مغامرة تعليمية في الحساب والمعلوماتية والعلوم", s.f_s, WHITE, (W // 2, 128))
            d, ann = s.nov_info()
            msg = "اليوم أول نوفمبر: كل عام وأنتم بخير!  الذكرى %d" % ann if d == 0 else "باقي %d يومًا على الذكرى %d لاندلاع الثورة" % (d, ann)
            pill = pygame.Rect(0, 0, 440, 34); pill.center = (W // 2, 170); pygame.draw.rect(sc, (20, 10, 50), pill, border_radius=17); pygame.draw.rect(sc, (0, 140, 70), pill, 2, border_radius=17)
            draw_flag(sc, pill.right - 44, pill.top + 4, 30, 20, s.t, 2, False); s.text(msg, s.f_s, WHITE, (pill.centerx - 10, pill.centery))
            s.text("الأعلى: %d" % s.data["high"], s.f_s, (190, 200, 235), (W // 2, 212))
            for i, (r, (t, a)) in enumerate(zip(s.menu_rects(), s.menu_items())):
                h = s.hov[i]; rr = r.inflate(int(18 * h), int(4 * h))
                base = {"nov": (0, 110, 60)}.get(a, (62, 52, 120)); hot = {"nov": (210, 40, 50)}.get(a, GOLD)
                pygame.draw.rect(sc, (0, 0, 0, 0) if False else dk(base, .5), rr.move(0, 4), border_radius=14)
                pygame.draw.rect(sc, mix(base, hot, h), rr, border_radius=14); pygame.draw.rect(sc, lt(mix(base, hot, h), .4), rr, 2, border_radius=14)
                sx = rr.left + ((s.t * 120 + i * 90) % (rr.width + 120)) - 60
                shine = pygame.Surface((26, rr.height), pygame.SRCALPHA); pygame.draw.polygon(shine, (255, 255, 255, 36), [(8, 0), (26, 0), (18, rr.height), (0, rr.height)])
                sc.set_clip(rr); sc.blit(shine, (sx, rr.top)); sc.set_clip(None)
                s.text(t, s.f_m, (30, 20, 0) if h > .6 and a != "nov" else WHITE, rr.center, shadow=True)
                if a == "nov": draw_flag(sc, rr.right - 46, rr.top + 11, 30, 22, s.t, 2, False)
            s.text("F11 ملء الشاشة  |  M كتم الصوت  |  النافذة قابلة لتغيير الحجم", s.f_s, (200, 190, 230), (W // 2, H - 18))
        elif st == "help":
            s.bg(); s.text_pop("كيف تلعب؟", s.f_b, GOLD, (W // 2, 50))
            lines = ["الحركة: الأسهم أو W A S D   |   إيقاف مؤقت: Esc   |   ملء الشاشة: F11   |   كتم الصوت: M",
                     "اجمع عملات الصفر لتكسب 10 نقاط لكل عملة.",
                     "اقترب من الباب الذهبي لتظهر لك مسألة. اختر الجواب بالأرقام 1-4 أو بالفأرة.",
                     "الإجابة الصحيحة تفتح الباب وتعطيك 100 نقطة، والخاطئة تخصم 50 نقطة.",
                     "إذا لمسك عدو خسرت قلبًا (3 قلوب لكل مرحلة). القلب الوردي يعوّضك قلبًا.",
                     "البلّورة الزرقاء تجمّد الأعداء لبضع ثوانٍ فيمكنك المرور بأمان.",
                     "المواد: الرياضيات والمعلوماتية والعلوم واللغة العربية وتاريخ الجزائر.",
                     "جرّب مرحلة «ذكرى أول نوفمبر 1954» من القائمة الرئيسية!"]
            y = 100
            for i, ln in enumerate(lines): y = s.para_fx(ln, s.f_s if i == 0 else s.f_m, WHITE, W // 2, y, 720, 30, start=.12 * i, delay=.2) + 10
            s.fade_text("اضغط Enter للعودة", s.f_s, GOLD, (W // 2, H - 40), 1.4)
        elif st == "select":
            s.bg(); s.text_pop("اختر شخصيتك", s.f_b, GOLD, (W // 2, 60))
            for i, (a, r) in enumerate(zip(AVATARS, s.select_rects())):
                sel = i == s.sel; r = r.inflate(14, 14) if sel else r
                pygame.draw.rect(sc, (92, 60, 172) if sel else (60, 40, 120), r, border_radius=18); pygame.draw.rect(sc, GOLD if sel else (120, 100, 190), r, 4 if sel else 2, border_radius=18)
                if sel: pygame.draw.ellipse(sc, (255, 200, 90), (r.centerx - 60, r.top + 198, 120, 22))
                s.avatar_big(r.centerx, r.top + 218, a, "front", 1, sel, s.t * 11 if sel else 0)
                s.text(a["name"], s.f_b, GOLD if sel else WHITE, (r.centerx, r.top + 262), shadow=True); s.para(a["desc"], s.f_s, WHITE, r.centerx, r.top + 292, 190, 22)
            s.fade_text("الأسهم للتنقل  |  Enter أو النقر للاختيار", s.f_s, GOLD, (W // 2, H - 40), .8)
        elif st == "levels":
            s.bg(); s.text_pop("اختيار المرحلة", s.f_b, GOLD, (W // 2, 52))
            for i, L in enumerate(LEVELS):
                r = s.level_rect(i); sel = i == s.lsel; op = s.level_open(i); r = r.inflate(12, 12) if sel else r
                pygame.draw.rect(sc, (30, 20, 70), r.move(0, 4), border_radius=16)
                g = pygame.Surface(r.size, pygame.SRCALPHA); gradient(g, L["sky"][0], L["sky"][1], r.height); sc.blit(g, r.topleft, special_flags=0) if False else None
                top = pygame.Surface((r.width, r.height)); 
                for yy in range(0, r.height, 3): pygame.draw.rect(top, mix(L["sky"][0], L["sky"][1], yy / r.height), (0, yy, r.width, 3))
                m = pygame.Surface(r.size, pygame.SRCALPHA); pygame.draw.rect(m, (255, 255, 255, 255), (0, 0, r.width, r.height), border_radius=16); top.blit(m, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
                if not op: top.fill((70, 70, 90), special_flags=pygame.BLEND_RGB_MULT)
                sc.blit(top, r); pygame.draw.rect(sc, GOLD if sel else (240, 240, 255), r, 4 if sel else 2, border_radius=16)
                s.text(str(i + 1) if i < 6 else "★", s.f_b, WHITE, (r.centerx, r.top + 42), shadow=True)
                s.para(L["short"], s.f_m, WHITE, r.centerx, r.top + 78, r.width - 10, 28)
                if op:
                    for k in range(3): draw_star(sc, r.centerx - 30 + k * 30, r.bottom - 34, 11, GOLD if k < s.data["stars"][i] else (60, 60, 90))
                else:
                    pygame.draw.rect(sc, (230, 230, 240), (r.centerx - 12, r.bottom - 44, 24, 18), border_radius=3); pygame.draw.arc(sc, (230, 230, 240), (r.centerx - 8, r.bottom - 58, 16, 22), 0, math.pi, 3)
                if i == 6: draw_flag(sc, r.left + 12, r.top + 12, 34, 22, s.t, 2, False)
            s.fade_text("الأسهم للتنقل  |  Enter أو النقر للبدء  |  Esc رجوع", s.f_s, GOLD, (W // 2, H - 30), .6)
        elif st == "cutscene": s.draw_cutscene()
        elif st == "card":
            L = LEVELS[s.level]; s.bg(*L["sky"]); c = L["card"]
            s.text_pop(c[0], s.f_xl if len(c[0]) < 12 else s.f_b, GOLD, (W // 2, 90))
            y = 160
            for i, ln in enumerate(c[1:]): y = s.para_fx(ln, s.f_m, WHITE, W // 2, y, 680, 36, start=.5 + .8 * i) + 10
            if L.get("nov"): draw_flag(sc, W // 2 - 60, 390, 120, 80, s.t, 6)
            else: s.avatar_big(W // 2, 535, s.pal, "side", 1, True, s.t * 11, k=3)
            s.fade_text("اضغط Enter للبدء", s.f_s, GOLD, (W // 2, H - 24), 2.4)
        elif st == "levelup":
            s.bg(*LEVELS[s.level]["sky"]); s.text_pop("أحسنت يا بطل!", s.f_xl, GREEN, (W // 2, 100))
            for i in range(3):
                k = ease_back((s.st - .6 - .4 * i) / .5); rr = 34 * k
                if k > 0: draw_star(sc, W // 2 - 80 + i * 80, 220, max(1, rr), GOLD if i < s.stars_got else (80, 70, 110))
            k = clamp((s.st - .6) / 1.2)
            s.fade_text("العملات: %d / %d" % (int(s.got * k), s.total_coins), s.f_m, WHITE, (W // 2, 300), .8)
            s.fade_text("مكافأة السرعة: %d" % int(s.bonus * k), s.f_m, WHITE, (W // 2, 345), 1.1)
            s.text_pop("النقاط: %d" % s.score, s.f_b, GOLD, (W // 2, 405), 1.5)
            s.fade_text("اضغط Enter للمتابعة", s.f_s, GOLD, (W // 2, H - 40), 2.2)
        elif st == "over":
            s.bg((40, 10, 20), (130, 30, 50)); s.text_pop("انتهت المحاولة", s.f_xl, RED, (W // 2, 130))
            s.para_fx("أمسك بك الأعداء… لكن الحقيقة تنتظرك، حاول مرة أخرى!", s.f_m, WHITE, W // 2, 240, 640, 40, .7, start=.5)
            s.text_pop("النقاط: %d    |    الأعلى: %d" % (s.score, s.data["high"]), s.f_b, GOLD, (W // 2, 340), 1.2)
            s.fade_text("Enter لإعادة المرحلة   |   Esc للقائمة", s.f_s, GOLD, (W // 2, H - 60), 1.8)
        elif st == "win":
            s.bg((20, 90, 150), (250, 170, 100)); s.text_pop("بطل نوفيرا!", s.f_xl, GREEN, (W // 2, 90))
            s.para_fx("فتحت البوابة وكشفت الحقيقة، وتعلّمت في الطريق حسابًا ومعلوماتية وعلومًا ولغة.\n«الصفر ليس نهاية العدّ، بل بدايته».", s.f_m, WHITE, W // 2, 170, 680, 42, .9, start=.4)
            for i, p in enumerate(AVATARS): s.avatar_big(W // 2 - 110 + i * 110, 500, p, "front", 1, True, s.t * 9 + i, k=3)
            s.text_pop("النقاط: %d    |    الأعلى: %d" % (s.score, s.data["high"]), s.f_b, GOLD, (W // 2, 330), 2.6)
            s.fade_text("اضغط Enter للعودة إلى القائمة", s.f_s, GOLD, (W // 2, H - 20), 3.4)
        elif st == "nov_end":
            gradient(sc, (0, 70, 40), (10, 30, 20)); stars(sc, s.t, 3, 90, 400)
            draw_flag(sc, W // 2 - 150, 90, 300, 200, s.t, 10)
            s.text_pop("المجد والخلود لشهدائنا الأبرار", s.f_b, GOLD, (W // 2, 340))
            s.para_fx("في أول نوفمبر 1954 انطلقت الثورة التحريرية بقيادة جبهة التحرير الوطني، وتحقق الاستقلال في 5 جويلية 1962 بتضحيات مليون ونصف مليون شهيد.", s.f_m, WHITE, W // 2, 385, 700, 34, .8, start=.8)
            s.text_pop("النجوم: %d / %d   |   النقاط: %d" % (s.got, s.total_coins, s.score), s.f_m, GOLD, (W // 2, 505), 2.6)
            s.fade_text("Enter للعودة إلى القائمة", s.f_s, WHITE, (W // 2, H - 18), 3.2)
        elif st in ("play", "quiz", "pause"):
            s.draw_world()
            if st == "quiz": s.draw_quiz()
            if st == "pause":
                v = pygame.Surface((W, H), pygame.SRCALPHA); v.fill((10, 5, 30, 190)); sc.blit(v, (0, 0))
                s.text("إيقاف مؤقت", s.f_xl, GOLD, (W // 2, 200), shadow=True)
                s.text("Esc أو Enter للمتابعة   |   Q للقائمة", s.f_m, WHITE, (W // 2, 300))
        s.draw_parts(True)
        if s.flash > 0: v = pygame.Surface((W, H), pygame.SRCALPHA); v.fill((230, 30, 30, int(110 * s.flash / .3))); sc.blit(v, (0, 0))
        if s.fa > 0: v = pygame.Surface((W, H), pygame.SRCALPHA); v.fill((0, 0, 0, int(s.fa))); sc.blit(v, (0, 0))
        pygame.display.flip()

    def draw_cutscene(s):
        real = s.screen; fn, dur, cap = s.cs[s.csi]
        if not hasattr(s, "cs_surf"): s.cs_surf = pygame.Surface((W, H))
        s.screen = s.cs_surf; fn(s, s.cs_surf, s.cst); s.screen = real
        real.fill((0, 0, 0)); real.blit(s.cs_surf, (0, -70))          # scene shifted up so captions never cover characters
        pygame.draw.rect(real, (0, 0, 0), (0, 0, W, 34)); pygame.draw.rect(real, (0, 0, 0), (0, H - 92, W, 92))
        s.para_fx(cap, s.f_m, WHITE, W // 2, H - 84, 720, 32, .5, .5, s.cst)
        s.text("Enter / Esc: تخطّي", s.f_s, (170, 170, 190), (14, 17), "midleft")
        for i in range(len(s.cs)): pygame.draw.circle(real, GOLD if i == s.csi else (90, 90, 110), (W - 20 - (len(s.cs) - 1 - i) * 16, 17), 4)
        a = max(255 * (1 - clamp(s.cst / .6)), 255 * clamp((s.cst - (dur - .5)) / .5))
        if a > 0: v = pygame.Surface((W, H), pygame.SRCALPHA); v.fill((0, 0, 0, int(a))); real.blit(v, (0, 0))

    def draw_world(s):
        sc = s.screen; L = LEVELS[s.level]; th = L["theme"]
        ox, oy = (random.randint(-4, 4), random.randint(-4, 4)) if s.shake > 0 else (0, 0)
        sc.fill((8, 8, 14)); torches = [(x * T + 20, 24) for x in range(2, COLS - 1, 4)] if th != "nov" else []
        for y in range(ROWS):
            for x in range(COLS):
                r = pygame.Rect(x * T + ox, y * T + HUD + oy, T, T); c = s.grid[y][x]
                pygame.draw.rect(sc, L["floor"][(x + y) % 2], r)
                if c == "#": draw_wall(sc, r, th, L["wallc"][(x * 7 + y * 13) % len(L["wallc"])] if th != "nov" else L["wallc"][(x + y) % 2], x, y, s.t)
                elif c == "D" and (x, y) not in s.opened:
                    d = math.hypot(s.px - (x * T + 20), s.py - (y * T + 20)); near = d < 110
                    rr = r.inflate(-4, 0).move(int(2 * math.sin(s.t * 40)) if near else 0, 0); pul = .5 + .5 * math.sin(s.t * 3 + x)
                    pygame.draw.rect(sc, (60, 30, 0), rr.inflate(4, 0), border_radius=4)
                    pygame.draw.rect(sc, (170 + int(40 * pul), 110 + int(30 * pul), 30), rr, border_radius=4)
                    pygame.draw.rect(sc, (255, 240, 150) if near else GOLD, rr, 3 + (1 if near else 0), border_radius=4)
                    s.text("0", s.f_b, (60, 30, 0), (rr.centerx, rr.centery + int(math.sin(s.t * 4 + x) * 2)))
        for (x, y), t in s.door_anim.items():
            hgt = int(T * (1 - ease_out(t / .5)))
            if hgt > 0: pygame.draw.rect(sc, (170, 110, 30), (x * T + 2 + ox, y * T + HUD + oy, T - 4, hgt)); pygame.draw.rect(sc, GOLD, (x * T + 2 + ox, y * T + HUD + oy, T - 4, hgt), 3)
        for m in s.motes:
            mx, my = m[0] + ox, m[1] + HUD + oy; a = .5 + .5 * math.sin(s.t * 2 + m[5])
            gl = pygame.Surface((16, 16), pygame.SRCALPHA); pygame.draw.circle(gl, (*m[4], int(70 * a)), (8, 8), 8); pygame.draw.circle(gl, (*lt(m[4], .6), int(220 * a)), (8, 8), 2); sc.blit(gl, (mx - 8, my - 8))
        ex, ey = s.ex[0] * T + 20 + ox, s.ex[1] * T + 20 + HUD + oy; pulse = 4 * math.sin(s.t * 4)
        if th == "nov": draw_flag(sc, ex - 12, ey - 34, 36, 24, s.t, 3)
        else:
            gl = pygame.Surface((90, 90), pygame.SRCALPHA); pygame.draw.circle(gl, (255, 120, 220, int(55 + 30 * math.sin(s.t * 3))), (45, 45), int(40 + pulse)); sc.blit(gl, (ex - 45, ey - 45))
            for rad, col in ((19, (255, 110, 220)), (14, (120, 80, 230)), (9, (255, 255, 255))): pygame.draw.circle(sc, col, (ex, ey), int(rad + pulse * (rad / 19)), 3 if rad > 9 else 0)
            for i in range(6): a = s.t * 2.2 + i * math.pi / 3; pygame.draw.circle(sc, CONFETTI[i % 5], (int(ex + 24 * math.cos(a)), int(ey + 24 * math.sin(a))), 3)
            s.text("0", s.f_m, (60, 20, 90), (ex, ey))
        for c in s.coins:
            ph = c[0] * .7 + c[1]; cx = c[0] * T + 20 + ox; cy = c[1] * T + 20 + HUD + oy + int(3 * math.sin(s.t * 4 + ph)); w = abs(math.cos(s.t * 3 + ph))
            if th == "nov":
                pts = []
                for i in range(10):
                    a = -math.pi / 2 + i * math.pi / 5; rr = 12 if i % 2 == 0 else 5; pts.append((cx + rr * math.cos(a) * (.35 + .65 * w), cy + rr * math.sin(a)))
                pygame.draw.polygon(sc, (225, 40, 50), pts); pygame.draw.polygon(sc, (255, 200, 200), pts, 2)
            else:
                wd = int(11 * w) + 1; pygame.draw.ellipse(sc, GOLD, (cx - wd, cy - 11, 2 * wd, 22)); pygame.draw.ellipse(sc, (255, 245, 170), (cx - wd, cy - 11, 2 * wd, 22), 2)
                if wd > 7: s.text("0", s.f_s, (120, 70, 0), (cx, cy))
            f = (s.t * 1.5 + ph) % 3
            if f < .35: z = int(7 * math.sin(f / .35 * math.pi)); pygame.draw.line(sc, WHITE, (cx + 9 - z, cy - 9), (cx + 9 + z, cy - 9), 2); pygame.draw.line(sc, WHITE, (cx + 9, cy - 9 - z), (cx + 9, cy - 9 + z), 2)
        for p in s.pickups:
            px, py = p["x"] * T + 20 + ox, p["y"] * T + 20 + HUD + oy + int(4 * math.sin(s.t * 3 + p["x"]))
            gl = pygame.Surface((50, 50), pygame.SRCALPHA); pygame.draw.circle(gl, ((255, 100, 150, 60) if p["k"] == "heart" else (150, 230, 255, 70)), (25, 25), 22); sc.blit(gl, (px - 25, py - 25))
            if p["k"] == "heart": heart(sc, px, py, int(26 + 3 * math.sin(s.t * 6)), (255, 90, 130))
            else:
                pygame.draw.polygon(sc, (170, 235, 255), [(px, py - 14), (px + 9, py), (px, py + 14), (px - 9, py)]); pygame.draw.polygon(sc, WHITE, [(px, py - 14), (px + 9, py), (px, py + 14), (px - 9, py)], 2)
        ents = []; fr = s.freeze > 0
        for i, e in enumerate(s.enemies):
            al = math.hypot(e["x"] - s.px, e["y"] - s.py) < 140 and not fr; ddx = e["dir"] if e["d"] == "h" else 0; ddy = e["dir"] if e["d"] == "v" else 0
            ents.append((e["y"], lambda e=e, al=al, ddx=ddx, ddy=ddy, i=i: draw_enemy(sc, s.t, L["kind"], e["x"] + ox, e["y"] + HUD + oy, ddx, ddy, al, i * 1.7, fr)))
        if s.inv <= 0 or int(s.t * 12) % 2: ents.append((s.py, lambda: draw_avatar(sc, s.t, s.px + ox, s.py + HUD + oy, s.pal, s.view, s.face, s.moving, s.wp)))
        for _, fn in sorted(ents, key=lambda e: e[0]): fn()
        s.draw_parts(False, ox, HUD + oy)
        if L["dark"] > 0:
            base = int(L["dark"] + 8 * math.sin(s.t * 9) + 4 * math.sin(s.t * 23)); d = s.dark_base; d.fill((24, 10, 60, max(0, base)))
            d.blit(s.mask_big, (int(s.px) - 280, int(s.py) - 280), special_flags=pygame.BLEND_RGBA_SUB)
            d.blit(s.mask_small, (s.ex[0] * T + 20 - 95, s.ex[1] * T + 20 - 95), special_flags=pygame.BLEND_RGBA_SUB)
            for (tx, ty) in torches: d.blit(s.mask_small, (tx - 95, ty - 89), special_flags=pygame.BLEND_RGBA_SUB)
            sc.blit(d, (ox, HUD + oy))
        for i, (tx, ty) in enumerate(torches):
            fl = 4 * math.sin(s.t * 13 + i * 2) + 2 * math.sin(s.t * 31 + i)
            pygame.draw.rect(sc, (110, 70, 40), (tx - 3 + ox, ty + HUD + 4 + oy, 6, 12)); pygame.draw.circle(sc, (255, 120, 30), (tx + ox, int(ty + HUD + oy - fl / 2)), int(7 + fl / 2)); pygame.draw.circle(sc, (255, 225, 110), (tx + ox, int(ty + HUD + oy + 1)), int(4 + fl / 3))
        if fr:
            v = pygame.Surface((W, ROWS * T), pygame.SRCALPHA); v.fill((140, 210, 255, int(40 + 20 * math.sin(s.t * 8)))); sc.blit(v, (0, HUD))
        for p in s.pops:
            img = (s.f_b if p["big"] else s.f_s).render(p["t"], True, p["col"]); img.set_alpha(int(255 * clamp(p["life"] / .5))); sc.blit(img, img.get_rect(center=(int(p["x"] + ox), int(p["y"] + HUD + oy))))
        if s.time < 2.4:
            t = s.time; k = ease_out(t / .5) if t < 1.9 else 1; a = int(255 * (1 if t < 1.9 else clamp((2.4 - t) / .5)))
            rb = pygame.Surface((W, 64), pygame.SRCALPHA); rb.fill((60, 20, 110, int(190 * a / 255))); sc.blit(rb, (0, HUD + 190))
            img = s.f_b.render(shape(L["name"]), True, GOLD); img.set_alpha(a); sc.blit(img, img.get_rect(center=(int(-300 + (W // 2 + 300) * k), HUD + 222)))
        for yy in range(HUD): pygame.draw.line(sc, mix((70, 36, 130), (28, 16, 70), yy / HUD), (0, yy), (W, yy))
        for i, c in enumerate(CONFETTI): pygame.draw.rect(sc, c, (i * W // 5, HUD - 4, W // 5 + 1, 4))
        for i in range(3):
            sz = 30 * (1 + .12 * math.sin(s.t * 8)) if (s.lives == 1 and i == 0) else 30
            heart(sc, 40 + i * 44, 32, int(sz), RED if i < s.lives else (80, 60, 90))
        if s.freeze > 0: s.text("❄ %.1f" % s.freeze, s.f_s, (170, 235, 255), (180, 32), "midleft")
        img = s.f_m.render(shape("النقاط: %d" % int(round(s.disp))), True, GOLD); k = 1 + .35 * s.bump
        img = pygame.transform.smoothscale(img, (int(img.get_width() * k), int(img.get_height() * k))); sc.blit(img, img.get_rect(center=(W // 2, 24)))
        s.text("%s %d/%d   |   الوقت: %d" % ("النجوم" if th == "nov" else "العملات", s.got, s.total_coins, int(s.time)), s.f_s, WHITE, (W // 2, 56))
        s.text(L["name"], s.f_m, WHITE, (W - 20, 28), "midright", True)
        if L.get("final"): s.text("أسئلة البوابة: %d/3" % s.gate_ok, s.f_s, (255, 200, 255), (W - 20, 58), "midright")
        else: s.text("الأبواب: %d/%d" % (len(s.opened), len(L["walls"])), s.f_s, (255, 230, 160), (W - 20, 58), "midright")
        if s.touch:
            pad = pygame.Surface((220, 220), pygame.SRCALPHA); pygame.draw.circle(pad, (255, 255, 255, 45), (110, 110), 100); pygame.draw.circle(pad, (255, 255, 255, 110), (110, 110), 100, 3)
            for ax, ay in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                cx, cy = 110 + ax * 62, 110 + ay * 62; pts = [(cx + ax * 14, cy + ay * 14), (cx - ax * 10 - ay * 13, cy - ay * 10 + ax * 13), (cx - ax * 10 + ay * 13, cy - ay * 10 - ax * 13)]
                pygame.draw.polygon(pad, (255, 255, 255, 170), pts)
            sc.blit(pad, (105 - 110, H - 105 - 110))
            pr = s.pause_rect(); pygame.draw.rect(sc, (20, 10, 50), pr, border_radius=12); pygame.draw.rect(sc, GOLD, pr, 2, border_radius=12)
            pygame.draw.rect(sc, WHITE, (pr.left + 14, pr.top + 12, 8, 26)); pygame.draw.rect(sc, WHITE, (pr.left + 28, pr.top + 12, 8, 26))

    def draw_quiz(s):
        real = s.screen; q = s.q; qs = s.qs; qs.fill((0, 0, 0, 0)); s.screen = qs
        label, scol = SUBJECTS[q["pool"]]
        pan = pygame.Rect(40, 14, W - 80, H - 28)
        pygame.draw.rect(qs, (34, 22, 82), pan, border_radius=18); pygame.draw.rect(qs, scol, pan, 4, border_radius=18)
        for i, c in enumerate(CONFETTI): pygame.draw.rect(qs, c, (pan.left + 30 + i * 130, pan.top + 4, 130, 4))
        tag = pygame.Rect(0, 0, 150, 30); tag.center = (W // 2, 40); pygame.draw.rect(qs, scol, tag, border_radius=15); s.text(label, s.f_s, (20, 10, 40), tag.center)
        s.text("بوابة الحقيقة" if s.ctx == "gate" else "باب مقفل - حلّ المسألة!", s.f_s, (210, 200, 240), (W - 70, 40), "midright")
        s.para(q["q"], s.f_b, WHITE, W // 2, 68, 680, 44)
        for i, r in enumerate(s.opt_rects()):
            r = r.move(int((1 - ease_out((s.qt - .12 - .07 * i) / .25)) * 170), 0); col = (56, 52, 108)
            if q["sel"] is None and r.collidepoint(pygame.mouse.get_pos()): col = (90, 86, 160)
            if q["sel"] is not None:
                if i == q["c"]: col = (30, 130, 76); g = int(6 * math.sin(s.at * 14) * max(0, 1 - s.at * 1.6)); r = r.inflate(g, g)
                elif i == q["sel"]: col = (160, 40, 54); r = r.move(int(10 * math.sin(s.at * 40) * max(0, 1 - s.at * 2.5)), 0)
            pygame.draw.rect(qs, col, r, border_radius=12)
            if q["sel"] is not None and i == q["c"]: pygame.draw.rect(qs, (200, 255, 220), r, 3, border_radius=12)
            pygame.draw.circle(qs, GOLD, (r.right - 28, r.centery), 15); s.text(str(i + 1), s.f_m, (30, 20, 0), (r.right - 28, r.centery))
            s.text(q["opts"][i], s.f_m, WHITE, (r.right - 58, r.centery), "midright")
        if q["sel"] is not None:
            ok = q["sel"] == q["c"]; k = ease_back(s.at / .35)
            s.text("إجابة صحيحة!" if ok else "إجابة خاطئة", s.f_b, GREEN if ok else RED, (W // 2, 448 - int(10 * (1 - k))))
            s.para(q["ex"], s.f_s, WHITE, W // 2, 474, 700, 22); s.text("اضغط Enter أو انقر للمتابعة", s.f_s, GOLD, (W // 2, H - 26))
        else: s.text("اضغط 1 - 4 أو انقر على الإجابة", s.f_s, (170, 180, 210), (W // 2, H - 26))
        s.screen = real
        v = pygame.Surface((W, H), pygame.SRCALPHA); v.fill((0, 0, 0, int(190 * clamp(s.qt / .2)))); real.blit(v, (0, 0)); k = ease_back(s.qt / .3)
        if k < .995 or k > 1.005:
            img = pygame.transform.smoothscale(qs, (max(1, int(W * k)), max(1, int(H * k)))); img.set_alpha(int(255 * clamp(s.qt / .15))); real.blit(img, img.get_rect(center=(W // 2, H // 2)))
        else: real.blit(qs, (0, 0))

    def run(s):
        run = True
        while run:
            dt = min(s.clock.tick(60) / 1000, .05)
            run = s.events(); s.update(dt); s.draw()
        pygame.quit()

if __name__ == "__main__":
    Game().run()
