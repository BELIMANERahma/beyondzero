# -*- coding: utf-8 -*-
"""Drawing helpers: text shaping, avatars, enemies, walls, flag, skyline."""
import math, random, re, pygame
import arabic_reshaper
from bidi.algorithm import get_display

W, H = 800, 560
GOLD = (255, 200, 80); WHITE = (240, 240, 245); RED = (230, 70, 70); GREEN = (80, 210, 120)
CONFETTI = [(255, 90, 90), (255, 200, 80), (90, 220, 130), (90, 170, 255), (200, 120, 255)]
_rs = arabic_reshaper.ArabicReshaper()

def shape(t):
    t = re.sub(r"\{([^}]*)\}", lambda m: "\u202A" + m.group(1) + "\u202C", t)   # {..} = shown left-to-right
    return get_display(_rs.reshape(t))
def protect(t): return re.sub(r"\{[^}]*\}", lambda m: m.group(0).replace(" ", "\u00a0"), t)
def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def ease_out(t): t = clamp(t); return 1 - (1 - t) ** 3
def ease_back(t): t = clamp(t) - 1; return 1 + 2.70158 * t ** 3 + 1.70158 * t ** 2
def dk(c, k=.7): return tuple(int(v * k) for v in c)
def lt(c, k=.35): return tuple(int(v + (255 - v) * k) for v in c)
def mix(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))

