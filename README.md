## TB Trends Analysis Dashboard

## Overview

This TB Trends Analysis Dashboard is a web application designed to facilitate the exploration, analysis, and visualization of historical tuberculosis (TB) data. Leveraging data from the World Health Organization (WHO), this application provides powerful tools for identifying patterns, trends, and correlations within TB data across different demographics and regions.

## Goal

The primary goal of this application is to empower students, researchers, public health officials, and policymakers with actionable insights into the epidemiology of TB. By providing a user-friendly interface for complex data queries and interactive visualizations, the application aims to promote effective TB control and prevention efforts worldwide.

## Intended Audience

- **Students and Educators**: For educational purposes, aiding in the study and understanding of TB trends over time.
- **Researchers**: To analyze historical TB data for academic and scientific studies.
- **Public Health Officials**: For planning, implementing, and evaluating TB control and prevention programs.
- **Policymakers**: To inform policy decisions based on data-driven insights into TB trends.

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- Pip (Python package manager)

### Setting Up the Environment

1. **Clone the Repository**: Start by cloning this repository to your local machine.

   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**: Change into the project directory.

   ```bash
   cd Tuberculosis-Trends
   ```

3. **Create a Virtual Environment**: Use Python to create a virtual environment for the project dependencies.

   ```bash
   python3 -m venv my_dash_env
   ```

4. **Activate the Virtual Environment**:

   - On macOS/Linux:
     ```bash
     source my_dash_env/bin/activate
     ```

### Installing Dependencies

With the virtual environment activated, install the required Python packages using pip.

1. **Install Dash and Plotly**:

   ```bash
   pip install dash plotly
   ```

2. **Verify Installation**: Ensure that Dash and Plotly have been installed correctly.

   ```bash
   python -c "import dash; print(dash.__version__)"
   python -c "import plotly; print(plotly.__version__)"
   ```

### Running the Application

1. **Navigate to the `src` Directory**: Where the `app.py` file is located.

   ```bash
   cd src
   ```

2. **Start the Dash Application**:

   ```bash
   python app.py
   ```

3. **Access the Dashboard**: Open a web browser and navigate to `http://127.0.0.1:8050/` to view the dashboard.

## Contributing

We welcome contributions from the community. If you're interested in contributing to the TB Trends Analysis Dashboard, please read our contributing guidelines and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
