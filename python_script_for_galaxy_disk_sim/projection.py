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


def ReadCoolingCurve():
    FileIn = open("cool_rates.in",'r')
    data = loadtxt(FileIn)
    FileIn.close()
    return (data[:,0],data[:,2])

(LogT, LogCoolRate) = ReadCoolingCurve()

def _cooling_rate(field,data):
    return 10.0**interp(log10(data["temperature"]), LogT, LogCoolRate)* YTQuantity(1,"erg*cm**3/s")

m_H = YTQuantity(1.67e-24,'g')
mu = 0.6*m_H
def _cooling_rate_per_volume(field,data):
    return 1.76*0.4* data["cooling_rate"] *data["density"]**2/m_H/mu

def _cooling_rate_per_cell(field,data):
    return data["cooling_rate_per_volume"]*data["cell_volume"]

def _x_ray_emission(field,data):
    return  1.76*0.4* data["cooling_rate"] *data["density"]**2/m_H/mu/YTQuantity(4*3.14159265,'sr') 


def see(i):
  fn = get_fn(i)

  ds = yt.load(fn)
  ad = ds.all_data()
  
  hot = ad.cut_region("obj['temperature']>2e6") 
  c1 = [0.001,0.001,0.001]

  a1="cooling_rate_per_volume"
  a1="SN_Colour"
  a1 = 'x_ray_emission'
  a=[a1]
  pj_all = yt.ProjectionPlot(ds, 'x', a,center=c1,weight_field=None,width=(400,'kpc'),data_source=hot)
  pj_all.save('projection_' + a1+ '_' + str(i)+ '_all.png' )


yt.add_field('number_density',function=_number_density, units  = '1/cm**3')
yt.add_field('cooling_rate',function=_cooling_rate,units="erg*cm**3/s")
yt.add_field('cooling_rate_per_volume',function=_cooling_rate_per_volume,units="erg/cm**3/s")
yt.add_field('cooling_rate_per_cell',function=_cooling_rate_per_cell,units="erg/s")
yt.add_field('x_ray_emission',function=_x_ray_emission,units="erg/cm**3/s/sr")



num = [202,300,330]
num=range(100,2100,100)
num=[1,10,50,100,150,200,240]
num=range(100,600,100)
for i in num:
   see(i)

