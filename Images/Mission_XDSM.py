from pyxdsm.XDSM import XDSM

#
opt = 'Optimization'
solver = 'MDA'
ecomp = 'Analysis'
icomp = 'ImplicitAnalysis'
group = 'Metamodel'
func = 'Function'

x = XDSM()

#x.add_system('const', comp, r'\text{Constants}')
x.add_system('DYMOS', opt, [r'\text{DYMOS}'])
x.add_system('ambient', ecomp, [r'\text{Ambient}'])
# x.add_system('USATM', comp, [r'\text{US Atm 1976}'])
# x.add_system('mach_comp', comp, [r'\text{MACH}'])       
x.add_system('prop_comp', icomp, [r'\text{Propeller}',r'\text{(OpenBEMT)}'])
x.add_system('e_comp', icomp, [r'\text{Electrical}',r'\text{(Zappy)}'])
x.add_system('engine_comp', icomp, [r'\text{Turboshaft}',r'\text{(pyCycle)}'])
# x.add_system('cool_comp', comp, [r'\text{Thermal}'])
x.add_system('solver', solver, [r'\text{Solver}'])
x.add_system('aero_comp', icomp, [r'\text{Wing Aerodynamics}',r'\text{(OpenAeroStruct)}'])
x.add_system('flight_dynamics', ecomp, [r'\text{Flight Dynamics}']) # AKA prebalance
x.add_system('balance', icomp, [r'\text{Balance}'])
# x.add_system('drag_comp', comp, [r'\text{Aero Drag}'])
x.add_system('EOM_comp', ecomp, [r'\text{State Rates}'])
# x.add_system('', comp, r'\text{}')        

x.add_input('prop_comp', r'\bar{X}_{propeller}')
x.add_input('e_comp', [r'\bar{X}_{electrical}',r'\bar{Y}_{electrical}'])
x.add_input('engine_comp', [r'\bar{X}_{turboshaft}',r'\bar{Y}_{turboshaft}'])
# x.add_input('cool_comp', r'Cooling_{const}')
# x.add_input('drag_comp', r'C_{D\_aircraft}')
x.add_input('aero_comp', [r'\bar{X}_{wing}',r'\bar{Y}_{wing}'])
x.add_input('flight_dynamics', r'w_{empty}')
x.add_input('EOM_comp', [r'C_{D\_aircraft}',r'w_{empty}'])

x.connect('DYMOS', 'ambient', [r'h, V_{\infty}'])
x.connect('DYMOS', 'prop_comp', r'V_{\infty}, T')
x.connect('DYMOS', 'aero_comp', r'V_{\infty}')
x.connect('DYMOS', 'flight_dynamics', 'w_{fuel}, T')
x.connect('DYMOS', 'engine_comp', r'h')
# x.connect('DYMOS', 'drag_comp', r'V_{\infty}')
# x.connect('DYMOS', 'cool_comp', r'T_{fins}')
x.connect('DYMOS', 'EOM_comp', r'h, V_{\infty}, V_{\infty}^*, w_{fuel}, T')

x.connect('ambient', 'prop_comp', r'\rho, \mu')
x.connect('ambient', 'aero_comp', r'MN, \rho, \mu')
# x.connect('ambient', 'drag_comp', r'\rho, \mu')
x.connect('ambient', 'EOM_comp', r'\rho, \mu')
# x.connect('ambient', 'cool_comp', r'T_{amb}, \rho, P_{tot}')
x.connect('ambient', 'engine_comp', r'MN')

# x.connect('prop_comp', 'cool_comp', r'V_{prop}')
x.connect('prop_comp', 'e_comp', r'P_{prop}, N')

x.connect('solver', 'aero_comp', r'\alpha') # , V_{\infty}
x.connect('solver', 'flight_dynamics', r'\alpha')

x.connect('aero_comp', 'flight_dynamics', r'L_{wing}')
x.connect('aero_comp', 'EOM_comp', r'D_{wing}')

x.connect('flight_dynamics', 'balance', r'\alpha_{LHS}, \alpha_{RHS}')

x.connect('balance', 'solver', r'\mathcal{R} \alpha')

x.connect('engine_comp', 'DYMOS', r'w_{fuel}^*')

# x.connect('e_comp', 'cool_comp', r'Q_{heat 1,2,3...}')
x.connect('e_comp', 'engine_comp', r'P_{shaft}, N')

# x.connect('cool_comp', 'DYMOS', r'T_{fins}^*')
# x.connect('cool_comp', 'drag_comp', 'D_{cool}')

# x.connect('drag_comp', 'EOM_comp', r'D_{tot}')

x.connect('EOM_comp', 'DYMOS', r'h^*, r^*')

x.add_output('DYMOS', r'r,h', side='right')
x.add_output('prop_comp', r'P_{prop,max}', side='right')
x.add_output('engine_comp', r'T_4', side='right')
# x.add_output('cool_comp', r'T_{fins}', side='right')

x.write('Mission_XDSM')