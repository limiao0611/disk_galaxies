import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
from yt import *
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import glob
from numpy import *

def get_fn(i):
    a0=''
    if (i<10):
      a0='000'
    if (10<=i<100):
      a0='00'
    if (100<=i<999):
      a0='0'
    filen='DD'+a0+str(i)+'/sb_'+a0+str(i)
    return filen

def _number_density(field,data):
    return abs(data['density']/YTQuantity(1.67e-24,'g'))

def see(i):
  fn = get_fn(i)
  ds = yt.load(fn)
  ad = ds.all_data()
  yt.add_xray_emissivity_field(ds, 0.5, 1.5,with_metals=False,constant_metallicity=2.0 )

#  p = yt.ProjectionPlot(ds, 'x', "xray_emissivity_0.5_2_keV")
#  p.save()
  time = ds.current_time.in_units("Gyr")
  emission_per_cell = ad["xray_emissivity_0.5_1.5_keV"]* ad["cell_volume"]
  total_xray_emission = sum(emission_per_cell.in_units("erg/s") )
  total_xray_luminosity = sum(ad['xray_luminosity_0.5_1.5_keV']).in_units('erg/s')
  f1=open('xray_emission_yt.dat','a')
  print (time, total_xray_emission, total_xray_luminosity,file = f1) 
  print (time, total_xray_emission,total_xray_luminosity) 
  f1.close()

num=range(101,601,100)
for i in num:
   see(i)
