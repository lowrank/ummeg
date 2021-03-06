from UMMEG import *

geometry = SplineGeometry()

geometry.AddCircle((0.0, 0.0), 1.0)

ngmesh = geometry.GenerateMesh(maxh=0.02)
mesh = Mesh(ngmesh)
mesh.Curve(3)

mu  = CoefficientFunction(1.0)
eps = CoefficientFunction(1.0 +   \
                          0.0 *IfPos( (x-0.1)**2 + (y-0.3)**2 - 0.16 , \
                                 1.0 + cos( sqrt( (x-0.1)**2 + (y-0.3)**2 ) * 5.0 * np.pi / 2 ) , 0))
sigma = CoefficientFunction(
    0.0* IfPos((x-0.05)**2 + (y-0.2)**2 - 0.16,
                1.0 + cos(sqrt((x-0.05)**2 + (y-0.2)**2) * 5.0 * np.pi / 2), 0))

freq = 3 * 2 * np.pi

# J_r    = CoefficientFunction(
#                     0.5 * IfPos((x-0.15)**2 + (y-0.3)**2 - 0.04,
#                                 1.0 + cos(sqrt((x-0.15)**2 + (y-0.3)**2 ) * 10.0 * np.pi / 2), 0))

# J_c = CoefficientFunction(
#     0.2 * IfPos((x-0.35)**2 + (y-0.5)**2 - 0.04,
#                 1.0 + cos(sqrt((x-0.35)**2 + (y-0.5)**2) * 10.0 * np.pi / 2), 0))

J_r = CoefficientFunction(0.)
J_c = CoefficientFunction(0.)

impedance_r = CoefficientFunction(1J * freq * (y * exp(-1J * freq * x)-(y+1) * exp(-1J * freq * y)))
impedance_c = CoefficientFunction(1J * freq * (-(x+1) * exp(-1J * freq * x) + x * exp(-1J * freq * y)))
class Arg(object):
    pass

args = Arg()
args.frequency    = freq
args.permittivity = eps
args.eps0         = 1.0
args.permeability = mu
args.conductivity = sigma
args.source       = CoefficientFunction((J_r, J_c))
args.imp          = CoefficientFunction((impedance_r, impedance_c))
args.mesh         = mesh
args.deg          = 3


m = UMMEG(args)
A, b = m.construct_variational_form()
Sol = m.solve(A, b, "result")
