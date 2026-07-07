# Pattern Library Frattale

## Collegamenti
- [[INDEX]]
- [[teoria_base]]
- [[pythagoras_document_analysis]]
- [[../../03_STRATEGIES/IDEAS/fractal_fft_pattern_projection]]
- [[../../04_BACKTEST/FFT_tests/template_test]]

## Obiettivo
Formalizzare una libreria di pattern frattali utile per:
- matching storico
- confronto tra asset
- proiezioni future
- backtest riproducibili

## Unita minima di pattern
Ogni pattern candidato dovrebbe avere almeno:
- `pattern_id`
- `range_candele`
- `pivot_count`
- `shape_vector`
- `ampiezza_relativa`
- `durata_relativa`
- `slope`
- `curvature`
- `entry_zone`
- `target_zone`
- `invalidazione`

## Range iniziali da usare
- `R1 = 3-6`
- `R2 = 6-12`
- `R3 = 12-24`
- `R4 = 24-39`
- `R5 = 39-56`

## Trasformazioni ammesse
Il materiale Pythagoras suggerisce che un pattern possa mantenere identita strutturale pur cambiando forma.

Trasformazioni da supportare:
- traslazione verticale
- traslazione temporale
- scaling in ampiezza
- scaling temporale
- inversione verticale
- lieve deformazione di slope
- lieve deformazione di curvature

## Scoring di similarita
Una prima metrica puo combinare:
- similarita dei pivot normalizzati
- similarita della durata relativa
- similarita della curvatura
- errore tra segmenti ricostruiti
- conferma di FFT dominante
- conferma di `d1` e `d2`

## Uso nel bot
La libreria non dovrebbe generare da sola un ordine.

Dovrebbe produrre:
- `pattern_match_score`
- `pattern_direction`
- `pattern_target_zone`
- `pattern_time_horizon`
- `pattern_complexity`
- `scenario_count`

## Estensione geometrica dal Fractal Circular Indicator
Per i pattern che usano geometria circolare o ellittica conviene aggiungere:
- `time_nodes`
- `center_axis`
- `circle_family`
- `ellipse_family`
- `diagonal_set`
- `fib_levels`
- `geometric_confluence_score`
- `reaction_zone_map`

Questa estensione serve a trasformare una lettura visiva in feature misurabili del `Pattern Layer`.

## Rischi
- overfitting visivo
- cherry picking dei pattern
- finestre scelte a posteriori
- eccesso di discrezionalita sui pivot
- confusione tra somiglianza grafica e edge statistico

## Definition of done minima
- almeno 1 pattern semplice formalizzato
- almeno 1 pattern complesso scomposto in sottopattern
- procedura di normalizzazione documentata
- procedura di match documentata
- test IS/OOS su almeno un asset
