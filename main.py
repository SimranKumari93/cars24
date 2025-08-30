import pandas as pd

# Load and clean the data
file_path = '/Data Analyst Data/Cars24/Lead2Disbursal_data.csv'
data = pd.read_csv(file_path)
data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], errors='coerce')
data = data.dropna(subset=['TIMESTAMP'])  # Remove rows with invalid timestamps
data['Month'] = data['TIMESTAMP'].dt.to_period('M')  # Extract month

# Step 1: Funnel Analysis
# Group data by Month and STEP to calculate user counts
funnel_counts = data.groupby(['Month', 'STEP'])['USERID'].nunique().unstack(fill_value=0)
funnel_counts = funnel_counts.rename(columns={
    'LOGIN': 'Login',
    'CREDIT_APPROVED': 'Credit Approved',
    'AGREEMENT_CREATED': 'Agreement Created',
    'DISBURSED': 'Disbursed'
})

# Calculate conversion rates
funnel_counts['Login to Credit Approved'] = (
    funnel_counts['Credit Approved'] / funnel_counts['Login']
)
funnel_counts['Credit Approved to Agreement Created'] = (
    funnel_counts['Agreement Created'] / funnel_counts['Credit Approved']
)
funnel_counts['Agreement Created to Disbursed'] = (
    funnel_counts['Disbursed'] / funnel_counts['Agreement Created']
)

# Extract July's data and previous months' averages
july_data = funnel_counts.loc['2024-07']
previous_months_data = funnel_counts.loc[:'2024-06']
average_previous_months = previous_months_data.mean()

# Step 2: RCA on Key Factors
factor_analysis = data.groupby(['Month', 'RISK_BUCKET', 'CIBIL_BUCKET']).agg({
    'RATE_OF_INTEREST': 'mean',
    'CAR_SELLING_PRICE': 'mean',
    'DISBURSABLE_LOAN_AMOUNT': 'mean',
    'USERID': 'nunique'
}).reset_index()

# Separate July's factors for comparison
july_factors = factor_analysis[factor_analysis['Month'] == '2024-07']
previous_factors = factor_analysis[factor_analysis['Month'] < '2024-07']

# Display the results
print("Funnel Metrics (Month on Month):")
print(funnel_counts)
print("\nJuly Metrics:")
print(july_data)
print("\nAverage Metrics (April-June):")
print(average_previous_months)
print("\nJuly Factors:")
print(july_factors)
print("\nPrevious Months Factors:")
print(previous_factors)


# Save Funnel Data for Power BI
funnel_counts.to_csv('/Data Analyst Data/Cars24/funnel_metrics.csv')

# Save RCA Data for Power BI
factor_analysis.to_csv('/Data Analyst Data/Cars24/factor_analysis.csv')
