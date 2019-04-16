from pyxdsm.XDSM import XDSM

#
opt = 'Optimization'
solver = 'MDA'
ecomp = 'Analysis'
icomp = 'ImplicitAnalysis'
group = 'Metamodel'
func = 'Function'

x = XDSM()

x.add_system('solver', solver, [r'\text{Solver}'])
x.add_system('thrust_comp', ecomp, [r'\text{Thrust}',r'\text{Required}'])
x.add_system('eng_ambient', ecomp, [r'\text{Propulsion}',r'\text{Ambient}'])
x.add_system('prop_comp', icomp, [r'\text{Propeller}',r'\text{(OpenBEMT)}'])
x.add_system('e_comp', icomp, [r'\text{Electrical}',r'\text{(Zappy)}'])
x.add_system('engine_comp', icomp, [r'\text{Turboshaft}',r'\text{(pyCycle)}'])
x.add_system('wing_ambient', ecomp, [r'\text{Wing}',r'\text{Ambient}'])
x.add_system('aero_comp', icomp, [r'\text{Wing Aerodynamics/}',r'\text{Structures}',r'\text{(OpenAeroStruct)}'])
x.add_system('aircraft_mass', ecomp, [r'\text{Aircraft Mass}']) # AKA prebalance
x.add_system('balance', icomp, [r'\text{Balance}'])

x.add_input('prop_comp', r'\bar{X}_{propeller}')
x.add_input('e_comp', r'\bar{X}_{electrical}')
x.add_input('engine_comp', r'\bar{X}_{turboshaft}')
x.add_input('aero_comp', r'\bar{X}_{wing}')
x.add_input('aircraft_mass', [r'\bar{X}_{aircraft}',r'm_{fuel}'])

x.add_output('e_comp', r'\bar{Y}_{electrical}', side='right')
x.add_output('engine_comp', r'\bar{Y}_{turboshaft}', side='right')
x.add_output('aero_comp', [r'\bar{Y}_{wing}'], side='right')
x.add_output('aircraft_mass', [r'm_{total}'], side='right')

x.connect('eng_ambient', 'prop_comp',[r'FC'])
x.connect('eng_ambient', 'engine_comp',[r'FC'])
x.connect('thrust_comp', 'prop_comp', [r'T'])
x.connect('prop_comp', 'e_comp', [r'P_{propeller}'])
x.connect('e_comp', 'engine_comp', [r'P_{generator}'])

x.connect('prop_comp', 'aircraft_mass', [r'm_{propeller}'])
x.connect('e_comp', 'aircraft_mass', [r'm_{electrical}'])
x.connect('engine_comp', 'aircraft_mass', [r'm_{turboshaft}'])
x.connect('wing_ambient', 'aero_comp',[r'FC'])
x.connect('aero_comp', 'aircraft_mass', [r'm_{wing}'])

x.connect('solver','thrust_comp',[r'm_{total}^*'])
x.connect('solver','aero_comp',[r'm_{total}^*'])
x.connect('solver','balance',[r'm_{total}^*'])
x.connect('aircraft_mass','balance',[r'm_{total}'])

x.connect('balance','solver',[r'm_{total} = m_{total}^*'])

x.write('Design_XDSM')