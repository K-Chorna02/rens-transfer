# 180DC Project - Dashboard

This project is a dashboard for RENS designed to upload and visualise their data.


## Tech Stack

- Flask backend  
- Plotly (Python) generates graph data and transfers it to JSON  
- Plotly (JavaScript) renders graphs from JSON on the client side (browser)  
- Flask-Login for authentication, requiring login for all graph URLs except those made public  
- CSV-based data input
  
## Functionality

### Autumn Cycle (Oct 2025)
Initial dashboard implementation with core features:

- Flask application serving Plotly graphs on individual URLs  
- Database design for storing data and graph configurations  
- Login system (info stored in database) with protected graph access  
- Public/private toggle for graph visibility  
- Basic set of visualisations  

---

### Spring Cycle (March 2026)
Redesign and feature improvements to enhance usability and accessibility:

- RENS branding applied across the dashboard  
- Revised and updated visualisations, including removal of redundant graphs and addition of new chart types such as heatmaps (old graphs are commented out)
- Front-end CSV upload 
- Automated data validation and basic cleaning (column checks, data types) for uploaded data 
- Error handling for missing or incorrectly formatted data  
- Dashboard aligned with updated CSV structure  
- Automatic updates of all visualisations after data upload
- Ability to embed graphs on external stakeholder websites  


