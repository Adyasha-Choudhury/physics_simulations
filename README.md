# 🔌 Transmission Line Reflection & Smith Chart Simulator

A web-based interactive tool for analyzing transmission line reflections, VSWR, and Smith Chart visualization with λ/4 impedance matching.

## 🌟 Features

- **Reflection Coefficient Analysis**: Visualize |Γ| vs frequency before and after matching
- **VSWR Calculation**: Compare Voltage Standing Wave Ratio with and without λ/4 transformer
- **Smith Chart Visualization**: Interactive Smith chart showing impedance transformation
- **λ/4 Impedance Matching**: Automatic quarter-wave transformer design
- **Customizable Parameters**: 
  - Center frequency (GHz)
  - Characteristic impedance Z₀
  - Load impedance (resistive and reactive components)
  - Relative permittivity (εᵣ) for different dielectric materials
  - Transmission line length (meters or fraction of λ)

## 🚀 Live Demo

Access the live app here: 

## 📋 How to Use

1. **Set Center Frequency**: Enter your operating frequency in GHz
2. **Define Line Parameters**: 
   - Characteristic impedance (typically 50Ω or 75Ω)
   - Relative permittivity (1.0 for air, ~2.1 for PTFE, ~4.5 for FR4)
3. **Specify Load Impedance**: Enter resistive (RL) and reactive (XL) components
4. **Choose Line Length**: Input as meters or fraction of wavelength
5. **Analyze Results**: View reflection coefficient, VSWR, and Smith chart plots

## 🛠️ Common Material Parameters

| Material | Relative Permittivity (εᵣ) |
|----------|---------------------------|
| Air/Vacuum | 1.0 |
| PTFE (Teflon) | 2.1 |
| Polyethylene | 2.3 |
| FR4 (PCB) | 4.3 - 4.5 |
| Alumina | 9.8 |

## 💻 Run Locally

To run this application on your local machine:

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/transmission-line-simulator.git
cd transmission-line-simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📚 Technical Background

### Reflection Coefficient (Γ)
The reflection coefficient represents the ratio of reflected to incident wave:
```
Γ = (ZL - Z0) / (ZL + Z0)
```

### VSWR (Voltage Standing Wave Ratio)
VSWR quantifies impedance mismatch:
```
VSWR = (1 + |Γ|) / (1 - |Γ|)
```

### λ/4 Transformer
A quarter-wave transformer matches impedances using:
```
Zt = √(Z0 × |ZL|)
```

## 🔧 Technologies Used

- **Streamlit**: Web application framework
- **scikit-rf**: RF and microwave engineering toolkit
- **NumPy**: Numerical computations
- **Matplotlib**: Data visualization

## 📖 Applications

- RF circuit design and analysis
- Antenna matching network design
- Microwave engineering education
- Transmission line impedance matching
- PCB transmission line analysis

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Your Name
- GitHub: [@Adyasha-Choudhury](https://github.com/Adyasha-Choudhury)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- RF calculations powered by [scikit-rf](https://scikit-rf.readthedocs.io/)

---

**Note**: For educational and research purposes. Always verify results with practical measurements for critical applications.
