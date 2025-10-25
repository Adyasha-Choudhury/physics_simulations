import skrf as rf
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("🔌 Transmission Line Reflection & Smith Chart Simulator with λ/4 Matching")
st.subheader("simulation designed by - Adyasha Choudhury")
st.sidebar.header("Input Parameters")

# --- 1. USER INPUTS ---
fc = st.sidebar.number_input("Center frequency (GHz)", min_value=0.1, max_value=100.0, value=2.4, step=0.1)
Z0 = st.sidebar.number_input("Characteristic impedance Z0 (Ω)", min_value=1.0, max_value=500.0, value=50.0, step=1.0)

# Add relative permittivity input
er = st.sidebar.number_input("Relative permittivity εᵣ", min_value=1.0, max_value=20.0, value=1.0, step=0.1,
                              help="εᵣ = 1 for air/vacuum, ~2.1 for PTFE, ~4.5 for FR4")

RL = st.sidebar.number_input("Resistive part of load RL (Ω)", min_value=0.1, max_value=1000.0, value=75.0, step=1.0)
XL = st.sidebar.number_input("Reactive part of load XL (Ω)", min_value=-500.0, max_value=500.0, value=50.0, step=1.0, 
                              help="+ve for inductive, -ve for capacitive")

vp = 3e8 / np.sqrt(er)  # phase velocity (m/s)
lambda_c = vp / (fc * 1e9)
st.sidebar.info(f"At {fc} GHz with εᵣ = {er:.2f}:\n- Phase velocity = {vp:.3e} m/s\n- Wavelength λ = {lambda_c:.4e} m")

choice = st.sidebar.radio("Line length input method:", ["Length in meters", "Fraction of λ"])

if choice == "Length in meters":
    length = st.sidebar.number_input("Line length (meters)", min_value=0.0001, max_value=10.0, value=lambda_c/4, format="%.6f")
else:
    fraction = st.sidebar.number_input("Line length as fraction of λ", min_value=0.01, max_value=10.0, value=0.25, step=0.01)
    length = fraction * lambda_c

st.sidebar.success(f"Line length = {length:.4e} m ({length/lambda_c:.2f} λ at {fc} GHz)")

# --- 2. DEFINE FREQUENCY RANGE ---
freq = rf.Frequency(start=fc - 1, stop=fc + 1, npoints=501, unit='GHz')
f = freq.f
beta = 2 * np.pi * f / vp
gamma = 1j * beta  # lossless line

# --- 3. CREATE TRANSMISSION LINE AND LOAD NETWORK ---
ZL = RL + 1j * XL
line = rf.DefinedGammaZ0(freq, gamma=gamma, z0=Z0)

# manually define the load reflection coefficient (constant vs frequency)
s11 = (ZL - Z0) / (ZL + Z0)
s = s11 * np.ones((len(freq), 1, 1), dtype=complex)
load = rf.Network(s=s, frequency=freq, z0=Z0)

# Network before matching
network_before = line.line(length, unit='m') ** load

# --- 4. CALCULATE PARAMETERS (Before Matching) ---
Gamma_before = network_before.s[:, 0, 0]
VSWR_before = (1 + abs(Gamma_before)) / (1 - abs(Gamma_before))

# --- 5. DESIGN λ/4 TRANSFORMER ---
Zt = np.sqrt(Z0 * abs(ZL))   # ideal λ/4 transformer impedance (at center freq)
lambda4_length = lambda_c / 4

st.header("📊 Results")

# Better formatting for metrics - use smaller text or display differently
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Load Impedance ZL:**")
    st.markdown(f"`{RL:+.1f} {XL:+.1f}j Ω`")
    st.markdown("**λ/4 Transformer Z:**")
    st.markdown(f"`{Zt:.2f} Ω`")
with col2:
    st.markdown("**λ/4 Length:**")
    st.markdown(f"`{lambda4_length:.4e} m`")
    st.markdown("**Effective εᵣ:**")
    st.markdown(f"`{er:.2f}`")

st.markdown("---")

# create transformer section
transformer = rf.DefinedGammaZ0(freq, gamma=gamma, z0=Zt)
network_after = transformer.line(lambda4_length, unit='m') ** load

# --- 6. CALCULATE PARAMETERS (After Matching) ---
Gamma_after = network_after.s[:, 0, 0]
VSWR_after = (1 + abs(Gamma_after)) / (1 - abs(Gamma_after))

# --- 7. PLOTS ---

# |Γ| vs Frequency
st.subheader("1. Reflection Coefficient Magnitude vs Frequency")
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(f, abs(Gamma_before), label="Before Matching", color='red', linewidth=2)
ax1.plot(f, abs(Gamma_after), label="After λ/4 Matching", color='green', linestyle="--", linewidth=2)
ax1.set_title("|Γ| vs Frequency", fontsize=14, fontweight='bold')
ax1.set_xlabel("Frequency (GHz)", fontsize=12)
ax1.set_ylabel("|Γ|", fontsize=12)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

# VSWR vs Frequency
st.subheader("2. VSWR vs Frequency")
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(f, VSWR_before, label="Before Matching", color='red', linewidth=2)
ax2.plot(f, VSWR_after, label="After λ/4 Matching", color='green', linestyle="--", linewidth=2)
ax2.set_title("VSWR vs Frequency", fontsize=14, fontweight='bold')
ax2.set_xlabel("Frequency (GHz)", fontsize=12)
ax2.set_ylabel("VSWR", fontsize=12)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)

# Smith Chart comparison
st.subheader("3. Smith Chart Comparison")
fig3, ax3 = plt.subplots(figsize=(10, 10))
network_before.plot_s_smith(ax=ax3, draw_labels=True, color='red')
network_after.plot_s_smith(ax=ax3, draw_labels=False, color='green')

# ensure legend (plot_s_smith may not add labels), use empty handles with same colors
ax3.plot([], [], color='red', label='Before Matching', linewidth=2)
ax3.plot([], [], color='green', label='After Matching', linewidth=2)
ax3.set_title("Smith Chart: Before vs After λ/4 Matching", fontsize=14, fontweight='bold')
ax3.legend(fontsize=11)
st.pyplot(fig3)

# Display key metrics at center frequency
center_idx = len(f) // 2
st.subheader("📈 Performance at Center Frequency")
col1, col2 = st.columns(2)
with col1:
    st.write("**Before Matching:**")
    st.write(f"- |Γ| = {abs(Gamma_before[center_idx]):.4f}")
    st.write(f"- VSWR = {VSWR_before[center_idx]:.4f}")
with col2:
    st.write("**After λ/4 Matching:**")
    st.write(f"- |Γ| = {abs(Gamma_after[center_idx]):.4f}")
    st.write(f"- VSWR = {VSWR_after[center_idx]:.4f}")
