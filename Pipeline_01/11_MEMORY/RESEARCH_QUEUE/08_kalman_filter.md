# Kalman Filter

## Priorità
P1

## Idea
Il filtro di Kalman serve a stimare uno stato nascosto partendo da osservazioni rumorose.
Nel trading può essere utile per stimare trend, slope e stato latente del mercato in modo più stabile.

## Perché è utile nel progetto
Il progetto già lavora con smoothing, derivata e ciclo.
Kalman può diventare un filtro di supporto per:
- trend estimate
- denoising
- state tracking
- anticipazione di cambi di regime

## Rischi
- Modello troppo rigido.
- Parametri sensibili.
- Falsa sensazione di precisione.

## Criterio di utilità
Serve se riesce a ridurre il rumore senza cancellare i movimenti utili.
