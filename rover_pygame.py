import pygame
import sys
import math
import random
from automata.fa.dfa import DFA


dfa = DFA(
    states={
        'Q0','Q1','Q2','Q3','Q4','Q5','Q6','Q7',
        'Q8','Q9','Q10','Q11','Q12','Q13','Q14','Q15','Q16','Q17'
    },
    input_symbols={'A','B','C','D','E','F','G','H','I','J','K','L'},
    transitions={
        'Q0' : {'A': 'Q1'},
        'Q1' : {'B': 'Q2',  'K': 'Q17'},
        'Q2' : {'B': 'Q4',  'C': 'Q3'},
        'Q3' : {'B': 'Q2',  'K': 'Q17'},
        'Q4' : {'D': 'Q5'},
        'Q5' : {'D': 'Q6',  'E': 'Q7'},
        'Q6' : {'F': 'Q8'},
        'Q7' : {'K': 'Q17', 'L': 'Q0'},
        'Q8' : {'F': 'Q9'},
        'Q9' : {'G': 'Q10'},
        'Q10': {'G': 'Q11'},
        'Q11': {'H': 'Q12', 'K': 'Q17'},
        'Q12': {'H': 'Q13'},
        'Q13': {'H': 'Q14', 'I': 'Q16'},
        'Q14': {'J': 'Q15'},
        'Q15': {},
        'Q16': {'L': 'Q0',  'K': 'Q17'},
        'Q17': {},
    },
    initial_state='Q0',
    final_states={'Q15', 'Q17'},
    allow_partial=True
)

def trans_disp(estado):
    return dfa.transitions.get(estado, {})

def prox_estado(estado, simbolo):
    return dfa.transitions.get(estado, {}).get(simbolo, None)

def e_final(estado):
    return estado in dfa.final_states

pygame.init()

W, H = 1100, 740
tela = pygame.display.set_mode((W, H))
pygame.display.set_caption("Rover Curiosity — Simulador de Automato")

def font(size, bold=False):
    for nome in ["Arial","Liberation Sans","DejaVu Sans","FreeSans"]:
        try: return pygame.font.SysFont(nome, size, bold=bold)
        except: pass
    return pygame.font.SysFont(None, size, bold=bold)

F_TITLE = font(24, bold=True)
F_HEAD  = font(14, bold=True)
F_BODY  = font(13)
F_SMALL = font(11)
F_BTN   = font(12, bold=True)
F_MONO  = pygame.font.SysFont("monospace", 11)

C = {
    'bg'        : (14,  16,  28),
    'sky_top'   : (8,   14,  48),
    'sky_bot'   : (28,  42,  88),
    'ground'    : (118, 56,  14),
    'ground_hi' : (158, 83,  28),
    'ground_sh' : (78,  36,  6),
    'panel'     : (18,  21,  38),
    'card'      : (24,  27,  48),
    'card_brd'  : (48,  53,  82),
    'accent'    : (70,  140, 255),
    'accent_dk' : (28,  68,  168),
    'green'     : (48,  198, 138),
    'green_dk'  : (22,  118, 78),
    'red'       : (228, 68,  68),
    'red_dk'    : (138, 33,  33),
    'yellow'    : (238, 188, 58),
    'yellow_dk' : (158, 118, 18),
    'white'     : (228, 233, 255),
    'gray'      : (138, 143, 168),
    'gray_dk'   : (58,  63,  88),
    'muted'     : (78,  83,  113),
}

ESTADOS = {
    'Q0' : ('ocioso',           C['gray']),
    'Q1' : ('missao recebida',  C['accent']),
    'Q2' : ('navegando',        C['accent']),
    'Q3' : ('desvio',           C['yellow']),
    'Q4' : ('area alvo',        C['accent']),
    'Q5' : ('analis. terreno',  C['accent']),
    'Q6' : ('terr. aprovado',   C['green']),
    'Q7' : ('terr. reprovado',  C['red']),
    'Q8' : ('posicionando',     C['green']),
    'Q9' : ('alinhado',         C['green']),
    'Q10': ('prep. braco',      C['accent']),
    'Q11': ('braco pronto',     C['green']),
    'Q12': ('coletando',        C['accent']),
    'Q13': ('valid. amostra',   C['accent']),
    'Q14': ('armazenando',      C['accent']),
    'Q15': ('missao concluida', C['green']),
    'Q16': ('falha',            C['red']),
    'Q17': ('abortado',         C['yellow']),
}

