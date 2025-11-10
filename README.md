# AI Data Analyst Assistant

This Streamlit app lets you upload a CSV and ask questions about the dataset using Google Gemini via langchain-google-genai.


This project is an intelligent data analysis assistant, developed with Streamlit and integrated with Google's Gemini AI. The system allows users to upload a CSV file and ask questions in natural language about the dataset.

### Main Features

- **Interactive Analysis**: Upload CSV files directly through the web interface.
- **Natural Language Queries**: Ask questions about your data in plain English, without needing to write code.
- **Intelligent Responses**: Uses Google Gemini to interpret questions, analyze the CSV, and generate clear answers.


### Architecture

- **Frontend**: Web interface built with **Streamlit** for user interaction.
- **Data Analysis**: **Pandas** for handling and structuring the CSV data.
- **AI**: **LangChain** with the **Google Gemini** model to create an agent capable of understanding and querying the data.

### Use Cases

- Quick exploratory analysis of new datasets.
- Obtaining insights and answers without needing to write Python or SQL scripts.
- Democratizing data analysis for users without technical programming knowledge.

## How to Set Up the Project

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key
- Git

### Step-by-Step

1.  **Clone the repository**
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd Data_Analyst_Assistant
    ```

2.  **Set up the virtual environment**
    ```bash
    python -m venv .venv
    ```
    - On **Windows**:
      ```powershell
      .venv\Scripts\Activate.ps1
      ```
    - On **Linux/Mac**:
      ```bash
      source .venv/bin/activate
      ```

3.  **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables**
    Create a file named `.env` in the project root and add your API key:

    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

    Alternatively, you can set the environment variable directly in your terminal.

5.  **Run the application**
    ```bash
    streamlit run analyst.py
    ```

6.  **Access the application**
    Streamlit will automatically open the application in your browser.

### How to Use

1.  **Upload CSV**: In the interface, click "Browse files" and select the `.csv` file you want to analyze.
2.  **Ask a Question**: Type your question about the data in the text input field.
3.  **Get the Answer**: The AI assistant will process your question and display the answer.

## Technologies Used

- **Streamlit**: Framework for creating the web interface.
- **Pandas**: Library for data manipulation and analysis.
- **LangChain**: Framework for LLM integration.
- **Google Gemini AI**: Language model for processing queries.
- **Python-dotenv**: For managing environment variables.

---

Developed by:
- **Julio Alejandro de Oliveira Montalvan**