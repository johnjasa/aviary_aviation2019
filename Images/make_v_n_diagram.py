# ------------------------------------------------------------------------------
# This code plots the V-n diagram.
# See CFR 14 Part 25.335 for requirements (https://www.ecfr.gov/cgi-bin/text-idx?SID=78fe626d61a72d136ceabbb18fa4242d&mc=true&node=pt14.1.25&rgn=div5).
# CFR 14 Part 23 does not seem to have any specific requirements, but for a
# tiltwing being designed for UAM, it makes sense to follow Part 25 for the gust loads.
# More on V-n diagrams can be found in most textbooks (e.g., Raymer or Nicolai and Carichner).
# Also explained in Prof. Matins' Aircraft design notes, ask Sham for them.
# Shamsheer S. Chauhan, Apr 19, 2019.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from __future__ import print_function
from matplotlib import pylab as plt
from matplotlib import rcParams as rcp
import numpy as np
import math

imported_niceplotes = False
try:
    import niceplots # using John Jasa's niceplots
    imported_niceplotes = True
except:
    pass

rcp['font.family'] = 'serif'
rcp['text.usetex'] = 'true'
rcp['font.size'] = '20'

# ------------------------------------------------------------------------------
# Function for the lift-curve slope [Raymer]
# ------------------------------------------------------------------------------

def lift_slope(slope_0, AR, d_fuselage, sweep, span, mach, S_exposed_to_S_ref_ratio):
    """ Lift-curve slope including compressibility effects """
    F = 1.07 * (1 + d_fuselage / span) ** 2
    beta = (1 - mach**2)**0.5
    return ( slope_0 * AR * F * S_exposed_to_S_ref_ratio /
            ( 2 + (4 + AR**2 * slope_0**2 *(1 + (math.tan(sweep / 180. * np.pi) / beta)**2 ) / (4 * np.pi**2) )**0.5))

# ------------------------------------------------------------------------------
# Tiltwing aircraft specifications
# (from Johnson et al. "Concept Vehicles for VTOL Air Taxi Operations",
# unless otherwise specified)
# ------------------------------------------------------------------------------

AR = 11.23 # Aspect ratio
d_fuselage = 6. # ***Rough guess*** for fuselage diameter in ft
sweep = 0. # Sweep in deg
mach = 0.3

W = 14039 # weight in lb
WS = 60 # wing loading in lb/ft^2

S = W / WS # wing area in ft^2
span = (AR * S)**0.5 #ft
S_exposed_to_S_ref_ratio = (span - d_fuselage) / span # very rough estimate for exposed planform area (planform minus fuselage part) to planform area
c_bar = S / span # mean chord

print("Wing ref area, S, is", S, "ft^2")
print("Wing span, span, is", span, "ft")
print("Wing mean chord, c_bar, is", c_bar, "ft")

rhoSL = 0.002377 # sea-level air density in slugs/ft**3
rho_alt = 0.002377 # Assuming 5,000 ft air density in slugs/ft**3

CL_max = 3. # ***Rough guess*** for max. CL estimate
CL_min = -1. # ***Rough guess*** for min CL estimate

# Equivalent air speeds (EAS) in knots
V_C = 230. * (rho_alt / rhoSL)**0.5 # EAS cruise speed, ***using*** max speed from Table 11.
V_D = 230. * 1.25 * (rho_alt / rhoSL)**0.5 # ***assuming*** max dive EAS is 25% greater than the max speed

# ------------------------------------------------------------------------------
# Diagram calcs
# ------------------------------------------------------------------------------

CL_alpha = lift_slope(2*np.pi, AR, d_fuselage, sweep, span, mach, S_exposed_to_S_ref_ratio)
print("Lift-curve slope (CL_alpha) is ", CL_alpha)

g = 32.174 # imperial units gravity

# FAR gust speed values
U_B = 66 #ft/s
U_C = 50 #ft/s
U_D = 25 #ft/s

# Speeds in knots
V_A = (2.5 * 2 * WS / CL_max / rhoSL)**0.5 / 1.688
print("V_A is", V_A)

V_A_neg = (-1 * 2 * WS / CL_min / rhoSL)**0.5 / 1.688
print("V_A_neg is", V_A_neg)

