# Real Estate Chatbot (MVP)

A simple web application that allows users to query real estate data and get insights like summaries, charts, and filtered tables. Built using **Django** (backend) and **React.js + Chart.js + Bootstrap** (frontend).

---

## Features

- Accepts user queries like `Analyze Wakad` or `Analyze Akurdi`.
- Filters real estate data from an **Excel dataset**.
- Returns:
  - **Text summary** of total sales and records found.
  - **Chart** showing Total Sales per Year.
  - **Filtered table** of relevant data.
- Responsive and interactive frontend using **React + Bootstrap**.
- Optionally allows users to **download filtered data** as CSV .

---

## Tech Stack

- **Backend:** Django + Python + Pandas
- **Frontend:** React.js + Bootstrap + Chart.js
- **Data:** Excel file (`Sample_data.xlsx`) as the data source

---

## Getting Started

### Prerequisites

- Python 3.x
- Node.js & npm
- Django
- React (via `create-react-app`)

### Backend Setup (Django)

```bash
cd backend_folder_name  # navigate to your Django project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```
### Frontend Setup (React)
 ```bash
cd frontend_folder_name  # navigate to React app
npm install
npm start
```
