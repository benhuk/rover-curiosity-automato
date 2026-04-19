# Rover Curiosity — Simulador de Autômato

**Trabalho 1 — Linguagens Formais e Autômatos 2026.1**  
UTFPR — Campus Ponta Grossa  
Professor: Gleifer Vaz Alves

## Autores

- [benhuk](https://github.com/benhuk)
- [Gabriele0p](https://github.com/Gabriele0p)

---

## Descrição

Simulador visual de autômato finito determinístico (AFD) baseado na missão de coleta de amostras do Rover Curiosity em Marte.

O autômato modela o ciclo completo de uma missão de coleta, desde o recebimento do objetivo até a conclusão ou abandono da missão, com 18 estados e 24 transições.

---

## Requisitos

- Python 3.10+
- pygame-ce
- automata-lib

---

## Instalação

```bash
python -m venv venv
source venv/bin/activate
pip install pygame-ce automata-lib
```

---

## Execução

```bash
# Simulador visual interativo
python rover_pygame.py

# Versão texto com testes automáticos
python rover_automato.py
```

---

## Autômato

**Tupla:** M = (Q, Σ, δ, q0, F)

- **Estado inicial:** Q0
- **Estados finais:** Q15 (missão concluída), Q17 (abortado)
- **Total de estados:** 18
- **Total de transições:** 24

### Estados

| Estado | Descrição |
|--------|-----------|
| Q0 | Ocioso |
| Q1 | Missão recebida |
| Q2 | Navegando |
| Q3 | Desvio de obstáculo |
| Q4 | Área alvo |
| Q5 | Analisando terreno |
| Q6 | Terreno aprovado |
| Q7 | Terreno reprovado |
| Q8 | Posicionando |
| Q9 | Alinhado |
| Q10 | Preparando braço |
| Q11 | Braço pronto |
| Q12 | Coletando |
| Q13 | Validando amostra |
| Q14 | Armazenando |
| Q15 | Missão concluída *(final)* |
| Q16 | Falha |
| Q17 | Abortado *(final)* |

### Alfabeto

| Símbolo | Evento |
|---------|--------|
| A | objetivo — novo objetivo de coleta recebido |
| B | rota_ok — rota calculada e livre de obstáculos |
| C | obstaculo — obstáculo detectado no trajeto |
| D | terreno_seguro — solo seguro para coleta |
| E | terreno_inseguro — solo inadequado para coleta |
| F | alinhado — posicionamento confirmado |
| G | braco_pronto — braço robótico operacional |
| H | coleta_ok — etapa de coleta executada |
| I | coleta_falha — amostra inválida |
| J | armazenado — amostra armazenada |
| K | aborta — cancelamento da missão |
| L | reset — reinicialização do rover |

---

## Exemplos de fitas

### Aceitas

| Fita | Descrição |
|------|-----------|
| `ABBDDFFGGHHHJ` | Missão concluída sem obstáculos |
| `ABCBBDDFFGGHHHJ` | Missão com desvio de obstáculo |
| `AK` | Missão abortada logo após receber objetivo |
| `ABBDEK` | Terreno reprovado e aborto |
| `ABBDDFFGGHHILABBDDFFGGHHHJ` | Falha na coleta, reset e nova missão concluída |

### Rejeitadas

| Fita | Motivo |
|------|--------|
| `ABB` | Para em Q4 — estado não final |
| `ABD` | Sem transição em (Q2, D) |
| `ABBDDFFGGHHH` | Para em Q14 — estado não final |
| `AKL` | Sem transição em (Q17, L) |