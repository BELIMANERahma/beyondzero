# -*- coding: utf-8 -*-
"""ما وراء الصفر  |  Beyond Zero  -  educational adventure game (pygame)"""
import os, sys, math, random, json, array, re
import pygame
import arabic_reshaper
from bidi.algorithm import get_display
from questions import EASY, MEDIUM, HARD

BASE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
SAVE = os.path.expanduser("~/.beyond_zero_score.json")
T, COLS, ROWS, HUD = 40, 20, 12, 80
W, H = COLS * T, ROWS * T + HUD
PS = 24  # player size

GOLD = (255, 200, 80); WHITE = (240, 240, 245); RED = (230, 70, 70); GREEN = (80, 210, 120)
_rs = arabic_reshaper.ArabicReshaper()
def shape(t):
    t = re.sub(r"\{([^}]*)\}", lambda m: "\u202A" + m.group(1) + "\u202C", t)   # {..} = expression shown left-to-right
    return get_display(_rs.reshape(t))
def protect(t): return re.sub(r"\{[^}]*\}", lambda m: m.group(0).replace(" ", "\u00a0"), t)

LEVELS = [
 dict(name="المستوى 1: الأرشيف", bg=(24, 54, 62), wall=(46, 96, 108), pool="easy", walls=[7, 14], doors={7: 5, 14: 6},
      pillars=[(3,2),(3,3),(4,8),(4,9),(10,2),(10,3),(11,8),(11,9),(16,3),(16,8)],
      coins=[(2,1),(5,10),(2,10),(5,1),(9,5),(12,1),(12,10),(9,10),(16,1),(17,10),(16,5)],
      guards=[(9,6,'v',80),(17,3,'v',90)], start=(1,5), exit=(18,5),
      card=["الأرشيف", "ظهر ضوء أحمر على الشاشة القديمة:", "«تم العثور على وريث المشروع صفر».", "الأبواب هنا لا تُفتح إلا بالمعرفة! اقترب من الباب وأجب عن السؤال."]),
 dict(name="المستوى 2: النفق", bg=(46, 34, 26), wall=(104, 76, 56), pool="medium", walls=[5, 10, 15], doors={5: 3, 10: 8, 15: 5},
      pillars=[(2,2),(3,2),(2,8),(3,8),(7,3),(8,3),(7,8),(8,8),(12,3),(13,3),(12,8),(13,8),(17,3),(17,8)],
      coins=[(1,1),(4,10),(1,10),(6,1),(9,1),(6,10),(9,5),(11,1),(14,1),(11,10),(14,10),(16,1),(18,10),(18,1)],
      guards=[(3,5,'v',90),(7,5,'h',110),(12,6,'h',110),(16,2,'v',120)], start=(1,5), exit=(18,5),
      card=["النفق", "قال أورمان بصوت خافت:", "«الأسوار لم تُبنَ لحمايتكم، بل لحماية السرّ من سكانها».", "اهرب من الحراس عبر النفق القديم، والأسئلة صارت أصعب!"]),
 dict(name="المستوى 3: البوابة", bg=(36, 28, 56), wall=(92, 72, 140), pool="hard", walls=[6, 13], doors={6: 5, 13: 6},
      pillars=[(3,3),(3,8),(9,2),(9,3),(10,8),(10,9),(16,3),(16,8)],
      coins=[(1,1),(5,10),(1,10),(5,1),(8,5),(11,1),(8,10),(11,10),(15,1),(18,10),(15,10),(18,1)],
      guards=[(4,2,'v',110),(8,5,'v',130),(12,3,'v',130),(16,5,'v',140)], start=(1,5), exit=(18,5),
      card=["البوابة", "وقف الملك زيركان أمام البوابة الحجرية:", "«ابتعد عن البوابة يا كاير، أنت لا تعرف ما الذي تحاول فتحه».", "لتفتح البوابة أجب عن ثلاثة أسئلة أخيرة. كل خطأ يكلّفك قلبًا!"]),
]
STYLE = [
 dict(floor=((70, 150, 185), (80, 162, 198)), walls=[(222, 92, 112), (84, 152, 232), (250, 182, 62), (102, 202, 142), (162, 102, 212)], sky=((20, 90, 150), (100, 210, 190))),
 dict(floor=((208, 152, 92), (218, 164, 104)), walls=[(152, 92, 202), (222, 112, 72), (62, 172, 172), (232, 172, 62)], sky=((120, 40, 110), (250, 160, 70))),
 dict(floor=((98, 72, 152), (108, 84, 164)), walls=[(72, 202, 222), (242, 112, 182), (250, 212, 92), (132, 112, 242)], sky=((40, 30, 120), (200, 90, 200))),
]
AVATARS = [
 dict(name="كاير", desc="الفتى الفضولي الذي يبحث عن الحقيقة", skin=(245, 200, 160), hair=(70, 45, 30), style="spiky", shirt=(60, 140, 240), pants=(40, 55, 120), shoe=(245, 245, 245), scarf=(235, 70, 85)),
 dict(name="ميليس", desc="الأخت الذكية التي تحمل رسالة الأب", skin=(238, 188, 152), hair=(40, 25, 40), style="long", shirt=(235, 90, 170), pants=(120, 70, 170), shoe=(250, 220, 240)),
 dict(name="خالد", desc="الأخ الشجاع صاحب القبعة", skin=(225, 175, 135), hair=(245, 170, 40), style="cap", shirt=(70, 195, 110), pants=(60, 90, 80), shoe=(250, 250, 250)),
]
GUARD = dict(skin=(232, 190, 150), hair=(150, 156, 178), style="helmet", shirt=(215, 55, 62), pants=(75, 40, 55), shoe=(40, 30, 40))
def dk(c, k=.7): return tuple(int(v * k) for v in c)
def lt(c, k=.35): return tuple(int(v + (255 - v) * k) for v in c)
INTRO = [
 "مدينة نوفيرا تبدو مثالية: شوارع نظيفة، وأبراج شاهقة، وأسوار ضخمة تحيط بها. عاش سكانها مقتنعين بأن العالم خارج الأسوار ظلام لا نهاية له.",
 "لكن كاير لم يكن يصدّق كل ما يسمعه. في ليلة اختفى والده جاف، وترك مفتاحًا صغيرًا وورقة كُتب عليها رقم واحد فقط: صفر.",
 "مهمتك: افتح الأبواب المقفلة بحلّ ألغاز الأرقام والصفر، واجمع عملات الصفر، وتجنّب حراس الملك، ثم صِل إلى البوابة القديمة وكشف الحقيقة.",
]
ENDING = "انفتحت البوابة، وظهرت أرض خضراء ومياه صافية ومدن تتلألأ عند الأفق. لم يكن وراء الأسوار ظلام أبدي، بل عالم كامل.\n«الصفر ليس نهاية العدّ، بل بدايته»."

