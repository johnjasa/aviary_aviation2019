from pyxdsm.XDSM import XDSM

#
opt = 'Optimization'
solver = 'MDA'
ecomp = 'Analysis'
icomp = 'ImplicitAnalysis'
group = 'Metamodel'
func = 'Function'


x = XDSM()

x.add_system('opt', opt, r'\text{Optimizer}')
x.add_system('des', icomp, [r'\text{Discipline Design}',r'\text{Models}'], stack=True)
x.add_system('miss', icomp, [r'\text{Mission Performance}',r'\text{Models}'], stack=True)

x.add_input('des', [r'\text{Discipline}',r'\text{Design Inputs}'])
x.add_input('miss', [r'\text{Mission Inputs}'])

x.connect('opt', 'des', [r'\text{Discipline}',r'\text{Design Variables}'])
x.connect('opt', 'miss', [r'\text{Optimal Control}',r'\text{Variables}'])
x.connect('des', 'miss', [r'\text{Discipline Design}',r'\text{Characteristics}'])

x.connect('des', 'opt', [r'\text{Design Constraints}'])
x.connect('miss', 'opt', [r'\text{Objective Function,}',r'\text{Operational Constraints}'])

x.write('General_XDSM')