SIMBOLOS = {
    'A': 'objetivo',  'B': 'rota_ok',    'C': 'obstaculo',
    'D': 'terr_ok',   'E': 'terr_fail',  'F': 'alinhado',
    'G': 'braco_ok',  'H': 'coleta_ok',  'I': 'coleta_fail',
    'J': 'armazenado','K': 'aborta',     'L': 'reset',
}

DESC_SIMBOLO = {
    'A': 'Novo objetivo de coleta recebido',
    'B': 'Rota calculada e livre de obstaculos',
    'C': 'Obstaculo detectado no trajeto',
    'D': 'Solo seguro para coleta',
    'E': 'Solo inadequado para coleta',
    'F': 'Posicionamento do rover confirmado',
    'G': 'Braco robotico operacional',
    'H': 'Etapa de coleta executada',
    'I': 'Amostra coletada invalida',
    'J': 'Amostra armazenada no rover',
    'K': 'Comando de cancelamento da missao',
    'L': 'Reinicializacao do rover',
}

COR_SIMBOLO = {
    'A': C['accent'], 'B': C['green'],  'C': C['yellow'],
    'D': C['green'],  'E': C['red'],    'F': C['green'],
    'G': C['green'],  'H': C['accent'], 'I': C['red'],
    'J': C['green'],  'K': C['red'],    'L': C['yellow'],
}

MARCOS = {
    'Q1' : ('Missao recebida',     C['accent']),
    'Q2' : ('Navegando',           C['accent']),
    'Q3' : ('Desviando obstaculo', C['yellow']),
    'Q4' : ('Area alvo alcancada', C['accent']),
    'Q5' : ('Analisando terreno',  C['accent']),
    'Q6' : ('Terreno aprovado',    C['green']),
    'Q7' : ('Terreno reprovado',   C['red']),
    'Q8' : ('Posicionando rover',  C['green']),
    'Q9' : ('Rover alinhado',      C['green']),
    'Q10': ('Preparando braco',    C['accent']),
    'Q11': ('Braco pronto',        C['green']),
    'Q12': ('Coletando amostra',   C['accent']),
    'Q13': ('Validando amostra',   C['accent']),
    'Q14': ('Armazenando',         C['accent']),
    'Q15': ('MISSAO CONCLUIDA',    C['green']),
    'Q16': ('FALHA NA COLETA',     C['red']),
    'Q17': ('MISSAO ABORTADA',     C['yellow']),
}

# --- Estado do simulador ---
estado_atual  = 'Q0'
historico     = []
trace         = []
trace_scroll  = 0
marcos_log    = []
log_scroll    = 0
rover_x       = 90.0
rover_x_alvo  = 90.0
fita_texto    = ""
fita_ativa    = False
fita_msg      = ""
fita_msg_cor  = C['gray']
resultado     = ""
tempo         = 0.0


fila_simbolos  = []
fila_timer     = 0.0
FILA_DELAY     = 3.0   
executando     = False


eventos_visuais = []

# Layout
CENA_H   = 240
ESTADO_Y = CENA_H
ESTADO_H = 72
PAINEL_Y = ESTADO_Y + ESTADO_H
PAINEL_H = 190
CTRL_Y   = PAINEL_Y + PAINEL_H
CTRL_H   = 42
FITA_Y   = CTRL_Y + CTRL_H
FITA_H   = 40
BTN_Y    = FITA_Y + FITA_H
BTN_H    = H - BTN_Y

rect_input    = pygame.Rect(65,  FITA_Y+5, 660, 30)
rect_executar = pygame.Rect(732, FITA_Y+5, 118, 30)
rect_limpar   = pygame.Rect(856, FITA_Y+5, 95,  30)
btn_resetar   = pygame.Rect(W-242, CTRL_Y+5, 112, 32)
btn_desfazer  = pygame.Rect(W-124, CTRL_Y+5, 112, 32)

TRACE_CARD  = pygame.Rect(12,  PAINEL_Y+8, int(W*0.52), PAINEL_H-16)
LOG_CARD_X  = TRACE_CARD.right + 10
LOG_CARD_W  = W - LOG_CARD_X - 12
LOG_CARD    = pygame.Rect(LOG_CARD_X, PAINEL_Y+8, LOG_CARD_W, PAINEL_H-16)
LINHA_H     = 16
TRACE_INNER_Y = PAINEL_Y + 8 + 30
LOG_INNER_Y   = PAINEL_Y + 8 + 30
TRACE_ROWS  = (PAINEL_H - 16 - 32) // LINHA_H
LOG_ROWS    = (PAINEL_H - 16 - 32) // LINHA_H

