# %%
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans

# %%
# 1. Get(wd) and Load Dataset
os.chdir(r"C:/EmreAksu/german-credit-analysis")
df = pd.read_csv(r"data/german_credit_data.csv", index_col=0)

# %%
# 2. Data Cleaning
print("Missing values before cleaning:")
print(df.isnull().sum())

# Fill missing values
df['Saving accounts'] = df['Saving accounts'].fillna('unknown')
df['Checking account'] = df['Checking account'].fillna('unknown')

# Encode categorical variables
le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    df[col] = le.fit_transform(df[col])

df.info()


# %%
# 3. Descriptive Statistics

df.describe().T #Basic stats

# Histogram for age
sns.histplot(df['Age'], bins=20, kde=True)
plt.title("Age Distribution")
plt.savefig("images/age_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# Distribution of credit amount
sns.histplot(df['Credit amount'], bins=30, kde=True)
plt.title("Credit Amount Distribution")
plt.savefig("images/credit_amount_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# Set categorical columns for visualization
for col in ['Housing', 'Sex', 'Saving accounts', 'Checking account', 'Purpose']:
    df[col] = df[col].astype('category')

# A. Scatter: Age vs Credit amount
sns.scatterplot(x='Age', y='Credit amount', data=df)
plt.title("Age vs Credit Amount")
plt.savefig("images/age_credit_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# B. Mean credit amount by Housing (use a FUNCTION for estimator)
sns.barplot(x='Housing', y='Credit amount', data=df, estimator=np.mean)  # or estimator=np.median
plt.title("Average Credit Amount by Housing Type")
plt.savefig("images/average_credit_amount_by_housing.png", dpi=300, bbox_inches="tight")
plt.show()



# %%
# 4. Credit Amount By Purpose

# Load raw data just to get the original text labels for Purpose
df_raw = pd.read_csv(r"C:\EmreAksu\DataProjects\german_credit_data.csv", index_col=0)
df['Purpose'] = df_raw['Purpose'] # Put the original Purpose labels back into your cleaned df

# Average credit amount by purpose, sorted
purpose_means = (
    df.groupby('Purpose')['Credit amount']
      .mean()
      .sort_values(ascending=False)
)

plt.figure(figsize=(7, 5))
colors = ["#084C8D", "#0D62A5", "#1976C2", "#3791D8", "#5AA9E6", "#7FC8F8", "#A4DCFF", "#C7EBFF"]
purpose_means.plot(kind="barh", color=colors) 


plt.xlabel("Average credit amount")
plt.ylabel("Loan purpose")
plt.title("Average Credit Amount by Loan Purpose")
plt.tight_layout()
plt.savefig("images/average_credit_amount_by_loan_purpose.png", dpi=300, bbox_inches="tight")
plt.show()


# %%
# 5. Savings & Checking Accounts vs. Credit Amount
df_raw = pd.read_csv(r"C:\EmreAksu\DataProjects\german_credit_data.csv", index_col=0)

df['Saving accounts'] = df_raw['Saving accounts'].fillna('unknown')
df['Checking account'] = df_raw['Checking account'].fillna('unknown')
df['Purpose'] = df_raw['Purpose'].fillna('unknown')

savings_order = ["unknown", "little", "moderate", "quite rich", "rich"]
plt.figure(figsize=(8,5))
sns.boxplot(
    data=df,
    x='Saving accounts',
    y='Credit amount',
    order=savings_order,
    palette="Blues"
)
plt.title("Credit Amount by Savings Account Level")
plt.ylabel("Credit Amount")
plt.xlabel("Savings Account Level")
plt.tight_layout()
plt.savefig("images/credit_amount_by_savings_account_level.png", dpi=300, bbox_inches="tight")
plt.show()


checking_order = ["unknown", "little", "moderate", "rich"]
plt.figure(figsize=(8,5))
sns.boxplot(
    data=df,
    x='Checking account',
    y='Credit amount',
    order=checking_order,
    palette="Blues"
)
plt.title("Credit Amount by Checking Account Level")
plt.ylabel("Credit Amount")
plt.xlabel("Checking Account Level")
plt.tight_layout()
plt.savefig("images/credit_amount_by_checking_account_level.png", dpi=300, bbox_inches="tight")
plt.show()



# %%
# 6. Correlation Heatmap
plt.figure(figsize=(9,6))
sns.heatmap(df.corr(), annot=True, cmap="Blues", fmt=".2f")
plt.title("Correlation Heatmap of Financial Features")
plt.tight_layout()
plt.savefig("images/correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()


# %%
# 7. K-Means Clustering
X = df[['Age', 'Credit amount', 'Duration']] # Select important numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Plot clusters
plt.figure(figsize=(7,5))
sns.scatterplot(
    data=df,
    x="Age", 
    y="Credit amount", 
    hue="Cluster", 
    palette='viridis'
)
plt.title("Customer Clusters Based on Age and Credit Amount")
plt.savefig("images/customer_clusters_based_on_age_and_credit.png", dpi=300, bbox_inches="tight")
plt.show()


# %%
# 8. Loan Duration Distribution
plt.figure(figsize=(7,5))
sns.histplot(df['Duration'], bins=15, kde=True)
plt.title("Distribution of Loan Duration")
plt.xlabel("Duration (months)")
plt.tight_layout()
plt.savefig("images/loan_duration_distribution.png", dpi=300, bbox_inches="tight")
plt.show()



