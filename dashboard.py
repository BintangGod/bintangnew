import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.title('Dashboard Sharing Bike')

st.header('Data Sharing Bike day')
day_df = pd.read_csv("./day.csv")
st.table(day_df.head())
datetime_columns = ["dteday"]
st.caption('dan seterusnya')

st.header('Data Sharing Bike hour')
hour_df = pd.read_csv("./hour.csv")
st.table(hour_df.head())
st.caption('dan seterusnya')

datetime_columns = ["dteday"]

for column in datetime_columns:
  day_df[column] = pd.to_datetime(day_df[column])

hour_df["Suhu_celcius"] = hour_df["temp"]*41
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
day_df["weather"] = day_df.season.apply(lambda x: "springer" if x == 1 else("summer" if x == 2 else("fall" if x == 3 else "winter")))
hour_df["suhu"] = hour_df.Suhu_celcius.apply(lambda x: "0-10" if x <= 10 else ("10-20" if x > 10 and x <= 20 else("20-30" if x >20 and x <= 30 else "30-41")))
hour_df["Time"] = hour_df.hr.apply(lambda x: "Morning" if x >= 0 and x <= 12 else ("Afternoon" if x > 12 and x <= 15 else("Evening" if x > 15 and x <= 18 else "Night")))

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]
tab1, tab2 = st.tabs(["Day", "Hour"])
 
with tab1:
    st.header("Day")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        main_df["dteday"],
        main_df["cnt"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
 
    st.pyplot(fig)
    st.write('Dari data harian pelanggan rental sepeda selama 2 tahun, terlihat sebenarnya terdapat peningkatan pelanggan secara keseluruhan pada 2012 dibandingkan 2011. Jika dilihat dari polanya, pada bulan 1 hingga bulan 7 akan terjadi peningkatan pelanggan dan dari bulan 7 hingga bulan 10 merupakan puncak pelanggan terbanyak dan menuju akhir tahun akan terjadi penurunan pelanggan kembali.')
 
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        main_df["dteday"],
        main_df["weather"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
 
    st.pyplot(fig)
    st.write('Jika dilihat berdasarkan musim, maka peningkatan pelanggan di awal tahun terjadi dikarenakan mulainya musim springer hingga summer dan puncaknya pada musim fall. Dan menuju akhir tahun terjadi penurunan pelanggan dikarenakan mulai memasukinya musim winter.')
    
    springer = day_df.groupby(by="weather").agg({"cnt": ["mean"]})
    st.write(round(springer))
    
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(x=day_df["weather"], y=day_df["cnt"], palette='Blues', ax=ax)

    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title("Rata-rata pelanggan harian", loc="center", fontsize=40)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    st.write('Walaupun pada musim winter terjadi penurunan pelanggan, namun untuk keseluruhan rata-rata pelanggan, pada musim fall menjadi musim dengan rata-rata pelanggan terbanyak dan musim springer menjadi musim dengan rata-rata pelanggan paling sedikit.')
    
    st.header('Kesimpulan')
    st.write('Pada data harian, setiap tahun memiliki pola data bahwa pada bulan 1-7 pelanggan mengalami tren naik dan puncaknya pada bulan 7-10 pelanggan mencapai jumlah terbanyaknya dikarenakan bulan 7-9 merupakan musim fall. Setelah bulan 10 menuju akhir tahun mengalami tren turun dikarenakan mulai memasukinya musim winter. Namun secara rata-rata pelanggan pada fall menjadi rata-rata pelanggan yang terbanyak dan pada springer yaitu periode bulan 1-3 menjadi rata-rata pelanggan paling sedikit.')
with tab2:
    st.header("Hour")
    suki = hour_df.groupby(by="suhu").agg({"cnt": ["mean"]})
    st.write(round(suki))
    
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(x=hour_df["suhu"], y=hour_df["cnt"], palette='Blues', ax=ax)

    ax.set_xlabel('Suhu (Celcius)', fontsize = 30)
    ax.set_ylabel('Pelanggan', fontsize=30)
    ax.set_title("Rata-rata pelanggan per jam", loc="center", fontsize=40)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    st.write('Visualisasi ini memberikan gambaran lebih jelas bahwa pelanggan banyak yang lebih memilih untuk menyewa sepeda disaat suhu tinggi dibanding disaat suhu rendah.')

    Waktu = hour_df.groupby(by="Time").agg({"cnt": ["mean"]})
    st.write(round(Waktu))
    
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(x=hour_df["Time"], y=hour_df["cnt"], palette='viridis', ax=ax)

    ax.set_xlabel('Waktu', fontsize = 30)
    ax.set_ylabel('Pelanggan', fontsize=30)
    ax.set_title("Rata-rata pelanggan berdasarkan waktu", loc="center", fontsize=40)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
    st.write("1. Evening (Jam 15-18)")
    st.write('2. Afternoon (Jam 12-15)')
    st.write('3. Night (Jam 18-23)')
    st.write('4. Morning (Jam 0-12)')
    st.write('Urutan Time atau waktu dimana pelanggan terbanyak sampai paling sedikit.')

    st.header('Kesimpulan')
    st.write('Pelanggan lebih banyak yang menyukai bersepeda disaat cuaca panas dibandingkan saat cuaca dingin, hal ini berkorelasi juga dengan musim yang ada. Dan kebanyakan dari pelanggan kita suka bersepeda di sore hari ditunjukkan dari rata-rata pelanggan pada jam 15-18 menjadi yang paling tinggi dan untuk waktu dengan rata-rata yang paling rendah adalah di pagi hari.')
    
text = st.text_area('Feedback')
st.write('Feedback: ', text)
rate = st.radio(
    label="Rating",
    options=('☆', '☆☆', '☆☆☆','☆☆☆☆','☆☆☆☆☆'),
    horizontal=False
)
if st.button('Send'):
    st.write('Thanks')