import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other' #autres champ nom 'Other' qui
    return categorical_map


def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    dataSal = pd.read_csv("survey_results_public.csv")
    dataSal = dataSal[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    dataSal = dataSal[dataSal["ConvertedComp"].notnull()]
    dataSal = dataSal.dropna()
    dataSal = dataSal[dataSal["Employment"] == "Employed full-time"]
    dataSal = dataSal.drop("Employment", axis=1)

    country_map = shorten_categories(dataSal.Country.value_counts(), 400)
    dataSal["Country"] = dataSal["Country"].map(country_map)
    dataSal = dataSal[dataSal["ConvertedComp"] <= 250000]
    dataSal = dataSal[dataSal["ConvertedComp"] >= 10000]
    dataSal = dataSal[dataSal["Country"] != "Other"]

    dataSal["YearsCodePro"] = dataSal["YearsCodePro"].apply(clean_experience)
    dataSal["EdLevel"] = dataSal["EdLevel"].apply(clean_education)
    dataSal = dataSal.rename({"ConvertedComp": "Salary"}, axis=1)
    return dataSal


dataSal = load_data()


def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(""" ### Stack Overflow Developer Survey 2020""")

    data = dataSal["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)

    st.write("""#### Mean Salary Based On Country""")

    data = dataSal.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""#### Mean Salary Based On Experience""")

    data = dataSal.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)