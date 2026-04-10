RENS Project Approach - Oct 2025.

STACK:
- Flask backend. 
- Plotly python library generates graph information and transfers it to JSON.
- Plotly javascript library renders graph from JSON on client side (browser).
- flask-login will require logging in for all graph urls EXCEPT those selected.

APPROACH:
- 10/11 roughly decide what sort of visualisations we will want in the final dashboard.
- 10/11 keep the intended audience in mind for designing visualisations.
- 10/11 data pre-processing.
- 10/11 data visualisation.
- 10/11 (provisional) flask app will serve Plotly graphs, each on its own URL.
- 10/11 designing database structure
- build a database to hold charity information (and graph information.)
- csv upload page, to introduce more data in the future.
- data pre-processing uses csv files and can upload at end. web development will design database with demo data
- page for managing which files should be public and which should be kept private.
- login page (info stored in database)

THINGS TO LEARN/UNDERSTAND:
- Basic understanding of Flask
- Learn PLOTLY IN PYTHON. Documentation online
- Basic understanding of CPanel
- brush up on SQL
- what kind of visualisations are we going to use?