def heart(s, x, y, sz, col):
    r = sz // 4
    pygame.draw.circle(s, col, (x - r, y - r // 2), r + 1); pygame.draw.circle(s, col, (x + r, y - r // 2), r + 1)
    pygame.draw.polygon(s, col, [(x - 2 * r - 1, y - 1), (x + 2 * r + 1, y - 1), (x, y + 2 * r + r // 2)])
def draw_star(sc, cx, cy, r, col, rot=-math.pi / 2, inner=.42):
    pts = []
    for i in range(10):
        a = rot + i * math.pi / 5; rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    pygame.draw.polygon(sc, col, pts)
def gradient(sc, top, bot, h=H, step=4):
    for y in range(0, h, step): pygame.draw.rect(sc, mix(top, bot, y / h), (0, y, W, step))

# ------------------------------------------------------------------ palettes
AVATARS = [
 dict(name="كاير", desc="الفتى الفضولي الذي يبحث عن الحقيقة", skin=(245, 200, 160), hair=(70, 45, 30), style="spiky", shirt=(60, 140, 240), pants=(40, 55, 120), shoe=(245, 245, 245), scarf=(235, 70, 85)),
 dict(name="ميليس", desc="الأخت الذكية التي تحمل رسالة الأب", skin=(238, 188, 152), hair=(40, 25, 40), style="long", shirt=(235, 90, 170), pants=(120, 70, 170), shoe=(250, 220, 240)),
 dict(name="خالد", desc="الأخ الشجاع صاحب القبعة", skin=(225, 175, 135), hair=(245, 170, 40), style="cap", shirt=(70, 195, 110), pants=(60, 90, 80), shoe=(250, 250, 250)),
]
GUARD = dict(skin=(232, 190, 150), hair=(150, 156, 178), style="helmet", shirt=(215, 55, 62), pants=(75, 40, 55), shoe=(40, 30, 40))
FATHER = dict(skin=(232, 188, 150), hair=(60, 50, 45), style="spiky", shirt=(150, 100, 60), pants=(60, 50, 70), shoe=(50, 40, 40), beard=True)
KING = dict(skin=(235, 190, 150), hair=(200, 200, 205), style="bald", shirt=(120, 50, 160), pants=(50, 30, 70), shoe=(30, 20, 30), crown=True, beard=True)
ORMAN = dict(skin=(225, 180, 145), hair=(235, 235, 240), style="bald", shirt=(90, 110, 130), pants=(50, 55, 70), shoe=(40, 35, 35), beard=True)

# ------------------------------------------------------------------ avatar
def draw_avatar(sc, t, x, y, pal, view, face, moving, phase, alert=False, seed=0):
    x = int(x); y = int(y)
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
    def crown(): pygame.draw.polygon(sc, GOLD, [P(-6, -8), P(-6, -15), P(-3, -11), P(0, -17), P(3, -11), P(6, -15), P(6, -8)])
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
        if pal.get("beard"): pygame.draw.ellipse(sc, hr, (x + face * 2 - 5, hy + 2, 10, 11))
        if st == "spiky": pygame.draw.polygon(sc, hr, [P(-7, -1), P(-8, -9), P(-4, -6), P(-3, -14), P(1, -8), P(4, -15), P(6, -8), P(10, -9), P(9, -1)])
        elif st == "long": pygame.draw.polygon(sc, hr, [P(-9, 3), P(-9, -6), P(-4, -10), P(4, -10), P(9, -5), P(9, -2), P(4, -4), P(-3, -3)])
        elif st == "cap": dome(hr); pygame.draw.rect(sc, dk(hr), pygame.Rect(min(x + face * 3, x + face * 13), hy - 3, 10, 3))
        elif st == "helmet": dome(hr, 1); pygame.draw.line(sc, dk(hr), P(2, -2), P(2, 5), 2)
        if pal.get("crown"): crown()
        ex = x + face * 5
        if blink: pygame.draw.line(sc, (20, 15, 30), (ex - 2, hy + 1), (ex + 2, hy + 1), 2)
        else: pygame.draw.circle(sc, WHITE, (ex, hy + 1), 3); pygame.draw.circle(sc, (20, 15, 30), (ex + face, hy + 1), 2)
        if not pal.get("beard"): pygame.draw.line(sc, (150, 70, 70), (x + face * 3, hy + 5), (x + face * 6, hy + 5 - (0 if alert else 1)), 2)
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
            pygame.draw.circle(sc, hr, (x, hy), 8.5)
            if st == "cap": dome(hr); pygame.draw.rect(sc, dk(hr), (x - 8, hy - 2, 16, 2))
            if st == "spiky": pygame.draw.polygon(sc, hr, spikes)
            if st == "bald": pygame.draw.circle(sc, sk, (x, hy), 8.5); pygame.draw.arc(sc, hr, (x - 9, hy - 9, 18, 18), 0, math.pi, 3)
            if pal.get("crown"): crown()
        else:
            pygame.draw.circle(sc, sk, (x, hy), 8.5)
            if pal.get("beard"): pygame.draw.ellipse(sc, hr, (x - 6, hy + 2, 12, 12))
            if st == "spiky": pygame.draw.polygon(sc, hr, spikes)
            elif st == "long": pygame.draw.polygon(sc, hr, [P(-9, 14), P(-9, -6), P(-5, -10), P(5, -10), P(9, -6), P(9, 14), P(6, 14), P(6, -4), P(-6, -4), P(-6, 14)])
            elif st == "cap": dome(hr); pygame.draw.rect(sc, dk(hr), (x - 9, hy - 3, 18, 3))
            elif st == "helmet": dome(hr, 1); pygame.draw.rect(sc, dk(hr), (x - 9, hy - 2, 18, 3))
            elif st == "bald": pygame.draw.arc(sc, hr, (x - 9, hy - 9, 18, 18), .4, math.pi - .4, 3)
            if pal.get("crown"): crown()
            for sg in (-1, 1):
                ex = x + sg * 3.5
                if blink: pygame.draw.line(sc, (20, 15, 30), (ex - 2, hy + 1), (ex + 2, hy + 1), 2)
                else: pygame.draw.circle(sc, WHITE, (int(ex), hy + 1), 3); pygame.draw.circle(sc, (20, 15, 30), (int(ex), hy + 2), 1.6)
                if alert: pygame.draw.line(sc, (40, 0, 0), (ex - sg * 3, hy - 3), (ex + sg * 2, hy - 1), 2)
            if alert: pygame.draw.ellipse(sc, (110, 40, 40), (x - 3, hy + 4, 6, 4))
            elif not pal.get("beard"): pygame.draw.arc(sc, (150, 70, 70), (x - 3, hy + 2, 6, 5), math.pi, 2 * math.pi, 2)
    if alert:
        by2 = int(y - 38 + math.sin(t * 14) * 3)
        pygame.draw.line(sc, (255, 230, 60), (x, by2 - 7), (x, by2 + 2), 4); pygame.draw.circle(sc, (255, 230, 60), (x, by2 + 7), 2)

# ------------------------------------------------------------------ enemies
def draw_enemy(sc, t, kind, x, y, dx, dy, alert, seed, frozen=False):
    x = int(x); y = int(y)
    if kind == "guard":
        view, face = ("side", dx) if dx else (("front" if dy > 0 else "back"), 1)
        draw_avatar(sc, t, x, y, GUARD, view, face or 1, not frozen, t * 8 + seed, alert, seed)
    elif kind == "robot":
        bob = 0 if frozen else math.sin(t * 9 + seed) * 1.5
        sh = pygame.Surface((28, 9), pygame.SRCALPHA); pygame.draw.ellipse(sh, (0, 0, 0, 80), (0, 0, 28, 9)); sc.blit(sh, (x - 14, y + 10))
        for wx in (-8, 8):
            pygame.draw.circle(sc, (40, 44, 60), (x + wx, y + 10), 5)
            a = t * 10 * (1 if dx >= 0 else -1) * (0 if frozen else 1)
            pygame.draw.line(sc, (150, 160, 180), (x + wx, y + 10), (x + wx + 4 * math.cos(a), y + 10 + 4 * math.sin(a)), 2)
        pygame.draw.rect(sc, (150, 165, 190), (x - 13, int(y - 12 + bob), 26, 22), border_radius=6); pygame.draw.rect(sc, (90, 100, 125), (x - 13, int(y - 12 + bob), 26, 22), 2, border_radius=6)
        pygame.draw.rect(sc, (20, 25, 45), (x - 9, int(y - 8 + bob), 18, 10), border_radius=3)
        ec = (255, 60, 60) if alert else (60, 255, 230)
        for ex in (-4, 4): pygame.draw.circle(sc, ec, (x + ex + (dx > 0) * 2 - (dx < 0) * 2, int(y - 3 + bob)), 2)
        pygame.draw.line(sc, (90, 100, 125), (x, int(y - 12 + bob)), (x, int(y - 19 + bob)), 2)
        pygame.draw.circle(sc, RED if int(t * 4 + seed) % 2 else (255, 200, 80), (x, int(y - 20 + bob)), 3)
    elif kind == "slime":
        k = 0 if frozen else math.sin(t * 6 + seed)
        w, h = int(30 * (1 + .14 * k)), int(22 * (1 - .14 * k)); r = pygame.Rect(0, 0, w, h); r.midbottom = (x, y + 12)
        sh = pygame.Surface((30, 9), pygame.SRCALPHA); pygame.draw.ellipse(sh, (0, 0, 0, 70), (0, 0, 30, 9)); sc.blit(sh, (x - 15, y + 8))
        pygame.draw.ellipse(sc, (90, 220, 110), r); pygame.draw.ellipse(sc, (40, 150, 70), r, 2)
        pygame.draw.ellipse(sc, (190, 255, 200), (r.left + 5, r.top + 3, 8, 5))
        for ex in (-5, 5):
            pygame.draw.circle(sc, WHITE, (x + ex, r.centery - 2), 4); pygame.draw.circle(sc, (20, 40, 20) if not alert else RED, (x + ex + (dx > 0) * 1 - (dx < 0) * 1, r.centery - 2), 2)
    elif kind == "dust":
        a = 0 if frozen else t * 6 + seed
        for i in range(8):
            ang = a + i * math.pi / 4
            pygame.draw.line(sc, (150, 105, 60), (x, y), (x + 13 * math.cos(ang), y + 13 * math.sin(ang)), 2)
            pygame.draw.circle(sc, (190, 140, 80), (int(x + 13 * math.cos(ang)), int(y + 13 * math.sin(ang))), 2)
        pygame.draw.circle(sc, (170, 120, 70), (x, y), 8); pygame.draw.circle(sc, (120, 80, 45), (x, y), 8, 2)
    if frozen:
        ov = pygame.Surface((34, 40), pygame.SRCALPHA); pygame.draw.rect(ov, (150, 220, 255, 140), (0, 0, 34, 40), border_radius=8)
        pygame.draw.rect(ov, (255, 255, 255, 200), (0, 0, 34, 40), 2, border_radius=8); sc.blit(ov, (x - 17, y - 24))

# ------------------------------------------------------------------ walls
def draw_wall(sc, r, theme, col, x, y, t):
    inner = r.inflate(-4, -4)
    pygame.draw.rect(sc, dk(col, .55), r); pygame.draw.rect(sc, col, inner, border_radius=6)
    pygame.draw.line(sc, lt(col), (inner.left + 5, inner.top + 3), (inner.right - 6, inner.top + 3), 2)
    if theme in ("archive", "library"):
        for i in range(5):
            c = CONFETTI[(x * 3 + y + i) % 5]; h = inner.height - 12 - ((i * 7 + x) % 7)
            pygame.draw.rect(sc, c, (inner.left + 4 + i * 6, inner.bottom - 4 - h, 5, h), border_radius=1)
    elif theme == "computer":
        scr = inner.inflate(-8, -10); pygame.draw.rect(sc, (12, 20, 44), scr, border_radius=3)
        for k in range(3):
            w = 6 + int((math.sin(t * 2 + x + k * 2) + 1) * 6); pygame.draw.line(sc, (80, 255, 170), (scr.left + 3, scr.top + 4 + k * 5), (scr.left + 3 + w, scr.top + 4 + k * 5), 2)
        pygame.draw.circle(sc, (255, 80, 80) if int(t * 2 + x) % 2 else (80, 255, 120), (inner.right - 5, inner.bottom - 4), 2)
    elif theme == "lab":
        liq = CONFETTI[(x + y) % 5]
        pygame.draw.polygon(sc, (235, 245, 255), [(inner.centerx - 3, inner.top + 4), (inner.centerx + 3, inner.top + 4), (inner.centerx + 10, inner.bottom - 5), (inner.centerx - 10, inner.bottom - 5)])
        pygame.draw.polygon(sc, liq, [(inner.centerx - 7, inner.centery + 2), (inner.centerx + 7, inner.centery + 2), (inner.centerx + 10, inner.bottom - 5), (inner.centerx - 10, inner.bottom - 5)])
        by = inner.bottom - 8 - int((t * 14 + x * 5) % 14); pygame.draw.circle(sc, WHITE, (inner.centerx + int(3 * math.sin(t * 3 + x)), by), 2)
    elif theme == "tunnel":
        pygame.draw.line(sc, dk(col, .7), (inner.left, inner.centery), (inner.right, inner.centery), 2)
        pygame.draw.line(sc, dk(col, .7), (inner.centerx + (x % 2) * 6 - 3, inner.top), (inner.centerx + (x % 2) * 6 - 3, inner.centery), 2)
        pygame.draw.line(sc, dk(col, .7), (inner.centerx - (y % 2) * 6 + 3, inner.centery), (inner.centerx - (y % 2) * 6 + 3, inner.bottom), 2)
    elif theme == "gate":
        c = lt(col, .55); k = 1 + .15 * math.sin(t * 3 + x)
        pygame.draw.polygon(sc, c, [(inner.centerx, inner.centery - 12 * k), (inner.centerx + 7, inner.centery), (inner.centerx, inner.centery + 12 * k), (inner.centerx - 7, inner.centery)])
    elif theme == "nov":
        if (x + y) % 2: draw_star(sc, inner.centerx, inner.centery, 8, (210, 30, 40))
        else: pygame.draw.circle(sc, (210, 30, 40), inner.center, 7); pygame.draw.circle(sc, col, (inner.centerx + 3, inner.centery), 6)

# ------------------------------------------------------------------ flag
_flags = {}
def flag_surface(w, h):
    if (w, h) in _flags: return _flags[(w, h)]
    s = pygame.Surface((w, h), pygame.SRCALPHA); s.fill((250, 250, 250)); pygame.draw.rect(s, (0, 125, 62), (0, 0, w // 2, h))
    R = int(h * .32); cx, cy = w // 2, h // 2
    cr = pygame.Surface((w, h), pygame.SRCALPHA); pygame.draw.circle(cr, (213, 32, 44), (cx, cy), R); pygame.draw.circle(cr, (0, 0, 0, 0), (cx + int(R * .28), cy), int(R * .8)); s.blit(cr, (0, 0))
    draw_star(s, cx + int(R * .42), cy, int(R * .5), (213, 32, 44), rot=-math.pi / 2 + .5)
    _flags[(w, h)] = s; return s
def draw_flag(sc, x, y, w, h, t, amp=5, pole=True):
    fs = flag_surface(w, h)
    for i in range(0, w, 2):
        off = int(amp * math.sin(i * .08 - t * 4) * min(1, .1 + i / (w * .5)))
        sc.blit(fs, (x + i, y + off), (i, 0, 2, h))
    if pole:
        pygame.draw.rect(sc, (190, 190, 200), (x - 4, y - 6, 4, h + 60)); pygame.draw.circle(sc, GOLD, (x - 2, y - 8), 4)

# ------------------------------------------------------------------ scenery
_stars = {}; _sk = {}
def stars(sc, t, seed, n=60, ymax=300):
    if seed not in _stars:
        r = random.Random(seed); _stars[seed] = [(r.randint(0, W), r.randint(0, ymax), r.random() * 6, r.choice((1, 1, 2))) for _ in range(n)]
    for x, y, ph, sz in _stars[seed]:
        a = .5 + .5 * math.sin(t * 2 + ph); c = int(120 + 135 * a); pygame.draw.circle(sc, (c, c, min(255, c + 20)), (x, y), sz)
def moon(sc, x, y, t, r=34):
    gl = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
    for k in range(5): pygame.draw.circle(gl, (255, 245, 200, 14), (r * 2, r * 2), r + k * 9)
    sc.blit(gl, (x - r * 2, y - r * 2)); pygame.draw.circle(sc, (255, 248, 215), (x, y), r); pygame.draw.circle(sc, (235, 225, 190), (x - 10, y - 6), 6); pygame.draw.circle(sc, (235, 225, 190), (x + 12, y + 9), 4)
def skyline(sc, t, base, seed, col, speed, hmin, hmax, lit=False):
    if seed not in _sk:
        r = random.Random(seed); x = 0; b = []
        while x < W:
            bw = r.randint(36, 76); bh = r.randint(hmin, hmax); b.append((x, bw, bh, [r.random() for _ in range(30)])); x += bw + r.randint(0, 8)
        _sk[seed] = b
    off = (t * speed) % W
    for k in (0, 1):
        for bx, bw, bh, win in _sk[seed]:
            px = bx - off + k * W
            if px > W or px + bw < 0: continue
            pygame.draw.rect(sc, col, (px, base - bh, bw, bh + 200))
            if lit:
                for i in range(0, min(30, (bw // 12) * (bh // 16))):
                    wx = px + 6 + (i % max(1, bw // 12)) * 12; wy = base - bh + 8 + (i // max(1, bw // 12)) * 16
                    if wy < base - 6 and win[i] > .45 + .1 * math.sin(t + win[i] * 20): pygame.draw.rect(sc, (255, 215, 120), (wx, wy, 5, 7))
def mountains(sc, base, col, seed, amp=90, freq=.012, shift=0):
    pts = [(0, H)]
    for x in range(0, W + 20, 20): pts.append((x, base - amp * (.55 + .3 * math.sin(x * freq + seed + shift) + .25 * math.sin(x * freq * 2.7 + seed * 2))))
    pts.append((W, H)); pygame.draw.polygon(sc, col, pts)
