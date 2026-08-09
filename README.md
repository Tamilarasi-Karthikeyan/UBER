# 🚗 Uber Business Intelligence & Analytics Dashboard

An interactive **Uber Business Intelligence dashboard** built with **Python, SQL, SQLite, Streamlit, and Plotly** to analyze ride performance, revenue, demand patterns, fare trends, payment methods, trip distances, and driver/vehicle performance.

The project transforms Uber trip data stored in a relational SQLite database into an executive-style analytics dashboard with interactive filters and data visualizations.

## 📊 Live Dashboard

🔗 **[View the Live Streamlit Dashboard](https://uber-data-analyst-project.streamlit.app/)**

## 📌 Project Overview

The **Uber Business Intelligence Dashboard** is designed to demonstrate how SQL-based data analysis can be combined with Python and interactive visualization tools to generate actionable business insights from ride-hailing data.

The application connects directly to a **SQLite database**, performs analytical queries using SQL, and presents the results through an interactive Streamlit dashboard.

Users can filter the data based on:

* Trip Status
* Payment Method
* Trip Distance
* Fare Amount
* Dashboard Theme

The dashboard dynamically updates its KPIs, charts, and data tables based on the selected filters.

## 🎯 Objectives

The main objectives of this project are to:

* Analyze Uber trip and ride performance data
* Identify ride-demand patterns throughout the day
* Analyze revenue and average fare performance
* Understand trip-distance distribution
* Compare fare trends against base fares
* Analyze payment-method performance
* Identify high-rated vehicle models
* Demonstrate practical SQL analytics
* Build an interactive Business Intelligence dashboard
* Present complex data in an executive-friendly format

## 🛠️ Technology Stack

| Technology    | Purpose                                     |
| ------------- | ------------------------------------------- |
| **Python**    | Application development and data processing |
| **SQL**       | Data querying and business analysis         |
| **SQLite**    | Relational database                         |
| **Streamlit** | Interactive dashboard development           |
| **Plotly**    | Interactive data visualization              |
| **KaggleHub** | Dataset acquisition                         |
| **Pandas**    | Data analysis and database inspection       |
| **HTML/CSS**  | Dashboard styling and custom UI             |

The project dependencies include Streamlit, Plotly, Pandas, KaggleHub and supporting Python packages.

## 📈 Dashboard Features

### 1. Executive KPI Dashboard

The dashboard provides high-level business metrics including:

* **Total Rides**
* **Gross Revenue**
* **Average Fare per Trip**
* **Average Trip Distance**
* **Average Surge Multiplier**

These KPIs are calculated dynamically using SQL queries against the SQLite database.

### 2. Interactive Data Filters

Users can dynamically filter the dashboard using:

* Trip Status
* Payment Method
* Trip Distance
* Fare Amount

The selected filters are converted into parameterized SQL conditions and applied across the dashboard's analytical queries.

### 3. Hourly Ride Demand

A bar chart analyzes the number of rides requested during each hour of the day.

**Business use case:**

This can help identify peak demand periods and support decisions related to driver availability and operational planning.

### 4. Average Fare Analysis

An interactive line chart compares:

* Average Total Fare
* Average Base Fare

across different hours of the day.

This helps identify changes in pricing patterns and potential periods of higher fare activity.

### 5. Weekly Trip Distribution

A pie chart shows the percentage of total rides occurring on each day of the week.

This provides visibility into weekly demand patterns and helps identify high-volume days.

### 6. Trip Distance Analysis

Trips are categorized into four distance tiers:

* **Short:** < 5 km
* **Medium:** 5–15 km
* **Long:** 15–30 km
* **Extra Long:** ≥ 30 km

A donut chart visualizes the proportion of rides within each distance category.

### 7. Payment Method Analytics

The dashboard analyzes completed trips by payment method and displays:

* Total completed trips
* Total revenue
* Average fare

This provides a simple view of payment-method contribution to overall revenue.

### 8. Vehicle & Driver Rating Analysis

The dashboard identifies the top-rated vehicle makes and models based on completed trips and average driver ratings.

Vehicles are considered only when they have more than 50 completed trips, helping avoid ranking vehicles based on extremely small sample sizes.

### 9. Database Record Inspector

A detailed data section provides three analytical views:

* **Recent Filtered Trips**
* **Payment Method Analytics**
* **Top Rated Vehicles**

This allows users to move from high-level KPIs and visualizations into the underlying records and analytical results.

### 10. Dark & Light Dashboard Themes

The application includes two dashboard themes:

* Black / Dark Mode
* White / Light Mode

The interface uses custom CSS and SVG icons to provide an executive-style Business Intelligence experience.

## 🗄️ Database

The project uses a **SQLite relational database** named:

```text
uber_data.sqlite
```

The application connects to the database using Python's built-in `sqlite3` library.

The primary analytics queries operate on the `trips` and `drivers` tables, including information such as:

* Trip ID
* Requested time
* Trip status
* Distance
* Duration
* Base fare
* Total fare
* Payment method
* Surge multiplier
* Driver information
* Vehicle make/model
* Driver rating

The repository also contains scripts for downloading and inspecting the Uber SQL dataset and preparing the local SQLite database.

## 🏗️ Project Structure

```text
UBER/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── source_code/
│   ├── app.py
│   ├── download_and_inspect.py
│   ├── requirements.txt
│   ├── setup_database.py
│   └── uber_data.sqlite
│
└── README.md
```

### File Description

| File                      | Description                                               |
| ------------------------- | --------------------------------------------------------- |
| `app.py`                  | Main Streamlit Business Intelligence dashboard            |
| `uber_data.sqlite`        | SQLite database containing Uber trip data                 |
| `setup_database.py`       | Downloads and prepares the SQLite database                |
| `download_and_inspect.py` | Downloads and inspects database tables and sample records |
| `requirements.txt`        | Python project dependencies                               |
| `.devcontainer/`          | Development container configuration                       |

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.x
* Git
* pip

### 1. Clone the Repository

```bash
git clone https://github.com/Tamilarasi-Karthikeyan/UBER.git
```

Navigate into the project:

```bash
cd UBER
```

### 2. Navigate to the Source Code

```bash
cd source_code
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Prepare the Database

If the SQLite database is not already available, run:

```bash
python setup_database.py
```

The setup script downloads the Uber SQL dataset through KaggleHub, locates the database file, copies it into the project directory, and inspects the database structure.

### 6. Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔍 SQL Analytics

This project demonstrates practical SQL skills through analytical queries including:

### KPI Aggregations

```sql
SELECT
    COUNT(*) AS total_trips,
    SUM(total_fare) AS gross_revenue,
    AVG(total_fare) AS avg_fare,
    AVG(distance_km) AS avg_distance,
    AVG(surge_multiplier) AS avg_surge
FROM trips;
```

### Hourly Demand Analysis

```sql
SELECT
    CAST(strftime('%H', requested_at) AS INTEGER) AS hour_of_day,
    COUNT(*) AS total_trips
FROM trips
GROUP BY hour_of_day
ORDER BY hour_of_day;
```

### Payment Method Analysis

```sql
SELECT
    payment_method,
    COUNT(*) AS total_trips,
    SUM(total_fare) AS total_revenue,
    AVG(total_fare) AS avg_fare
FROM trips
WHERE status = 'completed'
GROUP BY payment_method
ORDER BY total_revenue DESC;
```

### Vehicle Rating Analysis

```sql
SELECT
    d.vehicle_make,
    d.vehicle_model,
    COUNT(t.trip_id) AS trips_completed,
    AVG(d.rating) AS avg_driver_rating
FROM drivers d
JOIN trips t
    ON d.driver_id = t.driver_id
GROUP BY d.vehicle_make, d.vehicle_model
HAVING trips_completed > 50
ORDER BY avg_driver_rating DESC;
```

## 💡 Business Insights

The dashboard can be used by business and operations teams to investigate questions such as:

* When is ride demand highest?
* What hours generate higher average fares?
* Which days generate the greatest ride volume?
* What percentage of rides are short, medium, long, or extra-long?
* Which payment methods generate the most revenue?
* Which vehicle models have the highest driver ratings?
* How does trip distance relate to fare performance?
* How does surge pricing vary across the ride dataset?

## 📊 Business Intelligence Workflow

```text
Uber Trip Dataset
       │
       ▼
Kaggle Dataset
       │
       ▼
SQLite Database
       │
       ▼
SQL Queries
       │
       ├── KPI Calculations
       ├── Demand Analysis
       ├── Fare Analysis
       ├── Payment Analysis
       ├── Distance Analysis
       └── Vehicle/Driver Analysis
       │
       ▼
Python + Streamlit
       │
       ▼
Plotly Visualizations
       │
       ▼
Interactive BI Dashboard
```

## 🎓 Skills Demonstrated

This project demonstrates practical experience in:

* **SQL**
* **Python**
* **SQLite**
* **Data Analysis**
* **Business Intelligence**
* **Data Visualization**
* **Dashboard Development**
* **Data Modeling**
* **KPI Development**
* **Business Analytics**
* **Interactive Filtering**
* **Relational Database Analysis**
* **Data Storytelling**

## 📌 Key Takeaway

This project demonstrates how raw transportation data can be transformed into an interactive **Business Intelligence solution** using SQL-driven analytics and Python visualization.

Rather than presenting static charts, the dashboard allows users to interact with the data, apply business filters, explore operational KPIs, and drill into detailed analytical records.

## 👤 Author

**Tamilarasi Karthikeyan**

GitHub: [Tamilarasi-Karthikeyan](https://github.com/Tamilarasi-Karthikeyan)

## 📄 License

This project is intended for educational, portfolio, and demonstration purposes.
