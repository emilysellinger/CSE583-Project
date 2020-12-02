# Component Specification
## Components
**E-bird Data Cleanup**  
We use a script to reduce the E-bird sighting dataset from January 2020 to November 2020 in Oregon. For this project we are focusing on permanent Oregon resident species. 
This script does the following: 
- Load the data as a pandas dataframe.
- Remove extraneous columns from the dataset such as “Has Media”, “Trip Comments” and “Species Comments.”
- Subset the pandas dataframe according to resident status. For each species in the dataframe. 
  - Create a list of Oregon resident species.
  - For each entry in the dataframe, if the species matches a resident species in our list, append the sighting to a new pandas dataframe that only contains residents.
  - Save our resident dataframe for analysis.

**Air Quality Data Cleanup**  
- For each station and day, calculate the average 24-hour PM2.5 concentration using the hourly data.
- Create a list of the EPA’s PM2.5 breakpoint table for AQI.
- From the average PM2.5 concentrations, determine the day’s AQI category.
- A new pandas dataframe  includes the day, site ID, site latitude and longitude, average 24 hour PM2.5 concentration, and daily AQI category.
- Save this dataframe for analysis.
- An additional dataframe will be created with the average AQI for the state of Oregon for each day of the study period.

**Visualization of Data**  
A variety of interactive maps and plots will be used to visualize the effects of air quality on resident bird sightings in Oregon. These visualizations include:
- A map of Oregon with shaded regions representing different AQIs as well as icons representing bird sightings (and number of bird sightings) for resident bird species. This map will have a time slider that will allow the user to see how air quality and sightings change from day to day between January 2020 and November 2020. Additionally, it will have the ability to select which bird species the user wants to view.
- A chart of the number of sightings for various Oregon resident species over time. Icons on this chart will indicate days with AQIs in the Very Unhealthy and Hazardous categories, as a proxy for fire events. For this chart, the sightings and air quality will be grouped by region, and the user will have the option of seeing the data for all of Oregon or selecting just their region of interest from a drop down menu.

Python packages used:
- Plotly

**Web-based application for sharing of visualizations**  
The interactive visualizations created through plotly will be organized into a dashboard using dash, and this can be shared and embedded using html code.

Python packages used:
- Dash

## Interactions
**Birder:** 
A birder who lives in an area that was hard hit by the Oregon wildfires this summer is noticing that she is seeing less American crows this month than usual. She goes onto the Portland Audubon society website and finds the PHOENIX dashboard. She notices that this species disappeared almost completely after the wildfires in her area, but that they are still commonly sighted across Oregon. She feels relieved that it seems like they are returning to her area.

## List of Tasks (in priority order):  
Week 1
- Submit software design documents
- Air Quality data retrieval
- Create environment.yml
- Add license information to repo
- Data Cleanup
  - Air Quality
  - eBird Sightings
- Compile list of resident bird species
- Determine stat analysis for 1st use case

Week 2
- Link Travis CI to repo
- Visualization skeleton for use cases
  - Graphs for researchers
  - Dashboard for birders
- Code quality and comments

Week 3
- Add needed unit tests
- Ensure code is properly commented
- Prepare for project previews

Week 4
- Present project preview
  - Make any code updates following project previews
  - Update software design documents and README.md file to reflect current project direction
- Practice for final project presentation
