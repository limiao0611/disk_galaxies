import matplotlib
from numpy import *
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import yt
yt.enable_parallelism()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

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
  fig = plt.figure()
  grid = AxesGrid(fig, (0.075,0.075,0.70,0.90), 
                nrows_ncols = (3,3),
                axes_pad = 1,
                label_mode = "1",
                share_all = True,
                cbar_location="right",
                cbar_mode="each",
                cbar_size="20%",
                cbar_pad="0%")
#  fields = ['density','temperature','pressure','z-velocity']#,'CR_Energy_Density','z_den_flux']
#  fields = ['density','mass_flux_radial','vr','momentum_flux_radial']#,'CR_Energy_Density','z_den_flux']
  fields = ['density','temperature','pressure','z-velocity', 'mass_flux_radial', 'momentum_flux_radial', 'SN_Colour','cooling_time', 'mach_number'] 
#  fields = ['SN_Colour','grid_level','mach_number','momentum_flux_radial']#,'CR_Energy_Density','z_den_flux']
  c1=[0.5, 0.5  ,0.5]
#  c1= [0.503373    ,    0.498587 , 0.5]
  p=yt.SlicePlot(ds,'x',fields,center=c1,axes_unit='kpc',fontsize=11,width=(150,'kpc'))
#  p=yt.SlicePlot(ds,'x',fields,center=c1,axes_unit='kpc',fontsize=11,width=(400,'kpc'))
#  p=yt.SlicePlot(ds,'x',fields,center=c1,axes_unit='kpc',fontsize=15)
#  p.set_unit('radial_velocity','km/s')
  p.set_unit('z-velocity','km/s')
#  p.set_unit('radius','kpc')
  p.set_unit('cooling_time','Myr')
#  p.set_unit('CR_Energy_Density','dyne/cm**2')
  p.set_zlim('density',1e-29,1e-26)
  p.set_zlim('temperature',1e4,1e7)
  p.set_zlim('pressure',1e-14,1e-11)
  p.set_zlim('mass_flux_radial',1e-4,1e-1)
  p.set_zlim('momentum_flux_radial',1e-14,1e-11)
  p.set_zlim('SN_Colour',1e5,1e9)
  p.set_zlim('cooling_time',30,3e4)
  p.set_zlim('mach_number',1e-2,1e2)
#  p.set_zlim('grid_level',0.5,4)
#  p.set_zlim('CR_Energy_Density',1e-15,1e-8)
#  p.set_zlim('z-velocity',-2e3,2e3)
  p.annotate_timestamp(corner='upper_left',time_unit='Myr',text_args={'color':'black'})
  for j, field in enumerate(fields):
    plot = p.plots[field]
    plot.figure = fig
    plot.axes = grid[j].axes
    plot.cax = grid.cbar_axes[j]
  p._setup_plots()
  p.annotate_grids()
  p.annotate_timestamp(corner='upper_left',time_unit='Myr',text_args={'color':'black'})
  if yt.is_root():
     plt.savefig('multi_x_slice_'+str(i)+'_9panel.png')

yt.add_field('z_den_flux',function=_z_den_flux, units  = 'Msun/yr/kpc**2')
yt.add_field('vr',function=_vr, units  = 'km/s')
yt.add_field('mass_flux_radial',function=_mass_flux_radial, units  = 'msun/kpc**2/yr')
#yt.add_field('momentum_flux_radial',function=_momentum_flux_radial, units  = 'msun/kpc/yr**2')
yt.add_field('momentum_flux_radial',function=_momentum_flux_radial, units  = 'dyne/cm**2')
#yt.add_field('CR_Energy_Density', function=_CR_Energy_Density, units='dyne/cm**2')
#num=range(1,10)
#num=range(600,1050,10)
num=range(1500,4000,100)
for i in num:
   see(i)


