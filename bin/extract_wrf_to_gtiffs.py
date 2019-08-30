
def affine_from_wrfds( ds ):
    ''' 
    make an affine transform from a SNAP-prepped wrf dataset.
    * must be an xarray.Dataset or (potentially) xarray.DataArray object. *
    
    ARGUMENTS:
    ---
    ds = [xr.Dataset] dataset object representing a SNAP 'cleaned, stacked, prepped' WRF NetCDF file
    
    RETURNS:
    ---
    affine transform for the xr.dataset passed to the function

    '''
    lon = ds.xc.values
    lat = ds.yc.values
    lonres, latres = np.diff(lon)[0], np.diff(lat)[0]
    x0,y0 = np.array( lon.min()-(lonres/2.)), np.array(lat.max()+(latres/2.) )
    return rasterio.transform.from_origin( x0, y0, np.abs(lonres), np.abs(latres) )

if __name__ == '__main__':
    import os, rasterio, subprocess
    import xarray as xr
    import numpy as np
    import argparse

    parser = argparse.ArgumentParser( 
        prog='extract_wrf_to_gtiffs',
        description='''extract all layers along the time dimension in an HOURLY 
                        SNAP-prepped NetCDF file to compliant GeoTIFFs''',
        )
    parser.add_argument('-fn', '--fn', dest='fn', type=str, help='filename (including full path) of the SNAP-cleaned WRF NetCDF file to extract to individual GeoTIFFs')
    parser.add_argument('-o', '--out_path', dest='out_path', type=str, help='full directory path to output directory to dump the resulting GeoTIFF files')
    parser.add_argument('-v', '--variable', dest='variable', default=None, type=str, help='[optional] abbreviated name of the variable to be extracted from the NetCDF file. -- i.e. t2, pcpt')

    args = parser.parse_args()
    fn = args.fn
    variable = args.variable
    out_path = args.out_path

    # pull the variable name from the filename if it is not given.
    if variable is None:
        variable = os.path.basename(fn).split('_')[0]

    # filename-fu **this will only work with the standard WRF naming convention**
    out_fn_base = '_'.join(os.path.basename(fn).split('.')[0].split('_')[1:-1])
    out_fn_base = '_'.join(['{}',out_fn_base,'{}.tif'])

    # read in the data
    ds = xr.open_dataset(fn)
    da = ds[variable]
    count, height, width = da.shape # these info are needed for the meta header

    # get the affine transform to be passed into the GTiff
    transform = affine_from_wrfds(ds)

    # get the time variable and format it 
    # this turns the data into a Month-Day-Year-Hour format.  This can be re-ordered as necessary.
    times = da.time.to_index().strftime('%m-%d-%Y-%H') 

    # make a rasterio metadata dict to be passed into the GTiff header
    # NOTE: this is the actual proj4string for the WRF data: 
    #    '+units=m +proj=stere +lat_ts=64.0 +lon_0=-152.0 +lat_0=90.0 +x_0=0 +y_0=0 +a=6370000 +b=6370000'
    meta = {
        'compress':'lzw',
        'height':height,
        'width':width,
        'count':1, # this can change based on the number of layers being stacked into the resulting GTiff
        'driver':'GTiff',
        'transform':transform,
        'crs':rasterio.crs.CRS.from_string(ds.proj_parameters),
        'dtype':'float32',
        'nodata':None # <- this can be changed depending on the variable being worked with.
    }

    # make a list of output filenames. <-- this is clunky, but works.
    out_filenames = [os.path.join(out_path, out_fn_base.format(variable, i)) for i in times]

    # loop through the files and dump to disk
    for i in range(count):
        out_fn = out_filenames[i]
        print(out_fn)
        out_arr = da.isel(time=i).values.copy()
        with rasterio.open(out_fn, 'w', **meta) as out:
            out.write(out_arr.astype(np.float32), 1)

    # cleanup
    ds.close(); ds=None; da=None


# REMOVE WHEN DONE:
# # this is a cleaned/stacked/updated flipped
# fn = '/workspace/Shared/Tech_Projects/wrf_data/project_data/wrf_data/hourly_fix/t2/t2_hourly_wrf_ERA-Interim_historical_1980.nc'
# variable = 't2'
# out_path = '/workspace/Shared/Tech_Projects/wrf_data/project_data/test_to_gtiff'

