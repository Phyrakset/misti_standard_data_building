import streamlit as st
from config import get_connection
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# Fetch data from a specified table
def fetch_data(table_name):
    conn = get_connection()
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

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
    
    st.write("Not Available Year Round Water Sources:")
    not_available_year_round['total_abstraction_m3'] = not_available_year_round['total_abstraction'].apply(lambda x: f"{x} m³")
    st.write(not_available_year_round[['RawWaterSource_name', 'total_abstraction_m3']])

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

# Visualization function for grouped abstraction by availability
def visualize_grouped_abstraction():
    st.subheader("Total Abstraction by Availability Year Round")
    
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

# Visualization function for total abstraction capacity
def visualize_total_abstraction_capacity():
    st.subheader("Total Abstraction Capacity for Each Raw Water Source")
    
    # Fetch data
    data1 = fetch_data("raw_watersource")
    
    # Plot bar chart
    plt.figure(figsize=(12, 6))
    sns.barplot(x='RawWaterSource_name', y='total_abstraction', data=data1)
    plt.title('Total Abstraction Capacity for Each Raw Water Source')
    plt.xlabel('Raw Water Source')
    plt.ylabel('Total Abstraction (in cubic meters)')
    plt.xticks(rotation=90)
    st.pyplot(plt)

# Fetch data function for human resources analysis
def fetch_data_for_human_resources():
    data1 = fetch_data("raw_watersource")  # Fetch raw water source data
    data2 = fetch_data("human_resources")  # Fetch human resources data
    return pd.merge(data1, data2, on='idRawWaterSource')

# Streamlit app for human resources analysis
def human_resources_analysis():
    # Fetch and merge data
    df_merged12 = fetch_data_for_human_resources()
    
    # Human Resources - Total Staff per Raw Water Source
    st.subheader("Total Staff for Each Raw Water Source")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='total_staff', data=df_merged12, ax=ax)
    ax.set_title('Total Number of Staff for Each Raw Water Source')
    ax.set_xlabel('Raw Water Source Name')
    ax.set_ylabel('Total Staff')
    plt.xticks(rotation=90)  # Rotate x-axis labels to 90 degrees
    plt.tight_layout()  # Adjust layout to prevent labels from being cut off
    st.pyplot(fig)

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

    # Dual Axis Plot: Total Staff and Staff per 1000 Subscribers
    st.subheader("Total Staff and Staff per 1000 Subscribers for Each Raw Water Source")
    fig, ax1 = plt.subplots(figsize=(18, 7))
    
    # Bar plot for total staff
    ax1.bar(df_merged12['RawWaterSource_name'], df_merged12['total_staff'], color='skyblue', label='Total Staff')
    ax1.set_xlabel('Raw Water Sources')
    ax1.set_ylabel('Total Staff', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')
    ax1.set_xticklabels(df_merged12['RawWaterSource_name'], rotation=45, ha='right')

    # Create a second y-axis to plot staff per 1000 subscribers
    ax2 = ax1.twinx()
    ax2.plot(df_merged12['RawWaterSource_name'], df_merged12['staff_per_1000_subscribers'], color='orange', marker='o', label='Staff per 1000 Subscribers')
    ax2.set_ylabel('Staff per 1000 Subscribers', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    plt.title('Total Staff and Efficiency (Staff per 1000 Subscribers) per Raw Water Source')
    fig.tight_layout()
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    st.pyplot(fig)

    # Human Resources - Staff per 1000 Subscribers
    st.subheader("Staff per 1000 Subscribers")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='staff_per_1000_subscribers', data=df_merged12, ax=ax)
    ax.set_title('Staff per 1000 Subscribers Ratio')
    ax.set_xlabel('Raw Water Source Name')
    ax.set_ylabel('Staff per 1000 Subscribers')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)

    # Human Resources - Training Sessions per Raw Water Source
    st.subheader("Training Sessions Conducted for Each Raw Water Source")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='training_sessions', data=df_merged12, ax=ax)
    ax.set_title('Training Sessions per Raw Water Source')
    ax.set_xlabel('Raw Water Source Name')
    ax.set_ylabel('Training Sessions')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)

    # Function for Treatment Plant visualizations
def treatment_plant_visualizations():

    data1 = fetch_data("raw_watersource")
    data3 = fetch_data("treatment_plant")
    # Merge the data
    df_merged13 = pd.merge(data1, data3, on='idRawWaterSource')

    # Plot: Treatment Losses for Each Plant
    st.subheader("Treatment Losses for Each Plant")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='treatment_losses', data=df_merged13, ax=ax)
    ax.set_title('Treatment Losses for Each Plant')
    ax.set_xlabel('Treatment Plant of Water Resources')
    ax.set_ylabel('Treatment Losses (%)')
    plt.xticks(rotation=90)
    st.pyplot(fig)

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

    # Barplot: Chemical Consumption Across Treatment Plants
    st.subheader("Chemical Consumption Across Treatment Plants")
    data3_melted = df_merged13.melt(id_vars=['RawWaterSource_name'], value_vars=chemicals, var_name='Chemical', value_name='Consumption')
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='RawWaterSource_name', y='Consumption', hue='Chemical', data=data3_melted, ax=ax)
    ax.set_title('Chemical Consumption Across Treatment Plants')
    ax.set_xlabel('Treatment Plant fo Water Resources')
    ax.set_ylabel('Consumption (in units)')
    plt.xticks(rotation=90)
    st.pyplot(fig)

