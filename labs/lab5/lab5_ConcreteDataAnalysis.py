# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For creating plots
import seaborn as sns  # For advanced data visualization

from sklearn.model_selection import train_test_split  # To split data into training and test sets
from sklearn.linear_model import LinearRegression  # For linear regression modeling
from sklearn.metrics import mean_squared_error, r2_score  # For evaluating model performance
from sklearn.preprocessing import StandardScaler  # For scaling/normalizing features

def load_data(filepath):
    """
    Load the concrete dataset from the given Excel file.
    Replace zeros with NaN as done in the provided version,
    and strip whitespace from column names.
    """
    df = pd.read_excel(filepath)
    # Remove extra whitespace from column names
    df.columns = df.columns.str.strip()
    # Replace zeros with NaN (only if zeros are considered invalid)
    df.replace(0, np.nan, inplace=True)
    return df

def print_basic_info(df):
    """
    Print basic dataset information: first 10 rows, info, summary statistics, and missing values.
    """
    print("First 10 rows of the dataset:")
    print(df.head(10), "\n")  # Print first 10 rows for a quick glimpse
    
    print("Dataset info:")
    print(df.info(), "\n")  # Print dataset structure, data types, and non-null counts
    
    print("Summary statistics:")
    print(df.describe(), "\n")  # Print summary statistics for numeric columns
    
    print("Missing values per column (after replacing zeros with NaN):")
    print(df.isnull().sum(), "\n")  # Display count of missing values for each column

def plot_histograms(df):
    """
    Create histograms for all features and the target variable.
    Uses 128 bins as specified in the provided code.
    """
    # Create histograms for each column and get the axes array
    axes = df.hist(bins=128, figsize=(12, 8))
    # Iterate over each axis to adjust tick labels and subplot title font size
    for ax in axes.flatten():
        ax.tick_params(axis='both', labelsize=8)  # Set tick label font size to 8
        ax.title.set_fontsize(8)  # Set subplot title font size to 8
    plt.suptitle("Histograms of Features and Target", fontsize=16)  # Set the main title
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout, leaving space for the title
    plt.show()  # Display the histogram plots

def plot_correlation_heatmap(df):
    """
    Plot a correlation heatmap to visualize relationships between variables.
    """
    plt.figure(figsize=(10, 8))  # Set figure size for the heatmap
    corr_matrix = df.corr()  # Calculate the correlation matrix
    ax = sns.heatmap(corr_matrix,
                     annot=True,          # Annotate each cell with the correlation coefficient
                     cmap="coolwarm",     # Use the coolwarm colormap
                     fmt=".3f",           # Format annotations to 3 decimal places
                     annot_kws={"size": 8})  # Set annotation font size to 8
    ax.set_title("Correlation Heatmap", fontsize=16)  # Set the title for the heatmap
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right', fontsize=8)  # Adjust x-axis labels
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)  # Adjust y-axis labels
    plt.tight_layout()  # Prevent overlapping of elements
    plt.show()  # Display the heatmap

def preprocess_data(df):
    """
    Handle missing values by dropping any rows with missing data.
    Returns the cleaned DataFrame.
    """
    df.dropna(inplace=True)  # Remove rows that contain any missing values
    return df

def split_and_scale_data(df, target_column):
    """
    Split the DataFrame into training and testing sets,
    and scale the features using StandardScaler.
    Returns X_train_scaled, X_test_scaled, y_train, y_test.
    """
    # Separate features and target variable
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    # Split the data: 80% training and 20% testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    # Initialize StandardScaler and fit on training data only
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    # Transform the test data using the same scaler parameters
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train.values, y_test.values

def train_model(X_train_scaled, y_train):
    """
    Train a Linear Regression model on the scaled training data.
    Returns the trained model.
    """
    model = LinearRegression()  # Initialize the model
    model.fit(X_train_scaled, y_train)  # Train the model on training data
    return model

def evaluate_model(model, X_test_scaled, y_test):
    """
    Evaluate the model on the test data and print MSE, RMSE, and R^2.
    Returns mse, rmse, r2, and the predicted values.
    """
    # Predict target values using the test set
    y_pred = model.predict(X_test_scaled)
    # Compute Mean Squared Error (MSE)
    mse = mean_squared_error(y_test, y_pred)
    # Compute Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)
    # Compute R^2 score
    r2 = r2_score(y_test, y_pred)
    # Print the evaluation metrics
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R^2 Score: {r2:.2f}")
    return mse, rmse, r2, y_pred

def plot_predictions(y_test, y_pred):
    """
    Plot predicted vs. actual concrete compressive strength and the residual plot.
    """
    # Plot predicted vs. actual values
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.7)  # Scatter plot of actual vs. predicted
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
             color='red', linestyle='--')  # Plot ideal y = x line
    plt.xlabel("Actual Strength (MPa)")
    plt.ylabel("Predicted Strength (MPa)")
    plt.title("Predicted vs. Actual Concrete Compressive Strength")
    plt.show()
    
    # Plot residuals (difference between actual and predicted values)
    residuals = y_test - y_pred
    plt.figure(figsize=(6, 4))
    plt.scatter(y_pred, residuals, alpha=0.7)
    plt.axhline(y=0, color='red', linestyle='--')  # Reference line at zero residual
    plt.xlabel("Predicted Strength (MPa)")
    plt.ylabel("Residual (Actual - Predicted)")
    plt.title("Residual Plot")
    plt.show()

comma = input(str('Do you want to start?(y/n):'))
# Main execution block
if comma == "y":
    # 1. Load the dataset and replace zeros with NaN as in the provided version
    df = load_data("../../datasets/concrete_strength/Concrete_Data.xls")
    
    # 2. Perform Exploratory Data Analysis (EDA)
    print_basic_info(df)
    plot_histograms(df)
    plot_correlation_heatmap(df)
    
    # 3. Preprocess data by dropping rows with missing values
    df_clean = preprocess_data(df)
    
    # 4. Define the target column (ensure it exactly matches the column name after stripping)
    target_column = "Concrete compressive strength(MPa, megapascals)"  # Remove trailing spaces if present
    
    # 5. Split data into training and testing sets and scale features
    X_train_scaled, X_test_scaled, y_train, y_test = split_and_scale_data(df_clean, target_column)
    
    # 6. Train the Linear Regression model
    model = train_model(X_train_scaled, y_train)
    
    # 7. Evaluate the model on the test set
    mse, rmse, r2, y_pred = evaluate_model(model, X_test_scaled, y_test)
    
    # 8. Plot predictions vs actual values and the residual plot
    plot_predictions(y_test, y_pred)
