import streamlit as st
from config import get_connection,is_cloud_env
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px




def fetch_and_save_data(table_name, save_path):
    conn = get_connection()  # Make sure your local database connection works
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    conn.close()
    df.to_csv(save_path, index=False)  # Save the data to a CSV file
    return df

# Example usage
fetch_and_save_data("raw_watersource", "data/raw_watersource.csv")
fetch_and_save_data("human_resources", "data/human_resources.csv")
fetch_and_save_data("treatment_plant", "data/treatment_plant.csv")
fetch_and_save_data("water_quality", "data/water_quality.csv")
fetch_and_save_data("commercial", "data/commercial.csv")
fetch_and_save_data("financial", "data/financial.csv")
fetch_and_save_data("distribution_network", "data/distribution_network.csv")

def fetch_data(table_name):
    # Dictionary to map table names to file paths
    table_to_file = {
        "raw_watersource": "data/raw_watersource.csv",
        "human_resources": "data/human_resources.csv",
        "treatment_plant": "data/treatment_plant.csv",
        "water_quality": "data/water_quality.csv",
        "commercial": "data/commercial.csv",
        "financial": "data/financial.csv",
        "distribution_network": "data/distribution_network.csv"
    }

    # Load the data from the CSV file
    file_path = table_to_file.get(table_name)
    if file_path:
        df = pd.read_csv(file_path)
        return df
    else:
        raise ValueError(f"Unknown table: {table_name}")


    
 

# Visualization function for outlier detection and box plot
def visualize_outliers_in_abstraction():
    st.subheader("Outliers in Total Abstraction")
    
    # Fetch data
    data1 = fetch_data("raw_watersource")
    
    # Calculate the IQR for outlier detection
    Q1 = data1['total_abstraction'].quantile(0.25)
    Q3 = data1['total_abstraction'].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define the lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Find outliers
    outliers = data1[(data1['total_abstraction'] < lower_bound) | (data1['total_abstraction'] > upper_bound)]
    st.write("Outliers Detected:")
    st.write(outliers)
    
    # Plot a box plot for total abstraction
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot(data1['total_abstraction'], vert=False, patch_artist=True, boxprops=dict(facecolor='lightblue'))
    ax.set_title('Box Plot for Total Abstraction')
    ax.set_xlabel('Total Abstraction (m³)')
    st.pyplot(fig)

    st.write("""

    - **X-Axis**: The x-axis represents the total abstraction in cubic meters (m³), ranging from 0 to 5000 m³, with intervals of 1000 m³.
    - **Box Plot Components**:
      - **Whiskers**: The whiskers extend from approximately 0 to just over 1000 m³ on the lower end and from approximately 2500 m³ to near 4000 m³ on the upper end. These whiskers represent the range of the data, excluding outliers.
      - **Box**: The rectangular box spans from just over 1000 m³ to roughly 2500 m³. This box represents the interquartile range (IQR), which contains the middle 50% of the data.
      - **Median**: The line inside the box is at about 1500 m³, indicating the median value of total abstraction. This is the midpoint of the data, where half of the values are below and half are above this point.
    - **Insights**:
      - **Distribution**: The majority of the total abstraction values lie between just over 1000 m³ and 2500 m³.
      - **Median**: The median value of total abstraction is around 1500 m³, suggesting that half of the abstraction values are below this amount and half are above.
      - **Range**: The total abstraction values range from 0 to near 4000 m³, indicating variability in the amount of water abstracted from different sources.
    """)

# Visualization function for water sources availability
def visualize_water_sources_by_availability():
    st.subheader("Water Sources by Availability Year Round")
    
    # Fetch data
    data1 = fetch_data("raw_watersource")
    
    # Separate water sources into available year-round and not available year-round
    available_year_round = data1[data1['availability_year_round'] == 1]
    not_available_year_round = data1[data1['availability_year_round'] == 0]
    
    # Count the number of sources in each group
    available_count = available_year_round.shape[0]
    not_available_count = not_available_year_round.shape[0]
    
    st.write(f"Number of Water Sources Available Year Round: {available_count}")
    st.write(f"Number of Water Sources Not Available Year Round: {not_available_count}")
    
    # Display the tables
    st.write("Available Year Round Water Sources:")
    available_year_round['total_abstraction_m3'] = available_year_round['total_abstraction'].apply(lambda x: f"{x} m³")
    st.write(available_year_round[['RawWaterSource_name', 'total_abstraction_m3']])

    st.write("""
    - **Year-Round Available Sources with Their Total Abstraction**:
      - `Mekong River`: 5000.5 m³
      - `Tonle Sap Lake`: 4500.0 m³
      - `Bassac River`: 3200.3 m³
      - `Stung Sen River`: 3500.2 m³
      - `Pursat River`: 3100.4 m³
      - `Srepok River`: 2900.6 m³
      - `Stung Prek Kampong River`: 3300.1 m³
      - `Stung Prek Pnov River`: 2200.7 m³
      - `Stung Prek Kdam River`: 2000.8 m³
      - `Stung Prek Khsach River`: 1800.6 m³
      - `Stung Prek Krouch River`: 1600.1 m³
      - `Stung Prek Krouy River`: 1400.7 m³
      - `Stung Prek Krouch River`: 1200.8 m³
      - `Stung Prek Khsach River`: 1000.6 m³
      - `Stung Prek Kdam River`: 800.1 m³
      - `Stung Prek Pnov River`: 600.7 m³
      - `Stung Prek Kampong River`: 400.8 m³
      - `Srepok River`: 200.6 m³
      - `Stung Sen River`: 100.9 m³
      - `Stung Treng River`: 50.1 m³
      - `Pursat River`: 25.5 m³
      - `Prek Thnot River`: 12.7 m³
      - `Tonle Sap Lake`: 3.8 m³
      - `Stung Prek Kroum River`: 0.9 m³
      - `Stung Prek Kranh River`: 0.3 m³
      - `Stung Prek Kbal River`: 0.1 m³
      - `Stung Prek Tnaot River`: 0.03 m³
      - `Stung Prek Thnot River`: 0.01 m³
      - `Stung Chinit River`: 0.003 m³
    """)

    
    st.write("Not Available Year Round Water Sources:")
    not_available_year_round['total_abstraction_m3'] = not_available_year_round['total_abstraction'].apply(lambda x: f"{x} m³")
    st.write(not_available_year_round[['RawWaterSource_name', 'total_abstraction_m3']])

    st.write("""
    - **Not Available Year Round Water Sources**:
      - `Prek Thnot River`: 2800.7 m³
      - `Stung Treng River`: 2700.8 m³
      - `Stung Chinit River`: 2600.9 m³
      - `Stung Prek Thnot River`: 2400.5 m³
      - `Stung Prek Tnaot River`: 2100.3 m³
      - `Stung Prek Kbal River`: 1900.4 m³
      - `Stung Prek Kranh River`: 1700.9 m³
      - `Stung Prek Kroum River`: 1500.5 m³
      - `Stung Prek Kroum River`: 1300.3 m³
      - `Stung Prek Kranh River`: 1100.4 m³
      - `Stung Prek Kbal River`: 900.9 m³
      - `Stung Prek Tnaot River`: 700.5 m³
      - `Stung Prek Thnot River`: 500.3 m³
      - `Stung Chinit River`: 300.4 m³
      - `Bassac River`: 6.3 m³
      - `Mekong River`: 1.9 m³
      - `Stung Prek Krouch River`: 0.5 m³
      - `Stung Prek Khsach River`: 0.2 m³
      - `Stung Prek Kdam River`: 0.05 m³
      - `Stung Prek Pnov River`: 0.02 m³
      - `Stung Prek Kampong River`: 0.005 m³
    """)


