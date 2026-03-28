import pandas as pd
from database import get_db_connection
from datetime import datetime

def format_date(val):
    """Excel'den gelen tarihleri veritabanı formatına (YYYY-MM-DD) çevirir."""
    if pd.isna(val) or str(val).strip() == '' or str(val).lower() == 'nan':
        return None
    try:
        # Eğer zaten datetime objesiyse direkt çevir
        if isinstance(val, datetime):
            return val.strftime('%Y-%m-%d')
        # Metin ise (28.04.2021 gibi) parçala ve çevir
        date_str = str(val).split(' ')[0] # Saat varsa temizle
        for fmt in ('%d.%m.%Y', '%Y-%m-%d', '%m/%d/%Y'):
            try:
                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return None
    except:
        return None

def migrate_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        print(f"--- Excel Okundu. {len(df)} satır işleniyor... ---")

        mapping = {
            '[ProjectCode]': 'project_code',
            '[PriorityOrder]': 'priority',
            'Müşteri': 'customer',
            'Konu': 'subject',
            '[ItemQty]': 'item_quantity',
            '[Deadline]': 'deadline',
            '[DeadlineTime]': 'deadline_time',
            '[PE]': 'proengineer',
            '[ST]': 'prostatus',
            '[AnnoDt]': 'annodate',
            '[BB]': 'bid_bond',
            'Tender Reference': 'tender_reference',
            '[ProjectType]': 'project_type',
            '[OfferedQty]': 'offered_quantity',
            '[OfferAmount]': 'offer_amount',
            '[OfferCur]': 'offer_cur',
            '[OfferAmountEUR]': 'offer_amount_eur',
            '[BeklenenKar]': 'expected_profit',
            '[BeklenenCiro]': 'expected_turnover',
            '[OlasilikYuzde]': 'probability_percent',
            '[ContractQty]': 'contract_quantity',
            '[ContractAmount]': 'contract_amount',
            '[ContractCur]': 'contract_currency',
            '[ContractAmountEUR]': 'contract_amount_eur',
            '[FinalAcceptance]': 'final_acceptance'
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        count = 0

        for index, row in df.iterrows():
            project_val = str(row.get('[ProjectCode]', ''))
            if pd.isna(row.get('[ProjectCode]')) or 'Toplam' in project_val or project_val.strip() == '':
                continue

            try:
                data_to_insert = {}
                for excel_col, db_col in mapping.items():
                    val = row.get(excel_col)
                    
                    # --- TARİH DÜZELTME MANTIĞI ---
                    if db_col in ['deadline', 'annodate', 'final_acceptance']:
                        data_to_insert[db_col] = format_date(val)
                    elif pd.isna(val):
                        data_to_insert[db_col] = None
                    elif db_col == 'priority':
                        try:
                            # 'Priority' içinde sayı olmayan karakterleri temizle
                            data_to_insert[db_col] = int(''.join(filter(str.isdigit, str(val))))
                        except:
                            data_to_insert[db_col] = 5
                    else:
                        data_to_insert[db_col] = val

                data_to_insert['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                cols = ', '.join(data_to_insert.keys())
                placeholders = ', '.join(['%s'] * len(data_to_insert))
                sql = f"INSERT INTO projects ({cols}) VALUES ({placeholders})"
                
                cursor.execute(sql, list(data_to_insert.values()))
                count += 1
                
                if count % 50 == 0:
                    print(f">> {count} proje aktarıldı...")

            except Exception as e:
                print(f"!! Satır {index+2} Atlandı (Proje: {project_val}): {e}")

        conn.commit()
        cursor.close()
        conn.close()
        print(f"\n🚀 İŞLEM TAMAM! Toplam {count} proje veritabanına aktarıldı.")

    except Exception as e:
        print(f"Kritik Hata: {e}")

migrate_excel('ProjecList_veri.xlsx')