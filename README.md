# NEP36-CanOE Spatial Layer Outputs

__Main author:__  James Munroe

__Affiliation:__  Elemental Earth Data Ltd.

__Group:__        

__Location:__     

__Contact:__      e-mail: jmunroe@earthdata.ca | tel: 709-771-0450


- [Objective](#objective)
- [Summary](#summary)
- [Status](#status)
- [Contents](#contents)
  + [Subsections within contents](#subsections-within-contents)
- [Methods](#methods)
  + [Subsections within methods](#subsections-within-methods)
- [Requirements](#requirements)
- [Caveats](#caveats)
- [References](#references)


## Objective
Convert NEP36-CanOE climate model output into geotiff files for use on GIS-Hub.

## Summary
The numerical model produces NetCDF files. Users expect the data to be available as GeoTIFFs. 

## Status

Ongoing-improvements


## Contents

The script `extract_layers.py` computes the fall/winter and spring/summer means for the variables temp, salt, O2, NO3, PH, and speed. Both ocean surface and ocean bottom are extracted. For integrated primary production (ipp), the total primary production is integrated with depth. Mixed layer depth is also available.


## Methods

See associated Jupyter Notebook for details.


## Requirements

Assuming that the incoming the data is available locally, the following command will install the required software and
execute the script.

`$ conda env create`
`$ conda activate spatial-data`
`$ python extract_layers.py`

## Caveats

Expects the subdirectory `NEP36-CanOE` to be available.

## References

Key libraries:

- xarray [GitHub](ttps://github.com/pydata/xarray) [docs](http://xarray.pydata.org)
- rioxarray [GitHub](https://github.com/corteva/rioxarray) [docs](https://corteva.github.io/rioxarray)

