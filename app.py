import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------------
# 1. НАСТРОЙКИ СТРАНИЦЫ И СТИЛИ
# ---------------------------------------------------------
st.set_page_config(
    page_title="Token Sales Terminal",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

P = ["#2E86AB", "#06A77D", "#F4A261", "#E63946", "#8E7DBE", "#F4E04D"]
T = "plotly_white"

st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; max-width: 1400px;}
    .stTabs [data-baseweb="tab"] {
        height: 50px; padding: 0 20px; background: #F5F7FA;
        border-radius: 8px 8px 0 0; font-weight: 600; font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background: #2E86AB !important; color: white !important;
    }
    .kpi-card {
        background: white; border-radius: 10px; padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #E5E8EC;
    }
    .kpi-title {font-size: 13px; color: #666; margin-bottom: 5px; font-weight: 500;}
    .kpi-value {font-size: 26px; font-weight: 700; color: #2E86AB;}
    .kpi-delta {font-size: 13px; color: #06A77D; font-weight: 600;}
    
    .product-card {
        background: white; border-radius: 12px; padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #E5E8EC;
        text-align: center; transition: transform 0.2s;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.12); }
    .product-icon { font-size: 48px; margin-bottom: 10px; }
    .product-title { font-size: 18px; font-weight: 700; color: #333; margin-bottom: 5px; }
    .product-volume { font-size: 14px; color: #666; margin-bottom: 15px; }
    .product-price { font-size: 22px; font-weight: 800; color: #2E86AB; margin-bottom: 5px; }
    .product-date { font-size: 13px; color: #06A77D; font-weight: 600; margin-bottom: 20px; }
    .btn-buy {
        background: #06A77D; color: white; border: none; padding: 10px 20px;
        border-radius: 6px; font-weight: 600; cursor: pointer; width: 100%;
        font-size: 15px;
    }
    .btn-buy:hover { background: #05966a; }
    
    .law-box {
        background: #F8F9FA; border-left: 4px solid #2E86AB;
        padding: 12px 18px; margin-bottom: 12px; border-radius: 4px;
        font-size: 14px; color: #333;
    }
    .concept-hero {
        background: linear-gradient(135deg, #2E86AB 0%, #06A77D 100%);
        color: white; padding: 30px; border-radius: 12px; margin-bottom: 20px;
    }
    .concept-hero h1 {color: white; margin: 0; font-size: 32px;}
    .concept-hero p {color: rgba(255,255,255,0.9); margin: 10px 0 0; font-size: 16px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. ДЕМО-ДАННЫЕ
# ---------------------------------------------------------
df_gantt_seller = pd.DataFrame([
    dict(Task="Пшеница 3 кл.", Start='2025-06-01', Finish='2025-06-15', Type="Производство"),
    dict(Task="Пшеница 3 кл.", Start='2025-05-01', Finish='2025-06-15', Type="Продажа (УЦП)"),
    dict(Task="Пшеница 4 кл.", Start='2025-06-10', Finish='2025-06-25', Type="Производство"),
    dict(Task="Пшеница 4 кл.", Start='2025-05-05', Finish='2025-06-25', Type="Продажа (УЦП)"),
    dict(Task="Кукуруза", Start='2025-07-01', Finish='2025-07-20', Type="Производство"),
    dict(Task="Кукуруза", Start='2025-06-01', Finish='2025-07-20', Type="Продажа (УЦП)"),
])

fig_waterfall = go.Figure(go.Waterfall(
    name="Выручка", orientation="v",
    measure=["absolute", "relative", "relative", "relative", "total"],
    x=["Валовая выручка", "Комиссия ОИС", "Налоги", "Логистика", "Чистый доход"],
    textposition="outside", text=["120 млн ₽", "-1.2 млн ₽", "-7.2 млн ₽", "-3.5 млн ₽", "108.1 млн ₽"],
    y=[120, -1.2, -7.2, -3.5, None],
    connector={"line":{"color":"#888"}},
    decreasing={"marker":{"color":"#E63946"}}, increasing={"marker":{"color":"#06A77D"}}, totals={"marker":{"color":"#2E86AB"}}
))
fig_waterfall.update_layout(height=400, template=T, margin=dict(l=40, r=40, t=40, b=20), showlegend=False)

df_sunburst = pd.DataFrame({
    "Категория": ["Зерновые", "Зерновые", "Зерновые", "Зерновые", "Технические", "Технические"],
    "Подкатегория": ["Пшеница 3 кл.", "Пшеница 4 кл.", "Кукуруза", "Ячмень", "Подсолнечник", "Соя"],
    "Объем": [2000, 1500, 1000, 500, 800, 400]
})
fig_sunburst = px.sunburst(df_sunburst, path=['Категория', 'Подкатегория'], values='Объем',
                           color_discrete_sequence=P, title="Структура выпущенных УЦП (в тоннах)")
fig_sunburst.update_layout(height=400, template=T, margin=dict(l=20, r=20, t=60, b=20))

df_prices = pd.DataFrame({
    "Товар": ["Пшеница 3", "Пшеница 4", "Кукуруза", "Ячмень", "Подсолнечник", "Соя"],
    "Рынок": [12500, 11000, 9500, 8500, 30000, 40000],
    "УЦП": [12200, 10800, 9200, 8400, 29500, 39000],
    "Объем": [2000, 1500, 1000, 500, 800, 400]
})
fig_scatter = px.scatter(df_prices, x="Рынок", y="УЦП", size="Объем", color="Товар",
                         text="Товар", size_max=50, color_discrete_sequence=P,
                         title="Сравнение цен: Рынок vs УЦП (₽/т)")
fig_scatter.update_traces(textposition='top center')
fig_scatter.add_shape(type="line", x0=0, y0=0, x1=45000, y1=45000, line=dict(color="gray", width=2, dash="dash"))
fig_scatter.update_layout(height=400, template=T, margin=dict(l=20, r=20, t=60, b=20), showlegend=False)

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta", value=85, delta={'reference': 100, 'suffix': "% до плана"},
    title={'text': "Исполнение обязательств по УЦП", 'font': {'size': 20}},
    gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#06A77D"},
           'steps': [{'range': [0, 50], 'color': "#FFEBEE"}, {'range': [50, 80], 'color': "#FFF4E6"}, {'range': [80, 100], 'color': "#E8F5E9"}],
           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}
))
fig_gauge.update_layout(height=400, template=T, margin=dict(l=30, r=30, t=80, b=30))

weeks = ["Нед 1", "Нед 2", "Нед 3", "Нед 4", "Нед 5", "Нед 6"]
products = ["Пшеница 3", "Пшеница 4", "Кукуруза", "Ячмень"]
z_data = [[1, 1, 1, 1, -1, -1], [1, 1, 0, 1, 1, -1], [1, -1, -1, -1, -1, -1], [1, 1, 1, 0, 1, 1]]
fig_heatmap = go.Figure(data=go.Heatmap(
    z=z_data, x=weeks, y=products,
    colorscale=[[0, '#E63946'], [0.5, '#F4A261'], [1, '#06A77D']], showscale=False,
    text=[["В срок" if val==1 else ("Ожидается" if val==-1 else "Задержка") for val in row] for row in z_data],
    texttemplate="%{text}"
))
fig_heatmap.update_layout(title="Календарь поставок (6 недель)", height=400, template=T,
                          margin=dict(l=100, r=20, t=60, b=20), yaxis=dict(autorange="reversed"))

fig_sankey = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 20, thickness = 25, line = dict(color = "black", width = 0.5),
      label = ["Поиск поставщика", "Получение КП", "Согласование договора", "Согласование спецификации", "Получение счета", "Оплата", "Ожидание поставки",
               "Выбор товара", "Ознакомление с условиями", "Покупка УЦП"],
      color = ["#E63946", "#E63946", "#E63946", "#E63946", "#E63946", "#E63946", "#E63946", 
               "#06A77D", "#06A77D", "#06A77D"]
    ),
    link = dict(source = [0, 1, 2, 3, 4, 5, 6, 7, 8], target = [7, 7, 8, 8, 8, 9, 9, 9, 9],
      value = [1, 1, 1, 1, 1, 1, 1, 1, 1], color = ["rgba(230,57,70,0.2)"]*7 + ["rgba(6,167,125,0.2)"]*2)
)])
fig_sankey.update_layout(title="Трансформация сделки: 7 шагов (Красный) -> 3 шага (Зеленый)", 
                         height=400, template=T, margin=dict(l=20, r=20, t=60, b=20), font=dict(size=12))

df_gantt_buyer = pd.DataFrame([
    dict(Task="Пшеница 3 кл. (1000 т)", Start='2025-05-10', Finish='2025-09-01', Status="В пути"),
    dict(Task="Кукуруза (500 т)", Start='2025-06-15', Finish='2025-10-01', Status="Ожидает производства"),
    dict(Task="Пшеница 4 кл. (200 т)", Start='2025-07-01', Finish='2025-09-15', Status="В пути"),
    dict(Task="Ячмень (100 т)", Start='2025-04-20', Finish='2025-06-01', Status="Доставлено"),
])

categories = ['Доходность', 'Надежность', 'Ликвидность', 'Правовая защита', 'Диверсификация']
fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=[8, 9, 7, 10, 6], theta=categories, fill='toself', name='Мой портфель',
    line_color='#06A77D', fillcolor='rgba(6,167,125,0.3)'
))
fig_radar.add_trace(go.Scatterpolar(
    r=[6, 7, 8, 8, 7], theta=categories, fill='toself', name='Средний по рынку',
    line_color='#8E7DBE', fillcolor='rgba(142,125,190,0.1)'
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
    showlegend=True, template=T, height=400, margin=dict(l=40, r=40, t=40, b=40),
    title="Профиль портфеля (0-10)"
)

# ---------------------------------------------------------
# 3. САЙДБАР
# ---------------------------------------------------------
st.sidebar.markdown("## 🏭 Token Sales Terminal")
st.sidebar.caption("B2B-платформа для торговли УЦП")
st.sidebar.markdown("---")

role = st.sidebar.radio(
    "Выберите раздел:",
    ["📑 Концепция проекта", "🏭 Эмитент (Продавец)", "🛒 Покупатель (Инвестор)"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Статус системы:** 🟢 Онлайн")
st.sidebar.caption("Оператор: ОИС 'Цифровой Актив'")

# ---------------------------------------------------------
# 4. ЛОГИКА ОТОБРАЖЕНИЯ
# ---------------------------------------------------------
if role == "📑 Концепция проекта":
    st.markdown("""
    <div class="concept-hero">
        <h1>Token Sales Terminal</h1>
        <p>B2B-платформа для токенизации продаж производственных предприятий</p>
        <p style="font-size:14px; opacity:0.8; margin-top:10px">Сокращаем цикл сделки с 7 дней до 1 дня с помощью УЦП</p>
    </div>
    """, unsafe_allow_html=True)
    
    c_tab1, c_tab_aud, c_tab2, c_tab3, c_tab4, c_tab5 = st.tabs([
        "💡 Идея", "🎯 Целевая аудитория", "📊 Данные и методы", "⚙️ Алгоритм", "⚖️ Право и риски", "💰 Экономика"
    ])
    
    # --- 1. ИДЕЯ ---
    with c_tab1:
        st.markdown("### 📌 Проблема и ценностное предложение")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            fig_old = px.timeline(
                x_start=["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-05", "2025-01-06", "2025-01-07", "2025-01-08"],
                x_end=["2025-01-02", "2025-01-03", "2025-01-05", "2025-01-06", "2025-01-07", "2025-01-08", "2025-01-10"],
                y=["Поиск поставщика", "Получение КП", "Согласование договора", "Спецификация", "Счет", "Оплата", "Ожидание поставки"],
                color_discrete_sequence=["#E63946"]
            )
            fig_old.update_yaxes(autorange="reversed", title="")
            fig_old.update_xaxes(tickformat="%d", tickvals=pd.date_range(start="2025-01-01", end="2025-01-11"), title="Дни", ticktext=[str(i) for i in range(1, 11)])
            fig_old.update_layout(title="Традиционная сделка (до 10 дней)", height=400, template=T, margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
            st.plotly_chart(fig_old, use_container_width=True)
            
        with col2:
            fig_new = px.timeline(
                x_start=["2025-01-01", "2025-01-01", "2025-01-01"],
                x_end=["2025-01-02", "2025-01-02", "2025-01-02"],
                y=["Выбор товара", "Ознакомление с условиями", "Покупка УЦП"],
                color_discrete_sequence=["#06A77D"]
            )
            fig_new.update_yaxes(autorange="reversed", title="")
            fig_new.update_xaxes(tickformat="%d", tickvals=pd.date_range(start="2025-01-01", end="2025-01-11"), title="Дни", ticktext=[str(i) for i in range(1, 11)])
            fig_new.update_layout(title="Сделка через УЦП (1 день)", height=400, template=T, margin=dict(l=20, r=20, t=50, b=20), showlegend=False)
            st.plotly_chart(fig_new, use_container_width=True)

        st.markdown("### 🚀 Как это работает: от переговоров к маркетплейсу")
        st.markdown("""
        <div style="display: flex; gap: 15px; margin-bottom: 20px;">
            <div style="flex: 1; background: #F8F9FA; padding: 15px; border-radius: 8px; border-top: 4px solid #2E86AB;">
                <h4 style="margin-top: 0; color: #2E86AB;">1. Площадка</h4>
                <p style="font-size: 14px; margin-bottom: 0;">Предприятие размещает товары на собственной витрине (или действующем ОИС) в виде УЦП.</p>
            </div>
            <div style="flex: 1; background: #F8F9FA; padding: 15px; border-radius: 8px; border-top: 4px solid #F4A261;">
                <h4 style="margin-top: 0; color: #F4A261;">2. Условия</h4>
                <p style="font-size: 14px; margin-bottom: 0;">Заранее фиксируются в решении о выпуске: объем, цена, сроки поставки и другие параметры.</p>
            </div>
            <div style="flex: 1; background: #F8F9FA; padding: 15px; border-radius: 8px; border-top: 4px solid #06A77D;">
                <h4 style="margin-top: 0; color: #06A77D;">3. Покупка</h4>
                <p style="font-size: 14px; margin-bottom: 0;">Покупатель выбирает товар и приобретает право на поставку в несколько кликов за 1 день.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: white; border: 1px solid #E5E8EC; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                <div style="width: 45%; text-align: right; color: #E63946; font-weight: bold;">Традиционный путь (7 дней)</div>
                <div style="width: 10%; text-align: center; color: #888;">vs</div>
                <div style="width: 45%; text-align: left; color: #06A77D; font-weight: bold;">Путь через УЦП (1 день)</div>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="width: 45%; text-align: right; font-size: 13px; color: #666; line-height: 1.8;">
                    Поиск поставщика ➔ Переговоры ➔ Договор ➔ Спецификация ➔ Счет ➔ Оплата
                </div>
                <div style="width: 10%; text-align: center; font-size: 24px; color: #F4A261;">➔</div>
                <div style="width: 45%; text-align: left; font-size: 16px; font-weight: bold; color: #333; line-height: 1.8;">
                    Выбрал товар ➔ Ознакомился с условиями ➔ Купил УЦП
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🤝 Взаимная выгода")
        c1, c2 = st.columns(2)
        with c1:
            st.info("""
            **Для Предприятия (Эмитента):**
            *   Инструмент предварительного финансирования.
            *   Управление продажами и загрузкой мощностей.
            *   Цифровой рынок продукции (маркетплейс).
            """)
        with c2:
            st.success("""
            **Для Покупателя (Инвестора):**
            *   Фиксация цены и условий на будущее.
            *   Гарантия поставки в срок.
            *   Экономия времени (сделка за 1 день).
            """)
        
        st.markdown("""
        <div class="law-box" style="text-align: center; font-size: 15px;">
        <b>Главный результат:</b> Токенизация превращает десятки часов переговоров в стандартизированные сделки, которые заключаются значительно быстрее.
        </div>
        """, unsafe_allow_html=True)

    # --- 2. ЦЕЛЕВАЯ АУДИТОРИЯ ---
    with c_tab_aud:
        st.markdown("### 🎯 Для кого мы создаем продукт")
        st.markdown("Наш продукт закрывает потребности трех ключевых групп, создавая для каждой из них уникальную ценность.")
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #F8F9FA; border-left: 5px solid #2E86AB; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: #2E86AB;">🏭 Производственные предприятия</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">Агрохолдинги, заводы, добывающие компании</p>
                </div>
                <div style="background: #2E86AB; color: white; padding: 8px 15px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                    Эмитенты УЦП
                </div>
            </div>
            <hr style="border-top: 1px solid #DDD; margin: 15px 0;">
            <div style="display: flex; gap: 20px;">
                <div style="flex: 1;">
                    <b>Боль:</b><br>
                    <span style="color: #666; font-size: 14px;">Заморозка оборотного капитала. Нужны деньги сейчас, а товар будет готов только через 3 месяца. Долгие переговоры с каждым клиентом.</span>
                </div>
                <div style="flex: 1;">
                    <b style="color: #06A77D;">Эффект от продукта:</b><br>
                    <span style="color: #666; font-size: 14px;">Получение предоплаты (финансирования) за будущий урожай. Создание цифрового рынка продукции, где сделки совершаются в 1 клик.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #F8F9FA; border-left: 5px solid #F4A261; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: #F4A261;">🛒 B2B Покупатели</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">Трейдеры, крупные ритейлеры, переработчики</p>
                </div>
                <div style="background: #F4A261; color: white; padding: 8px 15px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                    Инвесторы
                </div>
            </div>
            <hr style="border-top: 1px solid #DDD; margin: 15px 0;">
            <div style="display: flex; gap: 20px;">
                <div style="flex: 1;">
                    <b>Боль:</b><br>
                    <span style="color: #666; font-size: 14px;">Волатильность цен на сырье. Риск срыва поставок. Бюрократия при заключении каждого договора (недели согласований).</span>
                </div>
                <div style="flex: 1;">
                    <b style="color: #06A77D;">Эффект от продукта:</b><br>
                    <span style="color: #666; font-size: 14px;">Фиксация цены на будущее. Гарантия поставки товара. Сделка совершается за 1 день (вместо 7-10 дней), без бумажной волокиты.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #F8F9FA; border-left: 5px solid #8E7DBE; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: #8E7DBE;">⚖️ Корпоративные юристы</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">Юридические департаменты и консалтинговые фирмы</p>
                </div>
                <div style="background: #8E7DBE; color: white; padding: 8px 15px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                    Пользователи
                </div>
            </div>
            <hr style="border-top: 1px solid #DDD; margin: 15px 0;">
            <div style="display: flex; gap: 20px;">
                <div style="flex: 1;">
                    <b>Боль:</b><br>
                    <span style="color: #666; font-size: 14px;">Рутинная работа по составлению типовых договоров и спецификаций. Высокий риск юридических ошибок в условиях сделки.</span>
                </div>
                <div style="flex: 1;">
                    <b style="color: #06A77D;">Эффект от продукта:</b><br>
                    <span style="color: #666; font-size: 14px;">Освобождение от рутины. Сделки «упаковываются» в УЦП автоматически, на основе заранее утвержденного решения о выпуске. Снижение правовых рисков.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- 3. ДАННЫЕ И МЕТОДЫ ---
    with c_tab2:
        st.markdown("### 🗂️ Данные и методы анализа")
        st.markdown("Платформа агрегирует разрозненные данные и применяет ML-модели для минимизации рисков и автоматизации юридических процессов.")
        
        st.markdown("#### 📊 Необходимые данные")
        
        df_data = pd.DataFrame({
            "Категория данных": ["Товарные позиции", "Реестр УЦП", "Финансовые показатели", "Данные о контрагентах", "Регуляторные данные"],
            "Что конкретно берем": [
                "Спецификации, объемы, цены (из ERP/1С)", 
                "Информация о выпущенных токенах, их владельцах", 
                "Выручка, дебиторская задолженность", 
                "История сделок, платежная дисциплина", 
                "Изменения в ФЗ-282, разъяснения ЦБ РФ"
            ],
            "Статус": [
                "<span style='color:#E63946; font-size:20px;'>●</span> Высокая", 
                "<span style='color:#06A77D; font-size:20px;'>●</span> Низкая", 
                "<span style='color:#F4A261; font-size:20px;'>●</span> Средняя", 
                "<span style='color:#E63946; font-size:20px;'>●</span> Высокая", 
                "<span style='color:#F4A261; font-size:20px;'>●</span> Средняя"
            ],
            "Для чего используем": ["Витрина товаров", "Учет прав", "Оценка рисков", "Скоринг покупателя", "Комплаенс-контроль"]
        })
        
        st.write(df_data.to_html(escape=False, index=False), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### 🧠 Архитектура методов анализа")
        st.markdown("Мы используем несколько уровней аналитики: от простого поиска аномалий до сложных нейросетей для юридической проверки.")
        
        df_methods = pd.DataFrame({
            "Метод": [
                "Скоринг контрагента (ML)", 
                "NLP: Анализ решения о выпуске", 
                "Антифрод-анализ",
                "Прогноз спроса и цен",
                "Классификация товаров",
                "Верификация по ФЗ-282"
            ],
            "Направление": ["Риск", "Юридический", "Риск", "Цены", "Риск", "Юридический"],
            "Вес": [25, 25, 20, 15, 15, 10]
        }).sort_values("Вес", ascending=True)

        fig_lollipop = go.Figure()
        
        color_map = {"Риск": "#2E86AB", "Юридический": "#8E7DBE", "Цены": "#F4A261"}
        
        for i, row in df_methods.iterrows():
            fig_lollipop.add_trace(go.Scatter(
                x=[0, row["Вес"]], y=[row["Метод"], row["Метод"]],
                mode='lines', line=dict(color='#DDDDDD', width=2), showlegend=False
            ))
            fig_lollipop.add_trace(go.Scatter(
                x=[row["Вес"]], y=[row["Метод"]], mode='markers+text',
                marker=dict(size=16, color=color_map[row["Направление"]]),
                text=[f"  {row['Вес']}%" if row['Вес'] > 20 else ""], 
                textposition="middle right", textfont=dict(color='#333', size=12),
                name=row["Направление"], showlegend=False
            ))

        fig_lollipop.update_layout(
            height=350, template=T, 
            title="Доля влияния методов на итоговое решение",
            xaxis_title="Вес метода (%)", yaxis_title="",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis=dict(range=[0, 30])
        )
        st.plotly_chart(fig_lollipop, use_container_width=True)

        st.markdown("#### 🔌 Источники данных")
        with st.expander("🔒 Корпоративные данные (Закрытые)"):
            st.markdown("""
            *   **ERP-системы (1С, SAP):** Выгрузка остатков, спецификаций и производственных планов.
            *   **CRM-системы:** История взаимоотношений с контрагентами.
            *   **Внутренние базы данных:** Реестр выпущенных УЦП, история транзакций.
            """)
        with st.expander("🌐 Открытые данные"):
            st.markdown("""
            *   **kad.arbitr.ru:** Проверка контрагентов на наличие судебных споров и банкротств.
            *   **ЕГРЮЛ:** Проверка юридической чистоты компании (директора, учредители).
            *   **Рыночные котировки:** Биржевые цены на сырье для сравнения и ценообразования.
            """)
        with st.expander("📊 Партнерские данные"):
            st.markdown("""
            *   **СПАРК / Контур.Фокус:** Оценка финансовой устойчивости, кредитные рейтинги.
            """)

    # --- 4. АЛГОРИТМ И КЕЙСЫ ---
    with c_tab3:
        st.markdown("### ⚙️ Схема работы продукта")
        
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; background: #F8F9FA; padding: 20px; border-radius: 10px; border: 1px solid #E5E8EC; margin-bottom: 20px;">
            <div style="text-align: center; flex: 1;">
                <div style="background: #2E86AB; color: white; width: 40px; height: 40px; line-height: 40px; border-radius: 50%; margin: 0 auto 10px; font-weight: bold;">1</div>
                <div style="font-weight: bold; font-size: 14px; color: #333;">Эмитент</div>
                <div style="font-size: 12px; color: #666;">Создает УЦП</div>
            </div>
            <div style="color: #F4A261; font-size: 24px; font-weight: bold;">➔</div>
            <div style="text-align: center; flex: 1;">
                <div style="background: #F4A261; color: white; width: 40px; height: 40px; line-height: 40px; border-radius: 50%; margin: 0 auto 10px; font-weight: bold;">2</div>
                <div style="font-weight: bold; font-size: 14px; color: #333;">ОИС</div>
                <div style="font-size: 12px; color: #666;">Проверяет</div>
            </div>
            <div style="color: #F4A261; font-size: 24px; font-weight: bold;">➔</div>
            <div style="text-align: center; flex: 1;">
                <div style="background: #8E7DBE; color: white; width: 40px; height: 40px; line-height: 40px; border-radius: 50%; margin: 0 auto 10px; font-weight: bold;">3</div>
                <div style="font-weight: bold; font-size: 14px; color: #333;">Витрина</div>
                <div style="font-size: 12px; color: #666;">Размещение</div>
            </div>
            <div style="color: #F4A261; font-size: 24px; font-weight: bold;">➔</div>
            <div style="text-align: center; flex: 1;">
                <div style="background: #06A77D; color: white; width: 40px; height: 40px; line-height: 40px; border-radius: 50%; margin: 0 auto 10px; font-weight: bold;">4</div>
                <div style="font-weight: bold; font-size: 14px; color: #333;">Покупатель</div>
                <div style="font-size: 12px; color: #666;">Выбирает</div>
            </div>
            <div style="color: #F4A261; font-size: 24px; font-weight: bold;">➔</div>
            <div style="text-align: center; flex: 1;">
                <div style="background: #06A77D; color: white; width: 40px; height: 40px; line-height: 40px; border-radius: 50%; margin: 0 auto 10px; font-weight: bold;">5</div>
                <div style="font-weight: bold; font-size: 14px; color: #333;">Сделка</div>
                <div style="font-size: 12px; color: #666;">Покупка</div>
            </div>
            <div style="color: #F4A261; font-size: 24px; font-weight: bold;">➔</div>
            <div style="text-align: center; flex: 1;">
                <div style="background: #2E86AB; color: white; width: 40px; height: 40px; line-height: 40px; border-radius: 50%; margin: 0 auto 10px; font-weight: bold;">6</div>
                <div style="font-weight: bold; font-size: 14px; color: #333;">Депозитарий</div>
                <div style="font-size: 12px; color: #666;">Учет прав</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Кейс 1: Завод продает будущий урожай"):
            st.markdown("""
            **Ситуация:** Завод хочет получить предоплату за продукцию, которая будет произведена через 3 месяца.
            **Решение:** Завод выпускает УЦП на 1 000 тонн пшеницы. Покупатель покупает УЦП сегодня, фиксируя цену. 
            Завод получает деньги сейчас и использует их как оборотный капитал. Покупатель получает гарантию поставки.
            """)
            
        with st.expander("Кейс 2: Трейдер покупает товар в 1 клик"):
            st.markdown("""
            **Ситуация:** Трейдеру срочно нужен объем кукурузы.
            **Решение:** Он заходит на платформу, видит стандартное решение о выпуске, покупает УЦП. 
            Вместо 7 дней переговоров сделка занимает 15 минут.
            """)

    # --- 5. ПРАВО И РИСКИ ---
    with c_tab4:
        st.markdown("### ⚖️ Юридический анализ (ФЗ-282)")
        
        st.markdown("""
        <div class="law-box">
        <b>Правовая база:</b> Деятельность регулируется Федеральным законом от 04.08.2026 № 282-ФЗ «О цифровых валютах и цифровых правах» (вступает в силу с 01.09.2026).
        </div>
        <div class="law-box">
        <b>Конфиденциальность:</b> Платформа обязуется обеспечивать конфиденциальность ключей доступа и информации о сделках (ст. 29 ФЗ-282).
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### ⚠️ Матрица рисков (Балл = Вероятность × Ущерб)")
            df_risks = pd.DataFrame({
                "Риск": ["Утечка данных / ключей", "Блокировка ЦБ", "Ошибка в решении о выпуске", "Сбой в работе ОИС"],
                "Балл риска": [40, 20, 35, 24],
                "Уровень": ["Критический", "Высокий", "Критический", "Высокий"]
            }).sort_values("Балл риска", ascending=True)
            
            fig_risk = go.Figure(go.Bar(
                x=df_risks["Балл риска"], y=df_risks["Риск"], orientation="h",
                marker_color=["#F4A261" if lvl=="Высокий" else "#E63946" for lvl in df_risks["Уровень"]],
                text=df_risks["Балл риска"], textposition="outside"
            ))
            fig_risk.update_layout(height=380, template=T, xaxis_title="Балл риска (0-50)", xaxis=dict(range=[0, 50]))
            st.plotly_chart(fig_risk, use_container_width=True)
            
        with col2:
            st.markdown("#### 📜 Ключевые нормы для продукта")
            st.markdown("""
            <div style="background: #F8F9FA; border-left: 4px solid #2E86AB; padding: 12px; margin-bottom: 10px; border-radius: 4px;">
                <b>Имущественный статус (ст. 2, 128 ГК РФ)</b><br>
                <span style="font-size: 13px; color: #555;">УЦП — это имущество. Права на него защищаются в суде. Можно включать в завещания и делить при разводе.</span>
            </div>
            <div style="background: #F8F9FA; border-left: 4px solid #F4A261; padding: 12px; margin-bottom: 10px; border-radius: 4px;">
                <b>Запрет на платежи (ст. 1 п. 6)</b><br>
                <span style="font-size: 13px; color: #555;">УЦП нельзя использовать как средство оплаты внутри РФ. Это только право требовать передачи товара, работы или услуги.</span>
            </div>
            <div style="background: #F8F9FA; border-left: 4px solid #06A77D; padding: 12px; margin-bottom: 10px; border-radius: 4px;">
                <b>Новая инфраструктура (ст. 17, 22)</b><br>
                <span style="font-size: 13px; color: #555;">УЦП больше не «заперты» в одной системе. Учет возможен через общую депозитарную инфраструктуру (вторичный рынок).</span>
            </div>
            <div style="background: #F8F9FA; border-left: 4px solid #E63946; padding: 12px; border-radius: 4px;">
                <b>Ужесточение контроля (ст. 35)</b><br>
                <span style="font-size: 13px; color: #555;">Вводится «цифровой анализ» (AML). Участники рынка обязаны проверять транзакции и адреса на связь с преступной деятельностью.</span>
            </div>
            """, unsafe_allow_html=True)

    # --- 6. ЭКОНОМИКА ---
        with c_tab5:
            st.markdown("### 💰 Экономика проекта")
            st.caption("Полная методология расчёта: от драйверов выручки до DCF-анализа, сценариев и чувствительности")
        
            # ---------- KPI ----------
            st.markdown("#### 📊 Ключевые инвестиционные показатели")
            kc1, kc2, kc3, kc4 = st.columns(4)
            kc1.metric("NPV (5 лет)", "1 704 млн ₽", "WACC = 19%")
            kc2.metric("IRR", "342%", ">> WACC 19%")
            kc3.metric("PI", "57.4×", "на 1 ₽ инвестиций")
            kc4.metric("DPP", "1.9 года", "дисконтированный")
            st.markdown("<br>", unsafe_allow_html=True)
        
            # ---------- Методология ----------
            st.markdown("#### 🧮 Методология расчёта")
            st.markdown("""
            Экономическая модель построена по стандарту инвестиционного анализа **DCF** 
            (Discounted Cash Flow) в **8 последовательных шагов**:
        
            | Шаг | Что рассчитываем | Метод / формула |
            |:---:|:---|:---|
            | 1 | **Выручка** | Комиссия 0.5% × GMV (кол-во клиентов × средний объём) |
            | 2 | **Затраты** | 5 категорий OPEX (ФОТ, облако, маркетинг, юристы, прочее) |
            | 3 | **EBITDA** | Revenue − OPEX |
            | 4 | **WACC** | CAPM (Ke) + стоимость долга (Kd), взвешенные по D/E |
            | 5 | **FCF** | NOPAT + D&A − CAPEX − ΔNWC |
            | 6 | **DCF** | Σ FCF/(1+WACC)ᵗ + Терминальная стоимость (TV) |
            | 7 | **Метрики** | NPV, IRR, PI, DPP |
            | 8 | **Сценарии + tornado** | Проверка устойчивости модели |
            """)
        
            # ---------- Шаг 1: Выручка ----------
            st.markdown("#### 💵 Шаг 1. Драйверы выручки")
            st.markdown("""
            Выручка платформы — это **комиссия 0.5% от объёма сделок (GMV)**. 
            GMV зависит от двух драйверов: **количество эмитентов** и **средний объём сделок на клиента**.
        
            **Формула:** `Revenue = Clients × Avg GMV per client × 0.5%`
            """)
        
            df_rev_drivers = pd.DataFrame({
                "Показатель": [
                    "Количество эмитентов, шт",
                    "Средний GMV на клиента, млрд ₽",
                    "Совокупный GMV, млрд ₽",
                    "Ставка комиссии",
                    "Выручка, млн ₽",
                ],
                "2026": ["5", "1.08", "5.4", "0.5%", "**27**"],
                "2027": ["15", "1.92", "28.8", "0.5%", "**144**"],
                "2028": ["40", "2.70", "108.0", "0.5%", "**540**"],
            })
            st.dataframe(df_rev_drivers, use_container_width=True, hide_index=True)
        
            fig_rev = go.Figure()
            fig_rev.add_trace(go.Bar(
                x=["2026", "2027", "2028"], y=[27, 144, 540],
                marker_color=[P[0], P[0], P[0]],
                text=["27 млн ₽", "144 млн ₽", "540 млн ₽"], textposition="outside"
            ))
            fig_rev.update_layout(
                title="Комиссионная выручка платформы (0.5% от GMV)",
                height=350, template=T, showlegend=False,
                yaxis_title="Выручка, млн ₽", margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_rev, use_container_width=True, key="econ_rev")
        
            st.info("""
            **Логика роста.** В 2026 — 5 пилотных эмитентов с оборотом ~1.1 млрд ₽ каждый. 
            К 2028 — 40 эмитентов с оборотом 2.7 млрд ₽. Рост GMV в 20× достигается 
            за счёт **сетевого эффекта**: каждый новый эмитент привлекает покупателей, 
            которые, в свою очередь, приводят новых эмитентов.
            """)
        
            # ---------- Шаг 2: Затраты ----------
            st.markdown("#### 💸 Шаг 2. Структура операционных затрат (OPEX)")
            st.markdown("""
            OPEX разбит на **5 категорий**, которые масштабируются с разной скоростью:
            - **ФОТ** — крупнейшая статья (62% в 2026 → 50% в 2028): команда растёт, но медленнее выручки
            - **Облачная инфраструктура** — переменная, растёт пропорционально GMV
            - **Маркетинг и B2B-продажи** — фиксированная ставка на привлечение эмитента
            - **Юристы и комплаенс** — полупеременная, растёт с регуляторной нагрузкой
            - **Прочее** — офис, IT, аутсорсинг
            """)
        
            df_costs = pd.DataFrame({
                "Категория": [
                    "ФОТ (разработка, продажи, поддержка)",
                    "Облачная инфраструктура",
                    "Маркетинг и B2B-продажи",
                    "Юридические и комплаенс",
                    "Прочее (офис, IT, аутсорсинг)",
                ],
                "2026": [30, 5, 8, 3, 2],
                "2027": [42, 8, 12, 5, 3],
                "2028": [90, 25, 35, 15, 15],
                "Итого OPEX": [48, 70, 180],
            })
        
            fig_costs = go.Figure()
            cost_colors_list = [P[0], P[1], P[2], P[3], P[4]]
            for i in range(5):
                fig_costs.add_trace(go.Bar(
                    name=df_costs.iloc[i]["Категория"].split(" (")[0],
                    x=["2026", "2027", "2028"],
                    y=[df_costs.iloc[i]["2026"], df_costs.iloc[i]["2027"], df_costs.iloc[i]["2028"]],
                    marker_color=cost_colors_list[i]
                ))
            fig_costs.update_layout(
                barmode="stack", title="Структура OPEX по категориям, млн ₽",
                height=400, template=T, yaxis_title="млн ₽",
                margin=dict(l=20, r=20, t=50, b=80),
                legend=dict(orientation="h", yanchor="bottom", y=-0.35, x=0)
            )
            st.plotly_chart(fig_costs, use_container_width=True, key="econ_costs")
        
            st.markdown("""
            **Ключевой эффект масштаба.** OPEX растёт в **3.75×** (48 → 180 млн ₽), 
            а выручка — в **20×** (27 → 540 млн ₽). Именно поэтому EBITDA margin 
            переходит из −78% в +67% за три года.
            """)
        
            # ---------- Шаг 3: EBITDA ----------
            st.markdown("#### 📈 Шаг 3. EBITDA и операционный рычаг")
            st.markdown("""
            **EBITDA = Revenue − OPEX.** Показывает операционную эффективность до 
            амортизации, процентов и налогов. Рост маржи — индикатор операционного рычага.
            """)
        
            fig_ebitda = go.Figure()
            fig_ebitda.add_trace(go.Bar(name="Выручка", x=["2026", "2027", "2028"], y=[27, 144, 540], marker_color=P[0]))
            fig_ebitda.add_trace(go.Bar(name="OPEX", x=["2026", "2027", "2028"], y=[48, 70, 180], marker_color=P[3]))
            fig_ebitda.add_trace(go.Scatter(
                name="EBITDA margin, %", x=["2026", "2027", "2028"], y=[-78, 51, 67],
                mode="lines+markers+text", text=["−78%", "51%", "67%"], textposition="top center",
                yaxis="y2", line=dict(color=P[1], width=3, dash="dash"), marker=dict(size=12)
            ))
            fig_ebitda.update_layout(
                barmode="group", title="Выручка vs OPEX и EBITDA margin",
                height=400, template=T, margin=dict(l=20, r=20, t=60, b=80),
                yaxis=dict(title="млн ₽"),
                yaxis2=dict(title="EBITDA margin, %", overlaying="y", side="right", range=[-100, 100]),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3)
            )
            st.plotly_chart(fig_ebitda, use_container_width=True, key="econ_ebitda")
        
            # ---------- Шаг 4: WACC ----------
            st.markdown("#### 🎯 Шаг 4. Ставка дисконтирования — WACC")
            st.markdown("""
            WACC (Weighted Average Cost of Capital) — средневзвешенная стоимость капитала. 
            Показывает минимальную доходность, которую проект должен генерировать, 
            чтобы создавать стоимость.
        
            **Формула:** `WACC = We × Ke + Wd × Kd × (1 − T)`
        
            **Стоимость собственного капитала (CAPM):** `Ke = Rf + β × ERP + Size premium`
        
            **Стоимость заёмного капитала:** `Kd = Ключевая ставка ЦБ + Спред`
            """)
        
            df_wacc = pd.DataFrame({
                "Компонент": [
                    "Risk-free rate (ОФЗ 10 лет)",
                    "ERP (премия за риск рынка)",
                    "Beta (unlevered, Software)",
                    "Size premium (Duff & Phelps)",
                    "**Стоимость собственного капитала (Ke)**",
                    "Ключевая ставка ЦБ РФ",
                    "Кредитный спред",
                    "Стоимость долга до налога (Kd)",
                    "Ставка налога на прибыль",
                    "**Стоимость долга после налога**",
                ],
                "Значение": ["8.5%", "7.5%", "1.20", "3.0%", "**20.5%**", "16.5%", "2.0%", "18.5%", "25%", "**13.9%**"],
                "Источник": ["ЦБ РФ, ОФЗ", "Damodaran", "Damodaran (Software)", "SBBI Yearbook", "CAPM", "ЦБ РФ", "Банковский рынок", "Расчёт", "НК РФ", "Kd × (1 − T)"],
            })
            st.dataframe(df_wacc, use_container_width=True, hide_index=True)
        
            st.markdown("""
            **Структура капитала:** целевое D/E = 0.30 → веса E = 77%, D = 23%.
        
            `WACC = 0.77 × 20.5% + 0.23 × 18.5% × (1 − 0.25) = 15.8% + 3.2% = 19.0%`
            """)
        
            # ---------- Шаг 5: FCF и DCF ----------
            st.markdown("#### 💎 Шаг 5. Свободный денежный поток (FCF) и DCF-анализ")
            st.markdown("""
            **FCF** — деньги, остающиеся у проекта после всех операционных расходов, 
            налогов и инвестиций:
        
            `FCF = NOPAT + D&A − CAPEX − ΔNWC`
        
            где `NOPAT = EBITDA × (1 − T)` (упрощённо).
            """)
        
            df_fcf = pd.DataFrame({
                "Показатель": ["EBITDA", "Налог на прибыль (25%)", "NOPAT", "+ Амортизация (D&A)", "− CAPEX", "− Изменение NWC", "**= FCF**"],
                "2026": [-21, 0, -21, 5, -15, -5, "**−36**"],
                "2027": [74, -16.5, 57.5, 8, -12, -8, "**45.5**"],
                "2028": [360, -87.5, 272.5, 10, -20, -15, "**247.5**"],
                "2029": [580, -142, 426, 12, -15, -25.5, "**397.5**"],
                "2030": [880, -216, 649, 15, -18, -46, "**600**"],
            })
            st.dataframe(df_fcf, use_container_width=True, hide_index=True)
        
            st.markdown("""
            **Терминальная стоимость (TV)** — стоимость проекта за пределами 5-летнего 
            горизонта. Используем консервативный **exit multiple = 3× EBITDA_2030**:
        
            `TV = 3 × 880 = 2 640 млн ₽`
        
            Далее дисконтируем каждый FCF и TV по ставке WACC = 19%.
            """)
        
            fcf_vals = [-36, 45.5, 247.5, 397.5, 600]
            wacc_val = 0.19
            dfs = [(1 / (1 + wacc_val) ** (i + 1)) for i in range(5)]
            dcf_vals = [fcf * df for fcf, df in zip(fcf_vals, dfs)]
            tv_disc = 2640 * dfs[-1]
            cum_dcf_5y = np.cumsum(dcf_vals)
        
            fig_dcf = go.Figure()
            fig_dcf.add_trace(go.Bar(name="FCF (недисконтированный)", x=["2026", "2027", "2028", "2029", "2030"], y=fcf_vals, marker_color="#CCCCCC"))
            fig_dcf.add_trace(go.Bar(name="DCF (дисконтированный)", x=["2026", "2027", "2028", "2029", "2030"], y=dcf_vals, marker_color=P[0]))
            fig_dcf.add_trace(go.Bar(name="TV (терминальная стоимость)", x=["2026", "2027", "2028", "2029", "2030"], y=[0, 0, 0, 0, tv_disc], marker_color=P[2]))
            fig_dcf.add_trace(go.Scatter(
                name="Накопленный DCF", x=["2026", "2027", "2028", "2029", "2030"], y=cum_dcf_5y,
                mode="lines+markers", line=dict(color=P[3], width=3), yaxis="y2"
            ))
            fig_dcf.update_layout(
                barmode="group", title="FCF, DCF и накопленный DCF, млн ₽",
                height=420, template=T, margin=dict(l=20, r=20, t=60, b=80),
                yaxis=dict(title="млн ₽"),
                yaxis2=dict(title="Накопленный DCF, млн ₽", overlaying="y", side="right"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3)
            )
            st.plotly_chart(fig_dcf, use_container_width=True, key="econ_dcf")
        
            npv_total = sum(dcf_vals) + tv_disc
            st.markdown(f"""
            **Суммируем дисконтированные потоки:**
        
            `NPV = (−30.2) + 32.1 + 146.9 + 198.2 + 251.4 + 1 106.2 = {npv_total:.0f} млн ₽`
        
            Накопленный DCF пересекает ноль в 2027 году — это и есть **дисконтированный 
            период окупаемости DPP ≈ 1.9 года**.
            """)
        
            # ---------- Шаг 6: Метрики ----------
            st.markdown("#### 🏆 Шаг 6. Инвестиционные метрики")
            mcol1, mcol2, mcol3, mcol4 = st.columns(4)
            mcol1.metric("NPV", "1 704 млн ₽", "> 0 — создаёт стоимость")
            mcol2.metric("IRR", "342%", ">> WACC 19%")
            mcol3.metric("PI", "57.4×", "на 1 ₽ инвестиций")
            mcol4.metric("DPP", "1.9 года", "окупаемость")
        
            with st.expander("📖 Формулы и логика метрик"):
                st.markdown("""
                - **NPV** = Σ FCF/(1+WACC)ᵗ + TV/(1+WACC)⁵ — чистая приведённая стоимость. 
                  Если NPV > 0, проект создаёт стоимость для инвесторов.
                - **IRR** — внутренняя норма доходности, ставка, при которой NPV = 0. 
                  Решается численно. Должна быть > WACC.
                - **PI** = PV(притоков) / PV(оттоков) — индекс рентабельности. 
                  Показывает, сколько рублей NPV приходится на 1 рубль инвестиций.
                - **DPP** — дисконтированный период окупаемости, момент, когда 
                  накопленный DCF становится положительным.
                """)
        
            # ---------- Шаг 7: Сценарии ----------
            st.markdown("#### 🎲 Шаг 7. Сценарный анализ")
            st.markdown("""
            Три сценария по трём ключевым драйверам: темп подписания клиентов, 
            средний GMV на клиента и ставка дисконтирования.
            """)
        
            df_scen = pd.DataFrame({
                "Параметр": [
                    "Темп подписания клиентов, /год",
                    "Средний GMV на клиента к 2028, млрд ₽",
                    "WACC",
                    "NPV, млн ₽",
                    "IRR",
                    "PI",
                    "DPP",
                ],
                "Пессимистичный": ["10", "1.5", "23%", "~350", "~55%", "~4×", "~3.5 года"],
                "Базовый": ["40", "2.7", "19%", "**1 704**", "**342%**", "**57.4×**", "**1.9 года**"],
                "Оптимистичный": ["60", "3.5", "16%", "~3 800", "~600%", "~110×", "~1.3 года"],
            })
            st.dataframe(df_scen, use_container_width=True, hide_index=True)
        
            fig_scen = go.Figure(go.Bar(
                x=["Пессимистичный", "Базовый", "Оптимистичный"],
                y=[350, 1704, 3800],
                marker_color=["#E63946", "#2E86AB", "#06A77D"],
                text=["350 млн ₽", "1 704 млн ₽", "3 800 млн ₽"],
                textposition="outside"
            ))
            fig_scen.update_layout(
                title="NPV по сценариям", height=350, template=T, showlegend=False,
                yaxis_title="NPV, млн ₽", margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig_scen, use_container_width=True, key="econ_scen")
        
            st.success("""
            **Вывод по сценариям.** Даже в пессимистичном сценарии (10 клиентов вместо 40, 
            GMV в 1.8× ниже, WACC 23%) проект остаётся **NPV-положительным**. 
            Ключевой риск — не экономика, а **скорость подписания первого якорного клиента**.
            """)
        
            # ---------- Шаг 8: Sensitivity ----------
            st.markdown("#### 🌪️ Шаг 8. Анализ чувствительности NPV (tornado)")
            st.markdown("""
            Однофакторный анализ: как меняется NPV при отклонении каждого драйвера 
            на ±20% относительно базового значения.
            """)
        
            tornado_drivers = ["Выручка (GMV)", "OPEX", "WACC", "CAPEX"]
            tornado_spread = [480, 340, 240, 90]
        
            fig_tornado = go.Figure()
            fig_tornado.add_trace(go.Bar(
                name="Худший сценарий", y=tornado_drivers,
                x=[-s for s in tornado_spread], orientation="h", marker_color="#E63946"
            ))
            fig_tornado.add_trace(go.Bar(
                name="Лучший сценарий", y=tornado_drivers,
                x=tornado_spread, orientation="h", marker_color="#06A77D"
            ))
            fig_tornado.update_layout(
                barmode="overlay", title="Диапазон ΔNPV при ±20% изменении драйверов",
                height=350, template=T, xaxis_title="ΔNPV, млн ₽",
                margin=dict(l=20, r=20, t=60, b=20),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_tornado, use_container_width=True, key="econ_tornado")
        
            st.warning("""
            **Выручка — самый чувствительный драйвер** (размах ±480 млн ₽ при ±20%). 
            Для OPEX, WACC и CAPEX знак эффекта противоположный (снижение расходов/ставки 
            увеличивает NPV), но диапазон составляет ±340, ±240 и ±90 млн ₽ соответственно.
            Операционный контроль за привлечением эмитентов и удержанием объёмов сделок — 
            критический фактор успеха.
            """)
        
            # ---------- Выводы ----------
            st.markdown("#### ✅ Экономические выводы")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%); padding: 22px; border-radius: 10px; border-left: 5px solid #06A77D; color: #333; font-size: 14px; line-height: 1.7;">
            <b>1. Проект экономически привлекателен.</b> NPV = 1 704 млн ₽, IRR = 342%, PI = 57× — 
            все метрики значительно превышают пороговые значения. Проект создаёт стоимость 
            уже в базовом сценарии.<br><br>
            <b>2. Операционный рычаг — ключевой драйвер.</b> EBITDA margin растёт с −78% до +67% 
            за три года благодаря тому, что OPEX увеличивается в 3.75×, а выручка — в 20×. 
            Это типичная характеристика SaaS-платформ.<br><br>
            <b>3. Быстрая окупаемость.</b> DPP ≈ 1.9 года — редкость для B2B-платформ, поскольку 
            стартовые инвестиции невелики (63 млн ₽ OPEX + CAPEX в первый год), а монетизация 
            комиссионная с первого года.<br><br>
            <b>4. Устойчивость к рискам.</b> Даже пессимистичный сценарий даёт положительный NPV. 
            Главный риск — <b>скорость привлечения первого якорного эмитента</b>, 
            а не юнит-экономика.<br><br>
            <b>5. Монетизация.</b> 0.5% комиссия с GMV — низкая для клиента (стимул к использованию), 
            но при больших объёмах даёт высокую маржинальность платформе. Дополнительные потоки: 
            подписка на аналитический модуль и white-label для холдингов (учтены в базовом сценарии).
            </div>
            """, unsafe_allow_html=True)

elif role == "🏭 Эмитент (Продавец)":
    st.title("🏭 Панель управления продажами")
    st.caption("Управляйте выпуском УЦП, ценами и исполнением обязательств")
    
    tab1, tab2, tab3 = st.tabs(["📊 Обзор рынка", "🛍️ Витрина и ценообразование", "📦 Исполнение обязательств"])
    
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<div class="kpi-card"><div class="kpi-title">Выставлено УЦП</div><div class="kpi-value">4 500 т</div><div class="kpi-delta">+12% к плану</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="kpi-card"><div class="kpi-title">Продано за месяц</div><div class="kpi-value">3 200 т</div><div class="kpi-delta">+8% к прошлому</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="kpi-card"><div class="kpi-title">Средняя цена</div><div class="kpi-value">11 200 ₽/т</div><div class="kpi-delta">Рынок: 11 500 ₽</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="kpi-card"><div class="kpi-title">Ср. срок до поставки</div><div class="kpi-value">45 дней</div><div class="kpi-delta" style="color:#E63946;">-5 дней</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(fig_waterfall, use_container_width=True, key="w1")
        with col2:
            fig_gantt = px.timeline(df_gantt_seller, x_start="Start", x_end="Finish", y="Task", color="Type",
                                    color_discrete_map={"Производство": "#8E7DBE", "Продажа (УЦП)": "#06A77D"})
            fig_gantt.update_yaxes(autorange="reversed")
            fig_gantt.update_layout(height=400, template=T, margin=dict(l=20, r=20, t=40, b=20), title="План производства vs Продажи")
            st.plotly_chart(fig_gantt, use_container_width=True, key="g1")

    with tab2:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(fig_sunburst, use_container_width=True, key="s1")
        with col2:
            st.plotly_chart(fig_scatter, use_container_width=True, key="s2")
        
    with tab3:
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.plotly_chart(fig_gauge, use_container_width=True, key="g2")
        with col2:
            st.plotly_chart(fig_heatmap, use_container_width=True, key="h1")

else:
    st.title("🛒 Витрина цифровых прав")
    st.caption("Покупайте права на поставку продукции в несколько кликов")
    
    tab4, tab5, tab6 = st.tabs(["🏪 Витрина УЦП", "📁 Портфель прав", "⚖️ Юридический конструктор"])
    
    with tab4:
        st.markdown("### Доступные предложения")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            <div class="product-card">
                <div class="product-icon">🌾</div>
                <div class="product-title">Пшеница 3 класс</div>
                <div class="product-volume">Объем: 1 000 тонн</div>
                <div class="product-price">12 200 ₽/т</div>
                <div class="product-date">Поставка: 01.09.2025</div>
                <button class="btn-buy">Купить УЦП</button>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="product-card">
                <div class="product-icon">🌾</div>
                <div class="product-title">Пшеница 4 класс</div>
                <div class="product-volume">Объем: 500 тонн</div>
                <div class="product-price">10 800 ₽/т</div>
                <div class="product-date">Поставка: 15.09.2025</div>
                <button class="btn-buy">Купить УЦП</button>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div class="product-card">
                <div class="product-icon">🌽</div>
                <div class="product-title">Кукуруза фуражная</div>
                <div class="product-volume">Объем: 2 000 тонн</div>
                <div class="product-price">9 200 ₽/т</div>
                <div class="product-date">Поставка: 01.10.2025</div>
                <button class="btn-buy">Купить УЦП</button>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.plotly_chart(fig_sankey, use_container_width=True, key="sankey1")

    with tab5:
        st.markdown("### Мой портфель цифровых прав")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<div class="kpi-card"><div class="kpi-title">Инвестировано</div><div class="kpi-value">14.2 млн ₽</div><div class="kpi-delta">+5.2% к рынку</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="kpi-card"><div class="kpi-title">Ожидаемая доходность</div><div class="kpi-value">12.5%</div><div class="kpi-delta">годовых</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="kpi-card"><div class="kpi-title">Активных УЦП</div><div class="kpi-value">4</div><div class="kpi-delta">2 в поставке</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="kpi-card"><div class="kpi-title">Ближайшая поставка</div><div class="kpi-value">45 дней</div><div class="kpi-delta" style="color:#F4A261;">Пшеница 4 кл.</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1.5, 1])
        with col1:
            fig_timeline = px.timeline(df_gantt_buyer, x_start="Start", x_end="Finish", y="Task", color="Status",
                                       color_discrete_map={"В пути": "#2E86AB", "Ожидает производства": "#F4A261", "Доставлено": "#06A77D"})
            fig_timeline.update_yaxes(autorange="reversed")
            fig_timeline.update_layout(title="График будущих поставок", height=400, template=T, margin=dict(l=20, r=20, t=60, b=20))
            st.plotly_chart(fig_timeline, use_container_width=True, key="tl1")
        with col2:
            st.plotly_chart(fig_radar, use_container_width=True, key="radar1")

    with tab6:
        st.markdown("### ⚖️ Жизненный цикл УЦП по ФЗ № 282-ФЗ")
        st.markdown("В соответствии с новым законом «О цифровых валютах и цифровых правах» (вступает в силу с 01.09.2026), УЦП — это имущественное право требования передачи товара. Оно не является средством платежа (в отличие от ЦВ), а выпускается и учитывается в информационной системе Оператора (ОИС).")
        
        fig_lifecycle = go.Figure(data=[go.Sankey(
            node = dict(
              pad = 25, thickness = 30, line = dict(color = "black", width = 0.5),
              label = ["Эмитент (Продавец)", "Решение о выпуске УЦП", "ОИС (Оператор)", 
                       "Цифровой депозитарий", "Покупатель (Инвестор)", "Исполнение (Поставка товара)"],
              color = ["#2E86AB", "#F4A261", "#8E7DBE", "#06A77D", "#2E86AB", "#06A77D"]
            ),
            link = dict(
              source = [0, 0, 1, 2, 2, 4, 0], 
              target = [1, 2, 2, 3, 4, 5, 5],
              value = [10, 5, 10, 10, 5, 5, 5],
              color = ["rgba(46,134,171,0.3)", "rgba(46,134,171,0.3)", "rgba(244,162,97,0.3)", 
                       "rgba(142,125,190,0.3)", "rgba(142,125,190,0.3)", "rgba(46,134,171,0.3)", "rgba(6,167,125,0.3)"]
            )
        )])
        fig_lifecycle.update_layout(title="Схема движения прав: от Эмитента к Покупателю", height=450, template=T, margin=dict(l=20, r=20, t=60, b=20), font=dict(size=13))
        st.plotly_chart(fig_lifecycle, use_container_width=True, key="sankey_law")

        st.markdown("---")
        st.markdown("### 📊 Сравнение инструментов: УЦП vs ЦФА")
        
        df_compare = pd.DataFrame({
            "Характеристика": ["Суть инструмента", "Базовый актив", "Цель выпуска", "Может ли быть средством платежа?", "Где учитывается?"],
            "УЦП (Утилитарные права)": [
                "Право требовать передачи вещи, выполнения работ или услуг",
                "Реальные товары, сырье, услуги",
                "Финансирование производства, гарантия сбыта",
                "Нет (ст. 1 п. 6 282-ФЗ). Только имущественное право",
                "ОИС, Цифровой депозитарий (ст. 22)"
            ],
            "ЦФА (Цифровые финансы)": [
                "Денежные требования, права на акции (цифровые акции)",
                "Деньги, эмиссионные ценные бумаги",
                "Привлечение инвестиций, секьюритизация",
                "Нет (ст. 1 п. 6 282-ФЗ). Только имущественное право",
                "ОИС, Цифровой депозитарий (ст. 22)"
            ]
        })
        st.dataframe(df_compare, use_container_width=True, hide_index=True)
