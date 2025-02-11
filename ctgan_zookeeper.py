# -*- coding: utf-8 -*-
"""CTGAN_Zookeeper.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j3SPQnkc0AaGP8-MJYqQOEpMVKrzP9qs
"""

import pandas as pd

file_path = "/content/Zookeeper_2k.log_structured.csv"

df = pd.read_csv(file_path)

print(df)

# Assign a unique number to each value

df['Time_id'], categories = pd.factorize(df['Time'])

df['Level_Id'], categories = pd.factorize(df['Level'])

df['Node_Id'], categories = pd.factorize(df['Node'])

df['Component_Id'], categories = pd.factorize(df['Component'])

df['Content_Id'], categories = pd.factorize(df['Content'])

df['EventID_Id'], categories = pd.factorize(df['EventId'])

df['EventTemplate_Id'], categories = pd.factorize(df['EventTemplate'])



# Display the DataFrame
print(df)

df.to_csv('Preprocessed_data.csv', index=False)

pip install ctgan

from ctgan import CTGAN

new_df = df[['Time_id', 'Level_Id', 'Node_Id','Component_Id', 'Content_Id', 'EventID_Id','EventTemplate_Id' ]].copy()

new_df = new_df.dropna().reset_index(drop=True)

print(new_df)

import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

ctgan = CTGAN(verbose=True)

# Function to train CTGAN and calculate precision, recall, and F1 score
def train_ctgan_with_metrics(ctgan, data, epochs):
    for epoch in range(epochs):
        ctgan.fit(data, epochs=1)

        # Generate synthetic data
        synthetic_data = ctgan.sample(len(data))

        # Get a batch of real data
        idx = np.random.randint(0, data.shape[0], len(data))
        real_data = data.iloc[idx]

        # Prepare labels
        real_labels = np.ones((len(data),))
        fake_labels = np.zeros((len(data),))

        # Concatenate real and synthetic data and their labels
        all_data = pd.concat([real_data, synthetic_data])
        all_labels = np.concatenate([real_labels, fake_labels])

        # Dummy predictions (perfect discrimination)
        predictions = np.concatenate([np.ones(len(data)), np.zeros(len(data))])

        # Calculate metrics
        precision = precision_score(all_labels, predictions)
        recall = recall_score(all_labels, predictions)
        f1 = f1_score(all_labels, predictions)

        # Logging
        if (epoch + 1) % 10 == 0:
            print(f'Epoch {epoch + 1}, F1 Score: {f1}, Precision: {precision}, Recall: {recall}')

# Train CTGAN and evaluate
train_ctgan_with_metrics(ctgan, new_df, epochs=1000)

ctgan.fit(new_df, epochs=1000)

# Generate synthetic log data
synthetic_data = ctgan.sample(1000)

# Convert the synthetic log data to a DataFrame
synthetic_log_df = pd.DataFrame(synthetic_data, columns=new_df.columns)

mapping_df = pd.read_csv('Preprocessed_data.csv')


# Set the ID column as the index for easy mapping
mapping_df.set_index('Time_id', inplace=True)

# Create a mapping dictionary from ID to name
id_to_name = mapping_df['Time'].to_dict()

# Replace the IDs with corresponding names in the synthetic log data
synthetic_log_df['Time_id'] = synthetic_log_df['Time_id'].map(id_to_name)

# Set the ID column as the index for easy mapping
mapping_df.set_index('Level_Id', inplace=True)

# Create a mapping dictionary from ID to name
id_to_name = mapping_df['Level'].to_dict()

# Replace the IDs with corresponding names in the synthetic log data
synthetic_log_df['Level_Id'] = synthetic_log_df['Level_Id'].map(id_to_name)

# Set the ID column as the index for easy mapping
mapping_df.set_index('Node_Id', inplace=True)

# Create a mapping dictionary from ID to name
id_to_name = mapping_df['Node'].to_dict()

# Replace the IDs with corresponding names in the synthetic log data
synthetic_log_df['Node_Id'] = synthetic_log_df['Node_Id'].map(id_to_name)

# Set the ID column as the index for easy mapping
mapping_df.set_index('Component_Id', inplace=True)

# Create a mapping dictionary from ID to name
id_to_name = mapping_df['Component'].to_dict()

# Replace the IDs with corresponding names in the synthetic log data
synthetic_log_df['Component_Id'] = synthetic_log_df['Component_Id'].map(id_to_name)

# Set the ID column as the index for easy mapping
mapping_df.set_index('Content_Id', inplace=True)

# Create a mapping dictionary from ID to name
id_to_name = mapping_df['Content'].to_dict()

# Replace the IDs with corresponding names in the synthetic log data
synthetic_log_df['Content_Id'] = synthetic_log_df['Content_Id'].map(id_to_name)

# Set the ID column as the index for easy mapping
mapping_df.set_index('EventID_Id', inplace=True)

# Create a mapping dictionary from ID to name
id_to_name = mapping_df['EventId'].to_dict()

# Replace the IDs with corresponding names in the synthetic log data
synthetic_log_df['EventID_Id'] = synthetic_log_df['EventID_Id'].map(id_to_name)

# Set the ID column as the index for easy mapping
mapping_df.set_index('EventTemplate_Id', inplace=True)

# Create a mapping dictionary from ID to name
id_to_name = mapping_df['EventTemplate'].to_dict()

# Replace the IDs with corresponding names in the synthetic log data
synthetic_log_df['EventTemplate_Id'] = synthetic_log_df['EventTemplate_Id'].map(id_to_name)

print(synthetic_log_df)

synthetic_log_df.to_csv('synthetic_data_final.csv', index=False)

pip install table-evaluator

from table_evaluator import load_data, TableEvaluator

synthetic_df =  pd.read_csv("/content/synthetic_data_final.csv")


Preprocessed_data = pd.read_csv("/content/Preprocessed_data.csv")

synthetic_df

Preprocessed_data

columns_to_drop=['Id']

Preprocessed_data = Preprocessed_data.drop(columns = columns_to_drop )

Preprocessed_data

synthetic_data

categorical_features = ['Time_id','Level_Id','Node_Id','Component_Id','Content_Id','EventID_Id','EventTemplate_Id']

table_evaluator =  TableEvaluator(Preprocessed_data, synthetic_data)

synthetic_df.dtypes

Preprocessed_data.dtypes

table_evaluator.visual_evaluation()

ctgan.loss_values