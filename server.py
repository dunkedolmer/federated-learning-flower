import flwr as fl

strategy = fl.server.strategy.FedAvg()

# Start Flower server
fl.server.start_server(
    server_address="0.0.0.0:8080",
    config=fl.server.ServerConfig(num_rounds=3), # Rounds: How many times we repeat the different steps     
    strategy=strategy
)