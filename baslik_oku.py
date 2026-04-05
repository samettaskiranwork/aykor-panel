import pandas as pd
import os

# Dosya adını buraya tam olarak yaz (Örn: Projeler.xlsx)
dosya_adi = 'senin_dosyan.xlsx' 

if os.path.exists(dosya_adi):
    df = pd.read_excel(dosya_adi)
    print("\n--- EXCELDEKİ BAŞLIKLARIN ---")
    print(df.columns.tolist())
    print("----------------------------\n")
else:
    print(f"Hata: '{dosya_adi}' dosyası bulunamadı. Dosyanın VS Code'da klasörün içinde olduğundan emin ol.")