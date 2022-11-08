# Software Design

## User Stories
#### Who is the user?
- What do they want to do with the tool?
- What needs and desires do they want for the tool?
- What is their skill level?

#### Researcher working with visible spectrum (Researcher in Built Environments)
- Get solar spectra to input into building simulation
- Get spectra ranging from 380 to 780nm given a (or, series of) time input
- Graduate student - graduate school level in other fields than CS

#### Broad Researcher (skin cancer, solar panels, evapotranspiration rates, etc.)
- Get solar spectra for research applications
- Get larger range of solar spectra (~300 - 1000nm)
- Familiarity with programming/lacking expertise.

#### Open source contributor (technician / evaluator)
- Improve software in some way
	- Improving precision or reducing complexity
	- Test model in different locations
- Very familiar with programming/software design  
  
  

## Use Cases
- Researcher in Built Environments
	- Input weather data (enumerated over time period t)
	- Input desired spectral range (month/date/hour)
	- Return spectral value (380-780nm) (vector) given t (or ts) in .csv format
- Broad Researcher
	- Input weather data (enumerated at time period t)
	- Return larger spectral value (~300 to 1000nm) given t (or ts) in .csv format
- Open Source Contributor
	- Input weather data (from other location / or with other weather data inputs than what we chose)
		- Maybe there will be a sample data for them to check the code only
	- Check the code to see how it’s being performed / what ML model is being used
		- Ask for improvements via git issue
	- Return graph of MSE / confidence intervals (if evaluated with different data) 
  

## Components
- Input Data (weather as set of vectors over time interval)
	- User’s weather data - used to generate estimates of solar spectra
- Model parameters
	- Parameters found through ML training - used to estimate solar spectra
- Train/test model code
	- Code that originally trained model and found estimation parameters
	- Will need to match solar spectra data to weather data
	- ML approach to train model
- User interface? (If we have time)
	- Is it a dashboard? Is it a python package? Just a bunch of code in github?
- Function - Input weather data
	- Change .csv to pandas dataframe
	- Combine based on same timeseries
- Function - Input time period
	- Output series of time periods given start and end date
- Function - Input spectral range (used for output spectral range)
	- Create range to put into the output
- Function
	- Output series of vector of spectra data