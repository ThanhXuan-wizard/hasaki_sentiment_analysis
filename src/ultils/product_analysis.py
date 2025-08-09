import pandas  as pd
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud


def GetProductInfoByCode(df_product, product_code):
    # Filter the product data by product name
    df_product_info = df_product.loc[df_product['ma_san_pham'] == product_code]

    # Check if the product exists
    if df_product_info.empty:
        print("Sản phẩm không tồn tại trong dữ liệu.")
        return

    # # Prepare the data
    df_info = GenerateProductDetailTable(df_product_info)
    return df_info

def GenerateProductDetailTable(df_product_info):
    # group by product code
    df_product = df_product_info.groupby('ma_san_pham').first().reset_index()
    
    short_desc = ' '.join(df_product['mo_ta'].values[0].split())
    df_info = pd.DataFrame(data = {
        'information': ['Tên sản phẩm', 'Giá bán', 'Giá gốc', 'Phân loại', 'Mô tả', 'Điểm trung bình'],
        'details': [
            df_product['ten_san_pham'].values[0],
            f"{df_product['gia_ban'].values[0]:,} VNĐ",  # Format as currency
            f"{df_product['gia_goc'].values[0]:,.0f} VNĐ",  # Format as currency
            df_product['phan_loai'].values[0].replace("\n", ", ") if pd.notnull(df_product['phan_loai'].values[0]) else "N/A",  # Replace newlines with commas
            f"{df_product['mo_ta'].values[0]}",
            f"{df_product['diem_trung_binh'].values[0]} ⭐"
        ]
    })
    
    # Set style for the first column
    styled_df_info = df_info.style.set_properties(subset=['information'], **{'background-color': '#ebf8ee'})
    st.dataframe(
    styled_df_info,
    column_config={
        "information": "Thông tin",
        "details": "Chi tiết"
    },
    hide_index=True,
    width=1000)  # Set the minimum width
    

def wcloud_visualize(df_sub, column, title):
    # Check if the column has data
    if df_sub[column].str.len().sum() == 0:
        print(f"Không có đủ dữ liệu để tạo Word Cloud cho {title}.")
        return

    # Generate the word cloud)
    text = ' '.join(set(df_sub[column].str.cat(sep=' ').split()))
    wc = WordCloud(
        background_color='white',
        max_words=50,
        width=1600,
        height=900,
        max_font_size=400
    )
    wc.generate(text)

    plt.figure(figsize=(6, 6))
    plt.imshow(wc, interpolation='bilinear')
    # plt.title(title, fontsize=16)
    plt.axis('off')
    st.pyplot(plt)

def DrawPieChart(data, categories):
    # Plot the enhanced pie chart
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.pie(data, labels=categories, autopct='%1.1f%%', colors=['salmon', 'skyblue'])
    ax.set_title('Sentiment Rate by Category')
    ax.axis('equal')

    # Show the plot using Streamlit
    st.pyplot(fig)

def VisualizeBarPlot(df, xlabel, ylabel, title):
    # Visualize df with bar plot
    fig, ax = plt.subplots()
    df.plot(kind='bar', color="green", ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    st.pyplot(fig)

def GetProductReview(df_review, product_code, df_raw_reviews = None):
    # Analyze the reviews for the selected product
    df_anlyze = df_review.loc[df_review['ma_san_pham'] == product_code]
    if df_anlyze.empty:
        print("Không có đánh giá nào cho sản phẩm này.")
        return
    
    st.write(df_anlyze[['ma_san_pham', 'Categorized', 'Count_Sentiment', 'Sentiment_Rate (%)']].head(5))
  

    st.markdown("#### 3. Trực quan thông tin:")
    col1, col2 = st.columns(2)
    with col1:
        # Prepare data for the pie chart
        sentiment_categories = ['Negative', 'Positive']
        sentiment_data = [0, 0]  # Initialize rates with 0 for all categories

        # Populate sentiment data
        for index, row in df_anlyze.iterrows():
            if row['Categorized'] == 0:  # Negative
                sentiment_data[0] = row['Sentiment_Rate (%)']
            elif row['Categorized'] == 1:  # Positive
                sentiment_data[1] = row['Sentiment_Rate (%)']

        DrawPieChart(sentiment_data, sentiment_categories)
    with col2:
        # Check if the product has reviews
        df_anlyze_2 = df_raw_reviews.loc[df_raw_reviews['ma_san_pham'] == product_code]
        df_rating = df_anlyze_2['so_sao'].value_counts().sort_index()

        VisualizeBarPlot(df_rating, 'Rating', 'Count', 'Product Ratings')
        

    # # Generate word clouds for each sentiment category
    s_positive = df_anlyze[df_anlyze['Categorized'] == 1]
    s_negative = df_anlyze[df_anlyze['Categorized'] == 0]

    col1_wc, col2_wc = st.columns(2)
    with col1_wc:
        st.markdown("\n**Top 50 từ Positive về sản phẩm**")
        wcloud_visualize(s_positive, 'Pos_words', 'Word Cloud - Positive')
    with col2_wc:
        st.write("\n**Top 50 từ Negative về sản phẩm**")
        wcloud_visualize(s_negative, 'Neg_words', 'Word Cloud - Negative')