from src import config, dataset, main

# Load dataset
product_dataset = dataset.ProductDataset(
    "../data/test.csv",
    config.NUM_PRODUCTS,
    config.MIN_PRODUCT_WIDTH,
    config.MAX_PRODUCT_WIDTH,
    config.MIN_PRODUCT_DEPTH,
    config.MAX_PRODUCT_DEPTH,
    config.MIN_PRODUCT_HEIGHT,
    config.MAX_PRODUCT_HEIGHT,
    config.MIN_PRODUCT_WEIGHT,
    config.MAX_PRODUCT_WEIGHT,
    force_overload=2,
)

# Get random order
order = product_dataset.get_order(50)

# Solve bin packing using the specified procedure to get
# a pool of bins without "flying" products
bin_pool = main.main(
    order,
    procedure="mr",
)

# Plot the bin pool

bin_pool.get_original_layer_pool().to_dataframe()
#%%
bin_pool.get_original_layer_pool().describe()
#%%
bin_pool.get_original_bin_pool().plot()
#%%
bin_pool.plot()
bin_pool.plot()