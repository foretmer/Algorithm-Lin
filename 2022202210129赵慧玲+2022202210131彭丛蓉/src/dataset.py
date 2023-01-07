import numpy
import pandas as pd


class ProductDataset:
    """
    导入数据集
    """

    def __init__(
            self,
            products_path,
            num_products,
            min_width,
            max_width,
            min_depth,
            max_depth,
            min_height,
            max_height,
            min_weight,
            max_weight,
            force_overload=False,
    ):
        self.products_path = products_path
        self.num_products = num_products
        self.min_width, self.max_width = min_width, max_width
        self.min_depth, self.max_depth = min_depth, max_depth
        self.min_height, self.max_height = min_height, max_height
        self.min_weight, self.max_weight = min_weight, max_weight
        self.products = self._load_products(force_overload)

    def _load_products(self, force_overload=False):
        products = pd.read_pickle(self.products_path)
        return products

    def get_order(self):
        """
            随机打乱
        """
        order = self.products.sample(frac=1.0)
        ids = pd.Series(order.index, name="id")
        return pd.concat([ids, order.reset_index(drop=True)], axis=1)
