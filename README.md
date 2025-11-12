# Spectrophotometer_CL399

# OD600 Sensor Calibration and Comparison

This project compares **optical density (OD600)** readings from actual spectrophotometric measurements with values recorded by the **AS7341** light sensor (and optionally TSL2591). It includes error analysis and visualizations to assess the performance of low-cost sensors for OD600 measurement.

## 📊 Features

- Line plot comparison of Actual OD600 vs AS7341 readings
- ±25% error bars for AS7341 measurements
- Optional support for TSL2591 sensor data
- Ideal line `y = x` for reference
- Visualization of sensor accuracy and trends

## 📁 Files

- `od600_comparison.py`: Main Python script for plotting and visualization
- `README.md`: Project documentation

## 🔧 Requirements

- Python 3.6+
- Libraries:
  - `matplotlib`
  - `numpy`

Install requirements with:

```bash
pip install matplotlib numpy
```

## 🚀 How to Run

1. Clone the repository or download the files.
2. Make sure your data is defined in the script or loaded from CSV.
3. Run the Python script:

```bash
python od600_comparison.py
```

This will display a plot comparing Actual OD600 and AS7341 values, with error bars.

## 📈 Sample Data Used

| S.No | Actual OD600 | AS7341 |
|------|--------------|--------|
| 2    | 0.014        | 0.012  |
| 3    | 0.062        | 0.056  |
| 4    | 0.609        | 0.598  |
| 5    | 0.647        | 0.602  |
| 6    | 0.854        | 0.957  |

## 📌 Notes

- AS7341 errors are assumed to be ±25% of the measured value.
- TSL2591 data can also be integrated by adding a similar array and plotting it.
- Sample 1 is excluded due to near-zero or invalid measurements.

## 📷 Example Output

![image](https://github.com/user-attachments/assets/b8cd8b2e-33ed-4f8e-97c4-0cbef26fe76e)