V_S = (1 * 2 * WS / CL_max / rhoSL)**0.5 / 1.688
print("V_S is", V_S)

V_S_neg = (-1 * 2 * WS / CL_min / rhoSL)**0.5 / 1.688
print("V_S_neg is", V_S)

mu = 2 * WS / (rho_alt * c_bar * CL_alpha * g)
print("mu is", mu)

K = 0.88 * mu /(5.3 + mu)
print("K is ", K)

# Solve quadratic formula to find interstion of stall and gust curves
a_VB = (1.688**2) * rhoSL * CL_max / 2 / WS
b_VB = -K * CL_alpha * U_B / 498 / WS
c_VB = -1

V_B = (-b_VB + (b_VB**2 - 4 * a_VB * c_VB)**0.5) / (2 * a_VB) # quadratic formula
print("V_B is ", V_B)

# maneuver load
x1 = np.arange(0,V_A,0.01)
y1 = rhoSL * CL_max * ((1.688 * x1)**2) / 2 / WS

x2 = np.arange(0,V_A_neg,0.01)
y2 = rhoSL * CL_min * ((1.688 * x2)**2) / 2 / WS

x3 = np.arange(V_A,V_D,0.01)
y3 = 2.5 * x3**0

x4 = np.arange(V_A_neg,V_C,0.1)
y4 = -1 * x4**0

y5 = np.arange(rhoSL*CL_min*((1.688*V_S)**2)/2/WS,1.,0.01)
x5 = V_S * y5**0

y6 = np.arange(0,2.5,0.01)
x6 = V_D * y6**0

x7 = [V_C,V_D]
y7 = [-1,0]

xg1 = np.arange(0, V_B, 0.1)
xg2 = np.arange(0, V_C, 0.1)
xg3 = np.arange(0, V_D, 0.1)
yg1 = 1 + K * CL_alpha * U_B * xg1 / 498 / WS
yg2 = 1 - K * CL_alpha * U_B * xg1 / 498 / WS
yg3 = 1 + K * CL_alpha * U_C * xg2 / 498 / WS
yg4 = 1 - K * CL_alpha * U_C * xg2 / 498 / WS
yg5 = 1 + K * CL_alpha * U_D * xg3 / 498 / WS
yg6 = 1 - K * CL_alpha * U_D * xg3 / 498 / WS

xe1 = [V_B, V_C, V_D, V_D, V_C, V_B]
print(xe1)
ye1 = [1 + K*CL_alpha*U_B*V_B/498/WS, 1+K*CL_alpha*U_C*V_C/498/WS, 1+K*CL_alpha*U_D*V_D/498/WS, 1-K*CL_alpha*U_D*V_D/498/WS, 1-K*CL_alpha*U_C*V_C/498/WS, 1-K*CL_alpha*U_B*V_B/498/WS]
print(ye1)

# ------------------------------------------------------------------------------
# Plot
# ------------------------------------------------------------------------------

plt.figure(figsize=(8,6))
plt.plot(x1,y1,'k',lw=2, label="$V_A$")
plt.plot(x2,y2,'k',lw=2, label=" ")
plt.plot(x3,y3,'k',lw=2, label="$V_D$")
plt.plot(x4,y4,'k',lw=2, label=" ")
plt.plot(x5,y5,'k',lw=2, label="$V_S$")
plt.plot(x6,y6,'k',lw=2, label=" ")
plt.plot(x7,y7,'k',lw=2, label="$V_C$")

plt.plot(xg1,yg1,'r--',lw=2, label="$V_B$")
plt.plot(xg1,yg2,'r--',lw=2, label=" ")
plt.plot(xg2,yg3,'b--',lw=2, label=" ")
plt.plot(xg2,yg4,'b--',lw=2, label=" ")
plt.plot(xg3,yg5,'b--',lw=2, label=" ")
plt.plot(xg3,yg6,'b--',lw=2, label=" ")

plt.plot(xe1,ye1,'r',lw=2, label=" ")

plt.xlim([0,330])
plt.ylim([-1.3,3.1])

plt.xlabel(r'$V_\mathrm{EAS}~\mathrm{(knots)}$')
plt.ylabel(r'$\mathrm{Load}~\mathrm{factor}~n$')
if imported_niceplotes:
    niceplots.draggable_legend()
plt.show()
