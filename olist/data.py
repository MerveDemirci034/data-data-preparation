from pathlib import Path
import pandas as pd


class Olist:
    """
    The Olist class provides methods to interact with Olist's e-commerce data.
    """

    def get_data(self):
        """
        Returns a dict where:
        - keys are dataset names (sellers, orders, order_items, ...)
        - values are pandas DataFrames loaded from CSV files
        """
        csv_path = Path("~/.workintech/olist/data/csv").expanduser()

        file_paths = list(csv_path.iterdir())
        file_names = [fp.name for fp in file_paths]

        key_names = []
        for name in file_names:
            key = (
    name
    .replace("olist_", "")
    .replace("_dataset.csv", "")
    .replace(".csv", "")
)

            key_names.append(key)

        data = {}
        for key, path in zip(key_names, file_paths):
            data[key] = pd.read_csv(path)

        return data

    def ping(self):
        """You call ping I print pong."""
        print("pong")
