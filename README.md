🎬 CinemaPulse: AI-Powered Movie Discovery
CinemaPulse is a full-stack movie recommendation engine that combines modern web technologies with machine learning to provide users with personalized movie suggestions. By leveraging TF-IDF Content-Based Filtering and the TMDB API, CinemaPulse offers a premium "Netflix-style" experience for exploring trending titles and finding similar movies based on plot descriptions.

LIVE-https://moviereccsystem-jakyvjy8tsfkanodvixqhi.streamlit.app/

🌟 Key Features
Premium Dark UI: A modern, responsive "Netflix-style" dashboard built with Streamlit.

Intelligent Search: Real-time keyword search with auto-suggestions powered by TMDB.

Dual-Engine Recommendations:

Content-Based (Local): Uses TF-IDF and Cosine Similarity on a local dataset to find movies with similar plot themes.

Genre-Based (Live): Fetches real-time recommendations from TMDB based on movie genres.

High-Performance Backend: FastAPI-powered REST API with asynchronous request handling.

Live Metadata: Fetches high-quality posters, backdrops, ratings, and overviews in real-time.

🏗️ Technical Architecture
The system is split into three main layers:

Frontend: Streamlit provides the interactive UI, managing session states and routing.

API Layer: FastAPI acts as the bridge, serving local ML data and proxying requests to external APIs.

Data Engine: A Python-based ML pipeline that pre-processes movie data and generates TF-IDF matrices stored as pickle files.

🚀 Getting Started
1. Prerequisites
Python 3.9+

A TMDB API Key (Get one for free at themoviedb.org)

2. Installation
Clone the repository:

Bash
git clone https://github.com/adarsh005599/Movie_Rec_System.git
cd Movie_Rec_System
Install dependencies:

Bash
pip install -r requirements.txt
3. Environment Setup
Create a .env file in the root directory and add your API key:

Code snippet
TMDB_API_KEY=your_api_key_here
4. Running the Application
You need to run the Backend and the Frontend simultaneously in two separate terminals.

Terminal 1 (FastAPI Backend):

Bash
python main.py
Terminal 2 (Streamlit Frontend):

Bash
streamlit run app.py
📂 Project Structure
Plaintext
├── app.py                # Streamlit Frontend (UI/UX)
├── main.py               # FastAPI Backend (REST API)
├── movie_recc.ipynb      # ML Pipeline / Model training
├── .env                  # Environment variables (private)
├── requirements.txt      # Python dependencies
├── df.pkl                # Processed movie dataframe
├── tfidf_matrix.pkl      # Pre-computed similarity matrix
└── movies_metadata.csv   # Raw dataset
🛠️ Built With
FastAPI - High-performance web framework.

Streamlit - For the interactive frontend.

Pandas/NumPy - Data manipulation.

Scikit-Learn - TF-IDF Vectorization and similarity metrics.

HTTPX - Asynchronous HTTP requests.