def water_quality_analysis():

    data1 = fetch_data("raw_watersource")
    data3 = fetch_data("treatment_plant")
    data4 = fetch_data("water_quality")
    df_merged13 = pd.merge(data1, data3, on='idRawWaterSource')
    # Merge data for analysis
    df_merged134 = pd.merge(data4, df_merged13, on='idTreatmentPlant')

    st.title("Water Quality Analysis")

    # Section 1: pH Level vs. Turbidity and Color
    st.subheader("pH Level vs. Turbidity and Color")
    
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    sns.scatterplot(x='ph_level', y='turbidity', data=df_merged134, ax=ax[0], hue='RawWaterSource_name', palette='Set1')
    ax[0].set_title("pH Level vs. Turbidity")
    ax[0].set_xlabel("pH Level")
    ax[0].set_ylabel("Turbidity")

    sns.scatterplot(x='ph_level', y='color', data=df_merged134, ax=ax[1], hue='RawWaterSource_name', palette='Set1')
    ax[1].set_title("pH Level vs. Color")
    ax[1].set_xlabel("pH Level")
    ax[1].set_ylabel("Color (in units)")

    plt.tight_layout()
    st.pyplot(fig)

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
    st.subheader("Population Served by Each Commercial Entity")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='population_served', data=df_merged135)
    plt.title('Population Served by Each Commercial Entity')
    plt.xlabel('Commercial Entity of Water Resources')
    plt.ylabel('Population Served')
    plt.xticks(rotation=90)  # Rotate x-axis labels to 90 degrees
    plt.tight_layout()
    st.pyplot(plt)

    # Section 2: Water Production vs. Water Sold
    st.subheader("Water Production vs. Water Sold by Commercial Entities")
    plt.figure(figsize=(17, 6))
    sns.barplot(data=df_merged1356, x='RawWaterSource_name', y='Water_Production', color='blue', label='Water Production')
    sns.barplot(data=df_merged1356, x='RawWaterSource_name', y='water_sold', color='orange', label='Water Sold')
    plt.title('Water Production vs. Water Sold by Commercial Entities')
    plt.xlabel('Commercial Entities of Water Ressources')
    plt.ylabel('Water Volume (m³)')
    plt.legend()
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Section 3: Average Daily Consumption per Capita
    st.subheader("Average Daily Consumption per Capita by Commercial Entities")
    plt.figure(figsize=(17, 6))
    sns.barplot(data=df_merged1356, x='RawWaterSource_name', y='average_consumption_per_capita', palette='viridis')
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

    # Section 5: Financial Overview
    st.subheader("Financial Overview: Cash from Water Sales and Other Cash")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_merged1356, x='RawWaterSource_name', y='cash_from_water_sales', color='green', label='Cash from Water Sales')
    sns.barplot(data=df_merged1356, x='RawWaterSource_name', y='other_cash', color='purple', label='Other Cash')
    plt.title('Financial Overview: Cash from Water Sales and Other Cash')
    plt.xlabel('Commercial Entities of Water Resources')
    plt.ylabel('Cash Amount')
    plt.legend()
    plt.xticks(rotation=45)
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

    # Section 7: Debt to Equity Ratio vs. Return on Equity
    st.subheader("Debt to Equity Ratio vs. Return on Equity")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_merged1356, x='debt_to_equity_ratio', y='return_on_equity', hue='RawWaterSource_name')
    plt.title('Debt to Equity Ratio vs. Return on Equity')
    plt.xlabel('Debt to Equity Ratio')
    plt.ylabel('Return on Equity')
    st.pyplot(plt)

    # Section 8: Service Coverage Area
    st.subheader("Service Coverage Area (License and Network)")
    coverage_areas = ['service_coverage_license_area', 'service_coverage_network_area']
    data5_coverage_melted = df_merged1356.melt(id_vars=['RawWaterSource_name'], value_vars=coverage_areas, var_name='CoverageType', value_name='Coverage')
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='RawWaterSource_name', y='Coverage', hue='CoverageType', data=data5_coverage_melted)
    plt.title('Service Coverage Area (License and Network)')
    plt.xlabel('Commercial Entity of Water Resources')
    plt.ylabel('Coverage Area (in percentage)')
    plt.legend(title='Coverage Type')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Section 9: Total Water Production and Water Sold
    st.subheader("Total Water Production and Water Sold")
    water_metrics = ['Water_Production', 'water_sold']
    data5_water_melted = df_merged1356.melt(id_vars=['RawWaterSource_name'], value_vars=water_metrics, var_name='WaterMetric', value_name='Volume')

    plt.figure(figsize=(12, 8))
    sns.barplot(x='RawWaterSource_name', y='Volume', hue='WaterMetric', data=data5_water_melted)
    plt.title('Total Water Production and Water Sold')
    plt.xlabel('Commercial Entity of Water Resouces')
    plt.ylabel('Volume (in cubic meters)')
    plt.legend(title='Water Metric')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Section 10: Non-Revenue Water
    st.subheader("Non-Revenue Water in m³")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='non_revenue_water', data=df_merged1356)
    plt.title('Non-Revenue Water in m³')
    plt.xlabel('Commercial Entity of Water Resources')
    plt.ylabel('Non-Revenue Water (in m³)')
    plt.xticks(rotation=90)
    plt.tight_layout()
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

    # Cash Flow from Water Sales
    st.subheader('Cash Flow from Water Sales for Each Commercial Entity')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='cash_from_water_sales', data=df)
    plt.title('Cash Flow from Water Sales for Each Commercial Entity')
    plt.xlabel('Commercial Entity Water Sources')
    plt.ylabel('Cash from Water Sales ($)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Amount Billed for Water Sales and Other Services
    st.subheader('Amount Billed for Water Sales and Other Services')
    billing_metrics = ['amount_billed_for_water_sales', 'amount_billed_for_other_services']
    data_billing_melted = df.melt(id_vars=['RawWaterSource_name'], value_vars=billing_metrics, var_name='BillingMetric', value_name='Amount')
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='RawWaterSource_name', y='Amount', hue='BillingMetric', data=data_billing_melted)
    plt.title('Amount Billed for Water Sales and Other Services')
    plt.xlabel('Commercial Entity of Water Sources')
    plt.ylabel('Amount ($)')
    plt.legend(title='Billing Metric')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Accounts Receivable and Bill Collection Ratios
    st.subheader('Accounts Receivable and Bill Collection Ratios')
    financial_metrics = ['accounts_receivable', 'bill_collection_ratio']
    data_financial_melted = df.melt(id_vars=['RawWaterSource_name'], value_vars=financial_metrics, var_name='FinancialMetric', value_name='Value')
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='RawWaterSource_name', y='Value', hue='FinancialMetric', data=data_financial_melted)
    plt.title('Accounts Receivable and Bill Collection Ratios')
    plt.xlabel('Commercial Entity of Water Sources')
    plt.ylabel('Value')
    plt.legend(title='Financial Metric')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Total Operating Expenses and Production Expenses
    st.subheader('Total Operating Expenses and Production Expenses')
    expense_metrics = ['total_operating_expenses', 'production_expenses']
    data_expense_melted = df.melt(id_vars=['RawWaterSource_name'], value_vars=expense_metrics, var_name='ExpenseMetric', value_name='Amount')
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='RawWaterSource_name', y='Amount', hue='ExpenseMetric', data=data_expense_melted)
    plt.title('Total Operating Expenses and Production Expenses')
    plt.xlabel('Commercial Entity of Water Sources')
    plt.ylabel('Amount ($)')
    plt.legend(title='Expense Metric')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Net Income for Each Commercial Entity
    st.subheader('Net Income for Each Commercial Entity')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='net_income', data=df)
    plt.title('Net Income for Each Commercial Entity')
    plt.xlabel('Commercial Entity of Water Sources')
    plt.ylabel('Net Income ($)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Net Profit Margin
    st.subheader('Net Profit Margin for Each Commercial Entity')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='net_profit_margin', data=df)
    plt.title('Net Profit Margin for Each Commercial Entity')
    plt.xlabel('Commercial Entity of Water Resources')
    plt.ylabel('Net Profit Margin (in percentage)')
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

    # Number of Leaks Repaired in Each Network
    st.subheader('Number of Leaks Repaired in Each Network')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='Number_leak_repaired', data=df)
    plt.title('Number of Leaks Repaired in Each Network in Quarter')
    plt.xlabel('Distribution Network Code')
    plt.ylabel('Number of Leaks Repaired')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Total Length of the Distribution Network
    st.subheader('Total Length of the Distribution Network')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='RawWaterSource_name', y='total_length', data=df)
    plt.title('Total Length of the Distribution Network')
    plt.xlabel('Distribution Network Code')
    plt.ylabel('Total Length (in kilometers)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    # Storage Capacity and Supply Duration
    st.subheader('Storage Capacity (m3) and Supply Duration (H)')
    storage_metrics = ['Storagecapacity', 'Supply_duration']
    data_storage_melted = df.melt(id_vars=['RawWaterSource_name'], value_vars=storage_metrics, var_name='StorageMetric', value_name='Value')

    # Multiply Supply_duration by 24
    data_storage_melted['Value'] = data_storage_melted.apply(lambda row: row['Value'] * 24 if row['StorageMetric'] == 'Supply_duration' else row['Value'], axis=1)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='RawWaterSource_name', y='Value', hue='StorageMetric', data=data_storage_melted)
    plt.title('Storage Capacity (m3) and Supply Duration (H)')
    plt.xlabel('Distribution Network Code')
    plt.ylabel('Value')
    plt.legend(title='Storage Metric')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)
