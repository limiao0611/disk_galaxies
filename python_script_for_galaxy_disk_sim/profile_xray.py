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

n = 0

def _number_density(field,data):
    return abs(data['density']/YTQuantity(1.67e-24,'g'))

def _xray_emission_per_cell(field, data):
   return data["xray_emissivity_0.5_2_keV"]* data["cell_volume"]

def see(i):
   global n,a,b
   fn  = get_fn(i)
   ds = yt.load(fn)
   ad = ds.all_data()

   print ('size(ad["density"])=', size(ad["density"])  )


   yt.add_xray_emissivity_field(ds, 0.5, 2,with_metals=False,constant_metallicity=2.0 )
   print ('ad["xray_emissivity_0.5_2_keV"]=', ad["xray_emissivity_0.5_2_keV"])
   print ('ad["xray_luminosity_0.5_2_keV"]=', ad["xray_luminosity_0.5_2_keV"])

   yt.add_field("xray_emission_per_cell",function= _xray_emission_per_cell, units='erg/s')  
#   yt.add_field('number_density',function=_number_density, units  = '1/cm**3')
  
#   print ("ad['number_density']=", ad['number_density'])
#   print ("ad[xray_emission_per_cell]=", ad['gas',"xray_emission_per_cell"])

   

   prof = yt.create_profile(ad, a, b, weight_field =None,logs=None, n_bins = 20 )
   z = prof.x.value
   z_y = prof[b].value

   time = (ds.current_time * 2.65895e12).in_units('Myr')
   t = round(float(time),2)
   print ("t=",t)
   print ("z[0:20]=",z[0:20])
   print ("z_y[0:20]=",z_y[0:20])
   cc=['g','black','r','blue','m','y','k','orange','crimson','pink','cyan']
   
   plt.plot(z, z_y, c=cc[n], label = 't='+ str(t)+'Myr')
#   plot= ProfilePlot.from_profiles(prof) # , z, z_y, c=cc[n], label = 't='+ str(t)+'Myr')
#   plot.set_unit('z','kpc')
#   plot.set_log('z', log=True)
#   plt.plot(ad[a], ad[b], c = cc[n], label = 't='+ str(t)+'Myr')

   n = n+1

a='z'

quan =['Ec','rho', 'press']
quan =["xray_emissivity_0.5_2_keV"]
quan =["xray_luminosity_0.5_2_keV"]

num =[100,200,300,400,500]
num=[200]
for b in quan:
  n=0
  fig = plt.figure()
  for  i  in num:
    see(i)
  plt.legend(loc= 'best')
#  plt.xlim(0,2200.)
  plt.grid()
  plt.savefig(a+'_'+b + ' '+str(num) +'_1d_Profile_Miao_plt.png')



