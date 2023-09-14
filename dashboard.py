import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')


def create_top_product(orders, products):
    order_success = orders[['product_id','order_status']][orders['order_status'] == 'delivered']
    group_order_success = pd.merge(products[['product_id', 'product_category_name_english']], order_success, on="product_id", how='inner') #.sort_values(by='jumlah', ascending=False)
    group_order_success = group_order_success.groupby('product_category_name_english').size().reset_index(name='jumlah').sort_values(by='jumlah', ascending=False).head(10)
    return group_order_success

def create_payment_type(orders):
    group_payment = orders.groupby('payment_type').agg({'order_id': 'count'}).reset_index()
    return group_payment

def create_order_approved_tren(orders):
    group_order_approved = orders.groupby('order_approved_at').agg({'order_id': 'count'}).reset_index()
    group_order_approved['order_approved_at'] = pd.to_datetime(group_order_approved['order_approved_at'], format='%Y-%m-%d')
    group_order_approved['year'] = group_order_approved['order_approved_at'].dt.year
    group_order_approved['month'] = group_order_approved['order_approved_at'].dt.month
    return group_order_approved

def create_sellers_map_data(sellers, geolocation):
    sellers_map_data = pd.merge(sellers[['seller_id', 'seller_zip_code_prefix']], geolocation[['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng']],left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left').drop(columns='geolocation_zip_code_prefix')
    return sellers_map_data

def create_customer_map_data(customers, geolocation):
    customer_map_data = pd.merge(customers[['customer_id', 'customer_zip_code_prefix']], 
    geolocation[['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng']], 
    left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left').drop(columns='geolocation_zip_code_prefix')
    return customer_map_data

def create_ratings_products(orders, products):
    ratings_products = orders[orders.order_status == 'delivered'][['product_id', 'review_score']]
    rating_product_data = pd.merge(ratings_products, products[['product_id', 'product_category_name_english']], on='product_id', how='left').drop(columns='product_id')
    rating_product_data = rating_product_data.dropna()
    group_rating_product = rating_product_data.groupby('product_category_name_english')['review_score'].mean().reset_index().sort_values(by='review_score', ascending=False).head(5)
    return group_rating_product

# import dataset
data_customers = pd.read_csv('./dataset/customers.csv')
data_geolocation = pd.read_csv('./dataset/geolocation.csv')
data_orders = pd.read_csv('./dataset/orders.csv')
data_products = pd.read_csv('./dataset/products.csv')
data_sellers = pd.read_csv('./dataset/sellers.csv')

# menyiapkan dataframe
group_order_success = create_top_product(data_orders, data_products)
group_payment = create_payment_type(data_orders)
group_order_approved = create_order_approved_tren(data_orders)
customer_map_data = create_customer_map_data(data_customers,data_geolocation)
sellers_map_data = create_sellers_map_data(data_sellers,data_geolocation)
group_rating_product = create_ratings_products(data_orders,data_products)

with st.sidebar:
    st.markdown(
        "<div style='display: flex; justify-content: center;'><h1>Nugroho Adi Wirapratama</h1></div>",
        unsafe_allow_html=True
    )

    # Menambahkan foto
    st.markdown(
        "<div style='display: flex; justify-content: center;'>"
        "<img src='https://raw.githubusercontent.com/adiwira09/dicoding/main/photo.png' width='200'>"
        "</div>",
        unsafe_allow_html=True
    )
    st.write('')

st.header("Dashboard E-Commerce Public Dataset")

# Visual 1
st.subheader("Top 10 kategori produk delivered (Quantity)")
plt.figure(figsize=(8, 4))
ax = sns.barplot(x='jumlah', y='product_category_name_english', data=group_order_success.sort_values(by='jumlah', ascending=True), color='yellow')

# Menambahkan nilai di atas setiap batang
for i,p in enumerate(ax.patches):
  width = p.get_width()
  plt.text(width, p.get_y() + p.get_height() / 2, f'{width:.0f}', va='center')

  # Memberikan warna berbeda untuk kategori dengan review_score paling atas
  if i == len(ax.patches) - 1:
    p.set_color('red')  # Atur warna kategori teratas menjadi merah

plt.margins(x=0.07)

# Menambahkan label dan judul
plt.xlabel('Jumlah')
plt.ylabel('')

# Memutar sumbu y
plt.gca().invert_yaxis()

st.pyplot(plt)

# Visual 2
st.subheader("Top 5 rata-rata review score kategori produk")
plt.figure(figsize=(8, 4))
ax = sns.barplot(x='review_score', y='product_category_name_english', data=group_rating_product.sort_values(by='review_score', ascending=True), palette='viridis')

# Menambahkan nilai di setiap batang
for i,p in enumerate(ax.patches):
    width = p.get_width()
    plt.text(width, p.get_y() + p.get_height() / 2, f'{width:.2f}', va='center')

    # Memberikan warna berbeda untuk kategori dengan review_score paling atas
    if i == len(ax.patches) - 1:
      p.set_color('red')  # Atur warna kategori teratas menjadi merah

plt.margins(x=0.07)

# Menambahkan label dan judul
plt.xlabel('Review score')
plt.ylabel('Kategori produk')

# Memutar sumbu y
plt.gca().invert_yaxis()

st.pyplot(plt)

# Visual 3
st.subheader("Jumlah tiap tipe payment")
plt.figure(figsize=(8, 4))
ax = sns.barplot(x='payment_type', y='order_id', data=group_payment)

# Menambahkan nilai di atas setiap batang
for bar in ax.patches:
    bar_value = int(bar.get_height())
    text = f'{bar_value:,}'
    text_x = bar.get_x() + bar.get_width() / 2
    text_y = bar.get_y() + bar_value
    bar_color = bar.get_facecolor()
    ax.text(text_x, text_y, text, ha='center', va='bottom', color='black', size=12)

# Bagian atas diberi ruang dengan margin
plt.margins(y=0.14)

# Menambahkan label dan judul
plt.xlabel('Tipe Pembayaran')
plt.ylabel('Jumlah')

st.pyplot(plt)

# Visual 4
st.subheader("Map persebaran customer dan seller")
col1,col2 = st.columns(2)

# import image map
map = plt.imread('map.png')
BBox = ((customer_map_data.geolocation_lng.min(), customer_map_data.geolocation_lng.max(),customer_map_data.geolocation_lat.min(), customer_map_data.geolocation_lat.max()))

with col1:
    st.markdown("<h3 style='text-align: center; font-size: 20px;'>Map customer</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize = (8,8))
    ax.scatter(customer_map_data.geolocation_lng, customer_map_data.geolocation_lat, zorder=1, alpha= 0.5, c='g', s=20)
    ax.imshow(map, zorder=0, extent = BBox, aspect= 'equal')    
    st.pyplot(fig)


with col2:
    st.markdown("<h3 style='text-align: center; font-size: 20px;'>Map seller</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize = (8,8))
    ax.scatter(sellers_map_data.geolocation_lng, sellers_map_data.geolocation_lat, zorder=1, alpha= 0.5, c='r', s=20)
    ax.imshow(map, zorder=0, extent = BBox, aspect= 'equal')
    st.pyplot(fig)

# Visual 5
st.subheader("Tren harian order approved")
col1,col2,col3 = st.columns(3)

with col1:
    st.markdown("<h3 style='text-align: center; font-size: 20px;'>2016</h3>", unsafe_allow_html=True)
    plt.figure(figsize=(5, 3))  # Ukuran gambar (opsional)
    plt.plot('order_approved_at', 'order_id', data=group_order_approved[group_order_approved['year'] == 2016], marker='', linestyle='-')
    plt.xticks(rotation=45)
    plt.ylabel('Qty')
    plt.grid(True)  # Menampilkan grid
    plt.tight_layout()
    st.pyplot(plt)

with col2:
    st.markdown("<h3 style='text-align: center; font-size: 20px;'>2017</h3>", unsafe_allow_html=True)
    plt.figure(figsize=(5, 3))  # Ukuran gambar (opsional)
    plt.plot('order_approved_at', 'order_id', data=group_order_approved[group_order_approved['year'] == 2017], marker='', linestyle='-')
    plt.xticks(rotation=45)
    # plt.ylabel('Qty')
    plt.grid(True)  # Menampilkan grid
    plt.tight_layout()
    st.pyplot(plt)

with col3:
    st.markdown("<h3 style='text-align: center; font-size: 20px;'>2018</h3>", unsafe_allow_html=True)
    plt.figure(figsize=(5, 3))  # Ukuran gambar (opsional)
    plt.plot('order_approved_at', 'order_id', data=group_order_approved[group_order_approved['year'] == 2018], marker='', linestyle='-')
    plt.xticks(rotation=45)
    # plt.ylabel('Qty')
    plt.grid(True)  # Menampilkan grid
    plt.tight_layout()
    st.pyplot(plt)

st.markdown("<h3 style='text-align: center; font-size: 20px;'>2018</h3>", unsafe_allow_html=True)
plt.figure(figsize=(10, 3))  # Ukuran gambar (opsional)
plt.plot('order_approved_at', 'order_id', data=group_order_approved, marker='', linestyle='-')
plt.ylabel('Qty')
plt.grid(True)  # Menampilkan grid
# plt.tight_layout()
st.pyplot(plt)
