import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Juice & Smoothie Sales Dashboard")

# File uploader (CSV or Excel)
uploaded_file = st.file_uploader(
    "Upload the juice sales dataset (CSV or Excel file)", 
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    # Read the file depending on type 
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # Preview of the dataset 
    st.write("### Preview of the Dataset")
    st.subheader("First Few Rows")
    st.dataframe(df.head())
    st.subheader("Last Few Rows")
    st.dataframe(df.tail())

  
    # Clean / Convert Date Ordered to a datetime column
    # Date Ordered -> datetime
    if "Date Ordered" in df.columns:
        df["Date Ordered"] = pd.to_datetime(df["Date Ordered"], errors="coerce")

    # "$ Sales" -> numeric Sales column
    if "$ Sales" in df.columns:
        df["Sales"] = (
            df["$ Sales"]
            .replace(r"[\$,]", "", regex=True)  # remove $ and commas if present
            .astype(float)
        )

    # Service Satisfaction Rating -> numeric
    if "Service Satisfaction Rating" in df.columns:
        df["Service Satisfaction Rating"] = pd.to_numeric(
            df["Service Satisfaction Rating"], errors="coerce"
        )

  
    tab1, tab2, tab3 = st.tabs([
        "Q1: Category Sales Comparison",
        "Q2: Sales Over Time",
        "Q3: Satisfaction Ratings"
    ])
    # Q1: Sales Performance of Juices vs Smoothies
    with tab1:
        st.subheader("Category Sales Comparison")

        # Group by Category and calculate the total $ Sales for each category
        category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        )

        # Show table of total sales by category
        st.write("Total sales by category:")
        st.dataframe(
            category_sales.reset_index().rename(
            columns={"$ Sales": "Total Sales ($)"}
            )
        )

        # Bar chart of sales by category
        fig1, ax1 = plt.subplots()
        ax1.bar(category_sales.index, category_sales.values)
        ax1.set_xlabel("Category")
        ax1.set_ylabel("Total Sales ($)")
        ax1.set_title("Total Sales by Category")

        st.pyplot(fig1)

        # Brief interpretation
        st.subheader("Interpretation")
        top_category = category_sales.idxmax()
        top_value = category_sales.max()

        st.write(
            f"- **{top_category}** has the highest total sales "
            f"(about **${top_value:,.2f}**)."
        )
        st.write(
            "- This comparison helps management see which category "
            "is performing better in terms of revenue."
        )
  
    # Q2: Sales Over Time
    with tab2:
        st.subheader("Question 2: Sales Over Time")

        # Drop rows with missing date or sales
        time_df = df.dropna(subset=["Date Ordered", "Sales"])

        # Group by date ordered and sum sales
        daily_sales = (
        time_df.groupby("Date Ordered")["Sales"]
        .sum()
        .sort_index()
        )

        # Show table of daily total sales
        st.write("Daily total sales:")
        st.dataframe(
            daily_sales.reset_index().rename(
                columns={"Sales": "Total Sales ($)"}
            )
        )

        # Line chart of trends in daily sales
        fig2, ax2 = plt.subplots()
        ax2.plot(daily_sales.index, daily_sales.values, marker="o")
        ax2.set_xlabel("Date Ordered")
        ax2.set_ylabel("Total Sales ($)")
        ax2.set_title("Daily Sales Over Time")
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig2)

        # Brief interpretation
        st.subheader("Interpretation")
        peak_date = daily_sales.idxmax()
        peak_value = daily_sales.max()

        st.write(
            f"- The highest sales day is **{peak_date}** "
            f"with about **${peak_value:,.2f}** in total sales."
        )
        st.write(
         "- This time series helps management identify busy days and "
         "slower days when promotions or staffing changes might be needed."
        )
    # Q3: Service Satisfaction  Distribution
    with tab3:
        st.subheader("Question 3: Service Satisfaction Rating Distribution")

        # Select the column and drop missing values(hide missing values)
        sat_df = df.dropna(subset=["Service Satisfaction Rating"])

        # Count how many customers selected each rating
        rating_counts = sat_df["Service Satisfaction Rating"].value_counts().sort_index()

        # Display the counts in a table
        st.write("Count of customers by service satisfaction rating:")
        st.dataframe(
            rating_counts.reset_index().rename(
             columns={"index": "Rating", "Service Satisfaction Rating": "Count"}
            )
        )

        # Plot the distribution as a bar chart 
        fig, ax = plt.subplots()
        ax.bar(rating_counts.index.astype(str), rating_counts.values)
        ax.set_xlabel("Service Satisfaction Rating")
        ax.set_ylabel("Number of Customers")
        ax.set_title("Service Satisfaction Rating Distribution")

        st.pyplot(fig)

        # Interpretation 
        st.subheader("Interpretation")
        most_common_rating = rating_counts.idxmax()
        most_common_count = rating_counts.max()

        st.write(
         f"- The most common service satisfaction rating is **{int(most_common_rating)}**, "
            f"with **{most_common_count}** customers giving this score."
        )
        st.write(
            "- Higher ratings indicate customers were generally satisfied with service. "
            "If low ratings appear often, this may signal areas for improvement"
        )
else:
    st.info("Please upload the juice sales dataset to begin.")