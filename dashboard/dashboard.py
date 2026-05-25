import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="HabitSense Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_and_process_data():
    df = pd.read_csv("dashboard/habitsense_clean.csv")

    df["Weight_Change"] = df["Target_Weight_kg"] - df["Weight_kg"]

    Q1 = df["Weight_Change"].quantile(0.25)
    Q3 = df["Weight_Change"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - (1.5 * IQR)
    upper = Q3 + (1.5 * IQR)

    df_clean = df[
        (df["Weight_Change"] >= lower) &
        (df["Weight_Change"] <= upper)
    ]

    return df, df_clean


try:
    df, df_clean = load_and_process_data()
except FileNotFoundError:
    st.error("File 'habitsense_clean.csv' tidak ditemukan. Pastikan file CSV berada satu folder dengan app.py.")
    st.stop()


# =========================
# SIDEBAR FILTER GLOBAL
# =========================
st.sidebar.title("Filter Dashboard")

bmi_options = st.sidebar.multiselect(
    "Pilih Kategori BMI",
    options=df["BMI_Category"].dropna().unique(),
    default=df["BMI_Category"].dropna().unique()
)

goal_options = st.sidebar.multiselect(
    "Pilih Goal Type",
    options=df["Goal_Type"].dropna().unique(),
    default=df["Goal_Type"].dropna().unique()
)

min_duration = int(df["Program_Duration_Days"].min())
max_duration = int(df["Program_Duration_Days"].max())

duration_range = st.sidebar.slider(
    "Rentang Durasi Program",
    min_value=min_duration,
    max_value=max_duration,
    value=(min_duration, max_duration)
)

min_age = int(df["Age"].min()) if "Age" in df.columns else None
max_age = int(df["Age"].max()) if "Age" in df.columns else None

if "Age" in df.columns:
    age_range = st.sidebar.slider(
        "Rentang Usia",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )
else:
    age_range = None


# Filter global
filtered_df = df[
    (df["BMI_Category"].isin(bmi_options)) &
    (df["Goal_Type"].isin(goal_options)) &
    (df["Program_Duration_Days"].between(duration_range[0], duration_range[1]))
]

filtered_clean_df = df_clean[
    (df_clean["BMI_Category"].isin(bmi_options)) &
    (df_clean["Goal_Type"].isin(goal_options)) &
    (df_clean["Program_Duration_Days"].between(duration_range[0], duration_range[1]))
]

if "Age" in df.columns:
    filtered_df = filtered_df[
        filtered_df["Age"].between(age_range[0], age_range[1])
    ]

    filtered_clean_df = filtered_clean_df[
        filtered_clean_df["Age"].between(age_range[0], age_range[1])
    ]


# =========================
# HEADER
# =========================
st.title("Eksplorasi Data Program Kesehatan HabitSense")
st.markdown(
    "Dashboard interaktif untuk menganalisis gaya hidup, kebutuhan kalori, "
    "dan perencanaan program kesehatan pengguna."
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Data", len(filtered_df))
col2.metric("Rata-rata Durasi Program", f"{filtered_df['Program_Duration_Days'].mean():.0f} hari")
col3.metric("Rata-rata Daily Steps", f"{filtered_df['Daily_Steps'].mean():.0f}")
col4.metric("Rata-rata Target Kalori", f"{filtered_df['Target_Calorie_Day'].mean():.0f} kcal")

st.markdown("---")


tab1, tab2, tab3 = st.tabs([
    "1. Gaya Hidup vs BMI",
    "2. Target Kalori vs Goal",
    "3. Durasi Program vs Perubahan Berat"
])


# =========================
# TAB 1
# =========================
with tab1:
    st.header("Gaya Hidup vs Kategori BMI")

    lifestyle_metric = st.selectbox(
        "Pilih metrik gaya hidup yang ingin dianalisis",
        ["Sleep_Duration", "Stress_Level", "Daily_Steps"]
    )

    bmi_order = ["Underweight", "Normal", "Overweight", "Obese"]

    bmi_analysis = (
        filtered_df
        .groupby("BMI_Category")[["Sleep_Duration", "Stress_Level", "Daily_Steps"]]
        .mean()
        .reindex(bmi_order)
        .dropna()
    )

    fig1, ax1 = plt.subplots(figsize=(10, 6))

    colors = ["#8dd3c7", "#bebada", "#fdb462", "#fb8072"]

    bars = ax1.bar(
        bmi_analysis.index,
        bmi_analysis[lifestyle_metric],
        color=colors[:len(bmi_analysis)]
    )

    ax1.set_title(f"Rata-rata {lifestyle_metric} berdasarkan Kategori BMI", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Kategori BMI")
    ax1.set_ylabel(lifestyle_metric)

    for bar in bars:
        yval = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            yval + (yval * 0.02),
            f"{yval:.1f}",
            ha="center",
            va="bottom"
        )

    sns.despine()
    plt.tight_layout()
    st.pyplot(fig1)

    st.subheader("Tabel Ringkasan")
    st.dataframe(bmi_analysis, use_container_width=True)

    st.markdown("""
    **Insight:**  
    Filter ini membantu melihat apakah pola gaya hidup pengguna berubah berdasarkan kategori BMI tertentu.  
    Dari grafik, metrik seperti langkah harian dapat dibandingkan langsung untuk melihat kelompok mana yang memiliki aktivitas fisik lebih rendah.
    """)


# =========================
# TAB 2
# =========================
with tab2:
    st.header("Target Kalori Harian vs Goal Type")

    calorie_view = st.radio(
        "Pilih jenis analisis kalori",
        ["Rata-rata", "Median", "Maksimum", "Minimum"],
        horizontal=True
    )

    agg_map = {
        "Rata-rata": "mean",
        "Median": "median",
        "Maksimum": "max",
        "Minimum": "min"
    }

    goal_order = ["Cutting", "Maintain", "Bulking"]

    goal_analysis = (
        filtered_df
        .groupby("Goal_Type")["Target_Calorie_Day"]
        .agg(agg_map[calorie_view])
        .reindex(goal_order)
        .dropna()
    )

    fig2, ax2 = plt.subplots(figsize=(9, 6))

    colors_goal = ["#fb8072", "#bebada", "#8dd3c7"]

    bars = ax2.bar(
        goal_analysis.index,
        goal_analysis.values,
        color=colors_goal[:len(goal_analysis)]
    )

    ax2.set_title(f"{calorie_view} Target Kalori Harian berdasarkan Goal Type", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Goal Type")
    ax2.set_ylabel("Target Kalori Harian (kcal)")

    for bar in bars:
        yval = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            yval + (yval * 0.02),
            f"{yval:.0f} kcal",
            ha="center",
            va="bottom",
            fontweight="bold"
        )

    sns.despine()
    plt.tight_layout()
    st.pyplot(fig2)

    st.subheader("Tabel Ringkasan")
    goal_df = goal_analysis.to_frame(name=f"{calorie_view} Target Kalori")
    st.dataframe(goal_df, use_container_width=True)

    st.markdown("""
    **Insight:**  
    Filter ini cocok untuk melihat apakah perbedaan target kalori antar goal tetap konsisten setelah data disaring berdasarkan BMI, usia, atau durasi program.
    """)


# =========================
# TAB 3
# =========================
with tab3:
    st.header("Durasi Program vs Target Perubahan Berat Badan")

    goal_filter_tab3 = st.multiselect(
        "Filter Goal Type untuk Scatter Plot",
        options=filtered_clean_df["Goal_Type"].dropna().unique(),
        default=filtered_clean_df["Goal_Type"].dropna().unique()
    )

    weight_min = float(filtered_clean_df["Weight_Change"].min())
    weight_max = float(filtered_clean_df["Weight_Change"].max())

    weight_change_range = st.slider(
        "Rentang Target Perubahan Berat Badan",
        min_value=weight_min,
        max_value=weight_max,
        value=(weight_min, weight_max)
    )

    scatter_df = filtered_clean_df[
        (filtered_clean_df["Goal_Type"].isin(goal_filter_tab3)) &
        (filtered_clean_df["Weight_Change"].between(weight_change_range[0], weight_change_range[1]))
    ]

    fig3, ax3 = plt.subplots(figsize=(10, 6))

    sns.scatterplot(
        data=scatter_df,
        x="Program_Duration_Days",
        y="Weight_Change",
        hue="Goal_Type",
        alpha=0.6,
        ax=ax3
    )

    ax3.axhline(y=0, linestyle="--")
    ax3.set_title("Program Duration vs Target Weight Change", fontsize=14, fontweight="bold")
    ax3.set_xlabel("Program Duration (Days)")
    ax3.set_ylabel("Weight Change (kg)")
    ax3.grid(True)

    plt.tight_layout()
    st.pyplot(fig3)

    st.subheader("Data Hasil Filter")
    display_cols = [
        "BMI_Category",
        "Goal_Type",
        "Program_Duration_Days",
        "Weight_kg",
        "Target_Weight_kg",
        "Weight_Change"
    ]

    st.dataframe(scatter_df[display_cols], use_container_width=True)

    st.markdown("""
    **Insight:**  
    Filter ini membantu melihat apakah durasi program berubah sesuai target berat tertentu.  
    Jika titik tetap menyebar acak setelah difilter, berarti durasi program belum mengikuti perhitungan target berat yang ideal.
    """)
