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
    page_title="光伏电站智能监控系统",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for industrial design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    .metric-card {
        background: rgba(20, 20, 40, 0.8);
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .station-card {
        background: linear-gradient(135deg, rgba(30, 30, 50, 0.9) 0%, rgba(20, 20, 40, 0.9) 100%);
        border: 2px solid #00ff88;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.4);
        transition: all 0.3s ease;
    }
    
    .station-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 40px rgba(0, 255, 136, 0.6);
    }
    
    h1, h2, h3 {
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        font-family: 'Orbitron', monospace;
    }
    
    .big-metric {
        font-size: 3rem;
        font-weight: bold;
        color: #00ff88;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.8);
        font-family: 'Digital', monospace;
    }
    
    .status-online {
        color: #00ff88;
        animation: pulse 2s infinite;
    }
    
    .status-warning {
        color: #ffaa00;
        animation: pulse 1s infinite;
    }
    
    .status-offline {
        color: #ff3366;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .industrial-button {
        background: linear-gradient(135deg, #00ff88 0%, #00ffff 100%);
        color: #0a0a0a;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .industrial-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
    }
    
    div[data-testid="metric-container"] {
        background-color: rgba(20, 20, 40, 0.8);
        border: 1px solid #00ffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #00ff88;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.6);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(20, 20, 40, 0.6);
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #00ffff;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 255, 255, 0.2);
    }
</style>

<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Initialize session state
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 5

# Header
col1, col2, col3 = st.columns([2, 3, 2])
with col1:
    st.markdown("### 🌟 新能源监控中心")
with col2:
    st.markdown(f"# 光伏电站智能监控系统")
with col3:
    st.markdown(f"### 🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Auto-refresh toggle
with st.sidebar:
    st.markdown("## ⚙️ 控制面板")
    st.session_state.auto_refresh = st.checkbox("自动刷新", value=st.session_state.auto_refresh)
    if st.session_state.auto_refresh:
        st.session_state.refresh_interval = st.slider("刷新间隔（秒）", 1, 30, 5)

# Get data
station_summary = get_station_summary()
total_stations = len(station_summary)
total_power = station_summary['total_power'].sum()
total_panels = station_summary['panel_count'].sum()
total_alerts = station_summary['alert_count'].sum()
avg_efficiency = station_summary['efficiency'].mean()

# Main metrics
st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("电站总数", f"{total_stations} 座", delta="+2 本月新增")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("总发电功率", f"{total_power:.1f} MW", delta=f"+{total_power*0.05:.1f} MW")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("光伏板总数", f"{total_panels:,} 块", delta="+150 本月新增")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("平均效率", f"{avg_efficiency:.1f}%", delta="+2.3%")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    alert_color = "🟢" if total_alerts == 0 else "🟡" if total_alerts < 5 else "🔴"
    st.metric("告警数量", f"{alert_color} {total_alerts}", delta="-3 较昨日")
    st.markdown('</div>', unsafe_allow_html=True)

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 实时监控", "🏭 电站详情", "📈 数据分析", "🔧 设备控制"])

with tab1:
    # Real-time monitoring dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Power generation trend
        st.markdown("### 📈 24小时发电功率趋势")
        
        # Generate time series data
        hours = pd.date_range(end=datetime.now(), periods=24, freq='H')
        power_data = pd.DataFrame({
            'time': hours,
            'power': np.random.normal(total_power, total_power*0.1, 24)
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=power_data['time'],
            y=power_data['power'],
            mode='lines+markers',
            name='发电功率',
            line=dict(color='#00ff88', width=3),
            marker=dict(size=8, color='#00ffff'),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 136, 0.2)'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff'),
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
            yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', title='功率 (MW)'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Efficiency gauge
        st.markdown("### 🎯 系统效率")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_efficiency,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "系统效率 (%)"},
            delta={'reference': 93},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#00ff88"},
                'steps': [
                    {'range': [0, 60], 'color': "rgba(255, 51, 102, 0.3)"},
                    {'range': [60, 80], 'color': "rgba(255, 170, 0, 0.3)"},
                    {'range': [80, 100], 'color': "rgba(0, 255, 136, 0.3)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff', size=16),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Station cards
    st.markdown("### 🏭 电站实时状态")
    
    cols = st.columns(3)
    for idx, (_, station) in enumerate(station_summary.iterrows()):
        with cols[idx % 3]:
            status_class = "status-online" if station['status'] == '运行中' else "status-warning"
            st.markdown(f"""
            <div class="station-card">
                <h3>{station['station_name']}</h3>
                <p class="{status_class}">● {station['status']}</p>
                <div class="big-metric">{station['total_power']:.1f} MW</div>
                <p>电压: {station['avg_voltage']:.1f}V | 电流: {station['avg_current']:.1f}A</p>
                <p>效率: {station['efficiency']:.1f}% | 板块: {station['panel_count']}块</p>
                <p>告警: <span style="color: {'#00ff88' if station['alert_count'] == 0 else '#ffaa00'}">
                    {station['alert_count']}个</span></p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    # Station details
    st.markdown("### 🏭 电站详细信息")
    
    selected_station = st.selectbox(
        "选择电站",
        options=station_summary['station_id'].tolist(),
        format_func=lambda x: station_summary[station_summary['station_id'] == x]['station_name'].iloc[0]
    )
    
    # Get panel data for selected station
    panel_data = get_panel_data(selected_station)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Panel status heatmap
        st.markdown("#### 光伏板状态热力图")
        
        # Create grid data for heatmap
        grid_size = int(np.sqrt(len(panel_data)))
        grid_data = panel_data['power'].values[:grid_size**2].reshape(grid_size, grid_size)
        
        fig = go.Figure(data=go.Heatmap(
            z=grid_data,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="功率 (W)")
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff'),
            height=500,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Panel statistics
        st.markdown("#### 面板统计")
        normal_panels = len(panel_data[panel_data['status'] == '正常'])
        warning_panels = len(panel_data[panel_data['status'] == '警告'])
        fault_panels = len(panel_data[panel_data['status'] == '故障'])
        
        fig = go.Figure(data=[go.Pie(
            labels=['正常', '警告', '故障'],
            values=[normal_panels, warning_panels, fault_panels],
            hole=.3,
            marker_colors=['#00ff88', '#ffaa00', '#ff3366']
        )])
        
        fig.update_layout(
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff'),
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("平均温度", f"{panel_data['temperature'].mean():.1f}°C")
        st.metric("总功率输出", f"{panel_data['power'].sum()/1000:.2f} kW")

with tab3:
    # Data analysis
    st.markdown("### 📊 数据分析中心")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Power distribution
        st.markdown("#### 功率分布分析")
        
        fig = px.histogram(
            panel_data, 
            x='power', 
            nbins=30,
            title="光伏板功率分布",
            color_discrete_sequence=['#00ff88']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff'),
            xaxis_title="功率 (W)",
            yaxis_title="数量"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Voltage vs Current scatter
        st.markdown("#### 电压-电流关系")
        
        sample_data = get_realtime_data()
        
        fig = px.scatter(
            sample_data.head(100), 
            x='voltage_v', 
            y='current_a',
            size='power_w',
            title="电压-电流散点图",
            color_discrete_sequence=['#00ffff']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(20, 20, 40, 0.8)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#00ffff'),
            xaxis_title="电压 (V)",
            yaxis_title="电流 (A)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Time series analysis
    st.markdown("#### 历史数据趋势")
    
    # Create sample time series
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    historical_data = pd.DataFrame({
        'date': dates,
        'daily_energy': np.random.normal(5000, 500, 30),
        'peak_power': np.random.normal(1000, 100, 30),
        'avg_efficiency': np.random.normal(95, 2, 30)
    })
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('日发电量 (kWh)', '峰值功率 (MW)', '平均效率 (%)'),
        vertical_spacing=0.1
    )
    
    fig.add_trace(
        go.Scatter(x=historical_data['date'], y=historical_data['daily_energy'],
                   mode='lines+markers', line=dict(color='#00ff88', width=2)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=historical_data['date'], y=historical_data['peak_power'],
                   mode='lines+markers', line=dict(color='#00ffff', width=2)),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=historical_data['date'], y=historical_data['avg_efficiency'],
                   mode='lines+markers', line=dict(color='#ffaa00', width=2)),
        row=3, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=False,
        plot_bgcolor='rgba(20, 20, 40, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#00ffff')
    )
    
    fig.update_xaxes(gridcolor='rgba(255, 255, 255, 0.1)')
    fig.update_yaxes(gridcolor='rgba(255, 255, 255, 0.1)')
    
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    # Equipment control
    st.markdown("### 🔧 设备控制面板")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### 快速控制")
        
        if st.button("🔄 系统重启", use_container_width=True):
            st.warning("系统重启需要管理员权限")
        
        if st.button("⚡ 紧急停机", use_container_width=True):
            st.error("紧急停机程序已启动")
        
        if st.button("🔧 维护模式", use_container_width=True):
            st.info("进入维护模式")
        
        st.markdown("#### 告警设置")
        
        low_voltage = st.number_input("低电压告警阈值 (V)", value=18.0, step=0.1)
        high_temp = st.number_input("高温告警阈值 (°C)", value=60.0, step=1.0)
        low_efficiency = st.number_input("低效率告警阈值 (%)", value=85.0, step=1.0)
    
    with col2:
        st.markdown("#### 面板控制")
        
        # Panel control interface
        selected_panel = st.selectbox(
            "选择面板",
            options=panel_data['panel_id'].tolist()
        )
        
        panel_info = panel_data[panel_data['panel_id'] == selected_panel].iloc[0]
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("当前电压", f"{panel_info['voltage']:.2f} V")
        with col_b:
            st.metric("当前电流", f"{panel_info['current']:.2f} A")
        with col_c:
            st.metric("输出功率", f"{panel_info['power']:.2f} W")
        
        st.markdown("---")
        
        col_1, col_2 = st.columns(2)
        
        with col_1:
            if panel_info['shutdown_capable']:
                if st.button(f"关断 {selected_panel}", type="primary", use_container_width=True):
                    st.success(f"{selected_panel} 已关断")
            else:
                st.button("该面板不支持远程关断", disabled=True, use_container_width=True)
        
        with col_2:
            if st.button(f"重置 {selected_panel}", use_container_width=True):
                st.success(f"{selected_panel} 已重置")
        
        # System logs
        st.markdown("#### 系统日志")
        
        log_data = pd.DataFrame({
            'timestamp': pd.date_range(end=datetime.now(), periods=10, freq='min'),
            'event': [
                '系统启动完成',
                'STATION_001 连接成功',
                'PANEL_015 温度告警',
                '自动优化算法启动',
                'STATION_002 数据同步',
                'PANEL_015 告警解除',
                '系统效率优化 +1.2%',
                'STATION_003 维护检查',
                '数据备份完成',
                '系统运行正常'
            ],
            'level': ['INFO', 'INFO', 'WARNING', 'INFO', 'INFO', 'INFO', 'SUCCESS', 'INFO', 'INFO', 'SUCCESS']
        })
        
        for _, log in log_data.iterrows():
            level_color = {'INFO': '#00ffff', 'WARNING': '#ffaa00', 'SUCCESS': '#00ff88', 'ERROR': '#ff3366'}
            st.markdown(
                f"""<div style="color: {level_color.get(log['level'], '#ffffff')}; 
                    padding: 5px; margin: 2px 0; 
                    border-left: 3px solid {level_color.get(log['level'], '#ffffff')};">
                    [{log['timestamp'].strftime('%H:%M:%S')}] {log['event']}</div>""", 
                unsafe_allow_html=True
            )

# Auto-refresh
if st.session_state.auto_refresh:
    time.sleep(st.session_state.refresh_interval)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """<div style='text-align: center; color: #00ffff; opacity: 0.7;'>
    光伏电站智能监控系统 v2.0 | © 2025 新能源科技有限公司
    </div>""", 
    unsafe_allow_html=True
)