# ---------------------------------------------------------------- helpers
def heart(s, x, y, sz, col):
    r = sz // 4
    pygame.draw.circle(s, col, (x - r, y - r // 2), r + 1)
    pygame.draw.circle(s, col, (x + r, y - r // 2), r + 1)
    pygame.draw.polygon(s, col, [(x - 2 * r - 1, y - 1), (x + 2 * r + 1, y - 1), (x, y + 2 * r + r // 2)])

def make_sounds():
    snd = {}
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=1)
    except Exception:
        return snd
    def tone(freqs, dur, vol=0.35):
        n = int(22050 * dur); b = array.array("h")
        for i in range(n):
            f = freqs[min(len(freqs) - 1, int(i / n * len(freqs)))]
            b.append(int(32767 * vol * (1 - i / n) * math.sin(2 * math.pi * f * i / 22050)))
        return b
    def mk(freqs, dur, vol=0.35): return pygame.mixer.Sound(buffer=tone(freqs, dur, vol).tobytes())
    snd["coin"] = mk([988, 1319], .12); snd["ok"] = mk([523, 659, 784], .35)
    snd["bad"] = mk([220, 160], .35); snd["hit"] = mk([140, 90], .4)
    snd["door"] = mk([330, 440, 554], .3); snd["win"] = mk([523, 659, 784, 1047, 1319], 1.0)
    # soft looping background music
    notes = [220, 262, 330, 262, 196, 247, 294, 247, 175, 220, 262, 220, 196, 247, 294, 392]
    b = array.array("h")
    for f in notes: b.extend(tone([f], .5, .12))
    snd["music"] = pygame.mixer.Sound(buffer=b.tobytes())
    return snd

def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def ease_out(t): t = clamp(t); return 1 - (1 - t) ** 3
def ease_back(t): t = clamp(t) - 1; return 1 + 2.70158 * t ** 3 + 1.70158 * t ** 2
CONFETTI = [(255, 90, 90), (255, 200, 80), (90, 220, 130), (90, 170, 255), (200, 120, 255)]

class Particle:
    def __init__(s, x, y, col, g=0, scr=False, speed=(40, 160), life=(.4, .9), size=4, spread=None):
        a = random.uniform(0, 6.28) if spread is None else random.uniform(*spread); v = random.uniform(*speed)
        s.x, s.y, s.vx, s.vy = x, y, math.cos(a) * v, math.sin(a) * v
        s.life = s.max = random.uniform(*life); s.col, s.g, s.scr, s.size = col, g, scr, size

# ---------------------------------------------------------------- game
class Game:
    def __init__(s):
        pygame.init()
        s.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("ما وراء الصفر - Beyond Zero")
        s.clock = pygame.time.Clock()
        f = os.path.join(BASE, "assets", "DejaVuSans.ttf"); fb = os.path.join(BASE, "assets", "DejaVuSans-Bold.ttf")
        s.f_s, s.f_m, s.f_b = pygame.font.Font(f, 19), pygame.font.Font(f, 24), pygame.font.Font(fb, 34)
        s.f_xl = pygame.font.Font(fb, 78)
        s.snd = make_sounds()
        if "music" in s.snd: s.snd["music"].set_volume(.35); s.snd["music"].play(-1)
        s.high = 0
        try: s.high = json.load(open(SAVE))["high"]
        except Exception: pass
        s.zeros = [[random.uniform(0, W), random.uniform(0, H), random.uniform(20, 70), random.uniform(10, 30)] for _ in range(24)]
        s.state = "menu"; s.t = 0; s.page = 0; s.parts = []; s.shake = 0
        s.decks = {}; s.prev = None; s.st = 0; s.fa = 255; s.pops = []; s.disp = 0; s.bump = 0; s.last_score = 0
        s.flash = 0; s.hov = [0, 0, 0]; s.door_anim = {}; s.dust_t = 0; s.wp = 0; s.face = 1; s.look = (0, 0)
        s.moving = False; s.qt = 0; s.at = 0; s.px = s.py = 0; s.time = 0; s.score = 0; s.lives = 3; s.level = 0
        s.zero_img = s.f_xl.render("0", True, (255, 255, 255))
        s.dark_base = pygame.Surface((W, ROWS * T), pygame.SRCALPHA)
        big = pygame.Surface((560, 560), pygame.SRCALPHA)
        for r in range(280, 0, -4): pygame.draw.circle(big, (0, 0, 0, int(150 * (1 - r / 280) ** 0.8)), (280, 280), r)
        s.mask_big = big; s.mask_small = pygame.transform.smoothscale(big, (190, 190))
        s.qs = pygame.Surface((W, H), pygame.SRCALPHA); s.blob = pygame.Surface((W, H), pygame.SRCALPHA)
        s.zero_tints = []
        for c in CONFETTI:
            im = s.zero_img.copy(); im.fill((*c, 255), special_flags=pygame.BLEND_RGBA_MULT); s.zero_tints.append(im)
        s.sel = 0; s.pal = AVATARS[0]; s.view = "side"
        s.motes = [[random.uniform(40, W - 40), random.uniform(40, ROWS * T - 40), random.uniform(-14, 14), random.uniform(-14, 14), random.choice(CONFETTI), random.uniform(0, 6)] for _ in range(28)]

    # --------------- text helpers
    def text(s, t, font, col, pos, anchor="center"):
        img = font.render(shape(t), True, col); r = img.get_rect(); setattr(r, anchor, pos)
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
        for ln in s.wrap(t, font, maxw):
            s.text(ln, font, col, (cx, y), "midtop"); y += lh
        return y
    def sound(s, k):
        if k in s.snd: s.snd[k].play()

    # --------------- game flow
    def new_game(s):
        s.lives, s.score, s.level = 3, 0, 0
        s.disp = 0; s.last_score = 0
        s.decks = {k: [] for k in ("easy", "medium", "hard")}
        s.state = "select"; s.page = 0
    def load_level(s):
        L = LEVELS[s.level]
        s.grid = [["#" if x in (0, COLS - 1) or y in (0, ROWS - 1) else "." for x in range(COLS)] for y in range(ROWS)]
        for wx in L["walls"]:
            for y in range(1, ROWS - 1): s.grid[y][wx] = "#"
            s.grid[L["doors"][wx]][wx] = "D"
        for (x, y) in L["pillars"]: s.grid[y][x] = "#"
        s.opened = set(); s.door_anim = {}; s.pops = []; s.coins = [list(c) for c in L["coins"]]; s.total_coins = len(s.coins)
        s.guards = [dict(x=gx * T + T / 2, y=gy * T + T / 2, d=d, sp=sp, dir=1) for gx, gy, d, sp in L["guards"]]
        s.px, s.py = L["start"][0] * T + T / 2, L["start"][1] * T + T / 2
        s.ex = L["exit"]; s.inv = 0; s.time = 0; s.door_lock = None; s.got = 0; s.parts = []; s.gate_ok = 0
        s.state = "play"
    def solid(s, r):
        for ty in range(r.top // T, (r.bottom - 1) // T + 1):
            for tx in range(r.left // T, (r.right - 1) // T + 1):
                if not (0 <= tx < COLS and 0 <= ty < ROWS): return True
                c = s.grid[ty][tx]
                if c == "#" or (c == "D" and (tx, ty) not in s.opened): return True
        return False
    def prect(s): r = pygame.Rect(0, 0, PS, PS); r.center = (int(s.px), int(s.py)); return r
    def next_q(s, pool):
        if not s.decks[pool]:
            s.decks[pool] = list({"easy": EASY, "medium": MEDIUM, "hard": HARD}[pool]); random.shuffle(s.decks[pool])
        q, opts, c, ex = s.decks[pool].pop()
        order = list(range(4)); random.shuffle(order)
        s.q = dict(q=q, opts=[opts[i] for i in order], c=order.index(c), ex=ex, sel=None)
    def start_quiz(s, ctx):
        s.next_q(LEVELS[s.level]["pool"]); s.ctx = ctx; s.state = "quiz"; s.qt = 0; s.at = 0
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
            if s.gate_ok >= 3: return s.end(True)
            return s.start_quiz("gate")
        if ok:
            s.opened.add(s.ctx); s.sound("door"); s.door_anim[s.ctx] = 0
            s.pops.append(dict(x=s.ctx[0] * T + 20, y=s.ctx[1] * T + 10, t="+100", col=GREEN, life=1.2, big=True))
            for _ in range(25): s.parts.append(Particle(s.ctx[0] * T + 20, s.ctx[1] * T + 20, GOLD))
        s.state = "play"
    def end(s, win):
        if s.score > s.high:
            s.high = s.score
            try: json.dump({"high": s.high}, open(SAVE, "w"))
            except Exception: pass
        s.state = "win" if win else "over"
        if win: s.sound("win")
    def level_complete(s):
        s.bonus = max(0, 500 - 5 * int(s.time)); s.score += s.bonus; s.state = "levelup"; s.sound("win")

    # --------------- update
    def update(s, dt):
        s.t += dt; s.st += dt
        grp = ("play", "quiz", "pause")
        if s.state != s.prev:
            s.st = 0
            if not (s.prev in grp and s.state in grp): s.fa = 255
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
        s.shake = max(0, s.shake - dt)
        for m in s.motes:
            m[0] = (m[0] + m[2] * dt) % W; m[1] = (m[1] + m[3] * dt) % (ROWS * T)
        s.disp += (s.score - s.disp) * min(1, 9 * dt)
        if s.score > s.last_score: s.bump = 1
        s.last_score = s.score; s.bump = max(0, s.bump - 3 * dt)
        if s.state in ("win", "levelup") and random.random() < dt * 45:
            s.parts.append(Particle(random.uniform(0, W), -10, random.choice(CONFETTI), g=140, scr=True, speed=(30, 120), life=(3, 4), size=5, spread=(1.2, 1.9)))
        if s.state == "menu":
            for i, r in enumerate(s.menu_rects()):
                s.hov[i] += ((1 if r.collidepoint(pygame.mouse.get_pos()) else 0) - s.hov[i]) * min(1, 12 * dt)
        if s.state == "quiz":
            s.qt += dt
            if s.q["sel"] is not None: s.at += dt
        if s.state != "play": return
        s.time += dt; s.inv = max(0, s.inv - dt)
        k = pygame.key.get_pressed()
        dx = (k[pygame.K_RIGHT] or k[pygame.K_d]) - (k[pygame.K_LEFT] or k[pygame.K_a])
        dy = (k[pygame.K_DOWN] or k[pygame.K_s]) - (k[pygame.K_UP] or k[pygame.K_w])
        s.moving = bool(dx or dy); s.look = (dx, dy)
        if dx: s.face = 1 if dx > 0 else -1; s.view = "side"
        elif dy: s.view = "front" if dy > 0 else "back"
        if s.moving:
            s.wp += 14 * dt; s.dust_t -= dt
            if s.dust_t <= 0:
                s.dust_t = .07; s.parts.append(Particle(s.px - s.face * 6, s.py + 11, (150, 150, 165), speed=(5, 28), life=(.25, .5), size=3))
        if dx and dy: dx *= .7071; dy *= .7071
        for ax, ay in ((dx * 190 * dt, 0), (0, dy * 190 * dt)):
            ox, oy = s.px, s.py; s.px += ax; s.py += ay
            if s.solid(s.prect()): s.px, s.py = ox, oy
        pr = s.prect()
        # coins
        for c in s.coins[:]:
            if pr.colliderect(pygame.Rect(c[0] * T + 8, c[1] * T + 8, 24, 24)):
                s.coins.remove(c); s.score += 10; s.got += 1; s.sound("coin")
                s.pops.append(dict(x=c[0] * T + 20, y=c[1] * T + 6, t="+10", col=GOLD, life=.8, big=False))
                for _ in range(8): s.parts.append(Particle(c[0] * T + 20, c[1] * T + 20, GOLD))
        # doors
        near = None
        for (tx, ty) in [(x, y) for y in range(ROWS) for x in range(COLS) if s.grid[y][x] == "D" and (x, y) not in s.opened]:
            if pr.inflate(8, 8).colliderect(pygame.Rect(tx * T, ty * T, T, T)): near = (tx, ty)
        if near is None: s.door_lock = None
        elif near != s.door_lock: s.door_lock = near; return s.start_quiz(near)
        # guards
        for g in s.guards:
            nx, ny = g["x"] + (g["dir"] * g["sp"] * dt if g["d"] == "h" else 0), g["y"] + (g["dir"] * g["sp"] * dt if g["d"] == "v" else 0)
            r = pygame.Rect(0, 0, 26, 26); r.center = (int(nx), int(ny))
            if s.solid(r): g["dir"] *= -1
            else: g["x"], g["y"] = nx, ny
            gr = pygame.Rect(0, 0, 26, 26); gr.center = (int(g["x"]), int(g["y"]))
            if s.inv <= 0 and gr.colliderect(pr.inflate(-6, -6)):
                s.lives -= 1; s.sound("hit"); s.shake = .3; s.inv = 1.6; s.flash = .3
                for _ in range(20): s.parts.append(Particle(s.px, s.py, RED))
                if s.lives <= 0: return s.end(False)
                s.px, s.py = LEVELS[s.level]["start"][0] * T + 20, LEVELS[s.level]["start"][1] * T + 20
        # exit
        if pr.colliderect(pygame.Rect(s.ex[0] * T + 4, s.ex[1] * T + 4, T - 8, T - 8)):
            if s.level == 2: s.start_quiz("gate"); s.px -= 14
            else: s.level_complete()

    # --------------- events
    def events(s):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if s.state == "menu": return False
                    s.state = "menu"; continue
                go = e.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER)
                if s.state == "menu":
                    if go: s.new_game()
                    elif e.key == pygame.K_h: s.state = "help"
                elif s.state == "select":
                    if e.key == pygame.K_RIGHT: s.sel = max(0, s.sel - 1)
                    elif e.key == pygame.K_LEFT: s.sel = min(len(AVATARS) - 1, s.sel + 1)
                    elif go: s.confirm_avatar()
                elif s.state == "help" and go: s.state = "menu"
                elif s.state == "intro" and go:
                    s.page += 1
                    if s.page >= len(INTRO): s.state = "card"
                elif s.state == "card" and go: s.load_level()
                elif s.state == "levelup" and go:
                    s.level += 1; s.state = "card"
                elif s.state in ("win", "over") and go: s.state = "menu"
                elif s.state == "play" and e.key == pygame.K_p: s.state = "pause"
                elif s.state == "pause" and e.key == pygame.K_p: s.state = "play"
                elif s.state == "quiz":
                    if s.q["sel"] is None and pygame.K_1 <= e.key <= pygame.K_4: s.answer(e.key - pygame.K_1)
                    elif s.q["sel"] is not None and go: s.quiz_done()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if s.state == "select":
                    for i, r in enumerate(s.select_rects()):
                        if r.collidepoint(e.pos):
                            if s.sel == i: s.confirm_avatar()
                            else: s.sel = i
                elif s.state == "menu":
                    for i, r in enumerate(s.menu_rects()):
                        if r.collidepoint(e.pos):
                            if i == 0: s.new_game()
                            elif i == 1: s.state = "help"
                            else: return False
                elif s.state == "quiz":
                    if s.q["sel"] is None:
                        for i, r in enumerate(s.opt_rects()):
                            if r.collidepoint(e.pos): s.answer(i)
                    else: s.quiz_done()
        return True

    # --------------- drawing helpers
    def menu_rects(s): return [pygame.Rect(W // 2 - 190, 300 + i * 70, 380, 54) for i in range(3)]
    def opt_rects(s): return [pygame.Rect(70, 190 + i * 62, 660, 52) for i in range(4)]
    def bg(s, top=(50, 25, 110), bot=(240, 110, 100)):
        for y in range(0, H, 4):
            k = y / H; pygame.draw.rect(s.screen, tuple(int(top[i] + (bot[i] - top[i]) * k) for i in range(3)), (0, y, W, 4))
        s.blob.fill((0, 0, 0, 0))
        for k in range(4):
            cx = W / 2 + 330 * math.sin(s.t * .25 + k * 1.7); cy = H / 2 + 200 * math.cos(s.t * .2 + k * 2.3)
            pygame.draw.circle(s.blob, (*CONFETTI[k], 34), (int(cx), int(cy)), 190); pygame.draw.circle(s.blob, (*CONFETTI[k], 30), (int(cx), int(cy)), 120)
        s.screen.blit(s.blob, (0, 0))
        for i, (x, y, sz, _) in enumerate(s.zeros):
            img = pygame.transform.smoothscale(s.zero_tints[i % 5], (int(sz), int(sz * 1.3))); img.set_alpha(80)
            s.screen.blit(img, (x + 12 * math.sin(s.t * .8 + i), y))
    def text_pop(s, t, font, col, pos, delay=0):
        k = clamp((s.st - delay) / .5)
        if k <= 0: return
        img = font.render(shape(t), True, col); sc = 1 + .6 * (1 - ease_back(k))
        img = pygame.transform.smoothscale(img, (max(1, int(img.get_width() * sc)), max(1, int(img.get_height() * sc))))
        img.set_alpha(int(255 * clamp(k * 2))); s.screen.blit(img, img.get_rect(center=pos))
    def para_fx(s, t, font, col, cx, y, maxw, lh, delay=.55, start=0):
        for i, ln in enumerate(s.wrap(t, font, maxw)):
            k = clamp((s.st - start - delay * i) / .6)
            if k > 0 and ln:
                img = font.render(shape(ln), True, col); img.set_alpha(int(255 * k))
                s.screen.blit(img, img.get_rect(midtop=(cx, y + (1 - k) * 14)))
            y += lh
        return y
    def fade_text(s, t, font, col, pos, delay=0, anchor="center"):
        k = clamp((s.st - delay) / .6)
        if k <= 0: return
        img = font.render(shape(t), True, col); img.set_alpha(int(255 * k)); r = img.get_rect(); setattr(r, anchor, pos); s.screen.blit(img, r)
    def draw_parts(s, scr, ox=0, oy=0):
        for p in s.parts:
            if p.scr == scr:
                pygame.draw.circle(s.screen, p.col, (int(p.x + ox), int(p.y + oy)), max(1, int(p.size * p.life / p.max)))

    # --------------- avatars
    def draw_avatar(s, x, y, pal, view, face, moving, phase, alert=False, seed=0):
        sc = s.screen; x = int(x); y = int(y); t = s.t
        sw = math.sin(phase) if moving else math.sin(t * 2 + seed) * .12
        bob = abs(math.cos(phase)) * 2.5 if moving else math.sin(t * 2.2 + seed) * .8
        by = y - bob; hy = int(by - 17)
        sk, hr, shirt, pants, shoe, st = pal["skin"], pal["hair"], pal["shirt"], pal["pants"], pal["shoe"], pal["style"]
        fe = face if view == "side" else 1
        P = lambda dx, dy: (x + fe * dx, hy + dy)
        blink = (t + seed) % 3.4 < .12
        sh = pygame.Surface((26, 9), pygame.SRCALPHA); pygame.draw.ellipse(sh, (0, 0, 0, 80), (0, 0, 26, 9)); sc.blit(sh, (x - 13, y + 11))
        def limb(sx, sy, L, a, w, col, end):
            ex, ey = sx + math.sin(a) * L * fe, sy + math.cos(a) * L
            pygame.draw.line(sc, col, (sx, sy), (ex, ey), w); pygame.draw.circle(sc, end, (int(ex), int(ey)), w // 2 + 1)
        def dome(col, dy0=-1): pygame.draw.polygon(sc, col, [P(-8.5, dy0), P(-8.5, -6), P(-5, -10), P(5, -10), P(8.5, -6), P(8.5, dy0)])
        spikes = [P(-8, -1), P(-9, -9), P(-4, -6), P(-2, -14), P(1, -7), P(4, -15), P(6, -7), P(9, -9), P(8, -1)]
        if view == "side":
            limb(x, by + 3, 11, -sw * .85, 6, dk(pants), shoe); limb(x, by - 8, 9, sw * .9, 4, dk(shirt), dk(sk))
            if st == "long":
                r = pygame.Rect(0, 0, 14, 24); r.center = (x - face * 4, hy + 7); pygame.draw.ellipse(sc, hr, r)
            pygame.draw.rect(sc, shirt, (x - 6, int(by - 11), 12, 15), border_radius=4)
            if pal.get("scarf"):
                pygame.draw.polygon(sc, pal["scarf"], [(x - face * 4, by - 10), (x - face * (13 + 5 * moving), by - 13 + math.sin(t * 12) * 3), (x - face * 4, by - 5)])
                pygame.draw.rect(sc, pal["scarf"], (x - 6, int(by - 12), 12, 4), border_radius=2)
            limb(x, by + 3, 11, sw * .85, 6, pants, shoe); limb(x, by - 8, 9, -sw * .9, 4, shirt, sk)
            pygame.draw.circle(sc, sk, (x + face, hy), 8)
            if st == "spiky": pygame.draw.polygon(sc, hr, [P(-7, -1), P(-8, -9), P(-4, -6), P(-3, -14), P(1, -8), P(4, -15), P(6, -8), P(10, -9), P(9, -1)])
            elif st == "long": pygame.draw.polygon(sc, hr, [P(-9, 3), P(-9, -6), P(-4, -10), P(4, -10), P(9, -5), P(9, -2), P(4, -4), P(-3, -3)])
            elif st == "cap":
                dome(hr); pygame.draw.rect(sc, dk(hr), pygame.Rect(min(x + face * 3, x + face * 13), hy - 3, 10, 3))
            elif st == "helmet":
                dome(hr, 1); pygame.draw.line(sc, dk(hr), P(2, -2), P(2, 5), 2)
            ex = x + face * 5
            if blink: pygame.draw.line(sc, (20, 15, 30), (ex - 2, hy + 1), (ex + 2, hy + 1), 2)
            else: pygame.draw.circle(sc, WHITE, (ex, hy + 1), 3); pygame.draw.circle(sc, (20, 15, 30), (ex + face, hy + 1), 2)
            pygame.draw.line(sc, (150, 70, 70), (x + face * 3, hy + 5), (x + face * 6, hy + 5 - (0 if alert else 1)), 2)
            if alert: pygame.draw.line(sc, (40, 0, 0), (ex - 3, hy - 3), (ex + 3, hy - 1 if face > 0 else hy - 5), 2)
        else:
            for sg in (-1, 1):
                lx = x + sg * 3.5; ly = by + 13 + sg * sw * 2.5
                pygame.draw.line(sc, pants, (lx, by + 3), (lx, ly), 6); pygame.draw.circle(sc, shoe, (int(lx), int(ly)), 4)
            if st == "long" and view == "back":
                r = pygame.Rect(0, 0, 20, 26); r.center = (x, hy + 8); pygame.draw.ellipse(sc, hr, r)
            for sg in (-1, 1):
                ax = x + sg * 8; ay = by + 1 - sg * sw * 3
                pygame.draw.line(sc, shirt, (ax - sg, by - 8), (ax, ay), 4); pygame.draw.circle(sc, sk, (int(ax), int(ay)), 3)
            pygame.draw.rect(sc, shirt, (x - 7, int(by - 11), 14, 15), border_radius=4)
            if pal.get("scarf"):
                pygame.draw.rect(sc, pal["scarf"], (x - 7, int(by - 12), 14, 4), border_radius=2)
                if view == "front": pygame.draw.polygon(sc, pal["scarf"], [(x + 1, by - 9), (x + 7, by - 9), (x + 5 + math.sin(t * 10) * 2, by + 1)])
            if view == "back":
                pygame.draw.circle(sc, hr if st != "helmet" else hr, (x, hy), 8.5)
                if st == "cap": dome(hr); pygame.draw.rect(sc, dk(hr), (x - 8, hy - 2, 16, 2))
                if st == "spiky": pygame.draw.polygon(sc, hr, spikes)
            else:
                pygame.draw.circle(sc, sk, (x, hy), 8.5)
                if st == "spiky": pygame.draw.polygon(sc, hr, spikes)
                elif st == "long":
                    pygame.draw.polygon(sc, hr, [P(-9, 14), P(-9, -6), P(-5, -10), P(5, -10), P(9, -6), P(9, 14), P(6, 14), P(6, -4), P(-6, -4), P(-6, 14)])
                elif st == "cap": dome(hr); pygame.draw.rect(sc, dk(hr), (x - 9, hy - 3, 18, 3))
                elif st == "helmet": dome(hr, 1); pygame.draw.rect(sc, dk(hr), (x - 9, hy - 2, 18, 3))
                for sg in (-1, 1):
                    ex = x + sg * 3.5
                    if blink: pygame.draw.line(sc, (20, 15, 30), (ex - 2, hy + 1), (ex + 2, hy + 1), 2)
                    else: pygame.draw.circle(sc, WHITE, (int(ex), hy + 1), 3); pygame.draw.circle(sc, (20, 15, 30), (int(ex), hy + 2), 1.6)
                    if alert: pygame.draw.line(sc, (40, 0, 0), (ex - sg * 3, hy - 3 - sg * 0), (ex + sg * 2, hy - 1), 2)
                if alert: pygame.draw.ellipse(sc, (110, 40, 40), (x - 3, hy + 4, 6, 4))
                else: pygame.draw.arc(sc, (150, 70, 70), (x - 3, hy + 2, 6, 5), math.pi, 2 * math.pi, 2)
        if alert: s.text("!", s.f_b, (255, 230, 60), (x, int(y - 36 + math.sin(t * 14) * 3)))
    def avatar_big(s, cx, cy, pal, view, face, moving, phase, k=3):
        tmp = pygame.Surface((70, 80), pygame.SRCALPHA); real = s.screen; s.screen = tmp
        s.draw_avatar(35, 48, pal, view, face, moving, phase); s.screen = real
        img = pygame.transform.smoothscale(tmp, (70 * k, 80 * k)); s.screen.blit(img, img.get_rect(center=(cx, cy)))
    def select_rects(s):
        return [pygame.Rect(0, 0, 220, 360).move(int(W - (i + .5) * W / 3 - 110), 110) for i in range(len(AVATARS))]
    def confirm_avatar(s): s.pal = AVATARS[s.sel]; s.state = "intro"; s.page = 0

    # --------------- screens
    def draw(s):
        sc = s.screen; st = s.state
        if st in ("card", "levelup"): s.bg(*STYLE[s.level]["sky"])
        elif st in ("menu", "help", "intro", "win", "over", "select"): s.bg()
        if st == "menu":
            img = s.f_xl.render(shape("ما وراء الصفر"), True, tuple(int(GOLD[i] + (255 - GOLD[i]) * (.5 + .5 * math.sin(s.t * 2)) * .5) for i in range(3)))
            k = 1 + .03 * math.sin(s.t * 2); img = pygame.transform.smoothscale(img, (int(img.get_width() * k), int(img.get_height() * k)))
            sc.blit(img, img.get_rect(center=(W // 2, 110 + int(7 * math.sin(s.t * 1.6)))))
            s.text("Beyond Zero  -  لعبة تعليمية في الأرقام والصفر", s.f_m, WHITE, (W // 2, 200))
            s.text("الرقم الأعلى: %d" % s.high, s.f_s, (170, 180, 210), (W // 2, 250))
            for i, (r, t) in enumerate(zip(s.menu_rects(), ["ابدأ اللعب  (Enter)", "كيف تلعب؟  (H)", "خروج  (Esc)"])):
                h = s.hov[i]; rr = r.inflate(int(16 * h), int(6 * h))
                pygame.draw.rect(sc, tuple(int(a + (b - a) * h) for a, b in zip((50, 56, 92), GOLD)), rr, border_radius=14)
                s.text(t, s.f_m, tuple(int(a + (b - a) * h) for a, b in zip(WHITE, (30, 20, 0))), rr.center)
            rx = (s.t * 150) % (W + 320) - 160; ph = s.t * 14
            s.draw_avatar(rx, H - 40, s.pal, "side", 1, True, ph); s.draw_avatar(rx - 110, H - 40, GUARD, "side", 1, True, ph + 1, True, 1)
        elif st == "select":
            s.text_pop("اختر شخصيتك", s.f_b, GOLD, (W // 2, 60))
            for i, (a, r) in enumerate(zip(AVATARS, s.select_rects())):
                sel = i == s.sel; r = r.inflate(14, 14) if sel else r
                pygame.draw.rect(sc, (255, 255, 255, 0) if False else ((90, 60, 170) if sel else (60, 40, 120)), r, border_radius=18)
                pygame.draw.rect(sc, GOLD if sel else (120, 100, 190), r, 4 if sel else 2, border_radius=18)
                if sel:
                    pygame.draw.ellipse(sc, (255, 200, 90), (r.centerx - 60, r.top + 198, 120, 22))
                s.avatar_big(r.centerx, r.top + 150, a, "front", 1, sel, s.t * 11 if sel else 0)
                s.text(a["name"], s.f_b, GOLD if sel else WHITE, (r.centerx, r.top + 262))
                s.para(a["desc"], s.f_s, WHITE, r.centerx, r.top + 292, 190, 22)
            s.fade_text("الأسهم للتنقل  |  Enter أو النقر للاختيار", s.f_s, GOLD, (W // 2, H - 40), .8)
        elif st == "help":
            s.text_pop("كيف تلعب؟", s.f_b, GOLD, (W // 2, 70))
            lines = ["الحركة: الأسهم أو W A S D  |  إيقاف مؤقت: P",
                     "اجمع عملات الصفر لتكسب 10 نقاط لكل عملة.",
                     "اقترب من الباب الذهبي لتظهر لك مسألة. اختر الجواب بالأرقام 1-4 أو بالفأرة.",
                     "الإجابة الصحيحة تفتح الباب وتعطيك 100 نقطة، والخاطئة تخصم 50 نقطة.",
                     "إذا لمسك حارس خسرت قلبًا، ولديك 3 قلوب فقط!",
                     "في آخر مستوى ستجيب عن 3 أسئلة عند البوابة، وكل خطأ يكلّفك قلبًا.",
                     "كل سؤال يأتي مع شرح بعد الإجابة، فتعلّم منه!"]
            y = 130
            for i, ln in enumerate(lines): y = s.para_fx(ln, s.f_m, WHITE, W // 2, y, 700, 34, start=.15 * i) + 12
            s.fade_text("اضغط Enter للعودة", s.f_s, GOLD, (W // 2, H - 50), 1.4)
        elif st == "intro":
            s.para_fx(INTRO[s.page], s.f_m, WHITE, W // 2, 190, 640, 46, .5)
            s.fade_text("%d / %d   -   اضغط Enter" % (s.page + 1, len(INTRO)), s.f_s, GOLD, (W // 2, H - 60), 1.5)
        elif st == "card":
            c = LEVELS[s.level]["card"]
            s.text_pop(c[0], s.f_xl, GOLD, (W // 2, 100))
            y = 210
            for i, ln in enumerate(c[1:]): y = s.para_fx(ln, s.f_m, WHITE, W // 2, y, 660, 40, start=.5 + .7 * i) + 14
            s.fade_text("اضغط Enter للبدء", s.f_s, GOLD, (W // 2, H - 60), 2.4)
        elif st == "levelup":
            s.text_pop("أحسنت يا كاير!", s.f_xl, GREEN, (W // 2, 120))
            k = clamp((s.st - .5) / 1.0)
            s.fade_text("العملات: %d / %d" % (int(s.got * k), s.total_coins), s.f_m, WHITE, (W // 2, 240), .5)
            s.fade_text("مكافأة السرعة: %d" % int(s.bonus * k), s.f_m, WHITE, (W // 2, 290), .8)
            s.text_pop("النقاط: %d" % s.score, s.f_b, GOLD, (W // 2, 360), 1.2)
            s.fade_text("اضغط Enter للمتابعة", s.f_s, GOLD, (W // 2, H - 60), 2)
        elif st == "win":
            s.text_pop("النهاية", s.f_xl, GREEN, (W // 2, 90))
            s.para_fx(ENDING, s.f_m, WHITE, W // 2, 190, 680, 42, .9, start=.4)
            s.text_pop("النقاط: %d    |    الأعلى: %d" % (s.score, s.high), s.f_b, GOLD, (W // 2, 430), 3)
            s.fade_text("اضغط Enter للعودة إلى القائمة", s.f_s, GOLD, (W // 2, H - 50), 3.8)
        elif st == "over":
            s.text_pop("انتهت اللعبة", s.f_xl, RED, (W // 2, 140))
            s.para_fx("أمسك بك حراس الملك… لكن الحقيقة تنتظرك، حاول مرة أخرى!", s.f_m, WHITE, W // 2, 250, 640, 40, .7, start=.5)
            s.text_pop("النقاط: %d    |    الأعلى: %d" % (s.score, s.high), s.f_b, GOLD, (W // 2, 360), 1.4)
            s.fade_text("اضغط Enter للعودة إلى القائمة", s.f_s, GOLD, (W // 2, H - 60), 2)
        elif st in ("play", "quiz", "pause"):
            s.draw_world()
            if st == "quiz": s.draw_quiz()
            if st == "pause":
                v = pygame.Surface((W, H), pygame.SRCALPHA); v.fill((0, 0, 0, 160)); sc.blit(v, (0, 0))
                s.text("إيقاف مؤقت - اضغط P", s.f_b, GOLD, (W // 2, H // 2))
        s.draw_parts(True)
        if s.flash > 0:
            v = pygame.Surface((W, H), pygame.SRCALPHA); v.fill((230, 30, 30, int(110 * s.flash / .3))); sc.blit(v, (0, 0))
        if s.fa > 0:
            v = pygame.Surface((W, H), pygame.SRCALPHA); v.fill((0, 0, 0, int(s.fa))); sc.blit(v, (0, 0))
        pygame.display.flip()

    def draw_world(s):
        sc = s.screen; L = LEVELS[s.level]; S = STYLE[s.level]
        ox, oy = (random.randint(-4, 4), random.randint(-4, 4)) if s.shake > 0 else (0, 0)
        sc.fill((8, 8, 14))
        torches = [(x * T + 20, 24) for x in range(2, COLS - 1, 4)]
        for y in range(ROWS):
            for x in range(COLS):
                r = pygame.Rect(x * T + ox, y * T + HUD + oy, T, T); c = s.grid[y][x]
                pygame.draw.rect(sc, S["floor"][(x + y) % 2], r)
                if c == "#":
                    col = S["walls"][(x * 7 + y * 13) % len(S["walls"])]; inner = r.inflate(-4, -4)
                    pygame.draw.rect(sc, dk(col, .55), r); pygame.draw.rect(sc, col, inner, border_radius=6)
                    pygame.draw.line(sc, lt(col), (inner.left + 5, inner.top + 4), (inner.right - 6, inner.top + 4), 2)
                    pygame.draw.circle(sc, lt(col, .6), inner.center, 3)
                elif c == "D" and (x, y) not in s.opened:
                    d = math.hypot(s.px - (x * T + 20), s.py - (y * T + 20)); near = d < 110
                    rr = r.inflate(-4, 0).move(int(2 * math.sin(s.t * 40)) if near else 0, 0)
                    pul = .5 + .5 * math.sin(s.t * 3 + x)
                    pygame.draw.rect(sc, (60, 30, 0), rr.inflate(4, 0), border_radius=4)
                    pygame.draw.rect(sc, (170 + int(40 * pul), 110 + int(30 * pul), 30), rr, border_radius=4)
                    pygame.draw.rect(sc, (255, 240, 150) if near else GOLD, rr, 3 + (1 if near else 0), border_radius=4)
                    s.text("0", s.f_b, (60, 30, 0), (rr.centerx, rr.centery + int(math.sin(s.t * 4 + x) * 2)))
        for (x, y), t in s.door_anim.items():
            k = ease_out(t / .5); hgt = int(T * (1 - k))
            if hgt > 0:
                pygame.draw.rect(sc, (170, 110, 30), (x * T + 2 + ox, y * T + HUD + oy, T - 4, hgt)); pygame.draw.rect(sc, GOLD, (x * T + 2 + ox, y * T + HUD + oy, T - 4, hgt), 3)
        for m in s.motes:   # colourful fireflies
            mx, my = m[0] + ox, m[1] + HUD + oy; a = .5 + .5 * math.sin(s.t * 2 + m[5])
            gl = pygame.Surface((16, 16), pygame.SRCALPHA); pygame.draw.circle(gl, (*m[4], int(70 * a)), (8, 8), 8); pygame.draw.circle(gl, (*lt(m[4], .6), int(220 * a)), (8, 8), 2); sc.blit(gl, (mx - 8, my - 8))
        ex, ey = s.ex[0] * T + 20 + ox, s.ex[1] * T + 20 + HUD + oy
        pulse = 4 * math.sin(s.t * 4)
        gl = pygame.Surface((90, 90), pygame.SRCALPHA); pygame.draw.circle(gl, (255, 120, 220, int(55 + 30 * math.sin(s.t * 3))), (45, 45), int(40 + pulse)); sc.blit(gl, (ex - 45, ey - 45))
        for rad, col in ((19, (255, 110, 220)), (14, (120, 80, 230)), (9, (255, 255, 255))):
            pygame.draw.circle(sc, col, (ex, ey), int(rad + pulse * (rad / 19)), 3 if rad > 9 else 0)
        for i in range(6):
            a = s.t * 2.2 + i * math.pi / 3; pygame.draw.circle(sc, CONFETTI[i % 5], (int(ex + 24 * math.cos(a)), int(ey + 24 * math.sin(a))), 3)
        s.text("0", s.f_m, (60, 20, 90), (ex, ey))
        for c in s.coins:
            ph = c[0] * .7 + c[1]; cx = c[0] * T + 20 + ox; cy = c[1] * T + 20 + HUD + oy + int(3 * math.sin(s.t * 4 + ph))
            w = int(11 * abs(math.cos(s.t * 3 + ph))) + 1
            pygame.draw.ellipse(sc, GOLD, (cx - w, cy - 11, 2 * w, 22)); pygame.draw.ellipse(sc, (255, 245, 170), (cx - w, cy - 11, 2 * w, 22), 2)
            if w > 7: s.text("0", s.f_s, (120, 70, 0), (cx, cy))
            f = (s.t * 1.5 + ph) % 3
            if f < .35:
                z = int(7 * math.sin(f / .35 * math.pi)); pygame.draw.line(sc, WHITE, (cx + 9 - z, cy - 9), (cx + 9 + z, cy - 9), 2); pygame.draw.line(sc, WHITE, (cx + 9, cy - 9 - z), (cx + 9, cy - 9 + z), 2)
        ents = []
        for i, g in enumerate(s.guards):
            al = math.hypot(g["x"] - s.px, g["y"] - s.py) < 140
            view, face = ("side", g["dir"]) if g["d"] == "h" else (("front" if g["dir"] > 0 else "back"), 1)
            ents.append((g["y"], lambda g=g, view=view, face=face, al=al, i=i: s.draw_avatar(g["x"] + ox, g["y"] + HUD + oy, GUARD, view, face, True, s.t * 8 + i, al, i * 1.7)))
        if s.inv <= 0 or int(s.t * 12) % 2:
            ents.append((s.py, lambda: s.draw_avatar(s.px + ox, s.py + HUD + oy, s.pal, s.view, s.face, s.moving, s.wp)))
        for _, fn in sorted(ents, key=lambda e: e[0]): fn()
        s.draw_parts(False, ox, HUD + oy)
        base = int(88 + 8 * math.sin(s.t * 9) + 4 * math.sin(s.t * 23))
        dk_ = s.dark_base; dk_.fill((24, 10, 60, base))
        dk_.blit(s.mask_big, (int(s.px) - 280, int(s.py) - 280), special_flags=pygame.BLEND_RGBA_SUB)
        dk_.blit(s.mask_small, (s.ex[0] * T + 20 - 95, s.ex[1] * T + 20 - 95), special_flags=pygame.BLEND_RGBA_SUB)
        for (tx, ty) in torches: dk_.blit(s.mask_small, (tx - 95, ty - 95 + 6), special_flags=pygame.BLEND_RGBA_SUB)
        sc.blit(dk_, (ox, HUD + oy))
        for i, (tx, ty) in enumerate(torches):
            fl = 4 * math.sin(s.t * 13 + i * 2) + 2 * math.sin(s.t * 31 + i)
            pygame.draw.rect(sc, (110, 70, 40), (tx - 3 + ox, ty + HUD + 4 + oy, 6, 12))
            pygame.draw.circle(sc, (255, 120, 30), (tx + ox, int(ty + HUD + oy - fl / 2)), int(7 + fl / 2)); pygame.draw.circle(sc, (255, 225, 110), (tx + ox, int(ty + HUD + oy + 1)), int(4 + fl / 3))
        for p in s.pops:
            img = (s.f_b if p["big"] else s.f_s).render(p["t"], True, p["col"]); img.set_alpha(int(255 * clamp(p["life"] / .5)))
            sc.blit(img, img.get_rect(center=(int(p["x"] + ox), int(p["y"] + HUD + oy))))
        if s.time < 2.4:
            t = s.time; k = ease_out(t / .5) if t < 1.9 else 1; a = int(255 * (1 if t < 1.9 else clamp((2.4 - t) / .5)))
            rb = pygame.Surface((W, 64), pygame.SRCALPHA); rb.fill((60, 20, 110, int(190 * a / 255)))
            sc.blit(rb, (0, HUD + 190)); img = s.f_b.render(shape(L["name"]), True, GOLD); img.set_alpha(a)
            sc.blit(img, img.get_rect(center=(int(-300 + (W // 2 + 300) * k), HUD + 222)))
        for yy in range(HUD):
            k = yy / HUD; pygame.draw.line(sc, (int(60 - 30 * k), int(30 - 10 * k), int(120 - 40 * k)), (0, yy), (W, yy))
        for i, c in enumerate(CONFETTI): pygame.draw.rect(sc, c, (i * W // 5, HUD - 4, W // 5 + 1, 4))
        for i in range(3):
            sz = 30 * (1 + .12 * math.sin(s.t * 8)) if (s.lives == 1 and i == 0) else 30
            heart(sc, 40 + i * 44, 34, int(sz), RED if i < s.lives else (80, 60, 90))
        img = s.f_m.render(shape("النقاط: %d" % int(round(s.disp))), True, GOLD); k = 1 + .35 * s.bump
        img = pygame.transform.smoothscale(img, (int(img.get_width() * k), int(img.get_height() * k))); sc.blit(img, img.get_rect(center=(W // 2, 24)))
        s.text("العملات: %d/%d   |   الوقت: %d" % (s.got, s.total_coins, int(s.time)), s.f_s, WHITE, (W // 2, 56))
        s.text(L["name"], s.f_m, WHITE, (W - 20, 28), "midright")
        if s.level == 2: s.text("أسئلة البوابة: %d/3" % s.gate_ok, s.f_s, (255, 200, 255), (W - 20, 58), "midright")

    def draw_quiz(s):
        real = s.screen; q = s.q; qs = s.qs; qs.fill((0, 0, 0, 0)); s.screen = qs
        pan = pygame.Rect(40, 14, W - 80, H - 28)
        pygame.draw.rect(qs, (36, 24, 84), pan, border_radius=18); pygame.draw.rect(qs, GOLD, pan, 3, border_radius=18)
        s.text("البوابة الأخيرة - أسئلة حاسمة" if s.ctx == "gate" else "باب مقفل - حلّ المسألة!", s.f_s, GOLD, (W // 2, 40))
        s.para(q["q"], s.f_b, WHITE, W // 2, 68, 680, 44)
        for i, r in enumerate(s.opt_rects()):
            r = r.move(int((1 - ease_out((s.qt - .12 - .07 * i) / .25)) * 170), 0); col = (50, 56, 96)
            if q["sel"] is None and r.collidepoint(pygame.mouse.get_pos()): col = (80, 90, 150)
            if q["sel"] is not None:
                if i == q["c"]:
                    col = (30, 120, 70); g = int(6 * math.sin(s.at * 14) * max(0, 1 - s.at * 1.6)); r = r.inflate(g, g)
                elif i == q["sel"]: col = (150, 40, 50); r = r.move(int(10 * math.sin(s.at * 40) * max(0, 1 - s.at * 2.5)), 0)
            pygame.draw.rect(qs, col, r, border_radius=12)
            if q["sel"] is not None and i == q["c"]: pygame.draw.rect(qs, (200, 255, 220), r, 3, border_radius=12)
            pygame.draw.circle(qs, GOLD, (r.right - 28, r.centery), 15); s.text(str(i + 1), s.f_m, (30, 20, 0), (r.right - 28, r.centery))
            s.text(q["opts"][i], s.f_m, WHITE, (r.right - 58, r.centery), "midright")
        if q["sel"] is not None:
            ok = q["sel"] == q["c"]; k = ease_back(s.at / .35)
            s.text("إجابة صحيحة!" if ok else "إجابة خاطئة", s.f_b, GREEN if ok else RED, (W // 2, 448 - int(10 * (1 - k))))
            s.para(q["ex"], s.f_s, WHITE, W // 2, 474, 700, 22)
            s.text("اضغط Enter أو انقر للمتابعة", s.f_s, GOLD, (W // 2, H - 26))
        else:
            s.text("اضغط 1 - 4 أو انقر على الإجابة", s.f_s, (170, 180, 210), (W // 2, H - 26))
        s.screen = real
        v = pygame.Surface((W, H), pygame.SRCALPHA); v.fill((0, 0, 0, int(190 * clamp(s.qt / .2)))); real.blit(v, (0, 0))
        k = ease_back(s.qt / .3)
        if k < .995 or k > 1.005:
            sw, sh = max(1, int(W * k)), max(1, int(H * k)); img = pygame.transform.smoothscale(qs, (sw, sh)); img.set_alpha(int(255 * clamp(s.qt / .15)))
            real.blit(img, img.get_rect(center=(W // 2, H // 2)))
        else: real.blit(qs, (0, 0))

    def run(s):
        run = True
        while run:
            dt = min(s.clock.tick(60) / 1000, .05)
            run = s.events(); s.update(dt); s.draw()
        pygame.quit()

if __name__ == "__main__":
    Game().run()
