import pandas as pd
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

############################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
############################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden
# oluşan veri setini okutma.

control_df = pd.read_excel("measurement_problems/datasets/ab_testing.xlsx", sheet_name="Control Group")
test_df = pd.read_excel("measurement_problems/datasets/ab_testing.xlsx", sheet_name="Test Group")

# Adım 2: Kontrol ve test grubu verilerini analizi.

control_df.shape
test_df.shape
control_df.head()
test_df.head()
control_df.describe().T
test_df.describe().T



df = pd.concat([control_df, test_df], ignore_index=True)

############################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
############################################################

# Adım 1: Hipotezin tanımlanması

# H0 : M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark yoktur.)
# anlamlı farklılık yoktur

# H1 : M1!= M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark vardır.)
# Anlamlı farklılık yoktur

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalama analizleri

control_df["Purchase"].mean()
# 550.8940587702316

test_df["Purchase"].mean()
# 582.1060966484675

# Ortalamalara bakıldığında
# average bidding'in maximum bidding'de daha fazla kazanç getirdiği gözlenir ama istatistiksel
# olarak incelemek gerekir.



############################################################
# Görev 3:  Hipotez Testinin Gerçekleştirilmesi
############################################################

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrolleri

# Varsayım kontrolü

#   -Normallik Varsayımı
#   -Varyans Homojenliği


# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
# Test sonucuna göre normallik varsayımı kontrol ve
# test grupları için sağlanıyor mu ? Elde edilen p-valuedeğerlerini yorumlayınız.

test_stat, pvalue = shapiro(control_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9773, p-value = 0.5891
# Normal dağılım varsayımı sağlanmaktadır.(p-value>0.05)

test_stat, pvalue = shapiro(test_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9589, p-value = 0.1541
# Normal dağılım varsayımı sağlanmaktadır.(p-value>0.05)

# Varyans Homojenliği :
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
# Kontrol ve test grubu için varyans homojenliğinin sağlanıp
# sağlanmadığını Purchase değişkeni üzerinden test ediniz.
# Test sonucuna göre normallik varsayımı sağlanıyor mu?
# Elde edilen p-valuedeğerlerini yorumlayınız.


test_stat, pvalue = levene(control_df["Purchase"], test_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 2.6393, p-value = 0.1083
# H0: Varyanslar homojendir. (p-value>0.05)

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testin seçilmesi

# Her iki varsayımda sağlandığı için bağımsız iki örneklem t testi (parametrik test) uygundur.

test_stat, pvalue = ttest_ind(control_df["Purchase"], test_df["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = -0.9416, p-value = 0.3493 (p-value > 0.05)


# Adım 3: Test sonucunda elde edilen p_valuedeğerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlama.

#  p-value = 0.3493 > 0.05 'den büyük olduğu için
#  H0 : M1 = M2 (Kontrol grubu ve test grubu satın alma ortalamaları arasında fark yoktur.) hipotezi
# sağlanmıştır.
# Yani istatistiki olarak average  bidding maximum bidding'den daha fazla dönüşüm getirmez, fark yoktur da diyebiliriz.


##############################################
# Görev 4:  Sonuçların Analizi
##############################################

# Adım 1: Hangi testin kullanıldığı ve açıklaması.

# Normallik Varsayımı ve Varyans Homojenliği shapiro ve levene testleri ile kontrol edildiğinde
# p-value değerlerinin 0.05'den büyük olduğu görülmektedir. Bu sebeple
# H0: Varyanslar Homojendir ve H0: Normal dağılım varsayımı sağlanmaktadır. hipozeteri Reddedilemezdir.
# Varsayımların her ikisi sağlandığı için iki örneklem t testi (parametrik test) kullanılmıştır.

# Adım 2: Elde edilen sonuçlara göre müşteriye geri dönüş.

# Kontrol grubuna Maximum Bidding, test grubuna  Average Bidding uygulandıktan sonra tıklanan reklamlar
# sonrası satın alınan ürün sayılarının ortlamalarına bakıldığında test grubunun daha yüksek bir ortalamaya
# sahip olduğu gözükmektedir. Fakat istatistiki olarak kontrol grubu ve test gruplarını incelemeye aldığımızda
# Maximum Bidding-Average Bidding uygulanması arasında tıklanan reklamlar sonrası satın alınan ürün sayılarında
# bir artış gözükmemektedir.
# Bundan dolayı, Facebook şirketi mevcut teklif verme uygulamasına devam etmeli,
# alternatif olarak yeni bir teklif türü olarak çıkarılan average bidding’in güncelleme alarak piyasaya tekrar
# sunulması ve bu süreçte eski teklif verme uygulamasının kullanılması gerekmektedir.








