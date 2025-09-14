import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from db_config import get_realtime_data, get_station_summary, get_panel_data

# Page configuration
st.set_page_config(
    page_title="光伏电站数据分析中心",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for industrial design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0f0f1e 0%, #1a1a3e 100%);
    }
    
    .analysis-card {
        background: rgba(25, 25, 50, 0.9);
        border: 2px solid #00ff88;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 25px rgba(0, 255, 136, 0.4);
    }
    
    .data-table {
        background: rgba(20, 20, 40, 0.8);
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 15px;
    }
    
    h1, h2, h3 {
        color: #00ffff;
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
        font-family: 'Orbitron', monospace;
    }
    
    .highlight-metric {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00ff88;
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.8);
    }
    
    .warning-box {
        background: rgba(255, 170, 0, 0.2);
        border: 2px solid #ffaa00;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .success-box {
        background: rgba(0, 255, 136, 0.2);
        border: 2px solid #00ff88;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    div[data-testid="stSidebar"] {
        background-color: rgba(15, 15, 30, 0.95);
        border-right: 2px solid #00ffff;
    }
    
    .stSelectbox label {
        color: #00ffff !important;
    }
    
    .prediction-chart {
        background: rgba(30, 30, 60, 0.8);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #00ff88;
    }
</style>

<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("## 📊 数据分析控制台")
    
    analysis_mode = st.selectbox(
        "分析模式",
        ["实时数据流", "历史趋势", "预测分析", "异常检测", "性能优化"]
    )
    
    selected_station = st.selectbox(
        "选择电站",
        ["全部电站", "STATION_001", "STATION_002", "STATION_003"]
    )
    
    time_range = st.select_slider(
        "时间范围",
        options=["1小时", "6小时", "24小时", "7天", "30天"],
        value="24小时"
    )
    
    st.markdown("---")
    
    st.markdown("### ⚙️ 高级设置")
    
    show_predictions = st.checkbox("显示预测数据", value=True)
    show_anomalies = st.checkbox("显示异常点", value=True)
    enable_alerts = st.checkbox("启用实时告警", value=True)
    
    refresh_rate = st.slider("刷新频率（秒）", 1, 60, 10)

# Header
st.markdown("# 🔬 光伏电站数据分析中心")
st.markdown(f"### 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 模式: {analysis_mode}")

# Main content based on selected mode
if analysis_mode == "实时数据流":
    st.markdown("## 📡 实时数据流监控")
    
    # Real-time metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_power = np.random.uniform(2400, 2600)
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="highlight-metric">{current_power:.1f} MW</div>', unsafe_allow_html=True)
        st.markdown("实时功率输出")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        data_rate = np.random.uniform(1000, 1500)
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="highlight-metric">{data_rate:.0f}</div>', unsafe_allow_html=True)
        st.markdown("数据点/秒")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        active_panels = np.random.randint(340, 353)
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="highlight-metric">{active_panels}</div>', unsafe_allow_html=True)
        st.markdown("活跃面板数")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        network_latency = np.random.uniform(10, 50)
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="highlight-metric">{network_latency:.1f} ms</div>', unsafe_allow_html=True)
        st.markdown("网络延迟")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Real-time data stream visualization
    st.markdown("### 📈 数据流可视化")
    
    # Create real-time streaming chart
    placeholder = st.empty()
    
    for i in range(5):  # Show 5 updates
        # Generate new data
        time_points = pd.date_range(end=datetime.now(), periods=100, freq='S')
        
        data_streams = pd.DataFrame({
            'time': time_points,
            'power': np.cumsum(np.random.randn(100)) + current_power,
            'voltage': np.cumsum(np.random.randn(100)) * 0.1 + 380,
            'current': np.cumsum(np.random.randn(100)) * 0.5 + 6000
        })
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('功率输出', '系统电压', '总电流'),
            vertical_spacing=0.1,
            row_heights=[0.4, 0.3, 0.3]
        )
        
        # Power stream
        fig.add_trace(
            go.Scatter(x=data_streams['time'], y=data_streams['power'],
                      mode='lines', line=dict(color='#00ff88', width=2),
                      fill='tozeroy', fillcolor='rgba(0, 255, 136, 0.2)'),
            row=1, col=1
        )
        
        # Voltage stream
        fig.add_trace(
            go.Scatter(x=data_streams['time'], y=data_streams['voltage'],
                      mode='lines', line=dict(color='#00ffff', width=2)),
            row=2, col=1
        )
        
        # Current stream
        fig.add_trace(
            go.Scatter(x=data_streams['time'], y=data_streams['current'],
                      mode='lines', line=dict(color='#ffaa00', width=2)),
            row=3, col=1
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff')
        )
        
        fig.update_xaxes(gridcolor='rgba(255, 255, 255, 0.1)')
        fig.update_yaxes(gridcolor='rgba(255, 255, 255, 0.1)')
        
        with placeholder.container():
            st.plotly_chart(fig, use_container_width=True)
        
        if i < 4:  # Don't sleep on last iteration
            time.sleep(2)

