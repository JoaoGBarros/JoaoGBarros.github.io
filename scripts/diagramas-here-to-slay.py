# Uso: python scripts/diagramas-here-to-slay.py <pasta-de-saida> <parte: 2 ou 3>
"""Gera os diagramas da parte 2 do Here To Slay (PT e EN) no visual Platinum do site."""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

INK = "#1c1f26"
MUTED = "#5d6370"
LINE = "#c9cdd6"
SOFT = "#f1f2f4"
NAVY = "#2b3a55"
NAVY_SOFT = "#e3e8f2"
RED = "#cf3439"
RED_SOFT = "#fbe7e8"
WHITE = "#ffffff"
FONT = "Rubik, 'Segoe UI', system-ui, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'Courier New', monospace"


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.title = w, h, title
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=13, weight=400, fill=INK, anchor="start", family=FONT, italic=False):
        style = ' font-style="italic"' if italic else ""
        self.add(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{style}>{escape(s)}</text>'
        )

    def rect(self, x, y, w, h, fill=WHITE, stroke=LINE, r=14, dash=None, sw=1.5):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def arrow(self, pts, label=None, lx=None, ly=None, color=NAVY, dash=None, head="arrow", anchor="middle", lcolor=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        p = " ".join(f"{x},{y}" for x, y in pts)
        marker = f' marker-end="url(#{head}-{color[1:]})"' if head else ""
        self.add(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="1.8"{d}{marker}/>')
        if label:
            if lx is None:
                (x1, y1), (x2, y2) = pts[len(pts) // 2 - 1], pts[len(pts) // 2]
                lx, ly = (x1 + x2) / 2, (y1 + y2) / 2 - 6
            self.label(lx, ly, label, lcolor or color, anchor)

    def label(self, x, y, s, color=NAVY, anchor="middle"):
        lines = s.split("\n")
        width = max(len(l) for l in lines) * 6.4 + 12
        h = 16 * len(lines) + 4
        bx = x - width / 2 if anchor == "middle" else (x if anchor == "start" else x - width)
        self.add(f'<rect x="{bx:.1f}" y="{y - 13}" width="{width:.1f}" height="{h}" rx="6" fill="{WHITE}" opacity="0.94"/>')
        tx = x if anchor == "middle" else (bx + 6 if anchor == "start" else x - 6)
        for i, l in enumerate(lines):
            self.text(tx, y + i * 16, l, size=11.5, weight=500, fill=color, anchor=anchor)

    def render(self):
        markers = []
        for c in (NAVY, RED, MUTED, INK):
            markers.append(
                f'<marker id="arrow-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
                f'<marker id="tri-{c[1:]}" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" orient="auto-start-reverse">'
                f'<path d="M1,1 L11,6 L1,11 z" fill="{WHITE}" stroke="{c}" stroke-width="1.4"/></marker>'
                f'<marker id="dia-{c[1:]}" viewBox="0 0 14 10" refX="13" refY="5" markerWidth="14" markerHeight="10" orient="auto-start-reverse">'
                f'<path d="M1,5 L7,1 L13,5 L7,9 z" fill="{WHITE}" stroke="{c}" stroke-width="1.4"/></marker>'
            )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
            f'role="img" aria-label="{escape(self.title)}">\n<title>{escape(self.title)}</title>\n'
            f'<defs>{"".join(markers)}</defs>\n'
            f'<rect width="{self.w}" height="{self.h}" rx="24" fill="{SOFT}"/>\n' + "\n".join(self.parts) + "\n</svg>\n"
        )


# ---------------------------------------------------------------- arquitetura
def architecture(lang):
    T = {
        "pt": dict(
            title="Arquitetura do Here To Slay antes do Kafka: clientes Electron conversam por WebSocket com um único servidor Java que guarda tudo em memória",
            heading="Antes do Kafka: um servidor, tudo em memória",
            clients="Clientes (um por jogador)",
            player="Jogador",
            client_stack=["Electron + React + Vite", "WebSocketProvider", "react-dnd · react-dice-3d", "GSAP · Framer Motion · Howler"],
            server="Servidor Java 21 · um processo · porta 8887",
            router="HereToSlay extends WebSocketServer",
            router_sub="onMessage(): lê o campo \"type\" e repassa",
            memory="Estado em memória (ConcurrentHashMap)",
            mem_items=["jogadores online", "lobbies", "partidas"],
            match="Match (uma por partida)",
            match_sub="máquina de estados",
            send="JSON {type, subtype, payload}",
            recv="broadcast(): estado da partida,\ntimer_update a cada 100 ms",
            risk="Se o processo cai, todas as partidas somem",
            singleton="singletons",
        ),
        "en": dict(
            title="Here To Slay architecture before Kafka: Electron clients talk over WebSocket to a single Java server that keeps everything in memory",
            heading="Before Kafka: one server, everything in memory",
            clients="Clients (one per player)",
            player="Player",
            client_stack=["Electron + React + Vite", "WebSocketProvider", "react-dnd · react-dice-3d", "GSAP · Framer Motion · Howler"],
            server="Java 21 server · one process · port 8887",
            router="HereToSlay extends WebSocketServer",
            router_sub="onMessage(): reads \"type\" and dispatches",
            memory="In-memory state (ConcurrentHashMap)",
            mem_items=["online players", "lobbies", "matches"],
            match="Match (one per game)",
            match_sub="state machine",
            send="JSON {type, subtype, payload}",
            recv="broadcast(): match state,\ntimer_update every 100 ms",
            risk="If the process dies, every match is gone",
            singleton="singletons",
        ),
    }[lang]
    s = Svg(1120, 560, T["title"])
    s.text(40, 52, T["heading"], size=22, weight=800)

    # clients
    s.text(40, 96, T["clients"], size=13, weight=600, fill=MUTED)
    for i in range(3):
        y = 112 + i * 18
        s.rect(40 + i * 10, y, 280, 300, fill=WHITE, stroke=LINE)
    cx, cy = 60, 148
    s.rect(cx, cy, 280, 300, fill=WHITE, stroke=NAVY, sw=1.8)
    s.text(cx + 20, cy + 34, f"{T['player']} 1, 2, 3…", size=15, weight=700)
    for i, item in enumerate(T["client_stack"]):
        yy = cy + 62 + i * 52
        s.rect(cx + 20, yy, 240, 38, fill=NAVY_SOFT if i else SOFT, stroke="none", r=10)
        s.text(cx + 34, yy + 24, item, size=12.5, weight=500, fill=NAVY if i else INK)

    # server
    sx, sy, sw_, sh = 510, 96, 570, 430
    s.rect(sx, sy, sw_, sh, fill=WHITE, stroke=NAVY, sw=1.8, r=20)
    s.text(sx + 24, sy + 34, T["server"], size=15, weight=700)

    rx, ry = sx + 24, sy + 56
    s.rect(rx, ry, sw_ - 48, 62, fill=NAVY, stroke="none", r=12)
    s.text(rx + 16, ry + 26, T["router"], size=13.5, weight=700, fill=WHITE, family=MONO)
    s.text(rx + 16, ry + 47, T["router_sub"], size=12, fill="#d6dcea")

    services = ["AuthService", "LobbyService", "MatchService"]
    svc_w, gap = 160, 21
    for i, name in enumerate(services):
        x = rx + i * (svc_w + gap)
        y = ry + 112
        s.rect(x, y, svc_w, 48, fill=NAVY_SOFT, stroke="none", r=10)
        s.text(x + svc_w / 2, y + 29, name, size=13, weight=600, fill=NAVY, anchor="middle", family=MONO)
        s.arrow([(x + svc_w / 2, ry + 62), (x + svc_w / 2, y)], color=NAVY)
        tag = ["auth", "lobby", "match"][i]
        s.label(x + svc_w / 2 + 2, ry + 90, f'type: "{tag}"')
    s.text(rx + (sw_ - 48), ry + 182, T["singleton"], size=11, fill=MUTED, anchor="end", italic=True)

    # match
    mx, my = rx + 2 * (svc_w + gap), ry + 210
    s.rect(mx, my, svc_w, 66, fill=WHITE, stroke=NAVY, r=10)
    s.text(mx + svc_w / 2, my + 26, T["match"], size=12.5, weight=700, fill=INK, anchor="middle")
    s.text(mx + svc_w / 2, my + 46, T["match_sub"], size=11, fill=MUTED, anchor="middle")
    s.arrow([(mx + svc_w / 2, ry + 160), (mx + svc_w / 2, my)], color=NAVY)

    # memory
    memx, memy = rx, ry + 210
    s.rect(memx, memy, 2 * svc_w + gap, 140, fill=RED_SOFT, stroke=RED, dash="6 5", r=12)
    s.text(memx + 16, memy + 26, T["memory"], size=12.5, weight=700, fill=RED)
    for i, it in enumerate(T["mem_items"]):
        s.rect(memx + 16 + i * 110, memy + 44, 98, 34, fill=WHITE, stroke="none", r=8)
        s.text(memx + 65 + i * 110, memy + 66, it, size=11.5, weight=500, fill=INK, anchor="middle")
    s.text(memx + 16, memy + 112, "⚠ " + T["risk"], size=12.5, weight=700, fill=RED)
    for i in range(2):
        x = rx + i * (svc_w + gap) + svc_w / 2
        s.arrow([(x, ry + 160), (x, memy)], color=MUTED, dash="4 4")
    s.arrow([(mx, my + 33), (memx + 2 * svc_w + gap, my + 33)], color=MUTED, dash="4 4")

    # arrows client <-> server
    s.arrow([(340, 236), (sx, 236)], T["send"], lx=425, ly=222)
    s.arrow([(sx, 372), (340, 372)], T["recv"], lx=425, ly=394, color=RED, lcolor=RED)
    return s.render()


# ---------------------------------------------------------------- classes
def class_box(s, x, y, w, name, stereo=None, fields=(), methods=(), accent=NAVY, abstract=False):
    head = 34 + (14 if stereo else 0)
    h = head + 10 + 17 * len(fields) + (10 + 17 * len(methods) if methods else 0) + 6
    s.rect(x, y, w, h, fill=WHITE, stroke=accent, r=10, sw=1.6)
    s.add(f'<path d="M{x},{y + head} h{w}" stroke="{accent}" stroke-width="1"/>')
    ty = y + 22
    if stereo:
        s.text(x + w / 2, ty - 4, stereo, size=10.5, fill=MUTED, anchor="middle", family=MONO)
        ty += 14
    s.text(x + w / 2, ty, name, size=13.5, weight=700, fill=accent, anchor="middle", family=MONO, italic=abstract)
    yy = y + head + 20
    for f in fields:
        s.text(x + 12, yy, f, size=11.5, fill=INK, family=MONO)
        yy += 17
    if methods:
        s.add(f'<path d="M{x},{yy - 8} h{w}" stroke="{LINE}" stroke-width="1"/>')
        yy += 10
        for m in methods:
            s.text(x + 12, yy, m, size=11.5, fill=MUTED, family=MONO)
            yy += 17
    return h


def classes(lang):
    T = {
        "pt": dict(
            title="Diagrama de classes do Here To Slay antes do Kafka: a partida guarda o estado de cada jogador, e os efeitos das cartas seguem os padrões Composite e Conditional",
            heading="Classes principais da partida e das cartas",
            composite="Composite: um efeito pode\nser uma lista de efeitos",
            conditional="Conditional: um efeito ou\noutro, conforme o estado",
            players="1 por jogador",
            effect="efeito",
            deck="baralho e\ndescarte",
            handparty="mão e grupo",
            states="11 estados da partida",
        ),
        "en": dict(
            title="Here To Slay class diagram before Kafka: the match holds each player's state, and card effects follow the Composite and Conditional patterns",
            heading="Core match and card classes",
            composite="Composite: an effect can\nbe a list of effects",
            conditional="Conditional: one effect or\nanother, based on state",
            players="1 per player",
            effect="effect",
            deck="draw and\ndiscard",
            handparty="hand and party",
            states="11 match states",
        ),
    }[lang]
    s = Svg(1180, 720, T["title"])
    s.text(40, 52, T["heading"], size=22, weight=800)

    # left column: Match and GameState
    class_box(s, 40, 90, 270, "Match", fields=[
        "matchState: MatchState",
        "players: Map<WebSocket, GameState>",
        "turnOrder: List<WebSocket>",
        "drawPile: Stack<Card>",
        "discardPile: List<Card>",
        "currentHeroCard: Card",
    ], methods=["playCard(state, cardId)", "challengeHero(conn)", "processHeroDiceRoll(state, roll)", "broadcast(message)"])
    class_box(s, 40, 420, 270, "GameState", fields=[
        "username: String",
        "leader: PartyLeader",
        "hand: List<Card>",
        "party: List<Card>",
        "currentAP / maxAP: int",
        "pendingHeroCard: Card",
    ])
    s.add(f'<polyline points="175,420 175,320" fill="none" stroke="{NAVY}" stroke-width="1.8" marker-end="url(#dia-2b3a55)"/>')
    s.label(110, 376, T["players"])

    # middle column: Card hierarchy
    class_box(s, 410, 90, 280, "Card", stereo="«abstract»", abstract=True, fields=[
        "cardId: Long",
        "cardName: String",
        "type: CardType",
        "effect: CompositeCardEffect",
    ])
    trunk = 550
    subs = [("HeroCard", ["diceValue: int"], 0, 300), ("MagicCard", [], 1, 300),
            ("ItemCard", [], 0, 400), ("ModifierCard", ["modifierValue: int"], 1, 400),
            ("ChallengeCard", [], 0, 490)]
    lowest = 0
    for name, f, col, y in subs:
        x = 390 if col == 0 else 570
        class_box(s, x, y, 140, name, fields=f)
        mid = y + 22
        lowest = max(lowest, mid)
        edge = 530 if col == 0 else 570
        s.add(f'<polyline points="{edge},{mid} {trunk},{mid}" fill="none" stroke="{NAVY}" stroke-width="1.6"/>')
    s.add(f'<polyline points="{trunk},{lowest} {trunk},222" fill="none" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#tri-2b3a55)"/>')

    # Match / GameState -> Card associations
    s.arrow([(310, 200), (410, 200)], color=MUTED)
    s.label(360, 176, T["deck"], MUTED)
    s.arrow([(310, 480), (340, 480), (340, 150), (410, 150)], color=MUTED)
    s.label(318, 398, T["handparty"], MUTED, anchor="end")

    # right column: effects
    class_box(s, 780, 90, 320, "CardEffect", stereo="«interface»", accent=RED, methods=["applyEffect(match, gameState)"])
    class_box(s, 740, 300, 190, "CompositeCardEffect", accent=RED, fields=["effects: List<CardEffect>"])
    class_box(s, 950, 300, 190, "ConditionalCardEffect", accent=RED, fields=["condition: Predicate", "effectIfTrue", "effectIfFalse"])
    dash = 'stroke-dasharray="6 4"'
    s.add(f'<polyline points="835,300 835,260 1160,260" fill="none" stroke="{RED}" stroke-width="1.6" {dash}/>')
    s.add(f'<polyline points="1045,300 1045,260" fill="none" stroke="{RED}" stroke-width="1.6" {dash}/>')
    s.add(f'<polyline points="940,260 940,182" fill="none" stroke="{RED}" stroke-width="1.6" {dash} marker-end="url(#tri-cf3439)"/>')
    leaves = [("DrawEffect", 740, 470), ("DestroyCardEffect", 880, 470), ("StealCardEffect", 1020, 470),
              ("StealHandEffect", 810, 535), ("TradeHandEffect", 950, 535)]
    for n, x, y in leaves:
        s.rect(x, y, 130, 38, fill=WHITE, stroke=RED, r=10)
        s.text(x + 65, y + 24, n, size=11.5, weight=600, fill=RED, anchor="middle", family=MONO)
    s.add(f'<polyline points="805,470 805,450 1160,450 1160,260" fill="none" stroke="{RED}" stroke-width="1.6" {dash}/>')
    for x in (945, 1085):
        s.add(f'<polyline points="{x},470 {x},450" fill="none" stroke="{RED}" stroke-width="1.6" {dash}/>')
    s.add(f'<polyline points="875,535 875,521 742,521 742,450 805,450" fill="none" stroke="{RED}" stroke-width="1.6" {dash}/>')
    s.add(f'<polyline points="1015,535 1015,521 1160,521 1160,450" fill="none" stroke="{RED}" stroke-width="1.6" {dash}/>')
    # composite holds a list of CardEffect
    s.add(f'<polyline points="740,318 728,318 728,135 780,135" fill="none" stroke="{RED}" stroke-width="1.8" marker-start="url(#dia-cf3439)" marker-end="url(#arrow-cf3439)"/>')
    s.label(835, 388, T["composite"], RED)
    s.label(1045, 420, T["conditional"], RED)
    # Card -> CompositeCardEffect
    s.arrow([(690, 205), (712, 205), (712, 345), (740, 345)], color=MUTED)
    s.label(706, 282, T["effect"], MUTED, anchor="end")

    # enums
    s.rect(40, 600, 1100, 90, fill=WHITE, stroke=LINE, r=12)
    enums = [
        ("«enum» MatchState", T["states"]),
        ("«enum» PartyLeader", "BARD · WIZARD · FIGHTER · THIEF · GUARDIAN · RANGER"),
        ("«enum» CardType", "HERO · MAGIC · ITEM · MODIFIER · CHALLENGE…"),
    ]
    for i, (n, d) in enumerate(enums):
        x = 64 + i * 360
        s.text(x, 634, n, size=12.5, weight=700, fill=NAVY, family=MONO)
        s.text(x, 660, d, size=11.5, fill=MUTED)
    return s.render()


def states(lang):
    T = {
        "pt": dict(
            title="Máquina de estados da partida do Here To Slay antes do Kafka",
            heading="A partida como máquina de estados",
            e=dict(
                start="nova partida",
                rolled="todos rolaram\no dado de ordem",
                chosen="todos escolheram\no líder",
                play_hero="joga um herói (janela de 5 s)",
                challenge="alguém desafia",
                hero_wins="herói vence:\njanela reabre",
                hero_loses="desafiante vence:\nherói descartado",
                timeout="tempo acaba",
                use_hero="usa a habilidade\nde um herói",
                needs_target="efeito pede alvo",
                no_target="sem alvo ou\nrolagem falhou",
                confirmed="alvos confirmados",
            ),
            unused="Declarados no enum, ainda não usados",
        ),
        "en": dict(
            title="Here To Slay match state machine before Kafka",
            heading="The match as a state machine",
            e=dict(
                start="new match",
                rolled="everyone rolled\nfor turn order",
                chosen="everyone picked\na leader",
                play_hero="plays a hero (5 s window)",
                challenge="someone challenges",
                hero_wins="hero wins:\nwindow reopens",
                hero_loses="challenger wins:\nhero discarded",
                timeout="time runs out",
                use_hero="uses a hero's\nability",
                needs_target="effect needs a target",
                no_target="no target or\nroll failed",
                confirmed="targets confirmed",
            ),
            unused="Declared in the enum, not used yet",
        ),
    }[lang]
    E = T["e"]
    s = Svg(1180, 640, T["title"])
    s.text(40, 52, T["heading"], size=22, weight=800)

    def state(x, y, name, w=200, main=False, unused=False, ghost=False):
        fill = NAVY if main else (SOFT if (unused or ghost) else WHITE)
        stroke = MUTED if unused else NAVY
        s.rect(x, y, w, 46, fill=fill, stroke=stroke, r=23, dash="6 5" if (unused or ghost) else None, sw=1.6)
        color = WHITE if main else (MUTED if unused else NAVY)
        s.text(x + w / 2, y + 28, name, size=12, weight=700, fill=color, anchor="middle", family=MONO)

    # row 1
    s.add(f'<circle cx="52" cy="143" r="9" fill="{INK}"/>')
    s.arrow([(61, 143), (100, 143)])
    s.label(80, 182, E["start"], MUTED)
    state(100, 120, "ORDER_SELECTION")
    state(380, 120, "PARTY_LEADER_SELECTION", w=230)
    state(700, 120, "GAMEPLAY", w=200, main=True)
    s.arrow([(300, 143), (380, 143)])
    s.label(340, 92, E["rolled"])
    s.arrow([(610, 143), (700, 143)])
    s.label(655, 92, E["chosen"])

    # row 2: challenge flow
    state(100, 300, "CHALLENGE_ROLL")
    state(420, 300, "CHALLENGE_WINDOW", w=210)
    state(760, 300, "WAITING_HERO_ROLL", w=220)
    s.arrow([(740, 166), (740, 236), (525, 236), (525, 300)])
    s.label(625, 262, E["play_hero"])
    s.arrow([(420, 315), (300, 315)])
    s.label(360, 297, E["challenge"])
    s.arrow([(300, 335), (420, 335)])
    s.label(360, 372, E["hero_wins"])
    s.arrow([(200, 300), (200, 196), (716, 196), (716, 166)])
    s.label(200, 238, E["hero_loses"])
    s.arrow([(630, 323), (760, 323)])
    s.label(695, 307, E["timeout"])
    s.arrow([(860, 166), (860, 300)])
    s.label(935, 228, E["use_hero"])
    s.arrow([(980, 323), (1080, 323), (1080, 143), (900, 143)])
    s.label(1085, 250, E["no_target"])

    # row 3: target selection
    sels = [(560, "SELECTING_CARDS"), (765, "SELECTING_HAND_CARDS"), (970, "SELECTING_PLAYER")]
    s.add(f'<polyline points="870,346 870,420" fill="none" stroke="{NAVY}" stroke-width="1.8"/>')
    s.add(f'<polyline points="655,420 1065,420" fill="none" stroke="{NAVY}" stroke-width="1.8"/>')
    for x, n in sels:
        s.arrow([(x + 95, 420), (x + 95, 470)])
        state(x, 470, n, w=190)
    s.label(965, 408, E["needs_target"])
    # back to gameplay through a ghost connector
    for x, _ in sels:
        s.add(f'<polyline points="{x + 95},516 {x + 95},560" fill="none" stroke="{NAVY}" stroke-width="1.8"/>')
    s.add(f'<polyline points="1065,560 655,560" fill="none" stroke="{NAVY}" stroke-width="1.8"/>')
    s.arrow([(655, 560), (520, 560)])
    state(360, 537, "GAMEPLAY", w=160, ghost=True)
    s.label(760, 584, E["confirmed"])

    # unused
    s.text(40, 452, T["unused"], size=12, weight=600, fill=MUTED)
    state(40, 470, "APPLYING_CARD_EFFECTS", w=230, unused=True)
    state(40, 537, "FINISHED", w=150, unused=True)
    return s.render()




# ================================================================ parte 3: Kafka
def kafka_architecture(lang):
    T = {
        "pt": dict(
            title="Arquitetura do Here To Slay com Kafka: clientes passam pelo Nginx até os gateways, e gateway, lobby e engine só conversam por tópicos num cluster de 3 brokers",
            heading="Depois do Kafka: serviços que só conversam por tópicos",
            clients="Clientes", clients_sub="Electron + React",
            nginx_sub="least_conn · porta 8889",
            gw="Gateway ×2", gw_sub="WebSocket ⇄ Kafka",
            cluster="Cluster Kafka · 3 brokers · KRaft",
            cluster_sub="3 partições e 3 réplicas por tópico",
            lobby="Lobby ×2", engine="Engine ×3",
            compact="compactado",
            legend_flow="produz / consome",
            legend_store="persiste o estado e relê no boot",
            note1="Chave = matchId: as ações de uma partida\ncaem na mesma partição, sempre em ordem",
            note2="3 engines no mesmo consumer group:\ncada partição tem um único dono",
            note3="Cada gateway tem um group.id único:\ntodos recebem todas as respostas",
        ),
        "en": dict(
            title="Here To Slay architecture with Kafka: clients go through Nginx to the gateways, and gateway, lobby and engine only talk through topics on a 3-broker cluster",
            heading="After Kafka: services that only talk through topics",
            clients="Clients", clients_sub="Electron + React",
            nginx_sub="least_conn · port 8889",
            gw="Gateway ×2", gw_sub="WebSocket ⇄ Kafka",
            cluster="Kafka cluster · 3 brokers · KRaft",
            cluster_sub="3 partitions and 3 replicas per topic",
            lobby="Lobby ×2", engine="Engine ×3",
            compact="compacted",
            legend_flow="produces / consumes",
            legend_store="persists state, re-read on boot",
            note1="Key = matchId: every action of a match\nlands on the same partition, in order",
            note2="3 engines in one consumer group:\neach partition has a single owner",
            note3="Each gateway has its own group.id:\nall of them receive every response",
        ),
    }[lang]
    s = Svg(1180, 640, T["title"])
    s.text(40, 52, T["heading"], size=22, weight=800)

    # clients and nginx
    s.rect(40, 250, 150, 84, fill=WHITE, stroke=NAVY, sw=1.8)
    s.text(115, 284, T["clients"], size=14, weight=700, anchor="middle")
    s.text(115, 306, T["clients_sub"], size=11.5, fill=MUTED, anchor="middle")
    s.rect(225, 250, 150, 84, fill=WHITE, stroke=NAVY, sw=1.8)
    s.text(300, 284, "Nginx", size=14, weight=700, anchor="middle")
    s.text(300, 306, T["nginx_sub"], size=11, fill=MUTED, anchor="middle")
    s.arrow([(190, 292), (225, 292)])

    # gateways
    s.rect(410, 150, 190, 330, fill=WHITE, stroke=NAVY, sw=1.8, r=18)
    s.text(505, 180, T["gw"], size=14, weight=700, anchor="middle")
    s.text(505, 200, T["gw_sub"], size=11.5, fill=MUTED, anchor="middle")
    for i in range(2):
        s.rect(432, 226 + i * 40, 146, 30, fill=NAVY_SOFT, stroke="none", r=8)
        s.text(505, 246 + i * 40, f"gateway-{i + 1}", size=11.5, weight=600, fill=NAVY, anchor="middle", family=MONO)
    s.arrow([(375, 292), (410, 292)])

    # kafka cluster
    cx, cy, cw, ch = 650, 96, 300, 430
    s.rect(cx, cy, cw, ch, fill=NAVY, stroke="none", r=20)
    s.text(cx + 20, cy + 30, T["cluster"], size=13.5, weight=700, fill=WHITE)
    s.text(cx + 20, cy + 50, T["cluster_sub"], size=11, fill="#c9d1e3")
    for i in range(3):
        s.rect(cx + 20 + i * 90, cy + 64, 80, 26, fill="#3c4d6e", stroke="none", r=8)
        s.text(cx + 60 + i * 90, cy + 82, f"broker-{i + 1}", size=10.5, fill=WHITE, anchor="middle", family=MONO)
    topics = [
        ("lobby-actions-in", 216, False), ("lobby-state-out", 256, False), ("lobby-state-store", 296, True),
        ("game-actions-in", 366, False), ("game-state-out", 406, False), ("match-state-store", 446, True),
    ]
    for name, y, compact in topics:
        s.rect(cx + 20, y - 16, cw - 40, 30, fill=RED_SOFT if compact else WHITE, stroke="none", r=8)
        s.text(cx + 34, y + 4, name, size=11.5, weight=600, fill=RED if compact else NAVY, family=MONO)
        if compact:
            s.text(cx + cw - 30, y + 4, T["compact"], size=10, fill=RED, anchor="end")

    # services
    s.rect(1000, 190, 150, 126, fill=WHITE, stroke=NAVY, sw=1.8, r=18)
    s.text(1075, 248, T["lobby"], size=14, weight=700, anchor="middle")
    s.rect(1000, 340, 150, 126, fill=WHITE, stroke=NAVY, sw=1.8, r=18)
    s.text(1075, 398, T["engine"], size=14, weight=700, anchor="middle")
    s.text(1075, 418, "heretoslay-engine", size=10, fill=MUTED, anchor="middle", family=MONO)

    L, R = cx + 20, cx + cw - 20
    # gateway <-> topics
    s.arrow([(600, 216), (L, 216)])
    s.arrow([(L, 256), (600, 256)])
    s.arrow([(600, 366), (L, 366)])
    s.arrow([(L, 406), (600, 406)])
    # topics <-> services
    s.arrow([(R, 216), (1000, 216)])
    s.arrow([(1000, 256), (R, 256)])
    s.arrow([(1000, 296), (R, 296)], color=RED, dash="5 4")
    s.arrow([(R, 366), (1000, 366)])
    s.arrow([(1000, 406), (R, 406)])
    s.arrow([(1000, 446), (R, 446)], color=RED, dash="5 4")

    # legend + notes
    s.add(f'<polyline points="650,556 690,556" stroke="{NAVY}" stroke-width="1.8" marker-end="url(#arrow-2b3a55)"/>')
    s.text(700, 560, T["legend_flow"], size=11.5, fill=MUTED)
    s.add(f'<polyline points="850,556 890,556" stroke="{RED}" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#arrow-cf3439)"/>')
    s.text(900, 560, T["legend_store"], size=11.5, fill=MUTED)
    for i, key in enumerate(["note1", "note2", "note3"]):
        x = 40 + i * 0
        y = 380 + i * 0
    s.rect(40, 360, 340, 62, fill=WHITE, stroke=LINE, r=12)
    for j, line in enumerate(T["note1"].split("\n")):
        s.text(56, 386 + j * 18, line, size=11.5, fill=INK)
    s.rect(40, 436, 340, 62, fill=WHITE, stroke=LINE, r=12)
    for j, line in enumerate(T["note2"].split("\n")):
        s.text(56, 462 + j * 18, line, size=11.5, fill=INK)
    s.rect(40, 512, 340, 62, fill=WHITE, stroke=LINE, r=12)
    for j, line in enumerate(T["note3"].split("\n")):
        s.text(56, 538 + j * 18, line, size=11.5, fill=INK)
    return s.render()


def kafka_flow(lang):
    T = {
        "pt": dict(
            title="O caminho de uma jogada pelo Kafka e o que acontece quando uma instância da engine cai",
            heading="Uma jogada, e o que acontece quando a engine cai",
            row1="Caminho normal",
            row2="Se a engine B cair no meio da partida",
            steps=[("Jogador", "clica em\n\"jogar carta\""), ("Gateway", "produz com\nchave = matchId"),
                   ("game-actions-in", "partição 2"), ("Engine B", "dona da\npartição 2"),
                   ("game-state-out", "novo estado"), ("Gateways", "repassam para\nos jogadores")],
            persist="snapshot salvo ao criar a partida",
            crash="Engine B cai",
            rebalance="rebalance: a partição 2\npassa para a engine C",
            restore="relê o tópico\ndo início, no boot",
            resume="assume a\npartição 2",
            gap_title="O que ainda falta",
            gap="O snapshot da partida só é salvo\nquando ela começa, e a releitura\naponta para localhost. Para lobbies,\na recuperação funciona.",
        ),
        "en": dict(
            title="The path of a move through Kafka and what happens when an engine instance dies",
            heading="One move, and what happens when the engine dies",
            row1="Normal path",
            row2="If engine B dies mid-match",
            steps=[("Player", "clicks\n\"play card\""), ("Gateway", "produces with\nkey = matchId"),
                   ("game-actions-in", "partition 2"), ("Engine B", "owns\npartition 2"),
                   ("game-state-out", "new state"), ("Gateways", "forward to\nthe players")],
            persist="snapshot saved when the match is created",
            crash="Engine B dies",
            rebalance="rebalance: partition 2\nmoves to engine C",
            restore="re-reads the topic\nfrom the start, on boot",
            resume="takes over\npartition 2",
            gap_title="What is still missing",
            gap="The match snapshot is only saved\nwhen the match starts, and the reload\npoints at localhost. For lobbies,\nrecovery works.",
        ),
    }[lang]
    s = Svg(1180, 560, T["title"])
    s.text(40, 52, T["heading"], size=22, weight=800)
    s.text(40, 96, T["row1"], size=13, weight=600, fill=MUTED)

    w, gap, y = 160, 32, 112
    for i, (name, sub) in enumerate(T["steps"]):
        x = 40 + i * (w + gap)
        topic = name.startswith("game-")
        s.rect(x, y, w, 96, fill=NAVY if topic else WHITE, stroke=NAVY, sw=1.8, r=16)
        s.add(f'<circle cx="{x + 22}" cy="{y + 22}" r="11" fill="{RED}"/>')
        s.text(x + 22, y + 26.5, str(i + 1), size=11.5, weight=700, fill=WHITE, anchor="middle")
        s.text(x + w / 2, y + 48, name, size=12.5 if topic else 14, weight=700, fill=WHITE if topic else INK,
               anchor="middle", family=MONO if topic else FONT)
        for j, line in enumerate(sub.split("\n")):
            s.text(x + w / 2, y + 68 + j * 15, line, size=11, fill="#c9d1e3" if topic else MUTED, anchor="middle")
        if i < len(T["steps"]) - 1:
            s.arrow([(x + w, y + 48), (x + w + gap, y + 48)])

    # persistence from engine B
    ex = 40 + 3 * (w + gap)
    s.rect(ex - 20, 262, w + 40, 46, fill=RED_SOFT, stroke=RED, dash="6 5", r=12)
    s.text(ex + w / 2, 290, "match-state-store", size=12, weight=700, fill=RED, anchor="middle", family=MONO)
    s.arrow([(ex + w / 2, y + 96), (ex + w / 2, 262)], color=RED, dash="5 4")
    s.label(ex + w / 2 + 70, 240, T["persist"], RED, anchor="start")

    # crash row
    s.text(40, 352, T["row2"], size=13, weight=600, fill=MUTED)
    s.rect(40, 372, 200, 96, fill=SOFT, stroke=MUTED, dash="6 5", r=16)
    s.text(140, 418, T["crash"], size=14, weight=700, fill=MUTED, anchor="middle")
    s.add(f'<path d="M120,436 l40,20 M160,436 l-40,20" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')
    s.rect(560, 372, 200, 96, fill=WHITE, stroke=NAVY, sw=1.8, r=16)
    s.text(660, 412, "Engine C", size=14, weight=700, anchor="middle")
    for j, line in enumerate(T["resume"].split("\n")):
        s.text(660, 434 + j * 15, line, size=11, fill=MUTED, anchor="middle")
    s.arrow([(240, 420), (560, 420)])
    s.label(400, 404, T["rebalance"])
    s.arrow([(ex + w / 2, 308), (ex + w / 2, 340), (660, 340), (660, 372)], color=RED, dash="5 4")
    s.label(705, 330, T["restore"], RED, anchor="start")
    s.rect(820, 372, 320, 120, fill=RED_SOFT, stroke=RED, r=16)
    s.text(840, 398, T["gap_title"], size=13, weight=700, fill=RED)
    for j, line in enumerate(T["gap"].split("\n")):
        s.text(840, 420 + j * 17, line, size=11.5, fill=INK)
    return s.render()


# ================================================================ parte 4: Kafka Streams
def streams_topology(lang):
    T = {
        "pt": dict(
            title="Topologia do serviço de monitoramento com Kafka Streams: lê as ações e os estados das partidas e só produz alertas",
            heading="Monitoramento: só lê, nunca escreve de volta",
            reads="lê",
            app="Serviço monitoring · Kafka Streams",
            app_sub='application.id = "heretoslay-monitoring" · stores em memória',
            g1="Sem estado", g1_sub="filter + map",
            g2="Janelas de tempo (DSL)", g2_sub="groupByKey + windowedBy + count",
            g3="Processor API + state store", g3_sub="estado próprio por partida ou jogador",
            items1=["Generous Soul"],
            items2=["Foco de ataque · 30 s", "Efeito em cadeia · 35 s", "Focusing / Focused · 2 min", "Combo · 6 s"],
            items3=["Histórico (últimas 25)", "Reviravolta de sorte (Allen)", "Frequent Buyer", "RNG Diff", "First Blood"],
            alerts="game-monitoring-alerts",
            gw="Gateway", gw_sub="repassa por WebSocket",
            ui=["toast", "badge por 20 s", "painel de histórico"],
            engine="Engine",
            engine_sub="joga a partida normalmente",
        ),
        "en": dict(
            title="Topology of the Kafka Streams monitoring service: it reads match actions and states and only produces alerts",
            heading="Monitoring: it only reads, never writes back",
            reads="reads",
            app="monitoring service · Kafka Streams",
            app_sub='application.id = "heretoslay-monitoring" · in-memory stores',
            g1="Stateless", g1_sub="filter + map",
            g2="Time windows (DSL)", g2_sub="groupByKey + windowedBy + count",
            g3="Processor API + state store", g3_sub="its own state per match or player",
            items1=["Generous Soul"],
            items2=["Attack focus · 30 s", "Chain effect · 35 s", "Focusing / Focused · 2 min", "Combo · 6 s"],
            items3=["History (last 25)", "Luck turnaround (Allen)", "Frequent Buyer", "RNG Diff", "First Blood"],
            alerts="game-monitoring-alerts",
            gw="Gateway", gw_sub="forwards over WebSocket",
            ui=["toast", "20 s badge", "history panel"],
            engine="Engine",
            engine_sub="plays the match as usual",
        ),
    }[lang]
    s = Svg(1180, 600, T["title"])
    s.text(40, 52, T["heading"], size=22, weight=800)

    # input topics + engine
    s.rect(40, 96, 220, 70, fill=WHITE, stroke=NAVY, sw=1.8, r=16)
    s.text(150, 126, T["engine"], size=14, weight=700, anchor="middle")
    s.text(150, 146, T["engine_sub"], size=11, fill=MUTED, anchor="middle")
    for i, name in enumerate(["game-actions-in", "game-state-out"]):
        y = 220 + i * 70
        s.rect(40, y, 220, 44, fill=NAVY, stroke="none", r=12)
        s.text(150, y + 27, name, size=12, weight=700, fill=WHITE, anchor="middle", family=MONO)
    s.arrow([(150, 166), (150, 220)], color=MUTED, dash="4 4")

    # streams app
    ax, ay, aw, ah = 320, 96, 560, 470
    s.rect(ax, ay, aw, ah, fill=WHITE, stroke=NAVY, sw=1.8, r=20)
    s.text(ax + 24, ay + 32, T["app"], size=15, weight=700)
    s.text(ax + 24, ay + 52, T["app_sub"], size=11, fill=MUTED, family=MONO)
    s.arrow([(260, 242), (ax, 242)])
    s.arrow([(260, 312), (ax, 312)])
    s.label(290, 228, T["reads"])

    groups = [
        (T["g1"], T["g1_sub"], T["items1"], ax + 24, ay + 76, 160),
        (T["g2"], T["g2_sub"], T["items2"], ax + 24, ay + 186, 245),
        (T["g3"], T["g3_sub"], T["items3"], ax + 290, ay + 76, 245),
    ]
    for title, sub, items, gx, gy, gw in groups:
        h = 58 + 34 * len(items)
        s.rect(gx, gy, gw, h, fill=SOFT, stroke="none", r=14)
        s.text(gx + 14, gy + 24, title, size=12.5, weight=700, fill=NAVY)
        s.text(gx + 14, gy + 42, sub, size=10.5, fill=MUTED, family=MONO)
        for j, it in enumerate(items):
            s.rect(gx + 12, gy + 54 + j * 34, gw - 24, 28, fill=WHITE, stroke="none", r=8)
            s.text(gx + 24, gy + 72 + j * 34, it, size=11.5, weight=500, fill=INK)

    # alerts topic -> gateway -> ui
    s.rect(930, 220, 210, 44, fill=RED, stroke="none", r=12)
    s.text(1035, 247, T["alerts"], size=11.5, weight=700, fill=WHITE, anchor="middle", family=MONO)
    s.arrow([(ax + aw, 242), (930, 242)], color=RED)
    s.rect(930, 320, 210, 70, fill=WHITE, stroke=NAVY, sw=1.8, r=16)
    s.text(1035, 350, T["gw"], size=14, weight=700, anchor="middle")
    s.text(1035, 370, T["gw_sub"], size=11, fill=MUTED, anchor="middle")
    s.arrow([(1035, 264), (1035, 320)], color=RED)
    for j, u in enumerate(T["ui"]):
        s.rect(950, 420 + j * 40, 170, 30, fill=RED_SOFT, stroke="none", r=10)
        s.text(1035, 440 + j * 40, u, size=11.5, weight=600, fill=RED, anchor="middle")
    s.arrow([(1035, 390), (1035, 420)], color=RED)
    return s.render()


def allen_relations(lang):
    T = {
        "pt": dict(
            title="As 13 relações da álgebra de Allen entre dois intervalos A e B, destacando as que disparam o alerta de reviravolta de sorte",
            heading="Álgebra de Allen: como dois intervalos se relacionam",
            sub="A = sequência que acabou de fechar · B = sequência ainda aberta de um rival",
            fires="dispara o alerta (os intervalos se sobrepõem)",
            quiet="não dispara (um vem antes do outro)",
        ),
        "en": dict(
            title="The 13 Allen interval algebra relations between two intervals A and B, highlighting the ones that trigger the luck turnaround alert",
            heading="Allen's interval algebra: how two intervals relate",
            sub="A = the streak that just closed · B = a rival's streak that is still open",
            fires="triggers the alert (the intervals overlap)",
            quiet="doesn't trigger (one comes before the other)",
        ),
    }[lang]
    rel = [  # name, A(start,end), B(start,end)  on a 0..10 scale
        ("BEFORE", (0, 3), (5, 9)), ("MEETS", (0, 4), (4, 9)), ("OVERLAPS", (0, 6), (3, 9)),
        ("STARTS", (2, 5), (2, 9)), ("DURING", (3, 6), (1, 9)), ("FINISHES", (5, 9), (1, 9)),
        ("EQUALS", (2, 8), (2, 8)), ("FINISHED_BY", (1, 9), (5, 9)), ("CONTAINS", (1, 9), (3, 6)),
        ("STARTED_BY", (2, 9), (2, 5)), ("OVERLAPPED_BY", (3, 9), (0, 6)), ("MET_BY", (4, 9), (0, 4)),
        ("AFTER", (5, 9), (0, 3)),
    ]
    quiet = {"BEFORE", "MEETS", "MET_BY", "AFTER"}
    s = Svg(1180, 510, T["title"])
    s.text(40, 52, T["heading"], size=22, weight=800)
    s.text(40, 78, T["sub"], size=12.5, fill=MUTED)
    cols, cw, chh = 5, 212, 118
    for i, (name, a, b) in enumerate(rel):
        col, row = i % cols, i // cols
        x, y = 40 + col * (cw + 10), 100 + row * (chh + 12)
        is_quiet = name in quiet
        s.rect(x, y, cw, chh, fill=WHITE if not is_quiet else SOFT, stroke=NAVY if not is_quiet else LINE, r=14,
               sw=1.6 if not is_quiet else 1.2)
        s.text(x + 14, y + 26, name, size=12, weight=700, fill=NAVY if not is_quiet else MUTED, family=MONO)
        scale = (cw - 60) / 10
        for k, (lab, (st, en)) in enumerate((("A", a), ("B", b))):
            by = y + 46 + k * 30
            s.text(x + 16, by + 13, lab, size=11, weight=700, fill=MUTED)
            color = (RED if lab == "A" else NAVY) if not is_quiet else MUTED
            s.rect(x + 34 + st * scale, by, (en - st) * scale, 18, fill=color, stroke="none", r=6)
    # legend
    lx, ly = 40 + 3 * (cw + 10), 100 + 2 * (chh + 12)
    s.rect(lx, ly, 2 * cw + 10, chh, fill=WHITE, stroke=LINE, r=14)
    s.rect(lx + 18, ly + 30, 34, 16, fill=WHITE, stroke=NAVY, r=5, sw=1.6)
    s.text(lx + 64, ly + 43, T["fires"], size=12, fill=INK)
    s.rect(lx + 18, ly + 70, 34, 16, fill=SOFT, stroke=LINE, r=5)
    s.text(lx + 64, ly + 83, T["quiet"], size=12, fill=MUTED)
    return s.render()


PART = sys.argv[2] if len(sys.argv) > 2 else "2"
for lang in ("pt", "en"):
    if PART == "2":
        (OUT / f"arquitetura.{lang}.svg").write_text(architecture(lang), encoding="utf-8")
        (OUT / f"classes.{lang}.svg").write_text(classes(lang), encoding="utf-8")
        (OUT / f"estados.{lang}.svg").write_text(states(lang), encoding="utf-8")
    elif PART == "4":
        (OUT / f"streams-topologia.{lang}.svg").write_text(streams_topology(lang), encoding="utf-8")
        (OUT / f"allen.{lang}.svg").write_text(allen_relations(lang), encoding="utf-8")
    else:
        (OUT / f"kafka-arquitetura.{lang}.svg").write_text(kafka_architecture(lang), encoding="utf-8")
        (OUT / f"kafka-jogada.{lang}.svg").write_text(kafka_flow(lang), encoding="utf-8")
print("ok")
