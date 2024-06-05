This Streamlit application is a multi-page dashboard that includes various features such as weather data visualization and route mapping using GeoJSON information. The application is structured with a sidebar for easy navigation between different pages.

Features
Home Page: A welcome page for the application.
Weather Dashboard: Displays weather data for selected cities, including daily, weekly, and monthly visualizations.
Route Map: Allows users to select multiple cities and visualize routes between them on a map using GeoJSON information.
Additional Page: Placeholder for additional pages or features.
Installation
To run this application, you need to have Python installed. Follow the steps below to set up and run the application.

1. clone this repo and install the requirements
2. configure the yaml with the necessary configuration
3. note that the path configuration accepts any spark format to scale the pipeline
4. Note that spark also will need to be able to operate with delta tables
5. It's better to configure spark operability with delta tables on spark environment itself and not hardcode
6. setup a job for weather ingestion using spark-submit to the cluster you want
7. run the streamlit dashboard when you need info on directions or weather

TODO:
1. Integrate traffic info with weather infos
2. Orchestrate spark job and streamlit run in airflow
