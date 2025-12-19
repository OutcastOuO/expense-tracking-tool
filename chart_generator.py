import matplotlib.pyplot as plt

def update_pie_chart(axis, data):
    """
    更新圓餅圖

    axis: Tkinter 傳進來的 Matplotlib 座標軸
    data: 從 JSON 讀出來的 list
    """
    axis.clear()


    # 設定字體、顏色
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    chart_colors = ['#E6BAA3', '#D2B48C', "#F9E0C7", '#BC8F8F', '#A0522D', '#91A088']
    text_color = "#4B3621"

    if not data:
        axis.text(0.5, 0.5, "還沒有支出紀錄喔", 
                horizontalalignment='center', 
                verticalalignment='center',
                fontsize=20, color='#A68A64')
        axis.axis('off')
        return

    # 整理數據
    sums = {}
    total_amount = 0
    for item in data:
        category = item.get('category', '未分類')
        amount = float(item.get('amount', 0))
        sums[category] = sums.get(category, 0) + amount
        total_amount += amount

    labels = list(sums.keys())
    values = list(sums.values())
    
    wedges, texts, autotexts = axis.pie(
        values, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=140,
        colors=chart_colors,
        pctdistance=0.8,
        wedgeprops={'width': 0.4, 'edgecolor': 'white', 'linewidth': 2},
        textprops={'color': text_color, 'fontsize': 12, 'fontweight': 'bold'}
    )

    plt.setp(autotexts, size=10, weight="bold", color="white")

    axis.text(0, 0.15, "總支出", ha='center', va='center', 
              fontsize=14, color='#8B4513', fontweight='bold')
    
    axis.text(0, -0.10, f"${total_amount:,.0f}", ha='center', va='center', 
              fontsize=18, color=text_color, fontweight='bold')

    axis.set_title("支出結構分析", pad=12, color=text_color, fontsize=18, fontweight='bold')
    axis.axis('equal')