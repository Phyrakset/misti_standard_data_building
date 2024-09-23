# MISTI Standard Data Collection and Analysis Platform

This platform is developed for data collection, management, analysis, and visualization of metrology instruments and related information under the Ministry of Industry, Science, Technology, and Innovation (MISTI).

## Table of Contents
- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Collection](#data-collection)
- [Data Analysis & Visualization](#data-analysis--visualization)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The MISTI Data Collection and Analysis Platform is a web-based application designed to handle various data submission processes and facilitate data analysis. Users can submit forms related to metrology, chemicals, machinery, and factory safety. The platform also provides features for data analysis and visualization to help MISTI departments make informed decisions.

## Directory Structure

project_directory/ │ ├── .streamlit/ # Streamlit config files ├── data/ # Folder to store collected data ├── images/ # Folder for images (e.g., logos) ├── misti_venv/ # Python virtual environment folder ├── scripts/ # Python scripts for form handling ├── pycache/ # Cache folder ├── .env # Environment variables file ├── .gitignore # Git ignore file ├── app.py # Main application entry point ├── config.py # Configuration settings for the app ├── README.md # Project guide and documentation ├── requirements.txt # List of required Python packages 

## Installation

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)
- `virtualenv` for managing the virtual environment

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/misti_standard_data_building.git
   cd misti_standard_data_building

2. **Create and activate a virtual environment**

 ```plaintext
    python -m venv misti_venv`
    source misti_venv/bin/activate  # For Linux/Mac
 ```
    # On Windows: misti_venv\Scripts\activate

3. **Install required dependencies**

    `pip install -r requirements.txt`

4. **Set up environment variables**

- Create a .env file and add necessary configuration such as database credentials, API keys, or secret tokens.

5 . **Run the application**

    `streamlit run app.py`
 Open your web browser and navigate to http://localhost:8501.

# Usage

## Submitting Forms

The application allows you to submit various forms for data collection. You can navigate to each form using the sidebar, select the type of form, and fill in the required details. Examples include:

- Metrology Applications
- Factory Inspection Reports
- Chemical Substance Registrations etc.

Each form submission is stored in the data/ directory in a structured format for later analysis.

## Data Collection

Navigate to the sidebar and select the form you need to submit.
Complete the form and hit the Submit button.
The collected data will be saved in the data/ folder in CSV format.

## Data Analysis & Visualization

1. Upload your collected data in the Data Analysis section.
2. You can perform various analyses, including:

- Viewing summary statistics
- Plotting data distributions
- Visualizing the correlation matrix

Data analysis features include basic visualizations such as histograms and correlation heatmaps using `Matplotlib` and `Seaborn`.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

# License
This project is licensed under the MIT License. See the LICENSE file for more details.


### Key Sections:
- **Project Overview**: A brief description of the project.
- **Directory Structure**: Lists important directories and files.
- **Installation**: Steps to set up the project locally.
- **Usage**: How to use the application for data collection and analysis.
- **Contributing**: Guidelines for contributing to the project.
- **License**: Licensing information.


