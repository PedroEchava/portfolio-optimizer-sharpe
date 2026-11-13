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

---

### Proyecto 3: Análisis Financiero y de Valoración Corporativa (Alpina / SIMEV)
*Crea un repositorio llamado `corporate-valuation-alpina` (o similar), añade un archivo `README.md` y pega lo siguiente:*

```markdown
# Corporate Valuation & Financial Statement Analysis (Alpina S.A.S.)

![Finance](https://img.shields.io/badge/Corporate-Finance-blue.svg)
![Valuation](https://img.shields.io/badge/Valuation-DCF%20%2F%2520Ratios-orange.svg)
![Regulation](https://img.shields.io/badge/Regulator-SIMEV%2FRNVE-green.svg)

A rigorous corporate finance case study and fundamental valuation model focused on Alpina Productos Alimenticios S.A. Extracted multi-year audited financial statements directly from regulatory filings (Superintendencia Financiera de Colombia / SIMEV & RNVE portals) to execute comprehensive financial statement analysis.

---

## Key Components
* **Data Extraction & Regulatory Research:** Navigated the SIMEV and Registro Nacional de Valores y Emisores (RNVE) portals to gather official historical balance sheets, income statements, and cash flow reports.
* **Financial Statement Analysis:** Computed core liquidity, leverage, efficiency, and profitability ratios across multiple fiscal years.
* **Valuation Frameworks:** Developed fundamental valuation metrics to assess capital structure, debt sustainability, and operational performance.
* **Strategic Insights:** Evaluated competitive positioning and market drivers within the Latin American consumer goods and food processing sector.

---

## Deliverables & Structure
* `financial_model.xlsx` / Python scripts used for ratio computations.
* `Valuation_Report.pdf`: Comprehensive analytical report detailing fundamental findings and strategic recommendations.
