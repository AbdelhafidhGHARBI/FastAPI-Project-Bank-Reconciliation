import io
import pandas as pd
from rapidfuzz import process, fuzz
from app.core.config import settings

class ReconciliationService:
    @staticmethod
    def safe_float(value):
        try:
            return float(str(value).replace(",", "."))
        except:
            return 0.0

    @staticmethod
    def detect_tiers(libelle: str):
        if not libelle:
            return {"tiers": "Inconnu", "compte": "471"}

        # Use partial_ratio to find good matches (e.g. "CHARGES..." inside "Frais CHARGES...")
        # limit=10 to find potential longer matches that might have slightly lower score than a short robust match
        # process.extract returns list of (match, score, index)
        matches = process.extract(libelle.upper(), settings.TIERS.keys(), scorer=fuzz.partial_ratio, limit=10)
        
        # Filter reasonable matches (threshold 80)
        candidates = [m for m in matches if m[1] >= 80]
        
        if candidates:
            # Sort by length of the key descending (Prefer "CHARGES D'INTERETS" over "ESCOMPTE")
            # match[0] is the key string
            best_match = sorted(candidates, key=lambda x: len(x[0]), reverse=True)[0]
            return settings.TIERS[best_match[0]]

        return {"tiers": "Inconnu", "compte": "471"}

    @staticmethod
    def process_bank_statement(content: bytes, filename: str):
        # Try detecting encoding
        df = None
        for encoding in ["utf-8", "latin-1", "cp1252"]:
            try:
                # use sep=None to sniff separator
                df = pd.read_csv(io.BytesIO(content), encoding=encoding, sep=None, engine='python')
                break
            except Exception as e:
                print(f"Failed decoding with {encoding}: {e}")
                continue
        
        if df is None:
            raise ValueError("Impossible de lire le fichier CSV. Vérifiez l'encodage.")

        # Normalize headers for matching
        original_columns = df.columns.tolist()
        df.columns = [str(c).lower().strip().replace("é", "e").replace("è", "e") for c in df.columns]
        print(f"Columns normalized: {original_columns} -> {df.columns.tolist()}")

        col_debit = next((c for c in df.columns if "debit" in c), None)
        col_credit = next((c for c in df.columns if "credit" in c), None)
        col_libelle = next((c for c in df.columns if "libelle" in c or "label" in c or "description" in c), None)
        col_date = next((c for c in df.columns if "date" in c), "date")

        print(f"Detected columns - Debit: {col_debit}, Credit: {col_credit}, Libelle: {col_libelle}")

        results = []

        for index, row in df.iterrows():
            libelle = str(row.get(col_libelle, "")) if col_libelle else "Inconnu"
            info = ReconciliationService.detect_tiers(libelle)

            debit_val = 0.0
            credit_val = 0.0

            if col_debit:
                debit_val = ReconciliationService.safe_float(row.get(col_debit))
            
            if col_credit:
                credit_val = ReconciliationService.safe_float(row.get(col_credit))

            # Logic Adjustment:
            # Bank Statement Debit = Money Leaving = Expense = Credit Bank (512), Debit Expense Account
            # Bank Statement Credit = Money Entering = Revenue = Debit Bank (512), Credit Revenue Account

            montant = 0.0
            if debit_val > 0:
                # Money leaving bank
                debit = info["compte"]
                
                # Logic Refinement for Escompte Fees:
                # If it's a 6xx charge (Interest/Services) or 4xx (TVA) related to Escompte/Agios -> Credit 5114
                is_escompte_related = any(k in libelle.upper() for k in ["ESCOMPTE", "COMMISSION", "INTERET", "AGIOS", "TVA", "SERVICES BANCAIRES"])
                if is_escompte_related and (debit.startswith("6") or debit.startswith("4")):
                    credit = "5114"
                else:
                    credit = "512"
                
                montant = debit_val
            elif credit_val > 0:
                # Money entering bank
                debit = "512"
                credit = info["compte"]
                montant = credit_val
            else:
                # No movement detected or 0
                debit = "?"
                credit = "?"
                montant = 0.0

            print(f"Row {index}: {libelle} | D:{debit_val} C:{credit_val} -> {debit}/{credit}")

            results.append({
                "date": str(row.get(col_date, "")),
                "libelle": libelle,
                "tiers": info["tiers"],
                "debit": debit,
                "credit": credit,
                "montant": round(abs(montant), 3)
            })

        return {"filename": filename, "transactions": results}
