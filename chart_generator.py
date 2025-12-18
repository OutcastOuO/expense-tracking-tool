import matplotlib.pyplot as plt

def update_pie_chart(axis, data):
    """
    更新圓餅圖

    axis: Tkinter 傳進來的 Matplotlib 座標軸
    data: 從 JSON 讀出來的 list
    """
    axis.clear()
    if not data:
        axis.set_title("尚無資料")
        return

    # 整理數據
    sums = {}
    for item in data:
        category = item['category']
        amount = float(item['amount'])
        sums[category] = sums.get(category, 0) + amount

    labels = list(sums.keys())
    values = list(sums.values())
    
    # 設定字體
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    
    axis.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    axis.set_title("支出圓餅圖")