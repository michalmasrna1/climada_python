from climada.hazard import TCTracks

tracks = TCTracks()
tracks.read_ibtracs_netcdf(provider='usa', basin='NA')
tracks.plot()
