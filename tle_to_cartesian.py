import math as m
import numpy as np
import spiceypy as spice
from datetime import date

spice.furnsh("de430.bsp")

#Gravitational parameters from Astronomical Almanac
gm_earth = 3.986004418e14 
gm_sun = 1.32712442099e20

def convert_tle(line1, line2):
    i_deg = float(line2[8:16])
    asc_node_deg = float(line2[17:25])
    e = float("." + line2[26:33])
    a_of_p_deg = float(line2[34:42])
    mean_a_deg = float(line2[43:51])
    mean_motion_rev_day = float(line2[53:63])

    epoch_day = float(line1[20:32])
    tle_year = int(line1[18:20])    
    if (0 <= tle_year <= 56):
        epoch_year = 2000 + tle_year
    else:
        epoch_year = 1900 + tle_year
    
    year_start_to_j2000 = (date(epoch_year, 1, 1) - date(2000, 1, 1)).days - .5
    days_since_j2000 = year_start_to_j2000 + epoch_day - 1
    print(days_since_j2000 + 2451545)
    seconds_since_j2000 = days_since_j2000 * 86400
    
    mean_motion_rad_s = mean_motion_rev_day * (2*m.pi) / 86400
    a = (gm_earth / (mean_motion_rad_s ** 2))**(1/3)
    r_p = a*(1-e)
    r_p_km = r_p / 1000

    i_r = m.radians(i_deg)
    asc_node_r = m.radians(asc_node_deg)
    a_of_p_r = m.radians(a_of_p_deg)
    mean_a_r = m.radians(mean_a_deg)
    gm_earth_km = gm_earth / 1e9
    keplerian_elements = np.array([r_p_km, e, i_r, asc_node_r, a_of_p_r, mean_a_r, seconds_since_j2000, gm_earth_km])

    sv_geo_km = spice.conics(keplerian_elements, seconds_since_j2000)
    sv_geo = sv_geo_km * 1000

    earth_sv = spice.spkssb(3, seconds_since_j2000, 'J2000') * 1000

    sv = np.add(sv_geo, earth_sv)
    return sv

if __name__ == "__main__":
    testline1 = "1 25544U 98067A   20244.64261447  .00001423  00000-0  33743-4 0  9990"
    testline2 = "2 25544  51.6469 335.0535 0001907  74.8621  70.2498 15.49203578243713"
    test_sv = convert_tle(testline1, testline2)
    print(test_sv)