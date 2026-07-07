# 11. Compendio formule essenziali

## Differenze discrete

$$
dP_t = P_t - P_{t-1}
$$

$$
d^2P_t = dP_t - dP_{t-1}
$$

## FFT / IFFT

$$
X_k = \sum_{n=0}^{N-1} x_n e^{-i2\pi kn/N}
$$

$$
x_n = \frac{1}{N}\sum_{k=0}^{N-1} X_k e^{i2\pi kn/N}
$$

## Fourier continua

$$
X(\omega) = \int_{-\infty}^{\infty} x(t)e^{-i\omega t}dt
$$

$$
x(t) = \frac{1}{2\pi}\int_{-\infty}^{\infty} X(\omega)e^{i\omega t}d\omega
$$

## Convoluzione

$$
(x * h)(t) = \int_{-\infty}^{\infty} x(\tau)h(t-\tau)d\tau
$$

## Parseval

$$
\int |x(t)|^2 dt = \frac{1}{2\pi} \int |X(\omega)|^2 d\omega
$$

## Funzione caratteristica

$$
\phi_X(u) = E[e^{iuX}]
$$

## Black-Scholes call

$$
C = S_0N(d_1) - Ke^{-rT}N(d_2)
$$

$$
d_1 = \frac{\ln(S_0/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}
$$

$$
d_2 = d_1 - \sigma\sqrt{T}
$$

## Butterworth

$$
|H(\omega)|^2 = \frac{1}{1 + (\omega/\omega_c)^{2n}}
$$

## Wiener-Kolmogorov

$$
\hat\xi = \Omega_\xi(\Omega_\xi + \Omega_\eta)^{-1}y
$$

$$
\hat\eta = \Omega_\eta(\Omega_\xi + \Omega_\eta)^{-1}y
$$

## Drawdown

$$
DD_t = \frac{\max_{s\le t}V_s - V_t}{\max_{s\le t}V_s}
$$

## Sharpe semplificato

$$
Sharpe = \frac{\overline{r-r_f}}{\sigma(r-r_f)}
$$

## Expectancy

$$
E = p\cdot \overline{win} - (1-p)\cdot \overline{loss}
$$
