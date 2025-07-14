import yfinance as yf       
import mplfinance as mpf

settings = {
    "style": {"value": "yahoo", "acceptable_inputs": mpf.available_styles()},  
    "time_period": {"value": "1mo", "acceptable_inputs": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]},
    "show_volume": {"value": "false", "acceptable_inputs": ["true", "false"]},
    "graph_type": {"value": "candle", "acceptable_inputs": ["candle", "ohlc", "line"]},   
}

def menu():
    # Function for displaying the menu. User will be brought back here after every action.
    while True:
        print("\nTHE MENU")
        print("Welcome to the Stock Price Viewer!"
            "\n1. View stock prices"
            "\n2. Settings"
            "\n3. Exit")
        choice = 0
        while choice not in ['1', '2', '3']:
            choice = input("Please select an option (1-3): ")
        if choice == '1': 
            view_stock_prices() 
        elif choice == '2':
            settings_Function()
        else:
            exit() # End of program

def settings_Function():
    # Settings function for updating all settings in the settings dictionary. Made to be scalable for future settings.
    settings_list = list(settings.keys())
    while True:
        print("\nTHE SETTINGS")
        for i in range(len(settings_list)):
            print(f"{i + 1}. {settings_list[i]}: {settings[settings_list[i]]['value']}")
        print(f"{len(settings_list) + 1}. Back to menu")
        
        choice = 0
        while True:
            choice = input(f"Please select an option (1-{len(settings_list) + 1}): ") 
            if int(choice) == len(settings_list) + 1:
                return 
            elif choice in [str(i) for i in range(1, len(settings_list) + 1)]:
                choice = int(choice)
                break

        setting_change = 0    
        while setting_change not in settings[settings_list[choice - 1]]['acceptable_inputs'] and setting_change != "exit":
            print(f"\nWhat would you like to change the setting '{settings_list[choice - 1]}' to?")
            setting_change = input(f"Acceptable inputs are: {settings[settings_list[choice - 1]]['acceptable_inputs']}, or type 'exit' to go back: ")
            if setting_change.lower() == "exit":
                break
            elif setting_change.lower() in settings[settings_list[choice - 1]]['acceptable_inputs']:
                settings[settings_list[choice - 1]]['value'] = setting_change
                print(f"Setting '{settings_list[choice - 1]}' changed to '{setting_change}'.")
                break
            else:
                print("Invalid input. try again.")

def view_stock_prices():
    symbol_input = input("Enter stock symbol (e.g., AAPL, TSLA): ").strip().upper()

    if settings["time_period"]["value"] == "ytd":
        graph_title = "January 1st of this year, to today"
    elif settings["time_period"]["value"] == "max":
        graph_title = "All available data"
    else:
        graph_title = settings["time_period"]["value"]

    try:
        ticker = yf.Ticker(symbol_input)
        df = ticker.history(period=settings["time_period"]["value"])
    except:
        print("Error retrieving data")
        return
    if df.empty:
        print("No data returned for this stock and time period.")
        return 
    
    show_volume_boolean = settings["show_volume"]["value"].lower() == "true"
    mpf.plot(df, type=settings["graph_type"]["value"], volume=show_volume_boolean, style=settings["style"]["value"], title=f'Graph of {symbol_input} stock, for time: {graph_title}')  

# START OF PROGRAM    
menu()
