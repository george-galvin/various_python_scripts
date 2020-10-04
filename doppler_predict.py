import numpy as np
from matplotlib import pyplot as plt
from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite
from skyfield.toposlib import Topos
from astropy.constants import c

c = c.value / 1000 #convert to km/s
ts = load.timescale()
plt.style.use("dark_background")

def predict_doppler_from_tle(tle1, tle2, start_time, gs, base_freq):

    end_time = ts.tt_jd(start_time.tt + 1) #predict for 1 day in future

    tle_sat = EarthSatellite(tle1, tle2)
    times, events = tle_sat.find_events(gs, start_time, end_time, altitude_degrees = 0.0)

    #Find events where the satellite sets below 10 degrees, and use this to split the times array up into individual passes
    sat_passes=[]
    start=-1
    end=-1
    for i, event in enumerate(events):
      if (event==0):
        start=i
      if (event==2) and (start > end):
        end=i
        sat_passes.append([times[start], times[end]])
      
    for sat_pass in sat_passes:
        
        p_start = sat_pass[0]
        p_end = sat_pass[-1]

        #Split pass timeframe into 1000
        time_points = ts.tt_jd(np.linspace(p_start.tt, p_end.tt, 1000))
        sat_range_rate = tle_sat.at(time_points).velocity.km_per_s - gs.at(time_points).velocity.km_per_s
        sat_range = tle_sat.at(time_points).position.km - gs.at(time_points).position.km
        
        #Take the range rate's component in the direction of the range
        radial_velocity = np.array([np.dot([a[b] for a in sat_range], [a[b] for a in sat_range_rate]) \
         / np.linalg.norm([a[b] for a in sat_range]) for b in range(1000)])
         
        shifted_freqs = base_freq / (1 + radial_velocity/c)
    
        plt.plot(time_points.tt, shifted_freqs, markersize=1)
        plt.xlabel("Time (Julian Days)")
        plt.ylabel("Shifted frequency (Hz)")
    plt.show()
        
if __name__ == "__main__":

    test_ground_station = Topos(latitude_degrees=52.834, longitude_degrees=6.379, elevation_m=10)
    test_freq_hz = 400000000
    today = ts.tt(2020, 10, 3, 0, 0, 0)
    test_tle_1 = "1 00733U 64002A   20276.41516155  .00000014  00000-0  22939-4 0  9994" #Test TLE data: Thor Agena D
    test_tle_2 = "2 00733  98.9962 172.0433 0032806 280.7415  79.0074 14.32406476954130"
