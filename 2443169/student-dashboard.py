import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide"
)

# Title
st.markdown(
    "<h1 style='text-align:center;color:blue;'>🎓 Student Performance Dashboard</h1>",
    unsafe_allow_html=True
)

st.write("Analyze and visualize student performance data")

# Load CSV
df = pd.read_csv("student_performance.csv")

# Sidebar filters
st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

semester = st.sidebar.multiselect(
    "Semester",
    sorted(df["Semester"].unique()),
    default=sorted(df["Semester"].unique())
)

attendance = st.sidebar.slider(
    "Attendance Range",
    int(df["Attendance"].min()),
    int(df["Attendance"].max()),
    (
        int(df["Attendance"].min()),
        int(df["Attendance"].max())
    )
)

# Unique small addition
search = st.sidebar.text_input(
    "Search Student Name"
)

# Filter data
filtered = df[
    (df["Department"].isin(department))
    &
    (df["Semester"].isin(semester))
    &
    (df["Attendance"].between(
        attendance[0],
        attendance[1]
    ))
]

if search:
    filtered = filtered[
        filtered["Name"].str.contains(
            search,
            case=False
        )
    ]

# Display data
st.subheader("Student Data")
st.dataframe(filtered)

# Summary
c1,c2,c3 = st.columns(3)

with c1:
    st.metric(
        "Students",
        len(filtered)
    )

with c2:
    st.metric(
        "Average Marks",
        round(filtered["Marks"].mean(),2)
    )

with c3:
    st.metric(
        "Average Attendance",
        round(filtered["Attendance"].mean(),2)
    )

# Top students (small unique feature)
st.subheader("🏆 Top 5 Students")

top = filtered.sort_values(
    by="Marks",
    ascending=False
).head(5)

st.table(
    top[["Name","Marks"]]
)

# Charts

fig1 = px.bar(
    filtered.groupby("Department")["Marks"]
    .mean()
    .reset_index(),
    x="Department",
    y="Marks",
    title="Average Marks by Department"
)

st.plotly_chart(fig1)

fig2 = px.pie(
    filtered,
    names="Semester",
    title="Semester Distribution"
)

st.plotly_chart(fig2)

fig3 = px.histogram(
    filtered,
    x="Marks",
    title="Marks Distribution"
)

st.plotly_chart(fig3)

fig4 = px.scatter(
    filtered,
    x="Attendance",
    y="Marks",
    color="Department",
    hover_data=["Name"],
    title="Attendance vs Marks"
)

st.plotly_chart(fig4)

# Download option
csv = filtered.to_csv(index=False)

st.download_button(
    "Download CSV",
    csv,
    "filtered_students.csv",
    "text/csv"
)