# extract.py
import matplotlib
matplotlib.use('Agg')
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import asyncio

def generate_images_stream(target_lat, target_lon, output_dir, folder_name):
    file_path = "./data/2025-06-01T00_00_00_cn_flatted.nc"
    ds = xr.open_dataset(file_path)
    lat = ds['latitude'].values
    lon = ds['longitude'].values

    lat_idx = np.abs(lat - target_lat).argmin()
    lon_idx = np.abs(lon - target_lon).argmin()

    if lat_idx >= lat.shape[0]:
        lat_idx = lat.shape[0] - 1
    if lon_idx >= lon.shape[0]:
        lon_idx = lon.shape[0] - 1

    t2m = (ds['t2m'][lat_idx, lon_idx, :] - 273.15).values
    u10 = ds['u10'][lat_idx, lon_idx, :].values
    v10 = ds['v10'][lat_idx, lon_idx, :].values
    wind_speed = np.sqrt(u10**2 + v10**2)
    time = ds['time'].values
    tp6h = ds['tp6h'][lat_idx, lon_idx, :].values if 'tp6h' in ds else None

    os.makedirs(output_dir, exist_ok=True)
    for i in range(len(time)):
        fig, ax1 = plt.subplots(figsize=(6, 4))
        ts = pd.to_datetime(str(time[i]))
        ts_str = ts.strftime('%Y-%m-%d %H:%M')
        ax1.set_title(f"Forecast - {ts_str}", fontsize=12)
        ax1.set_ylabel("Temperature (°C)", color='tab:red')
        ax1.plot(0, t2m[i], 'ro', label="Temperature")
        ax1.tick_params(axis='y', labelcolor='tab:red')
        ax1.set_ylim(-10, 40)
        ax1.quiver(1.5, t2m[i], u10[i], v10[i], angles='xy', scale_units='xy', scale=1, color='green')
        ax1.text(1.7, t2m[i], f"{wind_speed[i]:.1f} m/s", fontsize=9, color='green')
        ax1.set_xlim(-1, 3)
        if tp6h is not None:
            ax2 = ax1.twinx()
            ax2.set_ylabel("Rainfall (mm)", color='tab:blue')
            ax2.bar(0.5, tp6h[i], width=0.3, color='tab:blue')
            ax2.tick_params(axis='y', labelcolor='tab:blue')
            ax2.set_ylim(0, max(tp6h) * 1.2 if tp6h.max() > 0 else 10)
        fig.tight_layout()
        filename = os.path.join(output_dir, f"Forecast - {ts_str}.png")
        plt.savefig(filename)
        plt.close()
        # yield 静态访问路径
        yield f"/static/{folder_name}/Forecast - {ts_str}.png"
