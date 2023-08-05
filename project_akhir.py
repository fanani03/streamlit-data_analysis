import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        'registered': 'sum'
    })

    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday": "Month"
    }, inplace=True)

    return monthly_users_df

def create_season_count(df):
    season_count = df.groupby(by="season").cnt.sum().sort_values(ascending=False).reset_index()
    # Membuat dictionary untuk pemetaan nama musim
    mapping_season = {1: 'springer', 2: 'summer', 3: 'fall', 4: 'winter'}

    # Menggunakan metode map untuk merename nilai dalam kolom 'season'
    season_count['season'] = season_count['season'].map(mapping_season)
    return season_count


def create_weather_count(df):
    weather_count = df.groupby(by="weathersit").cnt.sum().sort_values(ascending=False).reset_index()
    mapping_weather = {1: 'Clear', 2: 'Mist', 3: 'Light Snow'}
    weather_count['weathersit'] = weather_count['weathersit'].map(mapping_weather)
    return weather_count

def create_perbandingan(df):
    df_season_casReg = df[['season', 'casual', 'registered']]
    mapping_season = {1: 'springer', 2: 'summer', 3: 'fall', 4: 'winter'}
    df_season_casReg['season'] = df_season_casReg['season'].map(mapping_season)

    return df_season_casReg


all_df = pd.read_csv("day.csv")


# Create filter berdasarkan order date dan delivery date
datetime_columns = [ "dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


# Membuat side bar

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:


    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# simpan data filter
main_df = all_df[(all_df["dteday"] >= str(start_date)) &
                (all_df["dteday"] <= str(end_date))]

monthly_users_df = create_monthly_users_df(main_df)
by_season = create_season_count(main_df)
by_weather = create_weather_count(main_df)
df_season_casReg = create_perbandingan(main_df)



#Dashboard

st.header('Dicoding Bike Dataset')

st.subheader('Monthly User')


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(monthly_users_df["Month"], monthly_users_df["casual"], marker='o', linewidth=2, color="green")
ax.plot(monthly_users_df["Month"], monthly_users_df["registered"], marker='o', linewidth=2, color="red")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


st.subheader("Season & Weather Favorits")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(x="season", y="cnt", data=by_season)
    ax.set_title("Musim Favorit", loc="center", fontsize=50)
    ax.set_ylabel('Jumlah ')
    ax.set_xlabel('Musim')
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    sns.barplot(x="weathersit", y="cnt", data=by_weather)

    ax.set_title("Cuaca Favorit", loc="center", fontsize=50)
    ax.set_ylabel('Jumlah ')
    ax.set_xlabel('Cuaca')
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.subheader('Perbandingan User Casual dan Registered')


st.set_option('deprecation.showPyplotGlobalUse', False)
# Melt DataFrame untuk memperbaiki struktur data agar sesuai dengan Seaborn
df_melted = df_season_casReg.melt(id_vars='season', value_vars=['casual', 'registered'], var_name='user_type', value_name='count')


sns.barplot(x='season', y='count', hue='user_type', data=df_melted)

ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
plt.xlabel('Season')
plt.ylabel('Count')
plt.title('Casual and Registered Users by Season')
plt.legend(title='User Type')

# Simpan plot ke file temporary
st.pyplot()
