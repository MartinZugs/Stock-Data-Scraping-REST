import requests
import mysql.connector

# 1 is yes and -1 is no for the label of good

mydb = mysql.connector.connect(
  host="#Redacted",
  user="root",
  passwd="#Redacted",
  database="stock_data",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

sql = "INSERT INTO historical_daily_stock_data (ticker_symbol, date, open_value, close_value, high_value, low_value, good, trade_volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

tickers = ["SBUX", "AAPL", "NXPI", "FB", "SFIX", "JNJ", "BRK.A", "BRK.B", "CNC", "SFM"]

# Test Case
# response = requests.get("https://api.worldtradingdata.com/api/v1/history?symbol=VTSAX&sort=newest&api_token=eTPYpHBAmNry2fUVo6fL8uCV5peWMwcmgMEpd0aGKQCxkyDYhfWpPwadOuXk").json()
# print(response)

try:
    for stock in tickers:
        
        response = requests.get("https://api.worldtradingdata.com/api/v1/history?symbol=" + stock + "&sort=newest&api_token=eTPYpHBAmNry2fUVo6fL8uCV5peWMwcmgMEpd0aGKQCxkyDYhfWpPwadOuXk").json()

        name = response['name']
        # print(name)

        for x in response['history']:

            # print (x)
            date = x
            
            for y in response['history'][x]:

                if (y == "open"):
                    open_val = response['history'][x][y]
                elif (y == "close"):
                    close_val = response['history'][x][y]
                elif (y == "high"):
                    high_val = response['history'][x][y]
                elif (y == "low"):
                    low_val = response['history'][x][y]
                elif (y == "volume"):
                    volume_val = response['history'][x][y]

            if (float(open_val) > float(close_val)):
                good = -1
            else:
                good = 1
                
            val = (str(name), str(date), str(open_val), str(close_val), str(high_val), str(low_val), str(good), str(volume_val))
            mycursor.execute(sql, val)
            mydb.commit()
            # print(mycursor.rowcount, "record inserted.")
except:
    print(response)
    
