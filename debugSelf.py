
import pandas as pd
import numpy as np

def main():
    print("Starting debugSelf.py...")
    df = generate_fake_flight_reservations(200)
    print(df)

def generate_fake_flight_reservations(n):
    import random
    import string
    pnr_list = ["".join(random.choices(string.ascii_uppercase + string.digits, k=6)) for _ in range(n)]
    passenger_list = [f"Passenger_{i+1}" for i in range(n)]
    airports = ['JFK', 'LAX', 'ORD', 'DFW', 'DEN', 'ATL', 'SFO', 'SEA', 'MIA', 'BOS']
    origin_list = [random.choice(airports) for _ in range(n)]
    destination_list = [random.choice([a for a in airports if a != origin_list[i]]) for i in range(n)]
    fare_list = [round(random.uniform(100, 1500), 2) for _ in range(n)]
    status_list = [random.choice(['Confirmed', 'Cancelled', 'Pending']) for _ in range(n)]
    data = {
        'PNR': pnr_list,
        'Passenger': passenger_list,
        'Origin': origin_list,
        'Destination': destination_list,
        'Fare': fare_list,
        'Status': status_list
    }
    return pd.DataFrame(data)
    

if __name__ == "__main__":
    main()