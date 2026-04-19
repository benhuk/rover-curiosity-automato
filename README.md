# Rover Curiosity — Simulador de Autômato

Trabalho 1 — Linguagens Formais e Autômatos 2026.1  
UTFPR — Campus Ponta Grossa

## Descrição

Simulador visual de autômato finito determinístico (AFD) baseado na missão 
de coleta de amostras do Rover Curiosity em Marte.

## Requisitos

- Python 3.10+
- pygame-ce
- automata-lib

## Instalação

```bash
python -m venv venv
source venv/bin/activate
pip install pygame-ce automata-lib
```

## Execução

```bash
# Simulador visual
python rover_pygame.py

# Versão texto com testes
python rover_automato.py
```

## Alfabeto

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

## Exemplo de fita aceita
ABBDDFFGGHHHJJ
