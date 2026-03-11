# Physics & Computational Analysis

Data analysis and computational modelling scripts developed across undergraduate physics laboratory work and coursework at the University of Toronto. All experimental data was collected first-hand through laboratory instrumentation.

## Contents

### Signal Processing and Time Series Analysis (`signal-processing-and-time-series-analysis.ipynb`)
A Jupyter notebook covering four independent computational analyses:
- Custom discrete convolution implementation benchmarked against NumPy across array sizes spanning three orders of magnitude
- Gaussian smoothing applied to a synthetic seismic waveform to simulate source-time function effects
- RL circuit impulse and step response modelled via convolution with a discretized analytical impulse response
- Atmospheric methane (CH₄) time series decomposed using both manual polynomial + harmonic regression and statsmodels, with out-of-sample forecasting evaluated by RMSE over 2020–2024

### Hall Effect (`constant_magnetic_field.py`)
Weighted linear regression of Hall voltage versus current across three magnetic field strengths (482, 780, 1071 mT). Includes residual plots and reduced chi-squared analysis to assess goodness of fit.

### Pendulum: Period vs. Initial Angle (`initial_angle.py`)
Models the dependence of pendulum period on amplitude using a symmetric quadratic fit. Derives period from zero-crossing detection across 14 trials, compares small-angle constant model against the full finite-angle correction, and quantifies asymmetry via a weighted linear slope.

### Pendulum: Period vs. String Length (`varied_length.py`)
Fits measured periods across five string lengths to the theoretical prediction T = (2π/√g)√(L+D), where D accounts for the distance from the attachment point to the centre of mass. Compares the best-fit slope against the theoretical value and evaluates residuals.

### Millikan Oil Drop (`millikan.py`)
Processes position-tracking CSV files for 50 oil droplets to compute terminal velocities, droplet radii, volumes, masses, and charges. Estimates the number of elementary charges per droplet using measured stopping voltages.

### Capacitor Discharge (`capacitor.py`)
Fits exponential decay curves to capacitor voltage data from two sources (cursor-selected and oscilloscope-imported), extracting the RC time constant in each case. Computes reduced chi-squared and plots residuals.

### Diode Characterization (`diode.py`)
Models diode current–voltage behaviour using the Shockley diode equation for forward-biased operation and a linear model for reverse bias. Fits are evaluated separately for positive and negative voltage regions with chi-squared analysis.

### Electron Charge-to-Mass Ratio (`electron_charge.py`)
Fits measured electron beam radii to a theoretical model under constant-current and constant-voltage conditions to extract the charge-to-mass ratio (e/m). Tests multiple model variants including horizontal and vertical offset corrections.

### CO₂ and Temperature Analysis (`co2_temperature_analysis.py`)
Fits a logarithmic relationship between atmospheric CO₂ concentration and surface temperature anomaly across historical data (1000–1995). Compares pre-industrial and industrial periods, identifies the decade of significant divergence, and predicts the temperature change expected from a doubling of CO₂.

### Simple Harmonic Oscillator — Statistical Mechanics (`SHO.py`)
Computes the multiplicity distribution for energy quanta shared between two Einstein solids and fits a Gaussian to the resulting probability distribution, verifying the approach to equilibrium in a large coupled system.

## Tools & Libraries
Python, NumPy, Pandas, Matplotlib, SciPy, statsmodels, seaborn

## Notes
Raw data files are not included in this repository. Scripts are shared to demonstrate analytical methodology, error analysis practices, and computational approach.
