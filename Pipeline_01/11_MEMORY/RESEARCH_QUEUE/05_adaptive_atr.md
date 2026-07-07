# Adaptive ATR

## Priorità
P0

## Idea
L'ATR classico misura la volatilità media.
La versione adattiva prova a renderlo più sensibile ai cambi di regime, così stop loss e take profit non restano fissi quando il mercato cambia ritmo.

## Perché è utile nel progetto
Hai già strategie che usano stop multipli di ATR. Un ATR più intelligente può migliorare:
- dimensione dello stop
- filtro di ingresso
- distanza del take profit
- confronto tra mercati diversi

## Ipotesi di ricerca
- L'ATR adattivo migliora la robustezza.
- I periodi di alta volatilità richiedono stop più larghi.
- I periodi di bassa volatilità richiedono stop più stretti.

## Come testarla
1. Confrontare ATR classico vs ATR adattivo.
2. Verificare impatto su drawdown e reward/risk.
3. Misurare miglioramento per regime.

## Rischi
- Stop troppo instabili.
- Eccessiva sensibilità ai spike.

## Criterio di utilità
Valido se rende il sistema più coerente con la volatilità reale del mercato.
