# SolarML

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
This project is an analysis project that aims to study if it is possible to accurately predict the solar spectra given atmospheric parameters. 

## Data
The training data comes from [NREL Solar Radiation Research Laboratory](https://midcdmz.nrel.gov/apps/sitehome.pl?site=BMS) where time interval data is saved. For this project, data from 2015 to 2021 is used. **Training data** is divided into two parts **(1) Atmospheric weather data**, and **(2) Continuous Solar spectra data**. 

### (1) Atmospheric Parameters
Atmospheric data used for training are specific data that contributes to color of the sky through scattering. 

#### A. [weather data](https://midcdmz.nrel.gov/apps/day.pl?BMS)
1. **Zenith Angle** 
2. **Azimuth Angle**
3. **Total Cloud Cover**: How much cloud there is in a fisheye image of the sky.
4. **Opaque Cloud Cover** How much thick cloud there is in a fisheye image of the sky.

#### B. [Aerosol Optical Depth (AOD)](https://midcdmz.nrel.gov/apps/daily.pl?site=AODSRRL1S&start=20150701&yr=2021&mo=9&dy=19) <br>
5. **AOD 400**: AOD is a measure of aerosols distributed within a column of air at a particular wavelength (i.e. 400nm). Measurement of Aerosols at different wavelength is related to the size distribution of the particles which affects scattering (thus color) of light.
6. **AOD 500**
7. **AOD 675**
8. **AOD 870**
9. **AOD 1020**
10. **SSA 675**: Single Scattering Albedo(SSA) represents the ratio of scattering efficiency to total extinction efficiency. Value of 1 means all particle extinction is due to scattering while 0 means all particle extinction is due to absorption. 675 represents SSA at 675nm wavelength.
11. **Asymmetry 675**: Value showing how much back scattering happens. 675 represents Asymmetry at 675nm wavelength.

#### C. [Precipitable Water](https://midcdmz.nrel.gov/apps/daily.pl?site=PWVSRRL&live=1)

12. **Precipitable Water**: This data represents how much water (in any form such as ice, water, water vapor etc.) is in a column of air.

Above 12 parameters are atmospheric weather data that is used to predict the solar spectra. Users are expected to input these parameters in order to get solar spectra as an output.

### (2) [Solar Spectra](https://midcdmz.nrel.gov/apps/spectra.pl?BMS)

This data shows radiation data (in unit of W/m<sup>2</sup>) for every nm. The wavelength ranges from 350nm to 1050nm. This spectral data represents the color of the sun.


