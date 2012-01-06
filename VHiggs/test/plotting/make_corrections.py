'''

Define the MC2DATA corrections used in the VH analysis.

This script produces corrections.C, which can be

ROOT.gROOT.ProcessLine('.L corrections.C++')

to enable access to the functions in TTree::Draw

Author: Evan K. Friis, UW Madison

'''

import FinalStateAnalysis.Utilities.CppTools as cpp

# Make the class name easier to write

Bins = cpp.CppKinematicBinning
Func = cpp.CppFunctionWrapper

barrel = lambda x: ('eta', 0, 1.44, x)
endcap = lambda x: ('eta', 1.44, None, x)

cfg = {
    'MuID' : Bins([
        ('pt', 0, 8, 1.0),
        ('pt', 8, 10, Bins([
            barrel(1.005),
            endcap(0.955),
        ])),
        ('pt', 10, 20, Bins([
            barrel(0.986),
            endcap(0.979),
        ])),
        ('pt', 20, 30, Bins([
            barrel(0.989),
            endcap(0.976),
        ])),
        ('pt', 30, 50, Bins([
            barrel(0.991),
            endcap(0.975),
        ])),
        ('pt', 50, 100, Bins([
            barrel(0.99),
            endcap(0.978),
        ])),
        ('pt', 100, None, Bins([
            barrel(0.99),
            endcap(0.978),
        ])),
    ]),
    'MuIso' : Bins([
        ('pt', 0, 8, 1.0),
        ('pt', 8, 10, Bins([
            barrel(0.968),
            endcap(0.936),
        ])),
        ('pt', 10, 20, Bins([
            barrel(0.992),
            endcap(0.990),
        ])),
        ('pt', 20, 30, Bins([
            barrel(1.0),
            endcap(0.998),
        ])),
        ('pt', 30, 50, Bins([
            barrel(1.0),
            endcap(0.998),
        ])),
        ('pt', 50, 100, Bins([
            barrel(1.0),
            endcap(1.0),
        ])),
        ('pt', 100, None, Bins([
            barrel(1.0),
            endcap(1.0),
        ])),
    ]),
    'MuIso' : Bins([
        ('pt', 0, 8, 1.0),
        ('pt', 8, 10, Bins([
            barrel(0.968),
            endcap(0.936),
        ])),
        ('pt', 10, 20, Bins([
            barrel(0.992),
            endcap(0.990),
        ])),
        ('pt', 20, 30, Bins([
            barrel(1.0),
            endcap(0.998),
        ])),
        ('pt', 30, 50, Bins([
            barrel(1.0),
            endcap(0.998),
        ])),
        ('pt', 50, 100, Bins([
            barrel(1.0),
            endcap(1.0),
        ])),
        ('pt', 100, None, Bins([
            barrel(1.0),
            endcap(1.0),
        ])),
    ]),
    'MuHLT8' : Bins([
        ('pt', 0, 8, 1.0),
        ('pt', 8, 10, Bins([
            barrel(0.972),
            endcap(1.003),
        ])),
        ('pt', 10, 20, Bins([
            barrel(0.989),
            endcap(0.988),
        ])),
        ('pt', 20, 30, Bins([
            barrel(0.987),
            endcap(0.987),
        ])),
        ('pt', 30, 50, Bins([
            barrel(0.986),
            endcap(0.984),
        ])),
        ('pt', 50, 100, Bins([
            barrel(0.985),
            endcap(0.982),
        ])),
        ('pt', 100, None, Bins([
            barrel(0.982),
            endcap(0.982),
        ])),
    ]),
}

with open('corrections.C', 'w') as output_file:
    output_file.write('#include <iostream>\n')
    for name, data in cfg.iteritems():
        # Add some extra logic to detect if we are running on MC or DATA
        fixed_data = Bins([
            ('run', None, 2, data),
            ('run', 2, None, 1.0), # DATA scale factor is always 1.0
        ])
        func = Func(
            name, fixed_data, 'pt', 'eta', 'run',
            default=-999,
            warn='std::cerr << "Warning out of bounds in function {name}" << std::endl;\n'
        )
        output_file.write(str(func))
        output_file.write('\n')
