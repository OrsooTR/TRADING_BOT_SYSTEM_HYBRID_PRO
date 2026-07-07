---
title: "SSRN 1734526 - Entropy Theory, Momentum and Reversal"
type: academic_source
topic:
  - behavioral_finance
  - entropy
  - momentum
  - reversal
  - volume
status: integrated
source_pdf: "../../assets/pdfs/academic/ssrn-1734526.pdf"
---

# SSRN 1734526 - Entropy Theory, Momentum and Reversal

## Identita fonte

Paper: *The Entropy Theory of Mind and Behavioral Finance*.

Autore: Jing Chen.

Tema: teoria dell'entropia applicata al giudizio degli investitori, alla formazione dei prezzi, al volume e al ciclo momentum/reversal.

## Idea centrale

Gli investitori non processano informazione nello stesso momento e con la stessa qualita. Gli investitori piu informati agiscono prima, mentre gli investitori meno informati reagiscono piu tardi a prezzo, news e segnali semplici. Questo produce un ciclo osservabile:

1. accumulo informato;
2. momentum visibile;
3. ingresso tardivo dei meno informati;
4. reversal e ritorno verso equilibrio.

## Punti teorici rilevanti

### 1. Informazione costosa

L'informazione utile ha un costo. Gli investitori piu grandi possono sostenere costi maggiori e quindi reagire prima a informazioni meno visibili.

Implicazione: volume e prezzo non sono solo output casuali, ma tracce del modo in cui gruppi diversi processano informazione.

### 2. Valore del giudizio

Il paper collega giudizio soggettivo, allocazione di portafoglio e rendimento atteso. In forma operativa, se un investitore stima una probabilita `q` di esito positivo e la volatilita/binario payoff e `d`, la quota rischiosa ottimale e proporzionale a:

`x = (2q - 1) / d`

Implicazione: quando il giudizio cambia, cambia la posizione desiderata; il cambio di posizione genera volume.

### 3. Volume come misura del cambio di giudizio

La variazione di giudizio determina la variazione di holding, quindi il volume. Questo e rilevante per strategie che combinano momentum, volume e reversal.

### 4. Momentum lifecycle

Il paper formalizza quattro fasi:

| Fase | Prezzo | Volume | Interpretazione |
|------|--------|--------|-----------------|
| Low volume winner | sale | basso | informati entrano presto |
| High volume winner | sale | alto | momentum diventa pubblico |
| High volume loser | scende o rallenta | alto | ritardatari comprano mentre informati vendono |
| Low volume loser | scende | basso | esaurimento e ritorno a equilibrio |

### 5. Strategia implicita

Il segnale non e "comprare momentum" in modo cieco. Il punto operativo e distinguere momentum giovane da momentum maturo:

- momentum con volume crescente ma non eccessivo puo continuare;
- momentum con volume estremo e deterioramento del rendimento puo anticipare reversal;
- high volume loser e fase di rischio massimo per inseguire il prezzo.

## Concetto backtestabile generato

- [[../../03_STRATEGIES/IDEAS/momentum_volume_lifecycle]]

## Regole operative da importare

- Ogni strategia momentum deve includere un filtro volume.
- Separare momentum giovane e momentum maturo.
- Testare reversal dopo volume anomalo e perdita di accelerazione.
- Non usare il solo rendimento passato come segnale completo.

## Collegamenti

- [[INDEX]]
- [[../../03_STRATEGIES/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../13_PDF_LIBRARY/academic_sources]]