# Visualization function for water sources abstraction bar chart
def visualize_abstraction_bar_chart():
    st.subheader("Water Sources Total Abstraction Bar Chart")
    
    # Fetch data
    data1 = fetch_data("raw_watersource")
    
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(data1['RawWaterSource_name'], data1['total_abstraction'], color='blue')
    
    ax.set_xlabel('Total Abstraction (m³)')
    ax.set_ylabel('Raw Water Source Name')
    ax.set_title('Total Abstraction by Raw Water Source')
    
    st.pyplot(fig)

    st.write("""
    - **Water Sources and Abstraction Volumes**:
      - `Stung Prek Krouy River`: Lower abstraction volume.
      - `Stung Prek Kroum River`: Two instances with varying abstraction volumes.
      - `Stung Prek Touch River`: Moderate abstraction volume.
      - `Stung Prek Thnot River`: Moderate abstraction volume.
      - `Stung Sen River`: Two instances with varying abstraction volumes.
      - `Stung Prek Kampong River`: Moderate abstraction volume.
      - `Chinit River`: Moderate abstraction volume.
      - `Sangker River`: Moderate abstraction volume.
      - `Pursat River`: Two instances with varying abstraction volumes.
      - `Tonle Sap Lake`: Higher abstraction volume.
      - `Mekong River`: Three instances with varying abstraction volumes.
      - `Bassac River`: Higher abstraction volume.
    - **Insights**:
      - **Distribution**: The chart shows a wide range of abstraction volumes across different water sources.
      - **High Abstraction**: Mekong River, Tonle Sap Lake, and Bassac River have higher abstraction volumes.
      - **Variability**: There is significant variability in the abstraction volumes, indicating different levels of water usage from each source.
    """)


# Visualization function for grouped abstraction by availability
def visualize_grouped_abstraction():
    st.subheader("Total Abstraction by Availability Year Round and Unavailable")
    
    # Fetch data
    data1 = fetch_data("raw_watersource")
    
    # Group by availability and sum total abstraction
    grouped = data1.groupby('availability_year_round').agg(
        total_abstraction_sum=('total_abstraction', 'sum'),
        water_sources=('RawWaterSource_name', lambda x: ', '.join(x))
    ).reset_index()
    
    # Plotting the grouped data
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(grouped['availability_year_round'], grouped['total_abstraction_sum'], color=['red', 'green'])
    
    ax.set_xticks(grouped['availability_year_round'])
    ax.set_xticklabels(['Not Available Year Round', 'Available Year Round'])
    ax.set_ylabel('Total Abstraction (m³)')
    ax.set_title('Total Abstraction by Availability Year Round')
    
    # Adding data labels on the bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 100, round(yval, 1), ha='center', va='bottom')
    
    st.pyplot(fig)

    st.write("""
    - **Bars**: There are two bars in the chart.
      - **Red Bar**: Labeled “Not Available Year Round,” with a total abstraction value of 22643.2 m³.
      - **Green Bar**: Labeled “Available Year Round,” with a total abstraction value of 38776.5 m³.
    - **Insights**:
      - **Comparison**: The chart visually compares the total abstraction quantities based on their availability throughout the year.
      - **Higher Abstraction**: The “Available Year Round” category has a significantly higher total abstraction (38902.9 m³) compared to the “Not Available Year Round” category (22516.8 m³).
      - **Implication**: This indicates that water sources available year-round contribute more to the total abstraction, highlighting their importance in water resource management.
    """)


