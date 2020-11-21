# Functional Specification
## Background
Under climate change, the likelihood of larger wildfires and longer fire seasons in the Western United States is projected to increase. This has already been realized in the past few years, when record-setting fire and smoke events have had considerable impact on the communities and ecology of these regions. To better understand the environmental consequences of future fires, it is useful to examine the outcomes of the recent ones.

We decided that an accessible and meaningful way to do this is to investigate the occurrences of bird observations before, during, and after a wildfire event in a given region. In particular, we are interested in the interaction between avian ecology and air quality as indirect impacts of wildfire, since it is apparent that the fires themselves can displace bird populations and result in direct mortality. In general, birds tend to be more susceptible to air contamination due to the anatomy of their respiratory systems—a well-known example of this is the use of canaries to warn coal miners of the presence of dangerous gases. And in studies of captive birds and poultry, exposure to smoke has resulted in damaged lung tissue and respiratory infections. 

However, the response and movement of a wild bird population as a result of smoke is not well understood and more difficult to study in detail. The distribution of individuals and air particles is constantly shifting and there may be a variety of behaviors between different taxonomic groups. Describing the regional movement patterns of a species or family, therefore, would be a useful step in understanding the avian ecology of a region impacted by wildfires.

Using detailed citizen scientist data from eBird and air quality data from the Oregon Department of Environmental Quality, we aim to perform an initial analysis and visualization of bird observation data against PM2.5 (particulate matter with diameters less than 2.5 micrometers). Due to their recency and significant air quality impact, we seek to provide insight into how the 2020 Oregon wildfires may have impacted observations in the state.

Although this project is motivated from a research perspective, the visualization tool is intended to be accessed by recreational birders, citizen scientists, and Audubon societies. If made widely available as an interactive map on a website, birders will be able to use this information to gain a better understanding of how to adjust their practices and get the most out of their experience.

## Data Sources
**eBird:** All bird sightings/identifications in Oregon from January through November 2020, acquired as raw data from eBird's database (maintained by Cornell Lab of Ornithology). Bird identifications are logged by users on their mobile device, and each datapoint includes a geolocation and bird ID, along with a suite of additional anonymized user and locale identifiers.

**Air Quality (PM 2.5):** The State of Oregon's Department of Environmental Quality maintains a database of hourly records of the air quality metric most closely associated with wildfires – concentration of particulate matter less than 2.5 micrometers in size. These records are collected at fifty different active monitoring stations across the state.

## Users
*Our target users are individuals interested in bird species' populations and geographies for research and/or recreational purposes. We are initially targeting two user types:*

**Ecological Researcher**  
Ecologists interested in utilizing our data synthesis will likely have some background in using data sharing, statistical, and graphical user interfaces. However, since ecologists are predominantly trained in R, whereas our tool is built in Python, our goal is to minimize the extent to which they must be familiar with this particular language. The domain knowledge needed to use this tool for answering specific research questions is a working knowledge of the taxonomic organization of birds, as well as typical migratory and occupancy patterns for species of interest.

**Recreational Birder**  
Birders will only need prior experience with graphical user interfaces to utilize our visualization tool. We plan to make our tool as user-friendly as possibly by color-coding air quality based on level of risk and translating PM 2.5 values to AQI risk designations (e.g., Low, Unhealthy for Sensitive Groups) to align our designations with those commonly seen in mainstream media. These users' necessary domain knowledge will include the locale they are interested in visualizing, and specific species' names if they intend to narrow the visualization to their favored species.

## Use Cases
**Ecological Researcher**  
Researchers interested in the effects of poor air quality from wildfires on bird species' distributions will likely have questions regarding impacts on particular species or by higher levels of taxonomic organization. For example, if a researcher is interested in the influence of air quality on raptor distribution across the state they could select raptors in our species selection list, select the regional designation as counties, and use our chart-based visualization tool to examine correlations between air quality, region, and raptor density.  

**Recreational Birder**  
We anticipate that avid birders will use our tool to visualize correlations between air quality and bird sightings at their favored birding locations. For example, a birder who is particularly keen to spot seabirds may wonder (a) if poor air quality leads to a decline in seabird sightings, and (b) how long it takes for species to return to areas they've vacated in the event of an extended poor air quality event. In our visualization map interface, this individual would first select only seabirds in the species selection list, then toggle the air quality index (AQI) slider between Low and Unhealthy or greater to examine how the frequency of seabird sightings changes with air quality. Next, they would set the starting date to mid-September (period of poorest air quality in Oregon due to wildfire smoke) and slide the visualization forward in time to look at how seabird sightings change with steadily improving air quality.
