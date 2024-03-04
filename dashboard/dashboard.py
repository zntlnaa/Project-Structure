import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Mengatur gaya seaborn
sns.set(style='dark')

# Fungsi untuk membuat DataFrame untuk jumlah penyewaan sepeda
def create_bike_sharing_counts(df):
    bike_sharing_counts_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    bike_sharing_counts_df = bike_sharing_counts_df.reset_index()
    bike_sharing_counts_df.rename(columns={
        "cnt": "total_count"
    }, inplace=True)
    
    return bike_sharing_counts_df

def create_season_df(df):
    season_df = df.groupby(["season", "yr"]).cnt.sum().sort_values(ascending=False).reset_index()
    return season_df

def create_monthly_counts_df(df):
    monthly_counts_df = df.groupby(['yr', 'mnth']).cnt.sum().unstack().fillna(0)
    return monthly_counts_df

# Load dataset day.csv
day_df = pd.read_csv("day.csv")

# Ubah tipe data kolom 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Membuat komponen filter tanggal menggunakan sidebar
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("bike.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan tanggal yang dipilih
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

# Membuat DataFrame untuk jumlah penyewaan sepeda
bike_sharing_counts_df = create_bike_sharing_counts(main_df)

# Tampilkan dashboard dengan berbagai visualisasi data
st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Rent Amount')

# Menampilkan informasi total order dan total revenue dalam bentuk metric
col1, col2 = st.columns(2)

with col1:
    rent_amount = bike_sharing_counts_df.total_count.sum()
    st.metric("Total rent", value=rent_amount)

# Memplot grafik jumlah penyewaan sepeda harian
fig1, ax1 = plt.subplots(figsize=(16, 8))
ax1.plot(
    bike_sharing_counts_df["dteday"],
    bike_sharing_counts_df["total_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax1.tick_params(axis='y', labelsize=15)
ax1.tick_params(axis='x', labelsize=12)
plt.xticks(rotation=45)
plt.xlabel('Date', fontsize=15)
plt.ylabel('Total Count', fontsize=15)
plt.title('Daily Bike Sharing Counts', fontsize=20)

# Menampilkan gambar grafik di Streamlit
st.pyplot(fig1)

# Membuat DataFrame untuk jumlah total penyewaan sepeda berdasarkan musim
season_df = create_season_df(main_df)

# Membuat Clustered Bar Chart menggunakan seaborn
fig2 = plt.figure(figsize=(10, 6))

# Menentukan urutan kategori hue
hue_order = [0, 1]

# Membuat bar plot
ax = sns.barplot(data=season_df, x='season', y='cnt', hue='yr', estimator=sum, errorbar=None, hue_order=hue_order)

# Mengatur label pada sumbu x dan menentukan posisi tanda sumbu x secara eksplisit
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])

plt.title('Bike Sharing Count by Season and Year')
plt.xlabel('Season')
plt.ylabel('Total Count')

# Mengatur label pada legend
plt.legend(title='Year', labels=['2011', '2012'])

# Menampilkan gambar grafik di Streamlit
st.pyplot(fig2)

# Membuat DataFrame untuk jumlah total sepeda yang disewa setiap bulan dan tahun
monthly_counts_df = create_monthly_counts_df(main_df)

# Membuat visualisasi
fig3, ax3 = plt.subplots(figsize=(10, 6))

# Plotting untuk setiap tahun
for year in monthly_counts_df.index:
    plt.plot(monthly_counts_df.loc[year], marker='o', label=f'Tahun {year + 2011}')

plt.title('Bike Sharing Count by Month (2011-2012)')
plt.xlabel('Month')
plt.ylabel('Total Count')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# Menampilkan gambar grafik di Streamlit
st.pyplot(fig3)
