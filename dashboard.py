import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman Dashboard
st.set_page_config(
    page_title="HabitSense Dashboard",
    page_icon="",
    layout="wide"
)

# 2. Memuat dan Memproses Data Eksak Sesuai File Notebook
@st.cache_data
def load_and_process_data():
    # Membaca file dataset utama kelompok Anda yang sudah bersih
    df = pd.read_csv("habitsense_clean.csv")
    
    # Formula pembersihan outlier untuk Pertanyaan 3 (Cell 33 di Notebook)
    df['Weight_Change'] = df['Target_Weight_kg'] - df['Weight_kg']
    
    Q1 = df['Weight_Change'].quantile(0.25)
    Q3 = df['Weight_Change'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - (1.5 * IQR)
    upper = Q3 + (1.5 * IQR)
    
    df_clean = df[
        (df['Weight_Change'] >= lower) &
        (df['Weight_Change'] <= upper)
    ]
    return df, df_clean

# Menjalankan fungsi load data
try:
    df, df_clean = load_and_process_data()
except FileNotFoundError:
    st.error("File 'habitsense_clean.csv' tidak ditemukan. Pastikan file CSV tersebut berada dalam satu folder yang sama dengan file 'app.py' ini.")
    st.stop()

# 3. Header Utama Dashboard
st.title("Eksplorasi Data Program Kesehatan HabitSense")
st.markdown("Platform analisis interaktif untuk mengamati karakteristik gaya hidup, target pemenuhan nutrisi, dan perencanaan program pengguna.")
st.markdown("---")

# ==============================================================================
# TAB PANEL UTK MASING-MASING PERTANYAAN
# ==============================================================================
tab1, tab2, tab3 = st.tabs([
    "1. Gaya Hidup vs BMI", 
    "2. Target Kalori vs Goal", 
    "3. Durasi Program vs Perubahan Berat"
])

# ------------------------------------------------------------------------------
# TAB 1: GAYA HIDUP VS KATEGORI BMI
# ------------------------------------------------------------------------------
with tab1:
    st.header("Pertanyaan 1: Bagaimana hubungan antara durasi tidur, tingkat stres, dan jumlah langkah harian terhadap kategori BMI pengguna selama program kesehatan berlangsung?")
    
    # Proses Analisis Eksak dari Kode Anda
    bmi_analysis = (
        df.groupby('BMI_Category')[
            ['Sleep_Duration', 'Stress_Level', 'Daily_Steps']
        ]
        .mean()
    )
    bmi_order = ['Underweight', 'Normal', 'Overweight', 'Obese']
    bmi_analysis = bmi_analysis.reindex(bmi_order)
    my_colors = ['#8dd3c7', '#fdb462', '#bebada', '#fb8072']

    # Visualisasi Eksak Seperti Di File Anda
    fig1, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig1.suptitle('Rata-rata Gaya Hidup terhadap Kategori BMI', fontsize=16, fontweight='bold', y=1.05)

    # Grafik Durasi Tidur
    axes[0].bar(bmi_analysis.index, bmi_analysis['Sleep_Duration'], color=my_colors)
    axes[0].set_title('Rata-rata Durasi Tidur', fontsize=12)
    axes[0].set_ylabel('Durasi (Jam)', fontsize=11)

    # Grafik Tingkat Stres
    axes[1].bar(bmi_analysis.index, bmi_analysis['Stress_Level'], color=my_colors)
    axes[1].set_title('Rata-rata Tingkat Stres', fontsize=12)
    axes[1].set_ylabel('Skala (1-10)', fontsize=11)

    # Grafik Langkah Harian
    axes[2].bar(bmi_analysis.index, bmi_analysis['Daily_Steps'], color=my_colors)
    axes[2].set_title('Rata-rata Langkah Harian', fontsize=12)
    axes[2].set_ylabel('Jumlah Langkah', fontsize=11)

    # Menambahkan Label Angka di Atas Bar
    for i, col in enumerate(['Sleep_Duration', 'Stress_Level', 'Daily_Steps']):
        for j, value in enumerate(bmi_analysis[col]):
            axes[i].text(j, value + (value * 0.02), f'{value:.1f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    st.pyplot(fig1)
    
    # TABEL DATA INTERAKTIF & UNDUH
    st.subheader("Tabel Data Rata-rata Gaya Hidup berdasarkan Kategori BMI")
    st.markdown("*Gunakan ikon di pojok kanan atas tabel untuk mengunduh file CSV. Anda juga bisa mengurutkan data dengan menekan nama kolom.*")
    st.dataframe(bmi_analysis, use_container_width=True)
    
    # Insight Eksak yang Sudah Disepakati
    st.subheader("Eksplorasi dan Interpretasi Data")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Fakta Data Berdasarkan Visualisasi:**
        1. **Durasi Tidur:** Rata-rata waktu tidur di seluruh kategori BMI menunjukkan nilai yang seragam, yaitu berada pada angka 7 jam.
        2. **Tingkat Stres:** Nilai rata-rata tingkat stres antar kategori berada di skala moderat (kisaran skala 5). Pengguna dengan kategori berat badan *Normal* memiliki angka stres terendah (4.9), sementara kategori *Underweight* mencatatkan angka tertinggi (5.1).
        3. **Langkah Harian:** Variasi paling kontras terlihat pada intensitas gerak fisik. Pengguna berkategori *Normal* melakukan aktivitas jalan kaki tertinggi (rata-rata 8180.6 langkah), sedangkan kelompok pengguna dengan obesitas (*Obese*) mencatatkan aktivitas gerak paling rendah yaitu sebesar 7947.0 langkah.
        """)
    with col2:
        st.markdown("""
        **Kesimpulan:**
        Variabel durasi tidur dan tingkat stres pengguna secara umum berada pada kondisi yang seimbang dan tidak memicu perbedaan klasifikasi klinis BMI yang signifikan. Faktor pembeda paling utama yang memengaruhi penempatan kategori berat badan pengguna dalam data ini adalah tingkat aktivitas fisik harian (mobilitas gerak kaki).
        
        **Saran Pengembangan Website:**
        Algoritma sistem rekomendasi di HabitSense terbukti sudah menyasar akar masalah yang tepat. Untuk memaksimalkan hasil kebugaran, sistem disarankan memberikan bobot prioritas rekomendasi yang lebih tinggi pada rutinitas pencapaian jalan kaki harian (*daily steps*), khususnya bagi kelompok pengguna di kategori *Overweight* dan *Obese*.
        """)

# ------------------------------------------------------------------------------
# TAB 2: TARGET KALORI VS GOAL TYPE
# ------------------------------------------------------------------------------
with tab2:
    st.header("Pertanyaan 2: Apakah pengguna dengan goal type berbeda memiliki kebutuhan target kalori harian yang berbeda selama periode program kesehatan?")
    
    # Proses Analisis Eksak dari Kode Anda
    goal_analysis = (
        df.groupby('Goal_Type')['Target_Calorie_Day']
        .mean()
    )
    goal_order = ['Cutting', 'Maintain', 'Bulking']
    goal_analysis = goal_analysis.reindex(goal_order)
    my_colors_goal = ['#fb8072', '#bebada', '#8dd3c7']

    # Visualisasi Eksak Seperti Di File Anda
    fig2, ax2 = plt.subplots(figsize=(9, 6))
    bars = ax2.bar(goal_analysis.index, goal_analysis.values, color=my_colors_goal)

    ax2.set_title('Rata-rata Target Kalori Harian Berdasarkan Goal Type', fontsize=15, fontweight='bold', pad=15)
    ax2.set_xlabel('Tujuan Program (Goal Type)', fontsize=12)
    ax2.set_ylabel('Rata-rata Target Kalori (kcal)', fontsize=12)

    # Menambahkan Label Angka di Atas Bar
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + (yval * 0.02), f'{yval:.0f} kcal',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

    sns.despine()
    plt.tight_layout()
    st.pyplot(fig2)
    
    # TABEL DATA INTERAKTIF & UNDUH
    st.subheader("Tabel Data Rata-rata Target Kalori berdasarkan Goal Type")
    st.markdown("*Gunakan opsi di pojok kanan atas tabel untuk menyaring atau mengunduh dataset ringkasan ini.*")
    goal_df = goal_analysis.to_frame(name='Rata-rata Target Kalori (kcal)')
    st.dataframe(goal_df, use_container_width=True)
    
    # Insight Eksak yang Sudah Disepakati
    st.subheader("Eksplorasi dan Interpretasi Data")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Fakta Data Berdasarkan Visualisasi:**
        Grafik batang menunjukkan adanya diferensiasi alokasi kalori harian rata-rata yang sangat jelas yang disesuaikan dengan tujuan program kesehatan yang dipilih. 
        * Pengguna dengan opsi penurunan berat badan (*Cutting*) dibatasi pada pemenuhan energi paling rendah, yakni sebesar **1719 kkal**.
        * Pengguna penjagaan berat badan (*Maintain*) menempati posisi menengah dengan pasokan **1826 kkal**.
        * Pengguna penambahan massa tubuh (*Bulking*) dialokasikan pada target kalori tertinggi mencapai **2114 kkal**.
        """)
    with col2:
        st.markdown("""
        **Kesimpulan:**
        Angka-angka ini membuktikan bahwa algoritma penentuan kalori di dalam sistem HabitSense sudah berjalan dengan benar. Sistem sudah otomatis menyesuaikan target kalori sesuai dengan prinsip kesehatan dasar, yaitu mengurangi asupan bagi yang ingin kurus dan menambah asupan bagi yang ingin gemuk.
        
        **Saran untuk Sistem:**
        Karena logika perhitungan kalorinya sudah terbukti akurat dan valid secara data, parameter ini sudah siap dan aman digunakan sebagai fondasi utama di balik layar aplikasi HabitSense. Algoritma yang ada saat ini sudah sangat cukup untuk mendukung program kesehatan pengguna, sehingga tidak perlu ada perombakan atau penambahan fitur perhitungan baru.
        """)

# ------------------------------------------------------------------------------
# TAB 3: DURASI PROGRAM VS TARGET PERUBAHAN BERAT BADAN
# ------------------------------------------------------------------------------
with tab3:
    st.header("Pertanyaan 3: Bagaimana pengaruh durasi program kesehatan terhadap perubahan target berat badan pengguna selama program berlangsung?")
    
    # Visualisasi Eksak Menggunakan df_clean Seperti Di File Anda
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.scatter(
        df_clean['Program_Duration_Days'],
        df_clean['Weight_Change'],
        alpha=0.5
    )
    
    # Garis tengah eksak
    ax3.axhline(
        y=0,
        linestyle='--'
    )

    ax3.set_title('Program Duration vs Target Weight Change')
    ax3.set_xlabel('Program Duration (Days)')
    ax3.set_ylabel('Weight Change (kg)')
    ax3.grid(True)
    
    plt.tight_layout()
    st.pyplot(fig3)
    
    # TABEL DATA INTERAKTIF & UNDUH
    st.subheader("Filter dan Telusuri Data Bersih (df_clean)")
    st.markdown("*Di bawah ini adalah data yang telah melewati pembersihan outlier ekstrem. Anda bisa memfilter, mencari ID tertentu, melakukan sorting, dan mengunduh seluruh baris data.*")
    display_cols = ['BMI_Category', 'Goal_Type', 'Program_Duration_Days', 'Weight_kg', 'Target_Weight_kg', 'Weight_Change']
    st.dataframe(df_clean[display_cols], use_container_width=True)
    
    # Insight Eksak yang Sudah Disepakati
    st.subheader("Eksplorasi dan Interpretasi Data")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Fakta Data Berdasarkan Visualisasi:**
        Grafik *scatter plot* menunjukkan sebaran data yang mendatar horizontal, yang menandakan tidak adanya korelasi antara besaran target perubahan berat dengan durasi program kesehatan. Detail sebaran data pada grafik menampilkan tiga karakteristik utama:
        1. **Kelompok Mayoritas Penurunan Berat Badan (Rentang -15 kg hingga -2 kg):** Kepadatan data paling tinggi dan berbentuk balok padat berada di area negatif, yang mewakili pengguna dengan program *Cutting*. Kelompok pengguna ini tersebar merata di seluruh durasi program, mulai dari jangka pendek (30 hari) hingga jangka panjang (365 hari) tanpa ada kecenderungan pola linier.
        2. **Kelompok Peningkatan Berat Badan (Rentang +2 kg hingga +10 kg):** Kepadatan kedua berada di area positif, yang mewakili pengguna dengan program *Bulking*. Sama seperti kelompok sebelumnya, sebaran titik data meluas secara konstan dari durasi 30 hingga 365 hari.
        3. **Kelompok Target Tetap (Garis Padat di Angka 0):** Terlihat sebuah garis lurus yang sangat solid tepat di angka 0, menunjukkan kelompok pengguna *Maintain* yang juga berkomitmen pada berbagai variasi durasi program dari 1 bulan hingga 1 tahun.
        4. **Pencilan Data (Di luar batas -15 kg dan +10 kg):** Terdapat titik-titik data yang menyebar di area bawah (antara -15 kg hingga -25 kg) dan sedikit di area atas (di atas +10 kg). Pengguna di area ini memiliki target yang relatif lebih besar, namun tetap menentukan durasi waktu secara acak.
        """)
    with col2:
        st.markdown("""
        **Kesimpulan:**
        Durasi program kesehatan tidak memiliki pengaruh terhadap besaran target perubahan berat badan yang ditentukan pengguna. Baik pengguna yang memiliki target ringan maupun target yang cukup berat (-25 kg), mereka tetap menentukan jumlah hari program secara acak berdasarkan preferensi subjektif, bukan berdasarkan perhitungan logis atau pedoman standar kesehatan.
        
        **Saran Pengembangan Website:**
        Fakta bahwa sebaran data berbentuk acak menunjukkan adanya kebutuhan panduan standar di dalam sistem. Pada formulir pendaftaran (*Onboarding*) website HabitSense, pengisian kolom durasi sebaiknya tidak dibiarkan kosong untuk diketik manual oleh pengguna. Website disarankan menerapkan **Fitur Saran Durasi Otomatis (Smart Suggestion)**. Ketika pengguna memasukkan target berat badan, antarmuka website akan langsung menghitung dan mengunci rekomendasi durasi yang aman berdasarkan standar medis (misalnya pembatasan otomatis dengan prinsip penurunan atau kenaikan berat badan maksimal 0.5 kg hingga 1 kg per minggu).
        """)