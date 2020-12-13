### Ocean's 4 Capstone CSE583 Project
# Phoenix 
[![Build Status](https://travis-ci.org/emilysellinger/Phoenix.svg?branch=main)](https://travis-ci.org/emilysellinger/Phoenix) [![Coverage Status](https://coveralls.io/repos/github/emilysellinger/Phoenix/badge.svg?branch=main)](https://coveralls.io/github/emilysellinger/Phoenix?branch=main)

## An investigation into the impact of air quality on bird observation counts

Phoenix offers an introductory exploration of how air quality surrounding the 2020 Oregon wildfire events impacted bird observations in the state. 

As 2020 highlighted, larger wildfires and longer fire seasons are increasingly likely in the Western U.S. under climate change. While the direct effects of fire are apparent, the secondary effect of smoke on avian ecology is somewhat elusive. In general, birds tend to be very susceptible to air contamination and are highly mobile. Paired with a constantly shifting distribution of air particles, this makes for a spatially and temporally difficult interaction to study. Using detailed citizen scientist data from eBird and air quality data from the Oregon Department of Environmental Quality, Phoenix is a first step in examining this dynamic. 

Phoenix presents an initial analysis of bird sightings (segmented by species, family, or class) against PM2.5 air quality levels for researchers and those familiar with statistical analyses. Additionally, Phoenix prioritizes scientific communication and community engagement: it includes a visualization mapping tool to be accessed by recreational birders. If made widely available as an interactive map on a website, birders will be able to use this information to gain a better understanding of how to adjust their practices and get the most out of their experience.

## Organization
The project has the following structure:
<pre>Phoenix/
  |- README.md
  |- phoenix/
     |- data/
        |-Daily_Avg_PM2.5_Location.csv
        |- ORAQ_StationCounties.csv
        |- OR_DailyAQ_byCounty.csv
        |- Oregon_Resident_Species.md
        |- Oregon_counties_map.geojson
        |- PM2.5_metadata.txt
        |- shortened_bird_data.csv
     |- demos/
        |- Dash_App_Demo.mp4
        |- Researcher_Demo_Altair_Visualizations.ipynb
        |- Researcher_Demo_Data_Cleaning.ipynb
     |- code/
        |- air_quality_knn.py
        |- app.py
        |- appfunctions.py
        |- data_cleaning.py
     |- tests/
        |- test_air_quality_knn.py
        |- test_app_functions.py
  |- docs/
     |- ComponentSpecification.md
     |- FunctionalSpecification.md
     |- TechnologyReview.pdf
     |- Presentation.pdf
  |- .gitignore
  |- .travis.yml
  |- License.md
  |- environment.yml
</pre>
## Installation
First, you will need an installation of `conda`. There are several ways to achieve this, which you can find at: https://docs.conda.io/projects/conda/en/latest/user-guide/install/

To install `Phoenix` you will need to first clone the repository onto your own computer using the following `git` command in the terminal at the directory you wish to install to:  
<pre>git clone https://github.com/emilysellinger/Phoenix.git</pre>

Next, you will need to have all of the software dependencies needed for `Phoenix` to run. The best way to do this is to use the virtual environment created for this project. You can create the `Phoenix` virtual environment on your computer by using the following command:
<pre>conda env create -f environment.yml</pre>

To begin using this environment, activate it with
<pre>conda activate project_CSE583</pre>

## How to Use Phoenix
Researchers should look to our demo jupyter notebook, where you can find a more detailed description of our analysis, as well as accompanying visualizations.Phoenix uses Altair for statistical visualizations, the code for which can be easily adapted for future research.

For recreational birders, we provide a dash app where you can explore resident species observations and air quaility index (AQI) at several geographic and taxonomic levels.

## Data Sources
### eBird Basic Dataset
- A comprehensive birding dataset that includes checklist and observation data submitted by citizen scientists and volunteers on the widely-used [eBird](https://ebird.org/home) app.
- This data is hosted and managed by the Cornell Lab of Ornithology and can be found at: https://ebird.org/science/download-ebird-data-products
- Citation: *eBird Basic Dataset. Version: EBD_relSept2020. Cornell Lab of Ornithology, Ithaca, NY. Oct 2020.*

### Oregon Department of Environmental Quality Station Reports
- Hourly air quality reports for monitoring stations across the state of Oregon. The PM2.5 data averaged over each day is the only air quality metric used for this project.
- This data is hosted and managed by the Oregon Department of Environmental Quality and can be found at: https://oraqi.deq.state.or.us/report/SingleStationReport 

## Limitations
This software is designed for exclusive use with the cleaned Oregon eBird and air quality datasets for 2020. 

The Phoenix repository will no longer be maintained beyond 2020. 
