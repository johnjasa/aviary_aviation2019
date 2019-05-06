from pyxdsm.XDSM import XDSM

#
opt = 'Optimization'
solver = 'MDA'
ecomp = 'Analysis'
icomp = 'ImplicitAnalysis'
group = 'Metamodel'
func = 'Function'


x = XDSM()

x.add_system('opt', opt, [r'\text{Manual Iteration}', r'\text{or Optimizer}'])

x.add_system('NPSS_opt', opt, [r'\text{Manual Iteration}', r'\text{or Optimizer}'])
x.add_system('NPSS_des', icomp, [r'\text{Engine Design}',r'\text{Model (NPSS)}'])
x.add_system('NPSS_od', icomp, [r'\text{Engine Performance}',r'\text{Model (NPSS)}'])

x.add_system('CAMRAD_opt', opt, [r'\text{Manual Iteration}', r'\text{or Optimizer}'])
x.add_system('CAMRAD_des', icomp, [r'\text{Rotor Design}',r'\text{Model (CAMRAD II)}'])
x.add_system('CAMRAD_od', icomp, [r'\text{Rotor Performance}',r'\text{Model (CAMRAD II)}'])

x.add_system('NDARC_opt', opt, [r'\text{Manual Iteration}', r'\text{or Optimizer}'])
x.add_system('NDARC_des', icomp, [r'\text{Aircraft Design}',r'\text{Model (NDARC)}'])
x.add_system('NDARC_od', icomp, [r'\text{Mission Performance}',r'\text{Model (NDARC)}'])


x.add_input('NPSS_des', [r'\text{Engine}',r'\text{Design Inputs}'])
x.add_input('CAMRAD_des', [r'\text{Rotor}',r'\text{Design Inputs}'])
x.add_input('NDARC_des', [r'\text{Aircraft}',r'\text{Design Inputs}'])


x.connect('NPSS_opt', 'NPSS_des', [r'\text{Engine Design}',r'\text{Variables}'])
x.connect('NPSS_des', 'NPSS_od', [r'\text{Engine Design}',r'\text{Characteristics}'])
x.connect('NPSS_des', 'NPSS_opt', [r'\text{Engine}',r'\text{Design Data}'])
x.connect('NPSS_od', 'NPSS_opt', [r'\text{Engine}',r'\text{Performance Data}'])


x.connect('CAMRAD_opt', 'CAMRAD_des', [r'\text{Rotor Design}',r'\text{Variables}'])
x.connect('CAMRAD_des', 'CAMRAD_od', [r'\text{Rotor Design}',r'\text{Characteristics}'])
x.connect('CAMRAD_des', 'CAMRAD_opt', [r'\text{Rotor}',r'\text{Design Data}'])
x.connect('CAMRAD_od', 'CAMRAD_opt', [r'\text{Rotor}',r'\text{Performance Data}'])


x.connect('NDARC_opt', 'NDARC_des', [r'\text{Aircraft Design}',r'\text{Variables}'])
x.connect('NDARC_des', 'NDARC_od', [r'\text{Aircraft Design}',r'\text{Characteristics}'])
x.connect('NDARC_des', 'NDARC_opt', [r'\text{Aircraft}',r'\text{Design Data}'])
x.connect('NDARC_od', 'NDARC_opt', [r'\text{Mission}',r'\text{Performance Data}'])



x.connect('NPSS_od', 'NDARC_od', [r'\text{Engine}',r'\text{Performance Data}'])
x.connect('CAMRAD_od', 'NDARC_od', [r'\text{Rotor}',r'\text{Performance Data}'])


x.connect('opt', 'NPSS_des', [r'\text{Engine Design}',r'\text{Variables}'])
x.connect('opt', 'CAMRAD_des', [r'\text{Rotor Design}',r'\text{Variables}'])
x.connect('opt', 'NDARC_des', [r'\text{Aircraft Design}',r'\text{Variables}'])
x.connect('NDARC_od', 'opt', [r'\text{Mission}',r'\text{Performance Data}'])


# x.connect('opt', 'des', [r'\text{Discipline}',r'\text{Design Variables}'])
# x.connect('opt', 'miss', [r'\text{Optimal Control}',r'\text{Variables}'])
# x.connect('des', 'miss', [r'\text{Discipline Design}',r'\text{Characteristics}'])

# x.connect('des', 'opt', [r'\text{Design Constraints}'])
# x.connect('miss', 'opt', [r'\text{Objective Function,}',r'\text{Operational Constraints}'])

x.write('Traditional_XDSM')