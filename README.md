[![DOI](https://zenodo.org/badge/252537964.svg)](https://zenodo.org/badge/latestdoi/252537964)

# Correlation of the development of COVID-19 cases/deaths and the Gold price

The global Corona crisis 2020 not only has a huge impact on health systems around the world, but also on the economic situation. Gold is traditionally known to be a go-to asset in times of crisis and uncertainty and its price therefore usually increases when stock indices collapse. However, the Austrian newspaper Kurier published an article [1] claiming that current market activity during the Corona crisis contradicts this theory. They also state that the gold price will stabilize again in the medium term as this also happened on other occasions.

This experiment aims at a data-driven approach to make validations of these assumptions easier. The development of the number of Corona cases and deaths in each country over time is compared to the corresponding gold prices. There are two outputs per country: A CSV file with the raw data and a diagram visualizing that data. Since we have not yet overcome the current situation, validating assumptions about medium-term consequences on the gold price cannot be made now, but might be with future data.

## Prerequisites

The following folders contain data and their existence should be verified before starting the analysis:

* `data/raw`
    * `data/raw/COVID-19` - Folder storing the dataset about Corona cases
    * `data/raw/Gold` - Folder storing the dataset about the Gold prices
* `data/output` - Folder where analysis results will be stored

## Data Sources

* COVID-19 data: European Centre For Disease Prevention And Control (2020) "Sonraí faoi choróinvíreas COVID-19". Publications Office. doi: 10.2906/101099100099/1. (Accessed on 02.04.2020 at https://data.europa.eu/euodp/de/data/dataset/covid-19-coronavirus-data/resource/260bbbde-2316-40eb-aec3-7cd7bfc2f590)
* Gold prices: ariva.de, downloaded freely from https://www.ariva.de/goldpreis-gold-kurs/historische_kurse?boerse_id=130&currency=USD with data between 01.01.2020 and 31.03.2020 (Accessed on 03.03.2020)  
The gold price values originate from FXCM (https://www.fxcm.com/uk/).


## Starting the analysis

Python 3 is needed to run the analysis. Additionally, the dependencies `pandas` and `matplotlib` are required. They can be installed with pip using the command `pip install pandas matplotlib`.

To preprocess the input data and merge both datasets, the `preprocess.py` script has to be run with the following command: 
`python preprocess.py <Path to the COVID-19 dataset> <Path to the Gold Price dataset> <STARTDATE> <ENDDATE>`
STARTDATE and ENDDATE define the timespan considered in the analysis. This script produces the intermediary (combined) dataset `preprocessed.csv` which is stored in the same directory as the script.

The command `python visualize.py ./preprocessed.csv <Path to output folder>` then produces the final output and creates the visualizations.

However, it is strongly recommended to use Docker deployment as specified in the next section.


### Docker

A `docker-compose.yml` file is provided which sets up the whole environment when starting with `docker-compose up` from within the folder. In this file, the start- and end-dates can be changed if necessary.
Two volumes are used to make the raw input data available to the container and to retrieve the computation results from outside the container. The location of the volumes on the host defaults to `./data/raw` and `./data/output` relative to the folder where the `docker-compose.yml` file is located.  
Please note that the computation can take a while and there are no visible log messages.


## Architecture
![Tool architecture](https://raw.githubusercontent.com/ludwig-burtscher/dss-ex1/master/documentation/architecture.png "Tool architecture")  
A detailed description of the tool can be found [here](https://github.com/ludwig-burtscher/dss-ex1/raw/master/documentation/overview.pdf "Overview") in `documentation/overview.pdf`.

## References
[1] https://kurier.at/wirtschaft/coronavirus-verliert-gold-seinen-ruf-als-krisenwaehrung/400787762
