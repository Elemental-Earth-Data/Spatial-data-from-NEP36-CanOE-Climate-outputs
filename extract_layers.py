import os
import rioxarray
import xarray as xr

input_dir = './NEP36-CanOE_masked_715'
ncfile_pattern = 'NEP36-CanOE_{variable}_{simulation}_monthly_715x715_mask.nc'


def process_climate_output(simulation, variable):

    print(f'Processing {simulation} for {variable}...')

    simulation_shortname = simulation.split('_')[0]

    path = os.path.join(input_dir, simulation_shortname)
    ncfile = os.path.join(path, ncfile_pattern.format(
        variable=variable, simulation=simulation))

    ds = xr.open_dataset(ncfile)

    if 'deptht' in ds:
        # use the same name for depth dimension
        ds = ds.rename({'deptht': 'depth'})

    darr = ds[variable]

    # handle the special case of integrated primary production
    if variable == 'TPP':
        variable = 'ipp'
        darr = darr.integrate('depth')

    darr['t'] = ['fallwinter', 'fallwinter', 'springsummer',     # JFM
                 'springsummer', 'springsummer', 'springsummer', # AMJ
                 'springsummer', 'springsummer', 'fallwinter',   # JAS
                 'fallwinter', 'fallwinter', 'fallwinter'        # OND
                 ]

    def average_and_save_geotiff(darr_level, outfile_pattern):
        """give a 2d dataarray save it as a geotiff for each season"""

        for season in ['springsummer', 'fallwinter']:
            darr_mean = darr_level.groupby('t').mean('t')

            darr_output = darr_mean.sel(t=season)
            darr_output.rio.set_crs('EPSG:4326', inplace=True)

            filename = outfile_pattern.format(season=season)
            darr_output.rio.to_raster(filename)

    if variable in ['mld', 'ipp']:
        # this is a 2d variable
        outfile_pattern = f'NEP36-CanOE_{simulation}_{variable}_{{season}}.tif'

        average_and_save_geotiff(darr, outfile_pattern)

    else:
        # this is a 3d variable
        for level in ['surface', 'bottom']:

            outfile_pattern = f'NEP36-CanOE_{simulation}_{variable}_{{season}}_{level}.tif'

            if level == 'surface':
                depth_index = 0
            else:  # find index of the "bottom"
                depth_index = darr.notnull().sum('depth') - 1

            darr_level = darr.isel(depth=depth_index)

            average_and_save_geotiff(darr_level, outfile_pattern)


if __name__ == "__main__":

    simulations = ['historical_1986-2005',
                   'RCP45_2046-2065',
                   'RCP85_2046-2065']

    variables = ['mld', 'TPP', 'O2', 'PH', 'temp', 'salt', 'NO3', 'speed']

    # iterate through all combinations of simulations and variables
    for variable in variables:
        for simulation in simulations:
            process_climate_output(simulation=simulation, variable=variable)
