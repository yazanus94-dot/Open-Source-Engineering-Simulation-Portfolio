"""Design calculations for the NE555 astable LED blinker."""
R1, R2, C1 = 1e3, 68e3, 10e-6
VCC, VF_LED, I_LED_TARGET = 9.0, 2.0, 10e-3
f = 1.44 / ((R1 + 2 * R2) * C1)
duty = (R1 + R2) / (R1 + 2 * R2)
t_high = 0.693 * (R1 + R2) * C1
t_low = 0.693 * R2 * C1
R3 = (VCC - 1.5 - VF_LED) / I_LED_TARGET   # 555 output saturation ~1.5 V at 10 mA (NE555 bipolar)
print(f"f = {f:.2f} Hz   period = {1/f:.3f} s   duty = {100*duty:.1f} %")
print(f"t_high = {t_high:.3f} s   t_low = {t_low:.3f} s")
print(f"LED resistor R3 >= {R3:.0f} ohm -> choose 470 ohm (I = {(VCC-1.5-VF_LED)/470*1e3:.1f} mA)")
