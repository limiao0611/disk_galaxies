import matplotlib
from numpy import *
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
yt.enable_parallelism()
import matplotlib.pyplot as plt

def get_fn(i):
    a0=''
    if (i<10):
      a0='000'
    if (10<=i<100):
      a0='00'
    if (100<=i<=999):
      a0='0'
    filen='DD'+a0+str(i)+'/sb_'+a0+str(i)
    return filen

def _z_den_flux(field,data):
    return abs(data['density']*data['z-velocity'])

def _CR_Energy_Density(field,data):
    return data['CREnergyDensity']* data.ds.mass_unit/data.ds.length_unit/data.ds.time_unit**2

def _vr(field,data):
   center = data.ds.domain_center
   location_vector = [data['x']-center[0], data['y']-center[1], data['z']-center[2]]
   vr =  data['x-velocity'] * (data['x']-center[0]) +  data['y-velocity'] * (data['y']-center[1])+  data['z-velocity'] * (data['z']-center[2])
   vr = vr/sqrt((data['x']-center[0])**2 + (data['y']-center[1])**2+ (data['z']-center[2])**2)
   return vr


def _mass_flux_radial(field,data):
   return abs(data['density']* data['vr'])

def _momentum_flux_radial(field,data):
   return data['density']* data['vr']**2 # * sign(data['vr'])

def see(i):
  fn = get_fn(i)
  ds = yt.load(fn)
  my_sphere = ds.sphere("c", (300.0, "kpc"))

  plot = yt.ProfilePlot(my_sphere, "radius", "density",
                      weight_field="cell_mass")

  plot.set_unit('radius', 'kpc')

  plot.save()

num=range(1,601,100)
for i in num:
   see(i)
