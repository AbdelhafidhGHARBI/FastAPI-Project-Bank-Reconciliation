from pydantic_settings import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    PROJECT_NAME: str = "via7 IA Reconciliation"
    API_V1_STR: str = "/api/v1"
    
    # Default Tiers configuration with specific business rules
    TIERS: Dict[str, Dict[str, str]] = {
        # --- Geld IN (Debit 512 / Credit Tiers) ---
        "CLIENT": {"tiers": "Client", "compte": "411"},
        "VIREMENT RECU": {"tiers": "Client", "compte": "411"},
        "REMISE CHEQUE": {"tiers": "Client", "compte": "411"}, # Or 511
        "ENCAISSEMENT EFFET": {"tiers": "Client", "compte": "411"},
        "TPE": {"tiers": "Client TPE", "compte": "411"},
        "BOUTIQUE EN LIGNE": {"tiers": "Client Web", "compte": "411"},
        "CAPITAL": {"tiers": "Actionnaire", "compte": "101"},
        "SUBVENTION": {"tiers": "Etat", "compte": "740"},
        "REMBOURSEMENT TVA": {"tiers": "Etat TVA", "compte": "4456"},
        "INTERETS RECUS": {"tiers": "Banque", "compte": "760"},
        
        # --- Salaire / Social ---
        "PRIME": {"tiers": "Employé", "compte": "641"},
        
        # --- Effets / LCR / Escompte ---
        "TRAITE": {"tiers": "Client Effet", "compte": "5112"},
        "LCR": {"tiers": "Client LCR", "compte": "5112"},
        "BILLET A ORDRE": {"tiers": "Client BO", "compte": "5112"},
        "LETTRE DE CHANGE": {"tiers": "Client LC", "compte": "5112"},
        "ESCOMPTE": {"tiers": "Banque Escompte", "compte": "5114"},
        "FINANCEMENT": {"tiers": "Banque Financement", "compte": "5114"},
        
        "CHARGES D'INTERETS": {"tiers": "Banque Escompte", "compte": "661"},
        "SERVICES BANCAIRES": {"tiers": "Banque Frais", "compte": "627"},
        "TVA SUR COMMISSIONS": {"tiers": "Etat", "compte": "44566"},
        
        # --- Geld OUT (Credit 512 / Debit Tiers) ---
        "AMAZON": {"tiers": "Amazon", "compte": "607"},
        "FOURNISSEUR": {"tiers": "Fournisseur", "compte": "401"},
        "FACTURE": {"tiers": "Fournisseur", "compte": "401"},
        "LOYER": {"tiers": "Bailleur", "compte": "613"},
        "CNSS": {"tiers": "CNSS", "compte": "431"},
        "URSSAF": {"tiers": "URSSAF", "compte": "431"},
        "IMPOTS": {"tiers": "Tresor Public", "compte": "445"},
        "TVA": {"tiers": "TVA", "compte": "445"},
        "SALAIRE": {"tiers": "Employé", "compte": "641"},
        "EMPRUNT": {"tiers": "Banque Pret", "compte": "164"},
        "AGIOS": {"tiers": "Banque Frais", "compte": "661"},
        "FRAIS BANCAIRE": {"tiers": "Banque Frais", "compte": "627"},
        "CARTE BANCAIRE": {"tiers": "Frais CB", "compte": "627"},
        "RETRAIT": {"tiers": "Caisse", "compte": "530"},
        "DIVIDENDES": {"tiers": "Associés", "compte": "457"},
        "PRELEVEMENT EXPLOITANT": {"tiers": "Exploitant", "compte": "108"},
    }

    class Config:
        case_sensitive = True

settings = Settings()
