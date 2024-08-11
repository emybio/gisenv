import pandas as pd
#from turkiye.models import Il,Ilce,Semt,Mahalle
#dosya okuma
excel_file = 'C:/Users/kur06/Documents/GitHub/gisenv/pk_list_29.04.2016.xlsx'
data = pd.read_excel(excel_file,sheet_name=None)

# Pandas ayarlarını güncelleme
pd.set_option('display.max_columns', None)  # Tüm sütunları gösterir
pd.set_option('display.max_rows', None)  # Tüm satırları gösterir
pd.set_option('display.max_colwidth', None)  # Sütun genişliğini sınırlandırmaz

# for sheet_name,df in data.items():
#     print(f"Sheet name: {sheet_name}")
#     print(df.head(20))

def load_data_from_excel(file_path):
    # Excel dosyasını okuma
    data = pd.read_excel(file_path, sheet_name=None)

    # İl tablosunu yükleme
    if 'Il' in data:
        il_df = data['Il']
        print("il df : ",il_df)
        for _, row in il_df.iterrows():
            print("il row: ",row)
            #Il.objects.get_or_create(ad=row['ad'])
  
#   # İlçe tablosunu yükleme
#     if 'Ilce' in data:
#         ilce_df = data['Ilce']
#         for _, row in ilce_df.iterrows():
#             il = Il.objects.get(ad=row['il'])
#             Ilce.objects.get_or_create(il=il, ad=row['ad'])
    
#     # Semt tablosunu yükleme
#     if 'Semt' in data:
#         semt_df = data['Semt']
#         for _, row in semt_df.iterrows():
#             ilce = Ilce.objects.get(ad=row['ilce'])
#             Semt.objects.get_or_create(ilce=ilce, ad=row['ad'])
    
#     # Mahalle tablosunu yükleme
#     if 'Mahalle' in data:
#         mahalle_df = data['Mahalle']
#         for _, row in mahalle_df.iterrows():
#             semt = Semt.objects.get(ad=row['semt'])
#             Mahalle.objects.get_or_create(semt=semt, ad=row['ad'])
            
# Yükleme fonksiyonunu çağırma
load_data_from_excel(excel_file)