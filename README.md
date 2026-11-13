# Quantitative Portfolio Optimization & Sharpe Ratio Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Quant](https://img.shields.io/badge/Quantitative-Finance-green.svg)
![Risk Management](https://img.shields.io/badge/Optimization-Markowitz-orange.svg)

A quantitative portfolio optimization engine designed to balance risk and return metrics using historical market data and Modern Portfolio Theory (MPT). The system computes the Efficient Frontier, maximizes the Sharpe Ratio, and determines optimal asset allocation weights.

---

## Key Features
* **Data Retrieval & Processing:** Pulls multi-year historical adjusted close prices for major equity baskets using Python/RStudio data pipelines.
* **Efficient Frontier Simulation:** Monte Carlo simulations to model thousands of random portfolio weight combinations and map the risk-return spectrum.
* **Sharpe Ratio Maximization:** Optimization algorithms (Scipy / base stats) to identify the tangent portfolio offering the highest risk-adjusted return.
* **Risk Analytics:** Computes annualized volatility, expected portfolio return, and individual asset covariance matrices.

## Tech Stack
* **Language:** Python / RStudio
* **Mathematical Libraries:** `NumPy`, `SciPy`, `Pandas`
* **Visualization:** `Matplotlib` / `Seaborn`

---

## How to Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/TU-USUARIO/portfolio-optimizer-sharpe.git](https://github.com/TU-USUARIO/portfolio-optimizer-sharpe.git)
   cd portfolio-optimizer-sharpe

2. Install dependencies:
   ```bash
    pip install -r requirements.txt

3. Run Optimization Script:
    ```bash
    python optimize.py
