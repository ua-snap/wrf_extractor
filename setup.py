from setuptools import setup

dependencies_list = ['numpy','rasterio','pandas','xarray']
scripts_list = ['bin/extract_wrf_to_gtiffs.py']

classifiers = [ 'Development Status :: Beta',
				'Operating System :: POSIX :: Linux',
				'Environment :: Console',
				'Intended Audience :: Science/Research',
				'Intended Audience :: End Users/Desktop',
				'Topic :: Software Development :: Build Tools',
				'License :: OSI Approved :: MIT License',
				'Programming Language :: Python :: 3.5',
				'Natural Language :: English',
				'Operating System :: POSIX :: Linux',
				'Topic :: Scientific/Engineering :: GIS',
				'Topic :: Scientific/Engineering :: WRF Dynamically Downscaled Data for Alaska/Western Canada'	
				]

setup(	name='wrf_extractor',
		version='0.1',
		description='Tools to extract data from SNAP prepped and cleaned WRF Dynamically Downscaled NetCDF files',
		url='https://github.com/ua-snap/wrf_extractor',
		author='Michael Lindgren',
		author_email='malindgren@alaska.edu',
		license='MIT',
		packages=['wrf_extractor'],
		install_requires=dependencies_list,
		zip_safe=False,
		include_package_data=True,
		scripts=scripts_list,
		classifiers=classifiers	)