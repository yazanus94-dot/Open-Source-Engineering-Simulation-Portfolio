"""Schematic-as-code with SKiDL: generates a KiCad netlist (555_blinker.net) for PCB layout in Pcbnew.
Requires KiCad symbol libraries (set KICAD_SYMBOL_DIR / KICAD8_SYMBOL_DIR) - pip install skidl"""
from skidl import *

vcc, gnd = Net("VCC"), Net("GND")
trig_thr, dis, out, cv = Net("TRIG_THR"), Net("DIS"), Net("OUT"), Net("CV")
led_a = Net("LED_A")
vcc.drive = POWER; gnd.drive = POWER

ne = Part("Timer", "NE555P", footprint="Package_DIP:DIP-8_W7.62mm")
R1 = Part("Device", "R", value="1k", footprint="Resistor_SMD:R_0805_2012Metric")
R2 = Part("Device", "R", value="68k", footprint="Resistor_SMD:R_0805_2012Metric")
R3 = Part("Device", "R", value="470", footprint="Resistor_SMD:R_0805_2012Metric")
C1 = Part("Device", "C", value="10u", footprint="Capacitor_SMD:C_1206_3216Metric")
C2 = Part("Device", "C", value="10n", footprint="Capacitor_SMD:C_0805_2012Metric")
C3 = Part("Device", "C", value="100n", footprint="Capacitor_SMD:C_0805_2012Metric")
D1 = Part("Device", "LED", footprint="LED_SMD:LED_0805_2012Metric")
J1 = Part("Connector", "Conn_01x02_Pin", footprint="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical")

# pins: 1 GND, 2 TRIG, 3 OUT, 4 RESET, 5 CV, 6 THR, 7 DIS, 8 VCC
ne[1] += gnd
ne[8, 4] += vcc
ne[2, 6] += trig_thr
ne[7] += dis
ne[3] += out
ne[5] += cv
R1[1] += vcc;  R1[2] += dis
R2[1] += dis;  R2[2] += trig_thr
C1[1] += trig_thr; C1[2] += gnd
C2[1] += cv;   C2[2] += gnd
C3[1] += vcc;  C3[2] += gnd          # supply decoupling
R3[1] += out;  R3[2] += led_a
D1["A"] += led_a; D1["K"] += gnd
J1[1] += vcc;  J1[2] += gnd

ERC()
generate_netlist(file_="555_blinker.net")
generate_xml(file_="555_blinker.xml")