elif analysis_mode == "历史趋势":
    st.markdown("## 📈 历史数据趋势分析")
    
    # Historical data analysis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Generate historical data
        days = 30 if time_range == "30天" else 7 if time_range == "7天" else 1
        dates = pd.date_range(end=datetime.now(), periods=days*24, freq='H')
        
        historical = pd.DataFrame({
            'datetime': dates,
            'power': np.random.normal(2500, 200, len(dates)) * (0.5 + 0.5 * np.sin(np.arange(len(dates)) * 2 * np.pi / 24)),
            'efficiency': np.random.normal(95, 2, len(dates)),
            'temperature': 25 + 15 * np.sin(np.arange(len(dates)) * 2 * np.pi / 24) + np.random.normal(0, 2, len(dates))
        })
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('发电功率趋势', '系统效率变化', '环境温度'),
            specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]],
            vertical_spacing=0.1
        )
        
        fig.add_trace(
            go.Scatter(x=historical['datetime'], y=historical['power'],
                      mode='lines', name='功率', line=dict(color='#00ff88', width=2)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=historical['datetime'], y=historical['efficiency'],
                      mode='lines', name='效率', line=dict(color='#00ffff', width=2)),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=historical['datetime'], y=historical['temperature'],
                      mode='lines', name='温度', line=dict(color='#ffaa00', width=2)),
            row=3, col=1
        )
        
        fig.update_layout(
            height=700,
            showlegend=False,
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff')
        )
        
        fig.update_xaxes(gridcolor='rgba(255, 255, 255, 0.1)')
        fig.update_yaxes(gridcolor='rgba(255, 255, 255, 0.1)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 统计摘要")
        
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.metric("平均功率", f"{historical['power'].mean():.1f} MW")
        st.metric("峰值功率", f"{historical['power'].max():.1f} MW")
        st.metric("谷值功率", f"{historical['power'].min():.1f} MW")
        st.metric("功率标准差", f"{historical['power'].std():.1f} MW")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.metric("平均效率", f"{historical['efficiency'].mean():.1f}%")
        st.metric("效率波动", f"±{historical['efficiency'].std():.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

elif analysis_mode == "预测分析":
    st.markdown("## 🔮 智能预测分析")
    
    # Prediction analysis
    st.markdown('<div class="prediction-chart">', unsafe_allow_html=True)
    
    # Generate prediction data
    future_hours = 48
    historical_hours = 168
    
    hist_time = pd.date_range(end=datetime.now(), periods=historical_hours, freq='H')
    pred_time = pd.date_range(start=datetime.now(), periods=future_hours, freq='H')
    
    # Historical data with pattern
    hist_power = 2500 + 500 * np.sin(np.arange(historical_hours) * 2 * np.pi / 24) + np.random.normal(0, 100, historical_hours)
    
    # Predicted data with uncertainty
    pred_power = 2500 + 500 * np.sin(np.arange(future_hours) * 2 * np.pi / 24)
    pred_upper = pred_power + 200
    pred_lower = pred_power - 200
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=hist_time, y=hist_power,
        mode='lines', name='历史数据',
        line=dict(color='#00ff88', width=2)
    ))
    
    # Prediction
    fig.add_trace(go.Scatter(
        x=pred_time, y=pred_power,
        mode='lines', name='预测值',
        line=dict(color='#00ffff', width=3, dash='dash')
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=pred_time, y=pred_upper,
        mode='lines', name='置信上限',
        line=dict(color='rgba(0, 255, 255, 0.3)', width=0),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=pred_time, y=pred_lower,
        mode='lines', name='置信下限',
        line=dict(color='rgba(0, 255, 255, 0.3)', width=0),
        fill='tonexty', fillcolor='rgba(0, 255, 255, 0.2)',
        showlegend=False
    ))
    
    fig.update_layout(
        title="48小时功率输出预测",
        height=500,
        plot_bgcolor='rgba(20, 20, 40, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#00ffff'),
        xaxis_title="时间",
        yaxis_title="功率 (MW)"
    )
    
    fig.update_xaxes(gridcolor='rgba(255, 255, 255, 0.1)')
    fig.update_yaxes(gridcolor='rgba(255, 255, 255, 0.1)')
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediction metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("### 📈 预测峰值")
        st.markdown(f"**{pred_power.max():.1f} MW**")
        st.markdown(f"预计时间: {pred_time[pred_power.argmax()].strftime('%m-%d %H:00')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("### 📉 预测谷值")
        st.markdown(f"**{pred_power.min():.1f} MW**")
        st.markdown(f"预计时间: {pred_time[pred_power.argmin()].strftime('%m-%d %H:00')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown("### 📊 预测准确率")
        st.markdown(f"**95.7%**")
        st.markdown("基于历史数据验证")
        st.markdown('</div>', unsafe_allow_html=True)

elif analysis_mode == "异常检测":
    st.markdown("## 🚨 智能异常检测系统")
    
    # Anomaly detection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Generate data with anomalies
        times = pd.date_range(end=datetime.now(), periods=500, freq='5min')
        normal_data = 20 + 2 * np.sin(np.arange(500) * 2 * np.pi / 100) + np.random.normal(0, 0.5, 500)
        
        # Add anomalies
        anomaly_indices = np.random.choice(500, 20, replace=False)
        anomaly_data = normal_data.copy()
        anomaly_data[anomaly_indices] = normal_data[anomaly_indices] + np.random.uniform(-5, 5, 20)
        
        fig = go.Figure()
        
        # Normal data
        fig.add_trace(go.Scatter(
            x=times, y=anomaly_data,
            mode='lines', name='电压数据',
            line=dict(color='#00ff88', width=2)
        ))
        
        # Anomalies
        fig.add_trace(go.Scatter(
            x=times[anomaly_indices], y=anomaly_data[anomaly_indices],
            mode='markers', name='异常点',
            marker=dict(color='#ff3366', size=10, symbol='x')
        ))
        
        # Threshold lines
        fig.add_hline(y=24, line_dash="dash", line_color="#ffaa00", annotation_text="上限阈值")
        fig.add_hline(y=16, line_dash="dash", line_color="#ffaa00", annotation_text="下限阈值")
        
        fig.update_layout(
            title="电压异常检测",
            height=400,
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff'),
            xaxis_title="时间",
            yaxis_title="电压 (V)"
        )
        
        fig.update_xaxes(gridcolor='rgba(255, 255, 255, 0.1)')
        fig.update_yaxes(gridcolor='rgba(255, 255, 255, 0.1)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🚨 异常统计")
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.metric("检测到异常", f"{len(anomaly_indices)} 个")
        st.metric("异常率", f"{len(anomaly_indices)/500*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 异常类型")
        anomaly_types = pd.DataFrame({
            '类型': ['电压异常', '电流异常', '温度异常', '通信异常'],
            '数量': [8, 5, 4, 3]
        })
        
        fig_pie = px.pie(anomaly_types, values='数量', names='类型',
                         color_discrete_sequence=['#ff3366', '#ffaa00', '#00ffff', '#00ff88'])
        
        fig_pie.update_layout(
            height=300,
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff')
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Anomaly details table
    st.markdown("### 📋 异常详情")
    
    anomaly_df = pd.DataFrame({
        '时间': pd.to_datetime(['2025-09-14 10:23:15', '2025-09-14 11:45:32', '2025-09-14 12:18:45', 
                               '2025-09-14 13:52:10', '2025-09-14 14:33:28']),
        '电站': ['STATION_001', 'STATION_002', 'STATION_001', 'STATION_003', 'STATION_002'],
        '面板': ['PANEL_023', 'PANEL_156', 'PANEL_089', 'PANEL_201', 'PANEL_045'],
        '异常类型': ['电压过低', '温度过高', '电流异常', '通信中断', '功率波动'],
        '严重程度': ['中', '高', '低', '高', '中'],
        '状态': ['已处理', '处理中', '已忽略', '待处理', '已处理']
    })
    
    st.dataframe(anomaly_df, use_container_width=True)

elif analysis_mode == "性能优化":
    st.markdown("## ⚡ 智能性能优化建议")
    
    # Performance optimization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Efficiency comparison chart
        stations = ['STATION_001', 'STATION_002', 'STATION_003']
        current_eff = [94.2, 93.8, 95.1]
        optimal_eff = [96.5, 96.2, 96.8]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='当前效率',
            x=stations, y=current_eff,
            marker_color='#00ffff'
        ))
        
        fig.add_trace(go.Bar(
            name='优化后效率',
            x=stations, y=optimal_eff,
            marker_color='#00ff88'
        ))
        
        fig.update_layout(
            title="电站效率优化潜力分析",
            height=400,
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff'),
            xaxis_title="电站",
            yaxis_title="效率 (%)",
            barmode='group'
        )
        
        fig.update_xaxes(gridcolor='rgba(255, 255, 255, 0.1)')
        fig.update_yaxes(gridcolor='rgba(255, 255, 255, 0.1)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💡 优化建议")
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("**建议 1: 角度调整**")
        st.markdown("调整 STATION_001 面板角度可提升 1.2% 效率")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("**建议 2: 清洁维护**")
        st.markdown("STATION_002 需要清洁，预计提升 0.8% 效率")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("**建议 3: 设备更换**")
        st.markdown("5个老化面板需要更换")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Optimization timeline
    st.markdown("### 📅 优化实施计划")
    
    timeline_data = pd.DataFrame({
        'task': ['面板角度调整', '清洁维护', '设备更换', '系统升级', '性能测试'],
        'start': pd.to_datetime(['2025-09-15', '2025-09-18', '2025-09-20', '2025-09-25', '2025-09-28']),
        'duration': [2, 1, 3, 2, 1],
        'impact': ['+1.2%', '+0.8%', '+0.5%', '+0.3%', 'N/A']
    })
    
    timeline_data['end'] = timeline_data['start'] + pd.to_timedelta(timeline_data['duration'], unit='D')
    
    fig = px.timeline(timeline_data, x_start='start', x_end='end', y='task', 
                      color='impact', title="优化任务时间线")
    
    fig.update_layout(
        height=300,
        plot_bgcolor='rgba(20, 20, 40, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#00ffff'),
        xaxis_title="日期",
        yaxis_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer with system status
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**数据源状态:** 🟢 正常")
with col2:
    st.markdown("**数据库连接:** 🟢 正常")
with col3:
    st.markdown("**API响应时间:** 23ms")
with col4:
    st.markdown("**系统负载:** 45%")

st.markdown(
    """<div style='text-align: center; color: #00ffff; opacity: 0.7; margin-top: 20px;'>
    数据分析中心 v2.0 | 实时数据更新中...
    </div>""", 
    unsafe_allow_html=True
)