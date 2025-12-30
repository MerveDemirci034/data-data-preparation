import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        orders = self.data['orders'].copy()
        
        if is_delivered:
            orders = orders[orders['order_status'] == 'delivered'].copy()
        
        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
        orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
        
        orders['wait_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']) / np.timedelta64(1, 'D')
        orders['expected_wait_time'] = (orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']) / np.timedelta64(1, 'D')
        
        orders['delay_vs_expected'] = orders['wait_time'] - orders['expected_wait_time']
        orders['delay_vs_expected'] = orders['delay_vs_expected'].apply(lambda x: x if x > 0 else 0)
        
        final_df = orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']].copy()
        
        return final_df

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews'].copy()

        # Yeni sütunlar oluştur
        reviews['dim_is_five_star'] = reviews['review_score'].map(lambda x: 1 if x == 5 else 0) # 5 ise 1 yaz değilse 0
        reviews['dim_is_one_star'] = reviews['review_score'].map(lambda x: 1 if x == 1 else 0) # 1 ise 1 yaz değilse 0

        # Sadece gerekli sütunları 
        final_reviews = reviews[['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']].copy()
        return final_reviews
    
    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        order_items = self.data['order_items'].copy()
        df = order_items.groupby('order_id')['order_item_id'].count().reset_index()
        df.rename(columns={'order_item_id': 'number_of_items'}, inplace=True)
        return df

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        order_items = self.data['order_items'].copy()
        df = order_items.groupby('order_id')['seller_id'].nunique().reset_index()
        df.rename(columns={'seller_id': 'number_of_sellers'}, inplace=True)
        return df

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        pass  # YOUR CODE HERE

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        pass  # YOUR CODE HERE
