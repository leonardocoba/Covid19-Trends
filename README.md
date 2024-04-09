# TB Trends Analysis Dashboard

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
   git clone https://github.com/leonardocoba/Tuberculosis-Trends
   ```

2. **Navigate to the Project Directory**: Change into the project directory.

   ```bash
   cd Tuberculosis-Trends
   ```

3. **Create a Virtual Environment**: Use Python to create a virtual environment for the project dependencies.

   ```bash
   python -m venv my_dash_env
   ```

4. **Activate the Virtual Environment**:

   - On macOS/Linux:
     ```bash
     source my_dash_env/bin/activate
     ```

   - On Windows:
     ```cmd
     my_dash_env\Scripts\activate
     ```

### Installing Dependencies

With the virtual environment activated, install the required Python packages using pip.

1. **Install Dash and Plotly**:

   ```bash
   pip install dash  pandas plotly
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
   python index.py
   ```

3. **Access the Dashboard**: Open a web browser and navigate to `http://127.0.0.1:8050/` to view the dashboard.

### Database connection 

1. **Navigate to the `src` Directory**

   ```bash
   pip install cx_Oracle
   ```

2. **Install the lastest version of oracle instant client**: Unzip the the file into any directory on your system

   [Library Download](https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html)

3. **Add the directory to the PATH environment varaibles on your system**: Make sure to include the actual library folder in the directory path
   #### Windows

   1. **Open System Properties**:
      - Press `Win + Pause/Break` or right-click on `This PC` and select `Properties`.
      - Click on `Advanced system settings` on the left sidebar.

   2. **Open Environment Variables**:
      - In the System Properties window, click on the `Environment Variables...` button.

   3. **Edit PATH Variable**:
      - In the Environment Variables window, under the "System variables" section, locate and select the `Path` variable, then click `Edit...`.

   4. **Add Directory**:
      - Click `New` and then paste the path of the directory you want to add.

   5. **Save Changes**:
      - Click `OK` on all windows to save the changes.

   6. **Verify**:
      - Open a new Command Prompt window and type `echo %PATH%` to verify that the directory has been added to the PATH.

   #### macOS

   1. **Open Terminal**:
      - Press `Cmd + Space` to open Spotlight Search.
      - Type `Terminal` and press `Enter` to open Terminal.

   2. **Edit .bash_profile (or .zshrc for zsh users)**:
      - Type `nano ~/.bash_profile` (or `nano ~/.zshrc` if you're using zsh) and press `Enter`.

   3. **Add Directory to PATH**:
      - In the opened editor, go to the end of the file and add the following line:
      ```
      export PATH="$PATH:/path/to/your/directory"
      ```
     Replace `/path/to/your/directory` with the actual path of the directory you want to add.

   4. **Save Changes**:
      - Press `Ctrl + X` to exit, then press `Y` to confirm changes, and finally press `Enter` to save the file.

   5. **Apply Changes**:
      - In Terminal, type `source ~/.bash_profile` (or `source ~/.zshrc` for zsh users) to apply the changes to your current session.

   6. **Verify**:
      - Type `echo $PATH` to verify that the directory has been added to the PATH.

4. **Edit Routes.py**
      - Replace line 2: "instant client path" with your instant client library absolute path
      - Replace line 6: "UF USERNAME" with your UFL username
      - Replace line 7: "CISE oracle password" with your CISE oracle password
         - Your password can be found by naviagting to the Manage Databases tab and selecting Oracle from this URL: https://register.cise.ufl.edu/

## License

This project is licensed under the MIT License - see the LICENSE file for details.

