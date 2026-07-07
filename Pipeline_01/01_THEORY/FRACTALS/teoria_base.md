# Frattali - Teoria Base

## Collegamenti
- [[INDEX]]
- [[pattern_library]]
- [[pythagoras_document_analysis]]
- [[../FFT/teoria_base]]
- [[../../03_STRATEGIES/IDEAS/fractal_fft_pattern_projection]]

## Idea centrale
Il mercato puo essere letto come insieme di strutture autosimili che si ripetono a scale temporali diverse.

Nel contesto del progetto questo significa:
- non osservare solo il prezzo
- osservare forma, durata, ampiezza, inclinazione e curvatura
- cercare pattern semplici e pattern composti

## Proprieta utili per il bot
- autosimilarita tra asset e timeframe
- strutture annidate: un pattern piu grande puo contenere pattern minori
- trasferibilita parziale: la forma puo restare simile anche se cambiano tempo e volatilita
- sensibilita alla finestra temporale: la stessa struttura puo apparire diversa se osservata con un range sbagliato

## Range di candele emersi dal materiale Pythagoras
- 3-6 candele: pattern semplici
- 6-12 candele
- 12-24 candele
- 24-39 candele
- 39-56 candele

Oltre 6 candele il documento tende a parlare di frattali complessi, cioe strutture composte da pezzi di frattali minori.

## Variabili strutturali
Un pattern non va trattato come sagoma rigida.

Le variabili operative da tracciare sono:
- numero di candele
- direzione prevalente
- ampiezza relativa
- inclinazione
- curvatura
- distanza tra swing principali
- velocita di sviluppo

## Cosa tenere e cosa no
Da tenere:
- visione multiscala
- relazione stretta tra pattern e timeframe
- idea di libreria di pattern
- distinzione tra pattern semplice e complesso

Da non trattare come base scientifica del bot:
- linguaggio metafisico su coscienza e anima
- equivalenze forti tra fisica quantistica e trading
- affermazioni predittive non validate statisticamente

## Traduzione tecnica minima
Per rendere il concetto frattale testabile servono:
- normalizzazione della finestra
- estrazione di pivot o swing
- rappresentazione canonica del pattern
- metrica di similarita
- scoring di match
- regola di proiezione e invalidazione

## Nota metodologica
Nel vault il termine "consapevolezza" va tradotto in variabili misurabili:
- volatilita dell'asset
- qualita del match
- qualita del contesto
- robustezza multi-timeframe
- allineamento con risk management
