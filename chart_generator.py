import matplotlib.pyplot as plt

def update_pie_chart(axis, data):
    """
    更新圓餅圖

    axis: Tkinter 傳進來的 Matplotlib 座標軸
    data: 從 JSON 讀出來的 list
    """
    axis.clear()

    # 設定字體
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    
    if not data:
        axis.text(0.5, 0.5, "尚無資料", 
                horizontalalignment = 'center', 
                verticalalignment = 'center',
                fontsize=28, color = 'gray')
        
        axis.set_xticks([]) # 隱藏座標軸刻度
        axis.set_yticks([])
        axis.set_title("支出統計")
        return

    # 整理數據
    sums = {}
    for item in data:
        category = item.get('category', '未分類')
        amount = float(item.get('amount', 0))
        sums[category] = sums.get(category, 0) + amount

    labels = list(sums.keys())
    values = list(sums.values())
    
    axis.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    axis.set_title("支出圓餅圖")