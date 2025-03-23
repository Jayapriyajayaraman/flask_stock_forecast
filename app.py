import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Check if the stock data file exists
csv_file = "GME_stock.csv"  # Ensure this file exists in your project folder

try:
    df = pd.read_csv(csv_file)

    # Check if 'close_price' column exists
    if "close_price" not in df.columns:
        print("Error: 'close_price' column not found in CSV.")
    else:
        # Train SARIMA model
        model = SARIMAX(df["close_price"], order=(1,1,1), seasonal_order=(1,1,1,12))
        results = model.fit()

        # Forecast next 5 days
        forecast = results.forecast(steps=5)
        forecast_df = pd.DataFrame(forecast, columns=["Forecasted Price"])

        # Save forecast data to CSV
        forecast_df.to_csv("forecast.csv", index=False)
        print("✅ Forecast saved to forecast.csv")

except FileNotFoundError:
    print(f"Error: {csv_file} not found. Make sure 'GME_stock.csv' is in your project directory.")
except Exception as e:
    print(f"An error occurred: {e}")
