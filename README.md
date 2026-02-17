# 🏦 FastAPI Bank Reconciliation Project

A smart bank reconciliation tool built with **FastAPI**, **Pandas**, and **RapidFuzz**. 
It automatically processes bank statements (CSV), identifies transaction types using fuzzy matching, and generates appropriate accounting entries based on specific business rules.

## 🚀 Features

- **Automated Reconciliation**: Upload a CSV bank statement and get instant accounting entries.
- **Smart Matching**: Uses fuzzy logic (`rapidfuzz`) to identify transaction partners (Clients, Suppliers, etc.) even with typo variations.
- **Advanced Accounting Logic**:
  - Handles **Escompte/Effets** (Bills of Exchange) with specific accounting rules (Credit 5114 vs 512).
  - Automatically splits fees (Agios, Commissions) and TVA.
  - Distinguishes between standard payments and complex financial instruments.
- **Web Interface**: Clean and simple HTML/JS frontend for easy file upload and visualization.
- **API First**: RESTful API design with Pydantic validation.

## 🛠️ Technology Stack

- **Backend**: Python 3.9+, FastAPI, Uvicorn
- **Data Processing**: Pandas, RapidFuzz
- **Configuration**: Pydantic Settings
- **Frontend**: Vanilla HTML/JavaScript/CSS

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbdelhafidhGHARBI/FastAPI-Project-Bank-Reconciliation.git
   cd FastAPI-Project-Bank-Reconciliation
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Usage

1. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the application**
   - Web Interface: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

3. **Upload your CSV**
   - Use the web interface to upload your `extrait_bancaire.csv`.
   - The system will detect encoding (UTF-8, Latin-1) automatically.

## 📊 Accounting Rules Configuration

The application uses a flexible configuration in `app/core/config.py` to map keywords to accounting schemas:

| Keyword | Type | Debit Account | Credit Account |
|---------|------|---------------|----------------|
| CLIENT | Income | 512 | 411 |
| FOURNISSEUR | Expense | 401 | 512 |
| ESCOMPTE | Expense | 512 | 5114 (Specific Rule) |
| SALAIRE | Expense | 641 | 512 |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
