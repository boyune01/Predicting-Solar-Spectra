# SolarML

[![Python Package using Conda](https://github.com/boyune01/Predicting-Solar-Spectra/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/boyune01/Predicting-Solar-Spectra/actions/workflows/python-package-conda.yml)

FINISH BY WEDNESDAY NIGHT

- Add tree (repository structure)
- Code quality
   - variables 1 letter
   - properly named variables / functions
   - is code easy to read?
   - Comments 
   - style (5 pts)
      - doc strings
      - triple doubles for doc strings
      - style checker

- test
    - mix of smoke / one shot / pattern test
    - each test function should test 1 test
    - Does unittest throughly cover all parts of the code?
    - Any code that reads in data / calculate not using ML should have tests
 
- continuous integration
    - add badge in the readme --> ??
    - code coverage badge? (for unittest)
    - do you have CI hub?

- Update design docs
    - use cases
    - inputs / outputs / data types
    - documentation? (To pull down repository and run the code --> should be in the readme)
   
    


INCLUDE
- What it does
- sortware dependencies
- Instructions on how to use the code
- Examples --> how to work with package
**

## Project Description
This analysis project seeks to build a model to accurately predict solar spectra given atmospheric parameters. Atmospheric data are recorded more often and in more places than solar spectral data. Currently, physics-based models are able to predict solar spectra based on atmospheric inputs, but are computationally expensive and only perform well within a select range of atmospheric conditions. This project seeks to streamline this process by using machine learning models to analyze the effect of atmospheric data on solar spectra and generate estimation paramaeters, allowing researchers to easily and accurately predict spectral data based on these atmospheric data, and incorporate solar spectra into analyses without the time and cost intensive need to collect or acquire spectral data themselves. These fields could include (but are not limited to) climate science, public health, built environments, photovoltaics, and agronomy. 

## Data
The training data comes from [NREL Solar Radiation Research Laboratory](https://midcdmz.nrel.gov/apps/sitehome.pl?site=BMS) where time interval data is saved. For this project, data from 2015 to 2021 is used, with records taken every half hour. **Training data** is divided into two parts **(1) Atmospheric weather data**, and **(2) Continuous Solar spectra data**. 

### (1) Atmospheric Parameters
Atmospheric data used for training are specific data that contributes to color of the sky through scattering. 

#### A. [weather data](https://midcdmz.nrel.gov/apps/day.pl?BMS)
1. **Zenith Angle** The angle between the sun and the vertical (degrees)
2. **Azimuth Angle** The angle between true North and the sun (degrees)
3. **Total Cloud Cover** How much cloud there is in a fisheye image of the sky (percentage)
4. **Opaque Cloud Cover** How much thick cloud there is in a fisheye image of the sky (percentage)

#### B. [Aerosol Optical Depth (AOD)](https://midcdmz.nrel.gov/apps/daily.pl?site=AODSRRL1S&start=20150701&yr=2021&mo=9&dy=19) <br>
AOD is a measure of aerosols distributed within a column of air at a particular wavelength (i.e. 400nm). Measurement of Aerosols at different wavelength is related to the size distribution of the particles which affects scattering (thus color) of light. The following wavelengths are accounted for as separate variables in the training data:

5. **AOD** (400nm)
6. **AOD** (500nm)
7. **AOD** (675nm)
8. **AOD** (870nm)
9. **AOD** (1020nm)

#### C. [Additional Scattering Data](https://midcdmz.nrel.gov/apps/daily.pl?site=AODSRRL1S&start=20150701&yr=2021&mo=9&dy=19) <br>
10. **Single Scattering Albedo** (or **SSA**) represents the ratio of scattering efficiency to total extinction efficiency. Value of 1 means all particle extinction is due to scattering while 0 means all particle extinction is due to absorption. 675 represents SSA at 675nm wavelength.
11. **Asymmetry** Value showing how much back scattering happens. 675 represents Asymmetry at 675nm wavelength.

#### D. [Precipitable Water](https://midcdmz.nrel.gov/apps/daily.pl?site=PWVSRRL&live=1)

12. **Precipitable Water** This data represents how much water (in any form such as ice, water, water vapor etc.) is in a column of air (millimeters)

Above 12 parameters are atmospheric weather data that is used to predict the solar spectra. Users are expected to input these parameters in order to get solar spectra as an output.

### (2) [Solar Spectra](https://midcdmz.nrel.gov/apps/spectra.pl?BMS)

This data shows radiation data (in unit of W/m<sup>2</sup>) for every nm. The wavelength ranges from 350nm to 1050nm. This spectral data represents the color of the sun.

For linear regression analysis, a the range of wavelength measurements comprising the solar spectra at each time interval are compressed into a single scalar value. **Correlated Color Temperature** (or **CCT**) provides a single value which corresponds to the predominant color of light as the sun's angle and other atmospheric conditions change over time. 

## Software

The modules included in this package are designed to be run via python on any atmospheric data containing the variables specifed above. The predict function requires only that the pandas (1.5.1) package be installed. Evaluation of the modeling code itself additionally requires the following packages: pytorch (1.13.0), scikit-learn (1.1.3), scipy (1.9.3), seaborn (0.12.1) and statsmodels (0.13.2).

Execution of prediction code will require variables to be named precisely. The list below specifes the necessary variable names. 

1. **Zenith Angle** - "Zenith Angle [degrees]"
2. **Azimuth Angle** - "Azimuth Angle [degrees]"
3. **Total Cloud Cover** - "Total Cloud Cover [%]"
4. **Opaque Cloud Cover** - "Opaque Cloud Cover [%]"
5. **AOD** (400nm) - "AOD [400nm]"
6. **AOD** (500nm) - "AOD [500nm]"
7. **AOD** (675nm) - "AOD [675nm]"
8. **AOD** (870nm) - "AOD [870nm]"
9. **AOD** (1020nm) - "AOD [1020nm]"
10. **SSA** - "SSA [675nm]"
11. **Asymmetry** - "Asymmetry [675nm]"
12. **Precipitable Water** - "Precipitable Water [mm]"