def pos_rover(q):
    m = {'Q0':90,'Q1':165,'Q2':248,'Q3':195,'Q4':340,'Q5':420,
         'Q6':505,'Q7':368,'Q8':588,'Q9':648,'Q10':705,'Q11':762,
         'Q12':820,'Q13':870,'Q14':920,'Q15':978,'Q16':730,'Q17':628}
    return m.get(q, 90)

def round_rect(surf, color, rect, r=8, border=0, bcolor=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if border and bcolor:
        pygame.draw.rect(surf, bcolor, rect, width=border, border_radius=r)

def draw_btn(surf, rect, txt, bg, brd, tcol=None):
    if tcol is None: tcol = C['white']
    round_rect(surf, bg, rect, 8, 1, brd)
    t = F_BTN.render(txt, True, tcol)
    surf.blit(t, (rect.centerx-t.get_width()//2, rect.centery-t.get_height()//2))

def desenhar_cena(surf, rx, t):
    # Gradiente céu
    for i in range(CENA_H-44):
        frac = i / (CENA_H-44)
        r = int(C['sky_top'][0]+(C['sky_bot'][0]-C['sky_top'][0])*frac)
        g = int(C['sky_top'][1]+(C['sky_bot'][1]-C['sky_top'][1])*frac)
        b = int(C['sky_top'][2]+(C['sky_bot'][2]-C['sky_top'][2])*frac)
        pygame.draw.line(surf, (r,g,b), (0,i), (W,i))

    for i,(sx,sy) in enumerate([(55,14),(145,28),(238,9),(345,33),(465,5),(595,21),
             (705,13),(795,30),(875,7),(965,25),(1055,17),(28,43),(178,53),
             (312,38),(445,48),(582,36),(722,44),(852,32),(982,48),(1082,40)]):
        bri = 140 + int(55*math.sin(t*1.4 + i*0.75))
        pygame.draw.circle(surf,(bri,bri,min(255,bri+25)),(sx,sy),1)

    pygame.draw.circle(surf,(178,78,38),(W-115,52),36)
    pygame.draw.circle(surf,(198,98,53),(W-123,44),26)
    pygame.draw.circle(surf,(155,58,22),(W-105,62),16)


    bx = 30

    pygame.draw.rect(surf, (80,90,110), (bx+18, CENA_H-95, 10, 58))

    pygame.draw.line(surf,(150,160,180),(bx+23,CENA_H-95),(bx+5, CENA_H-115),2)
    pygame.draw.line(surf,(150,160,180),(bx+23,CENA_H-95),(bx+40,CENA_H-112),2)
    pygame.draw.ellipse(surf,(60,70,95),(bx+2,CENA_H-118,22,10))
    pygame.draw.ellipse(surf,(80,95,120),(bx+3,CENA_H-117,20,8))

    pulse = int(200+55*math.sin(t*4))
    pygame.draw.circle(surf,(pulse,pulse,50),(bx+23,CENA_H-95),3)

    pygame.draw.rect(surf,(55,60,80),(bx, CENA_H-42, 55, 28), border_radius=4)
    pygame.draw.rect(surf,(65,72,95),(bx+2,CENA_H-40,51,24), border_radius=3)

    pygame.draw.rect(surf,(30,80,140),(bx+8,CENA_H-36,14,12), border_radius=2)
    pygame.draw.rect(surf,(50,120,200),(bx+9,CENA_H-35,12,10), border_radius=2)

    pygame.draw.rect(surf,(35,60,155),(bx+28,CENA_H-52,24,8), border_radius=2)
    pygame.draw.rect(surf,(50,85,180),(bx+29,CENA_H-51,22,6), border_radius=2)

    tbase = F_SMALL.render("BASE", True, (120,130,160))
    surf.blit(tbase,(bx+10, CENA_H-16))


    pygame.draw.rect(surf,C['ground_sh'],(0,CENA_H-46,W,46))
    pygame.draw.rect(surf,C['ground'],   (0,CENA_H-40,W,40))
    pygame.draw.rect(surf,C['ground_hi'],(0,CENA_H-40,W,5))


    for px2,py2,pw,ph in [(140,CENA_H-42,26,11),(310,CENA_H-40,18,8),
                           (480,CENA_H-43,30,13),(660,CENA_H-41,20,9),
                           (840,CENA_H-42,28,12),(1010,CENA_H-40,22,10)]:
        pygame.draw.ellipse(surf,(82,38,7),(px2,py2,pw,ph))
        pygame.draw.ellipse(surf,(102,53,16),(px2+2,py2+2,pw-4,ph-4))


    for tx in range(95, int(rx)-5, 22):
        pygame.draw.ellipse(surf,(88,43,9),(tx,CENA_H-22,8,4))
        pygame.draw.ellipse(surf,(88,43,9),(tx+4,CENA_H-24,8,4))


    rix, riy = int(rx), CENA_H-58


    s = pygame.Surface((62,14),pygame.SRCALPHA)
    pygame.draw.ellipse(s,(0,0,0,55),(0,0,62,14))
    surf.blit(s,(rix-31,riy+40))

    for wx in [rix-22,rix-7,rix+8]:
        pygame.draw.circle(surf,(52,56,70),(wx,riy+38),11)
        pygame.draw.circle(surf,(33,36,48),(wx,riy+38),8)
        pygame.draw.circle(surf,(88,93,108),(wx,riy+38),3)
    pygame.draw.rect(surf,(98,103,118),(rix-24,riy+34,46,4),border_radius=2)

    pygame.draw.rect(surf,(128,133,153),(rix-24,riy+10,48,26),border_radius=5)
    pygame.draw.rect(surf,(172,178,198),(rix-22,riy+11,44,22),border_radius=4)
    pygame.draw.rect(surf,(192,198,215),(rix-20,riy+12,40,10),border_radius=3)

    pygame.draw.rect(surf,(22,48,128),(rix-32,riy,64,12),border_radius=3)
    pygame.draw.rect(surf,(42,82,172),(rix-30,riy+1,60,9),border_radius=2)
    for dx in range(-18,24,9):
        pygame.draw.line(surf,(18,36,98),(rix+dx,riy),(rix+dx,riy+12),1)

    pygame.draw.line(surf,(182,188,208),(rix+8,riy+10),(rix+16,riy-12),2)
    ap = int(178+62*math.sin(t*3))
    pygame.draw.circle(surf,(ap,ap,48),(rix+16,riy-12),4)
    pygame.draw.circle(surf,(min(255,ap+30),min(255,ap+30),80),(rix+16,riy-12),2)

    if estado_atual in ('Q8','Q9','Q10','Q11','Q12','Q13','Q14','Q15'):
        pygame.draw.line(surf,(148,153,173),(rix+24,riy+18),(rix+40,riy+30),3)
        pygame.draw.line(surf,(128,133,153),(rix+40,riy+30),(rix+40,riy+40),2)
        tc = C['yellow'] if estado_atual in ('Q12','Q13') else (98,103,123)
        pygame.draw.circle(surf,tc,(rix+40,riy+40),5)

    nome_e,cor_e = ESTADOS[estado_atual]
    lbl = F_SMALL.render(estado_atual, True, cor_e)
    lb = pygame.Rect(rix-lbl.get_width()//2-4, riy-34, lbl.get_width()+8,16)
    s2 = pygame.Surface((lb.w,lb.h),pygame.SRCALPHA)
    s2.fill((0,0,0,148))
    surf.blit(s2,lb.topleft)
    surf.blit(lbl,(rix-lbl.get_width()//2, riy-33))

# --- Eventos visuais ---
def disparar_evento(letra, rx):
    cor = COR_SIMBOLO.get(letra, C['white'])
    desc = DESC_SIMBOLO.get(letra, "")
    parts = []
    for _ in range(22):
        ang = random.uniform(0, math.pi*2)
        spd = random.uniform(22, 65)
        parts.append({'x':float(rx),'y':float(CENA_H-62),
                      'vx':math.cos(ang)*spd,'vy':math.sin(ang)*spd-38,
                      'r':random.randint(2,5),'vida':1.2})
    eventos_visuais.append({'letra':letra,'desc':desc,'cor':cor,
                             'x':rx,'vida':2.8,'vida_max':2.8,'parts':parts})

def atualizar_eventos(dt):
    for ev in eventos_visuais[:]:
        ev['vida'] -= dt
        if ev['vida'] <= 0:
            eventos_visuais.remove(ev); continue
        for p in ev['parts']:
            p['x']  += p['vx']*dt
            p['y']  += p['vy']*dt
            p['vy'] += 85*dt
            p['vida'] -= dt

def desenhar_eventos(surf):
    for ev in eventos_visuais:
        frac = max(0, ev['vida']/ev['vida_max'])
        cor = ev['cor']
        # Partículas
        for p in ev['parts']:
            if p['vida'] > 0:
                c2 = tuple(min(255, int(v*0.6+70)) for v in cor)
                pygame.draw.circle(surf,c2,(int(p['x']),int(p['y'])),p['r'])
        # Notificação — posicionada logo acima do rover, não sobrepõe texto
        px = max(10, min(W-230, int(ev['x'])-115))
        py = max(5, int(CENA_H-110 - (1-frac)*20))
        sw, sh = 220, 40
        s = pygame.Surface((sw,sh),pygame.SRCALPHA)
        bg_a = int(frac*190)
        pygame.draw.rect(s,(*cor,bg_a//4),(0,0,sw,sh),border_radius=8)
        pygame.draw.rect(s,(*cor,bg_a),(0,0,sw,sh),width=1,border_radius=8)
        surf.blit(s,(px,py))
        # Letra
        tl = F_HEAD.render(ev['letra'], True, cor)
        surf.blit(tl,(px+8, py+4))
        # Separador
        pygame.draw.line(surf,(*cor,100),(px+26,py+6),(px+26,py+32),1)
        # Descrição em até 2 linhas
        desc = ev['desc']
        if len(desc) > 28:
            td1 = F_SMALL.render(desc[:28], True, C['white'])
            td2 = F_SMALL.render(desc[28:], True, C['white'])
            surf.blit(td1,(px+32, py+6))
            surf.blit(td2,(px+32, py+20))
        else:
            td = F_SMALL.render(desc, True, C['white'])
            surf.blit(td,(px+32, py+13))

# --- Botões ---
class Botao:
    def __init__(self, letra, x, y, w=80, h=52):
        self.letra = letra
        self.rect  = pygame.Rect(x, y, w, h)
        self.ativo = False
        self.hover = False
    def update(self, mp): self.hover = self.rect.collidepoint(mp)
    def desenhar(self, surf):
        if self.ativo:
            bg  = C['accent_dk'] if self.hover else (20,52,138)
            brd = C['accent']; cl = C['white']; ce = (168,198,255)
        else:
            bg  = (26,28,46) if self.hover else C['card']
            brd = C['card_brd']; cl = (72,78,108); ce = (52,58,82)
        round_rect(surf,bg,self.rect,10,1,brd)
        tl = F_HEAD.render(self.letra, True, cl)
        te = F_SMALL.render(SIMBOLOS[self.letra][:10], True, ce)
        surf.blit(tl,(self.rect.centerx-tl.get_width()//2, self.rect.y+7))
        surf.blit(te,(self.rect.centerx-te.get_width()//2, self.rect.y+28))
    def clicado(self, pos): return self.ativo and self.rect.collidepoint(pos)

botoes = []
BW,BH,GAP = 82,52,5
bx0 = (W-(6*(BW+GAP)-GAP))//2
by0 = BTN_Y+8
for i,letra in enumerate(SIMBOLOS.keys()):
    botoes.append(Botao(letra, bx0+(i%6)*(BW+GAP), by0+(i//6)*(BH+GAP)))

def atualizar_botoes():
    disp = trans_disp(estado_atual)
    for b in botoes: b.ativo = b.letra in disp

def processar(letra):
    global estado_atual, rover_x_alvo, resultado
    p = prox_estado(estado_atual, letra)
    if p is None: return False
    linha = f"({estado_atual}, {letra}: {SIMBOLOS[letra]})  =>  {p}"
    historico.append(estado_atual)
    trace.append(linha)
    estado_atual = p
    rover_x_alvo = pos_rover(p)
    if p in MARCOS: marcos_log.append(MARCOS[p])
    atualizar_botoes()
    resultado = ""
    disparar_evento(letra, rover_x_alvo)
    return True

def checar_resultado():
    global resultado
    if not trace: resultado = ""; return
    resultado = "ACEITA" if e_final(estado_atual) else "NAO_ACEITA"

def parsear_fita(txt):
    tokens = txt.strip().upper().split()
    if all(t in SIMBOLOS for t in tokens): return tokens
    chars = txt.strip().upper().replace(" ","")
    if all(c in SIMBOLOS for c in chars): return list(chars)
    return tokens

def iniciar_fila(txt):
    global fila_simbolos, fila_timer, executando, fita_msg, fita_msg_cor
    simbolos = parsear_fita(txt)
    if not simbolos:
        fita_msg = "fita vazia"; fita_msg_cor = C['yellow']; return
    # Valida tudo antes de começar
    estado_teste = estado_atual
    for s in simbolos:
        if s not in SIMBOLOS:
            fita_msg = f"simbolo '{s}' invalido"; fita_msg_cor = C['red']; return
    resetar()
    fila_simbolos  = list(simbolos)
    fila_timer     = 0.0
    executando     = True
    fita_msg       = f"executando {len(simbolos)} simbolos..."
    fita_msg_cor   = C['accent']

def resetar():
    global estado_atual,rover_x_alvo,historico,trace,trace_scroll
    global marcos_log,log_scroll,fita_msg,fita_msg_cor,resultado
    global fila_simbolos,fila_timer,executando
    estado_atual  = 'Q0'; rover_x_alvo = pos_rover('Q0')
    historico=[]; trace=[]; trace_scroll=0
    marcos_log=[]; log_scroll=0
    fita_msg=""; fita_msg_cor=C['gray']; resultado=""
    fila_simbolos=[]; fila_timer=0.0; executando=False
    atualizar_botoes()

def desfazer():
    global estado_atual,rover_x_alvo,trace_scroll,resultado,executando
    if executando: return
    if not historico: return
    trace.pop()
    if marcos_log and estado_atual in MARCOS: marcos_log.pop()
    estado_atual = historico.pop()
    rover_x_alvo = pos_rover(estado_atual)
    trace_scroll = max(0,trace_scroll-1)
    resultado = ""
    atualizar_botoes()

def draw_scrollable(surf, card_rect, title, lines, scroll, line_h, cor_last=None):
    """Desenha um card com conteúdo scrollável."""
    round_rect(surf, C['card'], card_rect, 10, 1, C['card_brd'])
    # Título
    surf.blit(F_HEAD.render(title, True, C['muted']), (card_rect.x+12, card_rect.y+10))
    pygame.draw.line(surf, C['card_brd'],
                     (card_rect.x+12, card_rect.y+28),
                     (card_rect.right-12, card_rect.y+28), 1)
    # Área de conteúdo
    inner_y = card_rect.y+34
    rows_vis = (card_rect.height-40) // line_h
    visible = lines[scroll: scroll+rows_vis]
    for i, (txt, cor) in enumerate(visible):
        use_cor = cor if cor else C['muted']
        if i == len(visible)-1 and cor_last:
            use_cor = cor_last
        t = F_MONO.render(txt[:68], True, use_cor)
        surf.blit(t, (card_rect.x+12, inner_y+i*line_h))
    # Scrollbar
    total = len(lines)
    if total > rows_vis:
        sb_h  = max(20, int(card_rect.height * rows_vis / total))
        sb_y  = card_rect.y + 34 + int((card_rect.height-40-sb_h) * scroll / max(1,total-rows_vis))
        pygame.draw.rect(surf, C['gray_dk'],
                         (card_rect.right-8, card_rect.y+34, 4, card_rect.height-40), border_radius=2)
        pygame.draw.rect(surf, C['gray'],
                         (card_rect.right-8, sb_y, 4, sb_h), border_radius=2)
    # Contador
    if total > 0:
        ct = F_SMALL.render(f"{total}", True, C['gray_dk'])
        surf.blit(ct, (card_rect.right-ct.get_width()-14, card_rect.y+10))

clock = pygame.time.Clock()
atualizar_botoes()
mpos = (0,0)

while True:
    dt = clock.tick(60)/1000.0
    tempo += dt
    atualizar_eventos(dt)

    # Fila de execução com delay
    if executando and fila_simbolos:
        fila_timer += dt
        if fila_timer >= FILA_DELAY:
            fila_timer = 0.0
            s = fila_simbolos.pop(0)
            if s not in SIMBOLOS:
                fita_msg = f"simbolo '{s}' invalido"
                fita_msg_cor = C['red']
                executando = False
                checar_resultado()
            elif not processar(s):
                fita_msg = f"sem transicao: ({estado_atual}, {s})"
                fita_msg_cor = C['red']
                executando = False
                checar_resultado()
            elif not fila_simbolos:
                executando = False
                fita_msg = "fita concluida"
                fita_msg_cor = C['green']
                checar_resultado()

    diff = rover_x_alvo - rover_x
    rover_x += diff*min(1.0,7*dt) if abs(diff)>0.5 else diff

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
        if ev.type == pygame.MOUSEMOTION: mpos = ev.pos
        if ev.type == pygame.MOUSEBUTTONDOWN:
            p = ev.pos
            fita_ativa = rect_input.collidepoint(p)
            if rect_executar.collidepoint(p): iniciar_fila(fita_texto)
            if rect_limpar.collidepoint(p):   fita_texto=""; fita_ativa=True
            for b in botoes:
                if b.clicado(p) and not executando:
                    processar(b.letra); checar_resultado()
            if btn_resetar.collidepoint(p):  resetar()
            if btn_desfazer.collidepoint(p): desfazer()
        if ev.type == pygame.MOUSEWHEEL:
            mp = mpos
            if TRACE_CARD.collidepoint(mp):
                rows = (PAINEL_H-16-34)//LINHA_H
                trace_scroll = max(0, min(trace_scroll-ev.y, max(0,len(trace)-rows)))
            if LOG_CARD.collidepoint(mp):
                rows = (PAINEL_H-16-34)//LINHA_H
                log_scroll = max(0, min(log_scroll-ev.y, max(0,len(marcos_log)-rows)))
        if ev.type == pygame.KEYDOWN:
            if fita_ativa:
                ctrl = pygame.key.get_mods() & pygame.KMOD_CTRL
                if ev.key == pygame.K_RETURN:
                    iniciar_fila(fita_texto); fita_ativa=False
                elif ev.key == pygame.K_ESCAPE:  fita_ativa=False
                elif ev.key == pygame.K_BACKSPACE:
                    if ctrl:
                        ps = fita_texto.rstrip().rsplit(' ',1)
                        fita_texto = ps[0] if len(ps)>1 else ""
                    else: fita_texto=fita_texto[:-1]
                elif ctrl and ev.key==pygame.K_c:
                    try: pygame.scrap.init(); pygame.scrap.put(pygame.SCRAP_TEXT,fita_texto.encode())
                    except: pass
                elif ctrl and ev.key==pygame.K_x:
                    try: pygame.scrap.init(); pygame.scrap.put(pygame.SCRAP_TEXT,fita_texto.encode()); fita_texto=""
                    except: pass
                elif ctrl and ev.key==pygame.K_v:
                    try:
                        pygame.scrap.init()
                        d = pygame.scrap.get(pygame.SCRAP_TEXT)
                        if d: fita_texto += d.decode('utf-8',errors='ignore').replace('\x00','').strip()
                    except: pass
                elif not ctrl: fita_texto += ev.unicode
            else:
                if not executando:
                    l = ev.unicode.upper()
                    if l in SIMBOLOS: processar(l); checar_resultado()
                if ev.key==pygame.K_r: resetar()
                if ev.key==pygame.K_z: desfazer()

    for b in botoes: b.update(mpos)

    # =========================================================================
    # DESENHO
    # =========================================================================
    tela.fill(C['bg'])
    desenhar_cena(tela, rover_x, tempo)
    desenhar_eventos(tela)

    # Barra de progresso da fila
    if executando and fila_simbolos:
        total_orig = len(trace) + len(fila_simbolos)
        prog = len(trace) / max(1, total_orig)
        pygame.draw.rect(tela, C['gray_dk'], (0, CENA_H-4, W, 4))
        pygame.draw.rect(tela, C['accent'],  (0, CENA_H-4, int(W*prog), 4))

    # --- Painel estado ---
    pygame.draw.rect(tela, C['panel'], (0,ESTADO_Y,W,ESTADO_H))
    pygame.draw.line(tela, C['card_brd'], (0,ESTADO_Y),(W,ESTADO_Y),1)
    pygame.draw.line(tela, C['card_brd'], (0,ESTADO_Y+ESTADO_H),(W,ESTADO_Y+ESTADO_H),1)

    nome_e,cor_e = ESTADOS[estado_atual]
    tela.blit(F_TITLE.render(f"{estado_atual}   {nome_e}", True, cor_e),(18,ESTADO_Y+8))

    # Badge resultado
    if resultado=="ACEITA":
        rtxt = "PALAVRA ACEITA — missao concluida!" if estado_atual=='Q15' else "PALAVRA ACEITA — missao abortada"
        rb,rbrd = (C['green_dk'],C['green']) if estado_atual=='Q15' else ((100,78,8),C['yellow'])
    elif resultado=="NAO_ACEITA" or (not trans_disp(estado_atual) and trace and not executando):
        rtxt,rb,rbrd = "PALAVRA NAO ACEITA — estado nao final",C['red_dk'],C['red']
    elif executando:
        restante = len(fila_simbolos)
        rtxt,rb,rbrd = f"executando... {restante} simbolo(s) restante(s)",C['accent_dk'],C['accent']
    else:
        rtxt,rb,rbrd = "em execucao...",C['gray_dk'],C['card_brd']

    rs = F_BODY.render(rtxt, True, C['white'])
    rr = pygame.Rect(18,ESTADO_Y+38,rs.get_width()+18,22)
    round_rect(tela,rb,rr,6,1,rbrd)
    tela.blit(rs,(rr.x+9,rr.y+4))

    hint = "R=resetar  Z=desfazer  Enter=executar fita  delay=3s entre simbolos"
    tela.blit(F_SMALL.render(hint,True,C['muted']),(18,ESTADO_Y+ESTADO_H-14))

    # --- Painel central ---
    pygame.draw.rect(tela, C['panel'], (0,PAINEL_Y,W,PAINEL_H))

    # Trace scrollável
    trace_lines = [(l, C['green'] if i==len(trace)-1 else C['muted']) for i,l in enumerate(trace)]
    draw_scrollable(tela, TRACE_CARD, "TRACE DE EXECUCAO", trace_lines, trace_scroll, LINHA_H)

    # Log da missão scrollável
    log_lines = [(txt, cor) for txt,cor in marcos_log]
    draw_scrollable(tela, LOG_CARD, "LOG DA MISSAO", log_lines, log_scroll, LINHA_H+2, cor_last=None)

    # --- Controles ---
    pygame.draw.rect(tela, C['panel'], (0,CTRL_Y,W,CTRL_H))
    pygame.draw.line(tela, C['card_brd'], (0,CTRL_Y),(W,CTRL_Y),1)

    tela.blit(F_SMALL.render("Disponiveis:", True, C['muted']),(16,CTRL_Y+14))
    for i,l in enumerate(trans_disp(estado_atual).keys()):
        r2 = pygame.Rect(108+i*38, CTRL_Y+7, 32, 24)
        round_rect(tela,C['accent_dk'],r2,6,1,C['accent'])
        t2 = F_BTN.render(l, True, C['white'])
        tela.blit(t2,(r2.centerx-t2.get_width()//2, r2.centery-t2.get_height()//2))

    draw_btn(tela, btn_resetar,  "Resetar  (R)",  C['gray_dk'], C['card_brd'])
    draw_btn(tela, btn_desfazer, "Desfazer (Z)",  C['gray_dk'], C['card_brd'])

    # --- Campo fita ---
    pygame.draw.rect(tela, C['panel'], (0,FITA_Y,W,FITA_H))
    pygame.draw.line(tela, C['card_brd'], (0,FITA_Y),(W,FITA_Y),1)

    tela.blit(F_SMALL.render("Fita:", True, C['muted']),(16,FITA_Y+11))
    brd_i = C['accent'] if fita_ativa else C['card_brd']
    round_rect(tela, C['card'], rect_input, 7, 2, brd_i)
    ti = F_BODY.render(fita_texto+("_" if fita_ativa and int(tempo*2)%2==0 else ""), True, C['white'])
    tela.blit(ti,(rect_input.x+9, rect_input.centery-ti.get_height()//2))
    draw_btn(tela, rect_executar, "Executar", C['accent_dk'], C['accent'])
    draw_btn(tela, rect_limpar,   "Limpar",   C['gray_dk'],   C['card_brd'])
    if fita_msg:
        tela.blit(F_SMALL.render(fita_msg, True, fita_msg_cor),(16,FITA_Y+FITA_H-12))

    # --- Botões ---
    pygame.draw.rect(tela, C['panel'], (0,BTN_Y,W,BTN_H))
    pygame.draw.line(tela, C['card_brd'], (0,BTN_Y),(W,BTN_Y),1)
    for b in botoes: b.desenhar(tela)

    pygame.display.flip()