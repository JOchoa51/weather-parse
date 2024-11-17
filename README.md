# Weather Station Data Parser and Organizer

This project is a Python-based tool designed to parse weather station data from a CSV file containing HTML strings, download relevant data files, and organize them into structured Excel files for further analysis. It supports managing data by geographic states and operational statuses of the stations.

## Features

- **HTML Parsing**: Extracts hyperlinks, titles, and metadata from HTML strings.
- **Data Retrieval**: Downloads weather data files from parsed URLs using randomized user-agent headers for added security.
- **File Organization**:
  - Classifies files by geographic states and operational statuses (e.g., "Operando" or "Suspendida").
  - Stores parsed data in individual Excel files for each state.
- **Excel Integration**: Writes organized data into structured Excel files using `pandas` and `openpyxl`.
- **Duplicate Handling**: Ensures no duplicate data is processed or stored.
- **Performance Metrics**: Measures and displays the time taken for execution.

## Requirements

- Python 3.x
- Required Libraries:
  - `pandas`
  - `bs4` (BeautifulSoup)
  - `requests`
  - `openpyxl`
  - `xlsxwriter`
  - `getuseragent`

## Installation

1. Clone or download the repository.
2. Install the required libraries:
   ```bash
   pip install pandas beautifulsoup4 requests openpyxl xlsxwriter getuseragent
   ```
3. Place your input CSV file (`interseccion2.csv`) in the project directory.

## Input Data Format

The input CSV file should include the following columns:
- `description`: Contains HTML strings with links and metadata.
- `Name`, `Status`, `layer`: Additional metadata about the weather stations.
- `x`, `y`: Coordinates of the stations.

## Usage

1. Run the script:
   ```bash
   python hrefSeparator.py
   ```
2. The script will:
   - Parse the HTML strings to extract data.
   - Download files for operational and suspended weather stations.
   - Save organized data into Excel files in the `Results` directory.

## Output

- **`intersectionLinks.xlsx`**: A summary of parsed links and metadata.
- **State-wise Excel Files**: Individual files for each state containing the organized weather data.
- **Error Logs**: A text file (`Not Found.txt`) listing any missing or inaccessible files.

## Notes

- Ensure the `Files` directory exists for downloaded files.
- The script checks and avoids overwriting existing files unless necessary.
- Execution time is displayed at the end of the process.

## Contact

For questions or support, please contact:  
Jesús Ochoa Contreras  
ochoacontrerasjesus8@gmail.com