# Visualization function for total abstraction capacity
# Visualization function for total abstraction capacity
def visualize_total_abstraction_capacity():
    st.subheader("Total Abstraction Capacity Trend for Each Raw Water Source")
    
    # Fetch data
    data1 = fetch_data("raw_watersource")
    data1 = data1.sort_values(by='total_abstraction', ascending=False)
    
    # Plot line chart
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        x='RawWaterSource_name', 
        y='total_abstraction', 
        data=data1, 
        marker='o',
        linewidth=2.5,
        color='blue'
    )
    plt.title('Total Abstraction Capacity Trend', fontsize=16, fontweight='bold')
    plt.xlabel('Raw Water Source', fontsize=12)
    plt.ylabel('Total Abstraction (in cubic meters)', fontsize=12)
    plt.xticks(rotation=45, fontsize=10, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

    st.write("""
    - **Bars**: Each bar represents the total abstraction capacity of a water source, with varying heights indicating different capacities.
    - **Water Sources and Abstraction Capacities**:
      
    - **Interpret** :
Larger, more prominent rivers like the Mekong River and Tonle Sap Lake dominate total abstraction capacities, likely due to their size and accessibility.
Smaller rivers and tributaries contribute less, potentially because of their limited capacity, geographical constraints, or lower demand.
- **Insights:**
The graph could help policymakers or engineers prioritize resource allocation, infrastructure development, or conservation efforts towards the most abstracted sources.

    """)


# Fetch data function for human resources analysis
def fetch_data_for_human_resources():
    data1 = fetch_data("raw_watersource")  # Fetch raw water source data
    data2 = fetch_data("human_resources")  # Fetch human resources data
    return pd.merge(data1, data2, on='idRawWaterSource')

# Streamlit app for human resources analysis
def human_resources_analysis():

    st.subheader("Human Resources Analysis")

    # Fetch and merge data
    df_merged12 = fetch_data_for_human_resources()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    df_merged12.groupby('RawWaterSource_name')['total_staff'].sum().plot.pie(
        autopct='%1.1f%%', startangle=90, ax=ax, legend=False
    )
    ax.set_ylabel('')  # Remove y-axis label for cleaner layout
    ax.set_title('Proportion of Total Staff by Raw Water Source')
    plt.tight_layout()
    st.pyplot(fig)
    st.write("""
    - **Distribution**: The chart shows a wide range of staff numbers across different water sources.
    - **High Staff Numbers**: Mekong River, Tonle Sap Lake, and Bassac River have the highest staff numbers.
    - **Variability**: There is significant variability in the staff numbers, indicating different levels of human resource allocation for each water source.
    """)


    # Human Resources - Comparison of Total Staff, Staff per 1000 Subscribers, and Training Sessions
    st.subheader("Comparison of Total Staff, Staff per 1000 Subscribers, and Training Sessions")
    fig, ax = plt.subplots(figsize=(16, 8))
    bar_width = 0.25  # Width of the bars
    index = np.arange(len(df_merged12['RawWaterSource_name']))  # The x locations for the groups
    
    # Create bars for each category
    bars1 = ax.bar(index, df_merged12['total_staff'], bar_width, label='Total Staff', color='skyblue')
    bars2 = ax.bar(index + bar_width, df_merged12['staff_per_1000_subscribers'], bar_width, label='Staff per 1000 Subscribers', color='lightgreen')
    bars3 = ax.bar(index + 2 * bar_width, df_merged12['training_sessions'], bar_width, label='Training Sessions', color='salmon')

    # Set labels and title
    ax.set_xlabel('Water Resouces')
    ax.set_ylabel('Count')
    ax.set_title('Water Resources Overview')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(df_merged12['RawWaterSource_name'], rotation=45, ha='right')
    
    # Add legend
    ax.legend()

    # Add data labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)

    st.write("""
    - **Distribution**: The chart shows a wide range of staff numbers, staff per 1000 subscribers, and training sessions across different water resources.
    - **High Values**: Mekong River, Tonle Sap Lake, and Bassac River have the highest values in all three categories.
    - **Variability**: There is significant variability in the values, indicating different levels of human resource allocation and training efforts for each water resource.
    """)

    fig = px.scatter(
    df_merged12,
    x='RawWaterSource_name',
    y='staff_per_1000_subscribers',
    size='total_staff',
    color='staff_per_1000_subscribers',
    title='Staff per 1000 Subscribers (Bubble Chart)',
    labels={'staff_per_1000_subscribers': 'Staff/1000 Subscribers', 'RawWaterSource_name': 'Raw Water Source'},
    size_max=50,
    color_continuous_scale='Viridis'
    )
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig)



    st.write("""
    - Represented by blue bars.
    - Indicates the number of staff members allocated to each raw water source.
    - For example, the Mekong River has the highest number of total staff compared to other sources.
    """)


    st.write("""
    - Represented by an orange line with markers.
    - Shows the efficiency of staffing relative to the number of subscribers.
    - This metric helps in understanding how well the human resources are distributed in relation to the demand (subscribers).
    - **Note**: Staff per 1000 Subscribers is calculated as (total staff / subscribers) * 1000.
    """)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        x='RawWaterSource_name', 
        y='training_sessions', 
        marker='o', 
        data=df_merged12, 
        color='green', 
        ax=ax
    )
    ax.set_title('Training Sessions Trend per Raw Water Source')
    ax.set_xlabel('Raw Water Source Name')
    ax.set_ylabel('Training Sessions')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)



    st.subheader("Key Insights")

    st.subheader("Mekong River")
    st.write("""
    - Has a relatively high number of training sessions, indicating a strong focus on training and development for this water source.
    """)

    st.subheader("Tonle Sap Lake")
    st.write("""
    - Also has a significant number of training sessions, suggesting that this source is a priority for training efforts.
    """)

    st.subheader("Other Water Sources")
    st.write("""
    - The number of training sessions varies across different water sources.
    - Some sources have fewer training sessions, which might indicate a need for increased training efforts to ensure consistent knowledge and skills across all sources.
    """)

    # Function for Treatment Plant visualizations
