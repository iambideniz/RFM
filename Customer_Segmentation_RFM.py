################ Customer Segmentation using with RFM #########################

# An e-commerce company wants to segment its customers and determine marketing strategies according to these segments. The company believes that marketing activities specific to customer segments that exhibit common behaviors will increase revenue. For example, it is desired to organize different campaigns for new customers and different campaigns to retain very profitable customers for the company.

# The dataset named Online Retail includes the sales of a UK-based online store between 01/12/2009-09/12/2011. This company's product catalog includes souvenirs. The majority of the company's customers are corporate customers.

# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# # Variables
# # InvoiceNo: Invoice Number, If this code starts with C, it means that the transaction has been canceled.
# # StockCode: Product code, Unique number for each product.
# # Description: Product Name
# # Quantity: Product Quantity expresses how many of the products in the Invoices have been sold.
# # InvoiceDate: Invoice Date
# # UnitPrice: Invoice price
# # CustomerID: Unique customer number
# # Country: Country name

import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

################## TASK 1 #########################

# Data Understanding

# Q1: Read the 2010-2011 data in the OnlineRetail II excel. Make a copy of the data frame you created.

df = pd.read_excel("hafta 3/ödev/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df.head()

df_copy = df.copy()
df_copy.head()

# Q2: Examine the descriptive statistics of the data set.

df.shape
df.info()
df.describe().T

# Q3: Are there any missing observations in the dataset? If yes, how many missing observations in which variable?

df.isnull().values.any()
df.isnull().sum()

# Q4: Remove the missing observations from the data set. Use "inplace=True" for subtraction.

df.dropna(inplace=True)
df.shape

# Q5: How many unique products?

df["StockCode"].nunique()

# Q6: How many of each product are there?

df["StockCode"].value_counts()

# Q7: Rank the 5 most ordered products from most to least.

df.groupby("StockCode").agg({"Quantity": "sum"}).sort_values(by="Quantity",ascending=False)

# Q8: "C" canceled transactions in the invoices are displayed. Remove the canceled transactions from the dataset.

df = df[~df["Invoice"].str.contains("C", na=False)]
df.shape

# Q9: Create a variable named "TotalPrice" that represents the total earnings per invoice.

df["TotalPrice"] = df["Quantity"] * df["Price"]
df.head()


################## TASK 2 #########################

######## Calculating RFM Metrics ###########

# Define recency, frequency, monetary.
# Calculate customer-specific recency, frequency, monetary metrics with groupby, agg, and lambda.
# Assign your calculated metrics to a variable named RFM.
# Change the names of the metrics you created to recency, frequency, monetary.

df["InvoiceDate"].max()
today_date = dt.datetime(2011, 12, 11)

# recency
# frequency
# monetary

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda x: (today_date - x.max()).days,
                               "Invoice": lambda x: x.nunique(),
                               "TotalPrice": lambda x: x.sum()})
rfm.head()

rfm.columns = ["recency", "frequency", "monetary"]
rfm

rfm = rfm[rfm["monetary"] > 0]
rfm

################## TASK 3 #########################

######## Calculating RFM Scores ###########

# Convert Recency, Frequency, and Monetary metrics to scores between 1-5 with the help of qcut.
# Record these scores as recency_score, frequency_score, and monetary_score.
# Express recency_score and frequency_score as a single variable and save it as RFM_SCORE.
# ATTENTION! We do not include monetary_score.

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])


rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))


################## TASK 4 #########################

######## Naming & Analysing RFM Segments ###########

# Make segment definitions so that the generated RFM scores can be explained more clearly.
# Convert the scores into segments with the help of the seg_map below.

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])


# Select the customer IDs of the Loyal Customers class and get the excel output.

rfm[rfm["segment"] == "loyal_customers"]

new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "loyal_customers"].index
new_df.head()

new_df.to_excel("loyal_customers.xlsx")


