# Sparkify Data Analysis and Visualization Project

## Project Overview
The Sparkify project aims to analyze and visualize user interactions with the Sparkify music streaming service. By processing log data, we extract insights into user behavior, popular songs, and artists. The project involves setting up a data pipeline using AWS services, MongoDB, and Flask to create an interactive web application for data visualization.

## Architecture
The project architecture consists of the following components:

1. **Data Storage**: User activity logs are stored in AWS S3 buckets.
2. **Data Processing**: AWS EMR clusters are used to process the log data using MapReduce with Python and PySpark.
3. **Database**: Processed data is stored in a MongoDB database hosted on an AWS EC2 instance.
4. **Web Application**: A Flask web application retrieves data from MongoDB and presents visualizations of user interactions.

## Technologies Used
- **Programming Languages**: Python
- **Data Storage and Processing**:
  - AWS S3
  - AWS EMR
  - MongoDB
- **Web Framework**: Flask
- **Libraries**:
  - Boto3 (AWS SDK for Python)
  - PySpark
  - IPython Parallel