def treatment_plant_visualizations():

    data1 = fetch_data("raw_watersource")
    data3 = fetch_data("treatment_plant")
    # Merge the data
    df_merged13 = pd.merge(data1, data3, on='idRawWaterSource')

    fig, ax = plt.subplots(figsize=(8, 8))
    df_pie = df_merged13.groupby('RawWaterSource_name')['treatment_losses'].sum()
    ax.pie(df_pie, labels=df_pie.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    ax.set_title('Proportion of Treatment Losses by Plant')
    st.pyplot(fig)


    st.subheader("Key Insights")

    st.subheader("Variation in Treatment Losses")
    st.write("""
    - The treatment losses vary across different plants, with some plants experiencing higher losses than others.
    - For example, some plants like “Mission Road” and “Brackenridge” have relatively lower treatment losses, while others like “Salado Creek 1” and “Dos Rios 3” have higher losses.
    """)

    st.subheader("Efficiency Indicators")
    st.write("""
    - Plants with lower treatment losses are more efficient in their water treatment processes.
    - Higher treatment losses might indicate inefficiencies or issues in the treatment process that need to be addressed.
    """)

    # Scatter Plot: Chemical Consumption vs Treatment Losses
    st.subheader("Chemical Consumption vs Treatment Losses")
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    chemicals = ['pac_consumption', 'alum_consumption', 'chlorine_consumption', 'lime_consumption']
    for i, col in enumerate(chemicals):
        sns.scatterplot(x=data3[col], y=data3['treatment_losses'], ax=axs[i//2, i%2])
        axs[i//2, i%2].set_title(f'{col} vs Treatment Losses')
        axs[i//2, i%2].set_xlabel(col)
        axs[i//2, i%2].set_ylabel('Treatment Losses')
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Interpretation")

    st.write("""
    **PAC Consumption vs Treatment Losses**:
    - Shows a positive correlation between PAC (Powdered Activated Carbon) consumption and treatment losses.
    - As PAC consumption increases, treatment losses tend to increase as well.

    **Alum Consumption vs Treatment Losses**:
    - Indicates a similar positive correlation between alum consumption and treatment losses.
    - Higher alum consumption is associated with higher treatment losses.

    **Chlorine Consumption vs Treatment Losses**:
    - Also displays a positive correlation.
    - Increased chlorine consumption corresponds to increased treatment losses.

    **Lime Consumption vs Treatment Losses**:
    - Follows the same trend, with higher lime consumption leading to higher treatment losses.
    """)

    st.subheader("Key Insights")

    st.write("""
    **Positive Correlation**:
    - All four scatter plots show a positive correlation between chemical consumption and treatment losses.
    - This suggests that as more chemicals are used in the treatment process, the percentage of water lost also increases.

    **Efficiency Considerations**:
    - The positive correlation might indicate inefficiencies in the treatment process where higher chemical usage does not necessarily translate to better treatment outcomes but rather increases losses.
    - Identifying the optimal levels of chemical usage that minimize treatment losses could improve overall efficiency.
    """)

    # Scatter Plot: Chemical Consumption vs Production Capacity
    st.subheader("Chemical Consumption vs Production Capacity")
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    for i, col in enumerate(chemicals):
        sns.scatterplot(x=data3[col], y=data3['production_capacity'], ax=axs[i//2, i%2])
        axs[i//2, i%2].set_title(f'{col} vs Production Capacity')
        axs[i//2, i%2].set_xlabel(col)
        axs[i//2, i%2].set_ylabel('Production Capacity')
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Interpretation and Key Insights")

    st.write("""
    PAC Consumption vs Production Capacity: Shows a positive correlation between PAC (Powdered Activated Carbon) consumption and production capacity. As PAC consumption increases, production capacity also tends to increase. Alum Consumption vs Production Capacity: Indicates a similar positive correlation between alum consumption and production capacity. Higher alum consumption is associated with higher production capacity. Chlorine Consumption vs Production Capacity: Also displays a positive correlation. Increased chlorine consumption corresponds to increased production capacity. Lime Consumption vs Production Capacity: Follows the same trend, with higher lime consumption leading to higher production capacity. Key Insights: Positive Correlation: All four scatter plots show a positive correlation between chemical consumption and production capacity. This suggests that as more chemicals are used, the production capacity increases. Efficiency Considerations: The positive correlation might indicate that higher chemical usage is effectively contributing to increased production capacity. Identifying the optimal levels of chemical usage that maximize production capacity could further improve efficiency.
    """)

    # Fuel and Electricity Consumption vs Treatment Losses
    st.subheader("Fuel and Electricity Consumption vs Treatment Losses")
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    sns.scatterplot(x=data3['fuel_consumption'], y=data3['treatment_losses'], ax=axs[0])
    axs[0].set_title('Fuel Consumption vs Treatment Losses')
    axs[0].set_xlabel('Fuel Consumption')
    axs[0].set_ylabel('Treatment Losses')

    sns.scatterplot(x=data3['electricity_consumption'], y=data3['treatment_losses'], ax=axs[1])
    axs[1].set_title('Electricity Consumption vs Treatment Losses')
    axs[1].set_xlabel('Electricity Consumption')
    axs[1].set_ylabel('Treatment Losses')

    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Interpretation and Key Insights")

    st.write("""
    Fuel Consumption vs Treatment Losses: Shows a positive correlation between fuel consumption and treatment losses. As fuel consumption increases, treatment losses also tend to increase. Electricity Consumption vs Treatment Losses: Indicates a similar positive correlation between electricity consumption and treatment losses. Higher electricity consumption is associated with higher treatment losses. Key Insights: Positive Correlation: Both scatter plots show a positive correlation between consumption (fuel or electricity) and treatment losses. This suggests that as more fuel or electricity is used in the treatment process, the percentage of water lost also increases. Efficiency Considerations: The positive correlation might indicate inefficiencies in the treatment process where higher consumption of fuel or electricity does not necessarily translate to better treatment outcomes but rather increases losses. Identifying the optimal levels of fuel and electricity usage that minimize treatment losses could improve overall efficiency.
    """)

    # Fuel and Electricity Consumption vs Production Capacity
    st.subheader("Fuel and Electricity Consumption vs Production Capacity")
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    sns.scatterplot(x=data3['fuel_consumption'], y=data3['production_capacity'], ax=axs[0])
    axs[0].set_title('Fuel Consumption vs Production Capacity')
    axs[0].set_xlabel('Fuel Consumption')
    axs[0].set_ylabel('Production Capacity')

    sns.scatterplot(x=data3['electricity_consumption'], y=data3['production_capacity'], ax=axs[1])
    axs[1].set_title('Electricity Consumption vs Production Capacity')
    axs[1].set_xlabel('Electricity Consumption')
    axs[1].set_ylabel('Production Capacity')

    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Interpretation and Key Insights")

    st.write("""
    Fuel Consumption vs Production Capacity: Shows a positive correlation between fuel consumption and production capacity. As fuel consumption increases, production capacity also tends to increase. Electricity Consumption vs Production Capacity: Indicates a similar positive correlation between electricity consumption and production capacity. Higher electricity consumption is associated with higher production capacity. Key Insights: Positive Correlation: Both scatter plots show a positive correlation between consumption (fuel or electricity) and production capacity. This suggests that as more fuel or electricity is used, the production capacity increases. Efficiency Considerations: The positive correlation might indicate that higher consumption of fuel or electricity is effectively contributing to increased production capacity. Identifying the optimal levels of fuel and electricity usage that maximize production capacity could further improve efficiency.
    """)

    # Correlation between Fuel Consumption and Electricity Consumption
    st.subheader("Correlation: Fuel vs. Electricity Consumption")
    correlation = data3['fuel_consumption'].corr(data3['electricity_consumption'])
    st.write(f"Correlation between Fuel Consumption and Electricity Consumption: {correlation:.2f}")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=data3['fuel_consumption'], y=data3['electricity_consumption'], s=100, ax=ax)
    ax.set_title('Fuel Consumption vs. Electricity Consumption')
    ax.set_xlabel('Fuel Consumption')
    ax.set_ylabel('Electricity Consumption')
    ax.text(275, 5100, f'Correlation: {correlation:.2f}', fontsize=12)
    st.pyplot(fig)
    st.write("""
    Correlation between Fuel Consumption and Electricity Consumption: The graph shows a nearly perfect diagonal line from the bottom left to the top right, indicating a strong positive correlation between fuel consumption and electricity consumption. The correlation coefficient is labeled as 1.00, suggesting a perfect positive correlation. This means that as fuel consumption increases, electricity consumption also increases proportionally. Key Insights: Strong Positive Correlation: The perfect correlation (1.00) indicates that fuel and electricity consumption are closely linked. Any increase in fuel consumption is directly associated with an increase in electricity consumption. Efficiency Considerations: The strong correlation might suggest that both fuel and electricity are being consumed in tandem, possibly due to the operational requirements of the treatment plants. Understanding this relationship can help in optimizing the use of both resources to improve overall efficiency.
    """)

    fig, ax = plt.subplots(figsize=(12, 8))
    df_stacked = df_merged13.set_index('RawWaterSource_name')[chemicals]
    df_stacked.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')
    ax.set_title('Chemical Consumption Across Treatment Plants (Stacked)')
    ax.set_xlabel('Treatment Plant of Water Resources')
    ax.set_ylabel('Consumption (in units)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)


    st.write("""
    PAC Consumption: The blue bars represent PAC consumption across different treatment plants. There is variability in PAC consumption, with some plants using significantly more PAC than others. Lime Consumption: The orange bars indicate lime consumption. Similar to PAC, lime consumption varies across treatment plants, with some plants showing higher usage. Chlorine Consumption: The green bars show chlorine consumption. Chlorine usage also varies, with some plants consuming more chlorine than others. Key Insights: Variability in Chemical Consumption: The graph highlights the differences in chemical consumption across various treatment plants. This variability could be due to differences in water quality, treatment processes, or operational practices at each plant. Efficiency Considerations: Understanding the consumption patterns of these chemicals can help identify opportunities for optimizing chemical usage. Plants with higher chemical consumption might need to review their processes to improve efficiency and reduce costs.
    """)

def water_quality_analysis():

    data1 = fetch_data("raw_watersource")
    data3 = fetch_data("treatment_plant")
    data4 = fetch_data("water_quality")
    df_merged13 = pd.merge(data1, data3, on='idRawWaterSource')
    # Merge data for analysis
    df_merged134 = pd.merge(data4, df_merged13, on='idTreatmentPlant')

    st.title("Water Quality Analysis")

    # Section 2: Treatment Losses vs Water Quality Parameters
    st.subheader("Treatment Losses vs Water Quality Parameters")
    
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='turbidity', y='treatment_losses', data=df_merged134, label='Turbidity', color='r')
    sns.scatterplot(x='ph_level', y='treatment_losses', data=df_merged134, label='pH Level', color='g')
    sns.scatterplot(x='total_dissolved_solids', y='treatment_losses', data=df_merged134, label='Total Dissolved Solids', color='b')
    plt.title('Treatment Losses vs Water Quality Parameters')
    plt.xlabel('Water Quality Parameters')
    plt.ylabel('Treatment Losses (%)')
    plt.legend()
    st.pyplot(plt)

    # Section 3: Average Levels of Key Water Quality Parameters
    st.subheader("Average Levels of Key Water Quality Parameters")
    
    quality_params = ['ph_level', 'arsenic_level', 'total_dissolved_solids', 'lead_level', 'nitrate_level']
    data4_melted = data4.melt(id_vars=['code'], value_vars=quality_params, var_name='Parameter', value_name='Level')

    plt.figure(figsize=(14, 10))
    sns.boxplot(x='Parameter', y='Level', data=data4_melted)
    plt.title('Average Levels of Key Water Quality Parameters')
    plt.xlabel('Water Quality Parameter')
    plt.ylabel('Level')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Section 4: Correlation Heatmap
    st.subheader("Correlation Heatmap of Treatment and Water Quality Data")
    
    plt.figure(figsize=(12, 8))
    numeric_df = data4.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Heatmap of Treatment and Water Quality Data')
    st.pyplot(plt)

def commercial_analysis():

    data1 = fetch_data("raw_watersource")
    data2 = fetch_data("human_resources")
    data3 = fetch_data("treatment_plant")
    data4 = fetch_data("water_quality")
    data5 = fetch_data("commercial")
    data6 = fetch_data("financial")

    df_merged13 = pd.merge(data1, data3, on='idRawWaterSource')

    # Merge data for analysis
    df_merged135 = pd.merge(data5, df_merged13, on='idTreatmentPlant')
    df_merged135.drop(columns=['code_x', 'code_y'], inplace=True)
    # Merge DataFrames if needed (example merging on idTreatmentPlant)
    df_merged1356 = pd.merge(df_merged135, data6, on='idCommercial')

    st.title("Commercial Analysis")

    # Section 1: Population Served by Each Commercial Entity

    fig = px.bar(
        df_merged135, 
        x='RawWaterSource_name', 
        y='population_served', 
        title='Population Served by Each Water Resource',
        labels={'population_served': 'Population Served', 'RawWaterSource_name': 'Water Resources'},
        text='population_served',  # Show population as text
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(xaxis_tickangle=-90)
    st.plotly_chart(fig)


    # Scatter plot with trendline
    st.subheader("Water Production vs. Water Sold by Commercial Entities")
    plt.figure(figsize=(17, 6))

    # Scatter plot to show relationship
    sns.scatterplot(data=df_merged1356, x='Water_Production', y='water_sold', color='blue')

    # Adding a regression line to show the trend
    sns.regplot(data=df_merged1356, x='Water_Production', y='water_sold', scatter=False, color='orange')

    plt.title('Water Production vs. Water Sold by Commercial Entities')
    plt.xlabel('Water Production (m³)')
    plt.ylabel('Water Sold (m³)')
    st.pyplot(plt)

    # Violin plot
    st.subheader("Average Daily Consumption per Capita by Commercial Entities")
    plt.figure(figsize=(17, 6))

    # Create a violin plot to visualize the distribution
    sns.violinplot(data=df_merged1356, x='RawWaterSource_name', y='average_consumption_per_capita', palette='viridis')

    # Adding labels and title
    plt.title('Average Daily Consumption per Capita by Commercial Entities')
    plt.xlabel('Commercial Entities of Water Resources')
    plt.ylabel('Average Consumption per Capita (m³)')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Section 4: Water Losses vs. Non-Revenue Water
    st.subheader("Water Losses vs. Non-Revenue Water")
    plt.figure(figsize=(20,16))
    ax=df_merged1356.set_index('RawWaterSource_name')[['water_losses', 'non_revenue_water']].plot(kind='bar', stacked=True)
    plt.title('Water Losses vs. Non-Revenue Water')
    plt.xlabel('Commercial Entities of Water Resources')
    plt.ylabel('Water Volume')
    plt.xticks(rotation=90)  # Rotate x-axis labels to 90 degrees
    # Adjust x-axis tick labels font size
    ax.tick_params(axis='x', labelsize=8)
    plt.tight_layout()
    st.pyplot(plt)

    # Stacked bar chart
    st.subheader("Financial Overview: Cash from Water Sales and Other Cash")
    plt.figure(figsize=(20, 6))

    # Plotting a stacked bar chart
    df_merged1356.set_index('RawWaterSource_name')[['cash_from_water_sales', 'other_cash']].plot(kind='bar', stacked=True, color=['green', 'purple'])

    plt.title('Financial Overview: Cash from Water Sales and Other Cash')
    plt.xlabel('Commercial Entities of Water Resources')
    plt.ylabel('Cash Amount in ($)')
    plt.xticks(rotation=80,fontsize=5)
    plt.legend(["Cash from Water Sales", "Other Cash"])

    st.pyplot(plt)

    # Section 6: Tariff Comparison
    st.subheader("Tariff Comparison by Commercial Entities")
    plt.figure(figsize=(20, 7))
    df_tariff = df_merged1356[['RawWaterSource_name', 'residential_tariff', 'commercial_tariff', 'government_tariff']].set_index('RawWaterSource_name')
    ax = df_tariff.plot(kind='bar')
    plt.title('Tariff Comparison by Commercial Entities', fontsize=14)
    plt.ylabel('Tariff Amount', fontsize=12)
    plt.xticks(rotation=90)  # Rotate x-axis labels to 90 degrees

    # Adjust x-axis tick labels font size
    ax.tick_params(axis='x', labelsize=8)

    plt.tight_layout()
    st.pyplot(plt)
  


    # Section 8: Service Coverage Area (Stacked Bar Chart)
    st.subheader("Service Coverage Area (License and Network)")

    # Melting the dataframe for easier plotting
    coverage_areas = ['service_coverage_license_area', 'service_coverage_network_area']
    data5_coverage_melted = df_merged1356.melt(id_vars=['RawWaterSource_name'], value_vars=coverage_areas, var_name='CoverageType', value_name='Coverage')

    # Grouping by RawWaterSource_name and CoverageType to avoid duplicates and get the mean coverage
    data_grouped = data5_coverage_melted.groupby(['RawWaterSource_name', 'CoverageType']).agg({'Coverage': 'mean'}).reset_index()

    # Pivoting the grouped data for the stacked bar chart
    data_pivoted = data_grouped.pivot(index='RawWaterSource_name', columns='CoverageType', values='Coverage')

    # Plotting a stacked bar chart
    plt.figure(figsize=(12, 8))
    data_pivoted.plot(kind='bar', stacked=True, color=['skyblue', 'orange'], width=0.8)

    # Title and labels
    plt.title('Service Coverage Area (License and Network)', fontsize=16)
    plt.xlabel('Commercial Entity of Water Resources', fontsize=12)
    plt.ylabel('Coverage Area (in percentage)', fontsize=12)

    # Adjusting the x-axis tick labels font size
    plt.xticks(rotation=90, fontsize=10)  # Rotate labels for better visibility

    # Adjusting the legend font size
    plt.legend(title='Coverage Type', fontsize=10)

    # Ensuring the layout is tight to avoid overlap
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)

    # Section 9: Total Water Production and Water Sold (Stacked Bar Chart)
    st.subheader("Total Water Production and Water Sold")

    # Melting the dataframe to reshape for easier plotting
    water_metrics = ['Water_Production', 'water_sold']
    data5_water_melted = df_merged1356.melt(id_vars=['RawWaterSource_name'], value_vars=water_metrics, var_name='WaterMetric', value_name='Volume')

    # Grouping by RawWaterSource_name and WaterMetric to aggregate values
    data_grouped = data5_water_melted.groupby(['RawWaterSource_name', 'WaterMetric']).agg({'Volume': 'sum'}).reset_index()

    # Pivoting the grouped data for the stacked bar chart
    data_pivoted = data_grouped.pivot(index='RawWaterSource_name', columns='WaterMetric', values='Volume')

    # Plotting a stacked bar chart
    plt.figure(figsize=(12, 8))
    data_pivoted.plot(kind='bar', stacked=True, color=['blue', 'orange'], width=0.8)

    # Title and labels
    plt.title('Total Water Production and Water Sold', fontsize=16)
    plt.xlabel('Commercial Entity of Water Resources', fontsize=12)
    plt.ylabel('Volume (in cubic meters)', fontsize=12)

    # Adjusting the x-axis tick labels font size
    plt.xticks(rotation=90, fontsize=10)  # Rotate labels for better visibility

    # Adjusting the legend font size
    plt.legend(title='Water Metric', fontsize=10)

    # Ensuring the layout is tight to avoid overlap
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)

    # Section 10: Non-Revenue Water (Bar Chart)
    st.subheader("Non-Revenue Water in m³")

    # Grouping by RawWaterSource_name to handle any potential duplicates by summing the non-revenue water values
    data_grouped = df_merged1356.groupby('RawWaterSource_name')['non_revenue_water'].sum().reset_index()

    # Plotting a bar chart for Non-Revenue Water
    plt.figure(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='non_revenue_water', data=data_grouped)

    # Adding title and labels
    plt.title('Non-Revenue Water in m³', fontsize=16)
    plt.xlabel('Commercial Entity of Water Resources', fontsize=12)
    plt.ylabel('Non-Revenue Water (in m³)', fontsize=12)

    # Adjusting the x-axis tick labels font size
    plt.xticks(rotation=90, fontsize=10)  # Rotate labels for better visibility

    # Ensuring the layout is tight to avoid overlap
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)

def plot_financial_data():
    st.header('Financials Analysis')

    data1 = fetch_data("raw_watersource")
    data2 = fetch_data("human_resources")
    data3 = fetch_data("treatment_plant")
    data4 = fetch_data("water_quality")
    data5 = fetch_data("commercial")
    data6 = fetch_data("financial")

    df_merged13 = pd.merge(data1, data3, on='idRawWaterSource')

    # Merge data for analysis
    df_merged135 = pd.merge(data5, df_merged13, on='idTreatmentPlant')
    df_merged135.drop(columns=['code_x', 'code_y'], inplace=True)
    # Merge DataFrames if needed (example merging on idTreatmentPlant)
    df_merged1356 = pd.merge(df_merged135, data6, on='idCommercial')
    df = df_merged1356.copy()

    # Set the aesthetic style of the plots
    sns.set_style("whitegrid")

    # Cash Flow from Water Sales (Stacked Bar Chart)
    st.subheader('Cash Flow from Water Sales for Each Commercial Entity')
    df_cash_flow = df[['RawWaterSource_name', 'cash_from_water_sales']]
    df_cash_flow = df_cash_flow.set_index('RawWaterSource_name')
    df_cash_flow.plot(kind='bar', stacked=True, figsize=(10, 6), color=['green'])
    plt.title('Cash Flow from Water Sales for Each Commercial Water Resource')
    plt.xlabel('Commercial Entity Water Sources')
    plt.ylabel('Cash from Water Sales ($)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Amount Billed for Water Sales and Other Services (Stacked Bar Chart)
    st.subheader('Amount Billed for Water Sales and Other Services')
    df_billing = df[['RawWaterSource_name', 'amount_billed_for_water_sales', 'amount_billed_for_other_services']]
    df_billing = df_billing.set_index('RawWaterSource_name')
    df_billing.plot(kind='bar', stacked=True, figsize=(12, 8), color=['blue', 'orange'])
    plt.title('Amount Billed for Water Sales and Other Services')
    plt.xlabel('Commercial Entity of Water Sources')
    plt.ylabel('Amount ($)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Accounts Receivable and Bill Collection Ratios (Stacked Bar Chart)
    st.subheader('Accounts Receivable and Bill Collection Ratios')
    df_financial = df[['RawWaterSource_name', 'accounts_receivable', 'bill_collection_ratio']]
    df_financial = df_financial.set_index('RawWaterSource_name')
    df_financial.plot(kind='bar', stacked=True, figsize=(12, 8), color=['red', 'purple'])
    plt.title('Accounts Receivable and Bill Collection Ratios')
    plt.xlabel('Commercial Entity of Water Sources')
    plt.ylabel('Value')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Total Operating Expenses and Production Expenses (Stacked Bar Chart)
    st.subheader('Total Operating Expenses and Production Expenses')
    df_expenses = df[['RawWaterSource_name', 'total_operating_expenses', 'production_expenses']]
    df_expenses = df_expenses.set_index('RawWaterSource_name')
    df_expenses.plot(kind='bar', stacked=True, figsize=(12, 8), color=['green', 'brown'])
    plt.title('Total Operating Expenses and Production Expenses')
    plt.xlabel('Commercial Entity of Water Sources')
    plt.ylabel('Amount ($)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Net Income for Each Commercial Entity (Stacked Bar Chart)
    st.subheader('Net Income for Each Commercial Entity')
    df_net_income = df[['RawWaterSource_name', 'net_income']]
    df_net_income = df_net_income.set_index('RawWaterSource_name')
    df_net_income.plot(kind='bar', stacked=True, figsize=(10, 6), color=['teal'])
    plt.title('Net Income for Each Commercial Entity')
    plt.xlabel('Commercial Entity of Water Sources')
    plt.ylabel('Net Income ($)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

def plot_distribution_network_data():

    st.header('Distribution Network Analysis')

    data1 = fetch_data("raw_watersource")
    data2 = fetch_data("human_resources")
    data3 = fetch_data("treatment_plant")
    data4 = fetch_data("water_quality")
    data5 = fetch_data("commercial")
    data6 = fetch_data("financial")
    data7 = fetch_data("distribution_network")

    df_merged13 = pd.merge(data1, data3, on='idRawWaterSource')

    # Merge data for analysis
    df_merged135 = pd.merge(data5, df_merged13, on='idTreatmentPlant')
    df_merged135.drop(columns=['code_x', 'code_y'], inplace=True)
    # Merge DataFrames if needed (example merging on idTreatmentPlant)
    df_merged1356 = pd.merge(df_merged135, data6, on='idCommercial')
    # Merge DataFrames if needed (example merging on idTreatmentPlant)
    df = pd.merge(df_merged1356, data7, on='idCommercial')

    # Set the aesthetic style of the plots
    sns.set_style("whitegrid")

    # Supply Pressure at End Connection for Each Network
    st.subheader('Supply Pressure at End Connection for Each Network')
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='RawWaterSource_name', y='Supply_Pressure_end_connection', data=df, marker='o')
    plt.title('Supply Pressure at End Connection for Each Network')
    plt.xlabel('Distribution Network Code')
    plt.ylabel('Supply Pressure (in units)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Number of Leaks Repaired in Each Network (Heatmap)
    st.subheader('Number of Leaks Repaired in Each Network')

    # Pivot the data for heatmap compatibility (RawWaterSource_name on rows, values on columns)
    heatmap_data = df.pivot_table(index='RawWaterSource_name', values='Number_leak_repaired')

    # Create the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="g", cmap="YlGnBu", cbar_kws={'label': 'Number of Leaks Repaired'})
    plt.title('Number of Leaks Repaired in Each Network')
    plt.xlabel('Distribution Network')
    plt.ylabel('Commercial Water Sources')
    plt.tight_layout()
    st.pyplot(plt)


    # Total Length of the Distribution Network (Horizontal Bar Chart)
    # Total Length of the Distribution Network (Violin Plot)
    st.subheader('Total Length of the Distribution Network')

    plt.figure(figsize=(12, 6))
    sns.violinplot(x='RawWaterSource_name', y='total_length', data=df, color='purple')
    plt.title('Total Length of the Distribution Network')
    plt.xlabel('Distribution Network Code')
    plt.ylabel('Total Length (in kilometers)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Storage Capacity and Supply Duration (Stacked Bar Chart)
    st.subheader('Storage Capacity (m3) and Supply Duration (H)')
    storage_metrics = ['Storagecapacity', 'Supply_duration']
    data_storage_melted = df.melt(id_vars=['RawWaterSource_name'], value_vars=storage_metrics, var_name='StorageMetric', value_name='Value')

    # Multiply Supply_duration by 24 to convert into hours (if needed)
    data_storage_melted['Value'] = data_storage_melted.apply(lambda row: row['Value'] * 24 if row['StorageMetric'] == 'Supply_duration' else row['Value'], axis=1)

    # Pivot data to get the values in the correct format for a stacked bar chart
    df_pivot = data_storage_melted.pivot_table(index='RawWaterSource_name', columns='StorageMetric', values='Value', aggfunc='sum')
    
    # Plot the stacked bar chart
    plt.figure(figsize=(12, 8))
    df_pivot.plot(kind='bar', stacked=True)
    plt.title('Storage Capacity (m3) and Supply Duration (Hours) by Network')
    plt.xlabel('Distribution Network Code')
    plt.ylabel('Value')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)
# Introduction
def introduction():
    st.title("Water Supplier Monitoring System (WSMS)")

    st.header("Description")
    st.write("""
    The WSMS project encompasses several key components:

    - **Raw Water Sources**: This table includes information about the primary water sources, such as the Mekong River and Tonle Sap Lake, detailing their availability and total abstraction rates.
    - **Treatment Plants**: This table provides data on the treatment processes, including losses, chemical consumption, electricity usage, and production capacities, linked to specific raw water sources.
    - **Human Resources**: This table tracks the staffing levels, training sessions, and organizational structures associated with each water source, ensuring adequate human resource management.
    - **Water Quality**: This table monitors various water quality parameters, such as color, turbidity, pH levels, and the presence of contaminants, to ensure the safety and compliance of the water supply.
    - **Commercial Operations**: This table details the commercial aspects of the water supply, including population served, service coverage, water production and sales, and customer complaints, providing insights into the operational efficiency and customer satisfaction.
    - **Financial Performance**: This table captures the financial metrics, such as cash flow from water sales, billing, expenses, and profitability, to assess the economic viability of the water supply operations.
    - **Distribution Network**: This table includes data on the distribution infrastructure, such as supply pressure, leak repairs, and storage capacity, to ensure the reliability and efficiency of the water distribution system.
    """)

# Description of the 7 tables
def describe_tables():
    st.header("Description of the 7 Tables")

    st.subheader("1. Raw Water Source Table ")
    st.write("""
    - **Columns:**
      - `idRawWaterSource`: Unique identifier for each raw water source.
      - `code`: Code representing the raw water source.
      - `RawWaterSource_name`: Name of the raw water source.
      - `availability_year_round`: Indicates if the water source is available year-round (1 for yes, 0 for no).
      - `total_abstraction`: Total amount of water abstracted from the source (in cubic meters).
      - `Drawing_RawWater_PumpingStation`: Drawing of the raw water pumping station (BLOB).
      - `Drawing_Water_Transmission_Network`: Drawing of the water transmission network (BLOB).
      - `Drawing_Water_Treatment_Plant`: Drawing of the water treatment plant (BLOB).
    """)

    st.subheader("2. Human Resources Table ")
    st.write("""
    - **Columns:**
      - `idHumanresources`: Unique identifier for each human resource record.
      - `code`: Code representing the human resource record.
      - `total_staff`: Total number of staff.
      - `staff_per_1000_subscribers`: Number of staff per 1000 subscribers.
      - `training_sessions`: Number of training sessions conducted.
      - `organization_chart`: Organization chart (BLOB).
      - `idRawWaterSource`: Foreign key linking to the raw water source table.
    """)

    st.subheader("3. Treatment Plant Table ")
    st.write("""
    - **Columns:**
      - `idTreatmentPlant`: Unique identifier for each treatment plant.
      - `code`: Code representing the treatment plant.
      - `treatment_losses`: Amount of water lost during treatment (in cubic meters).
      - `pac_consumption`: Consumption of powdered activated carbon (PAC) (in units).
      - `pac_per_m3_produced`: PAC consumption per cubic meter of water produced.
      - `alum_consumption`: Consumption of alum (in units).
      - `alum_per_m3_produced`: Alum consumption per cubic meter of water produced.
      - `chlorine_consumption`: Consumption of chlorine (in units).
      - `chlorine_per_m3_produced`: Chlorine consumption per cubic meter of water produced.
      - `electricity_consumption`: Electricity consumption (in kWh).
      - `electricity_per_m3_produced`: Electricity consumption per cubic meter of water produced.
      - `lime_consumption`: Consumption of lime (in units).
      - `lime_per_m3_produced`: Lime consumption per cubic meter of water produced.
      - `fuel_consumption`: Fuel consumption (in liters).
      - `fuel_per_m3_produced`: Fuel consumption per cubic meter of water produced.
      - `production_capacity`: Production capacity of the treatment plant (in cubic meters).
      - `idRawWaterSource`: Foreign key linking to the raw water source table.
    """)

    st.subheader("4. Water Quality Table ")
    st.write("""
    - **Columns:**
      - `idWaterQuality`: Unique identifier for each water quality record.
      - `code`: Code representing the water quality record.
      - `color`: Color of the water (in units).
      - `turbidity`: Turbidity of the water (in NTU).
      - `ph_level`: pH level of the water.
      - `arsenic_level`: Arsenic level in the water (in mg/L).
      - `total_dissolved_solids`: Total dissolved solids in the water (in mg/L).
      - `manganese_level`: Manganese level in the water (in mg/L).
      - `zinc_level`: Zinc level in the water (in mg/L).
      - `sulfate_level`: Sulfate level in the water (in mg/L).
      - `copper_level`: Copper level in the water (in mg/L).
      - `hydrogen_sulfide`: Hydrogen sulfide level in the water (in mg/L).
      - `hardness`: Hardness of the water (in mg/L).
      - `aluminum_level`: Aluminum level in the water (in mg/L).
      - `chloride_level`: Chloride level in the water (in mg/L).
      - `iron_level`: Iron level in the water (in mg/L).
      - `ammonia_level`: Ammonia level in the water (in mg/L).
      - `barium_level`: Barium level in the water (in mg/L).
      - `cadmium_level`: Cadmium level in the water (in mg/L).
      - `chromium_level`: Chromium level in the water (in mg/L).
      - `fluoride_level`: Fluoride level in the water (in mg/L).
      - `lead_level`: Lead level in the water (in mg/L).
      - `mercury_level`: Mercury level in the water (in mg/L).
      - `nitrate_level`: Nitrate level in the water (in mg/L).
      - `nitrite_level`: Nitrite level in the water (in mg/L).
      - `sodium_level`: Sodium level in the water (in mg/L).
      - `residual_chlorine`: Residual chlorine level in the water (in mg/L).
      - `idTreatmentPlant`: Foreign key linking to the treatment plant table.
    """)

    st.subheader("5. Commercial Table ")
    st.write("""
    - **Columns:**
      - `idCommercial`: Unique identifier for each commercial record.
      - `code`: Code representing the commercial record.
      - `population_served`: Population served by the commercial entity.
      - `service_coverage_license_area`: Service coverage area under license (in percentage).
      - `service_coverage_network_area`: Service coverage area under network (in percentage).
      - `Water_Production`: Total water production (in cubic meters).
      - `water_sold`: Total water sold (in cubic meters).
      - `water_supplied_without_charge`: Water supplied without charge (in cubic meters).
      - `total_water_consumption`: Total water consumption (in cubic meters).
      - `water_losses`: Total water losses (in cubic meters).
      - `non_revenue_water`: Non-revenue water (in percentage).
      - `average_daily_consumption`: Average daily water consumption (in cubic meters).
      - `average_consumption_per_connection`: Average water consumption per connection (in cubic meters).
      - `average_consumption_per_capita`: Average water consumption per capita (in cubic meters).
      - `total_water_connections`: Total number of water connections.
      - `residential_connections`: Number of residential connections.
      - `commercial_connections`: Number of commercial connections.
      - `public_entity_connections`: Number of public entity connections.
      - `factory_connections`: Number of factory connections.
      - `sme_connections`: Number of SME connections.
      - `poor_connections`: Number of connections for poor households.
      - `poor_household_ratio`: Ratio of poor households (in percentage).
      - `customer_complaints`: Number of customer complaints.
      - `complaints_per_1000_connections`: Number of complaints per 1000 connections.
      - `license_area_profile`: Profile of the license area.
      - `network_area_population`: Population in the network area.
      - `network_area_houses`: Number of houses in the network area.
      - `licensed_area_population`: Population in the licensed area.
      - `licensed_area_houses`: Number of houses in the licensed area.
      - `CommercialRegistrationID`: Commercial registration ID.
      - `RegistrationNumber`: Registration number.
      - `RegistrationIssuedDate`: Date when the registration was issued.
      - `RegistrationExpiryDate`: Date when the registration expires.
      - `ProductID`: Product ID.
      - `commercialregistrationcertificate`: Commercial registration certificate (BLOB).
      - `commercial_tariff`: Commercial tariff (in currency units).
      - `CommercialName`: Name of the commercial entity.
      - `idTreatmentPlant`: Foreign key linking to the treatment plant table.
    """)

    st.subheader("6. Financial Table")
    st.write("""
    - **Columns:**
      - `idFinancial`: Unique identifier for each financial record.
      - `code`: Code representing the financial record.
      - `cash_from_water_sales`: Cash flow from water sales (in currency units).
      - `other_cash`: Cash flow from other sources (in currency units).
      - `amount_billed_for_water_sales`: Amount billed for water sales (in currency units).
      - `amount_billed_for_other_services`: Amount billed for other services (in currency units).
      - `accounts_receivable`: Accounts receivable (in currency units).
      - `average_tariff`: Average tariff (in currency units).
      - `bill_collection_ratio`: Bill collection ratio (in percentage).
      - `total_operating_expenses`: Total operating expenses (in currency units).
      - `operating_ratio`: Operating ratio.
      - `production_expenses`: Production expenses (in currency units).
      - `unit_production_cost`: Unit production cost (in currency units).
      - `net_income`: Net income (in currency units).
      - `net_profit_margin`: Net profit margin (in percentage).
      - `investment_expenditures`: Investment expenditures (in currency units).
      - `loans`: Loans (in currency units).
      - `accounts_payable`: Accounts payable (in currency units).
    """)

    st.subheader("7. Distribution Network Table ")
    st.write("""
      - **Columns:**
        - `idDistributionNetwork`: Unique identifier for each distribution network record.
        - `code`: Code representing the distribution network.
        - `total_length`: Total length of the distribution network (in kilometers).
        - `number_of_pipelines`: Total number of pipelines in the network.
        - `pipeline_diameter`: Diameter of the pipelines (in millimeters).
        - `pipeline_material`: Material of the pipelines (e.g., PVC, steel).
        - `number_of_pumping_stations`: Total number of pumping stations in the network.
        - `number_of_reservoirs`: Total number of reservoirs in the network.
        - `total_storage_capacity`: Total storage capacity of the reservoirs (in cubic meters).
        - `average_age_of_pipelines`: Average age of the pipelines (in years).
        - `leakage_rate`: Leakage rate in the distribution network (in percentage).
        - `maintenance_costs`: Annual maintenance costs for the distribution network (in currency units).
        - `idTreatmentPlant`: Foreign key linking to the treatment plant table.
      """)