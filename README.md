# Efficient-resampling-of-sensor-signals
Efficient Resampling of Recorded Inertial Sensor Signals

# 1. Py_resample 
  is a python module that performs resampling using Sic Interpolation and Decimation along with Anti-Aliasing filter.

  usage: resample.py [-h] file_path filename rate

  positional arguments:
    * file_path   Path to the input file
    * filename    Input filename
    * rate        New Sample Rate

  optional arguments:
    -h, --help  show this help message and exit
  
  execution command from terminal: python -m py_resample.resample <file_path><file name> <target frequency>
  
-----------------------------------------------------------------------------------------------------------------------

# 2. mat_resample 
  contains .m files, that perform resampling using Sic Interpolation and Decimation along with Anti-Aliasing filter.

  usage: resample() from command window in MATLAB

  arguments:
  * file_path   		Path to the input file
  * filename       	Input filename
  * current_frequency 	Sample Rate of the sensor data
  * target_frequency	Sample rate the data must be resampled to

  execution command from MATLAB command window: resample <file_path> <filename> <current_frequency> <target_frequency>

------------------------------------------------------------------------------------------------------------------------

# 3. MATLAB_resample 
  contain .m file, that performs resampling using MATLAB resample function

  usage: mresample() from command window in MATLAB

  arguments:
  * file_path   		Path to the input file
    * filename       	Input filename
    * current_frequency 	Sample Rate of the sensor data
    * target_frequency	Sample rate the data must be resampled to

  execution command from MATLAB command window: mresample <file_path> <filename> <current_frequency> <target_frequency>
