# Streamlit Sentiment Analysis

## Overview
This project is a Streamlit application designed for sentiment analysis. It allows users to input text and receive sentiment predictions based on a pre-trained machine learning model. The application provides a user-friendly interface for analyzing sentiments in various texts.

## Project Structure
```
streamlit_sentiment_analysis
├── streamlit_sentiment.py       # Main application code for the Streamlit sentiment analysis tool
├── data
│   └── sample_data.csv          # Sample data used for sentiment analysis
├── models
│   └── sentiment_model.pkl       # Serialized machine learning model for sentiment analysis
├── requirements.txt              # Python package dependencies for the project
└── README.md                     # Documentation for the project
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit_sentiment_analysis
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run src/streamlit_sentiment.py
   ```

## Usage
- Open the application in your web browser.
- Input the text you want to analyze in the provided text box.
- Click on the "Analyze" button to receive sentiment predictions.

## License
This project is licensed under the MIT License.