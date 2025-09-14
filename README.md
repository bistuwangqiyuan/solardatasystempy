# 光伏电站智能监控系统 (Photovoltaic Power Station Monitoring System)

一个高端的分布式光伏电站监控和管理系统，具有工业化设计风格和实时数据可视化功能。

## 🌟 系统特点

- **实时监控**: 实时显示各电站的发电功率、效率、状态等关键指标
- **分布式架构**: 支持多个光伏电站的集中监控和管理
- **面板级控制**: 每个发电板都具有独立的电压/电流监测和远程关断能力
- **智能分析**: 包含历史趋势分析、预测分析、异常检测和性能优化建议
- **工业化UI**: 采用深色主题和霓虹效果，营造高科技工业感
- **数据持久化**: 使用Supabase作为后端数据库，无需搭建传统后端

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 现代Web浏览器（推荐Chrome/Edge）

### 安装步骤

1. 克隆项目到本地：
```bash
git clone <repository-url>
cd photovoltaic-power-station-monitoring
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
   - 项目已包含 `.env` 文件，其中包含了Supabase连接信息
   - 如需使用自己的Supabase实例，请修改 `.env` 文件中的配置

4. 运行主监控系统：
```bash
streamlit run app.py
```

5. 运行辅助分析系统（可选）：
```bash
streamlit run auxiliary_dashboard.py
```

## 📊 系统架构

### 主要组件

1. **app.py** - 主监控大屏
   - 实时监控仪表板
   - 电站详细信息
   - 数据分析
   - 设备控制面板

2. **auxiliary_dashboard.py** - 数据分析中心
   - 实时数据流
   - 历史趋势分析
   - 预测分析
   - 异常检测
   - 性能优化建议

3. **db_config.py** - 数据库配置和数据访问层
   - Supabase连接管理
   - 数据查询接口
   - 示例数据生成

### 数据结构

系统使用以下主要数据表：
- `pv_measurements` - 光伏测量数据
- `panel_measurements` - 面板级详细数据
- `station_summary` - 电站汇总信息

## 🎨 界面预览

系统采用深色工业风格设计，主要特点：
- 深蓝/黑色背景配合霓虹蓝绿色调
- 实时动态数据更新
- 响应式布局适配不同屏幕
- 丰富的可视化图表

## 📝 使用说明

### 主监控系统

1. **实时监控**: 查看所有电站的实时状态和关键指标
2. **电站详情**: 深入查看特定电站的面板分布和状态
3. **数据分析**: 查看功率分布、电压-电流关系等分析图表
4. **设备控制**: 远程控制面板开关，设置告警阈值

### 数据分析中心

1. **实时数据流**: 监控实时数据流和网络状态
2. **历史趋势**: 分析历史数据趋势和统计信息
3. **预测分析**: 基于AI的发电量预测
4. **异常检测**: 自动检测和报告系统异常
5. **性能优化**: 智能优化建议和实施计划

## 🔧 配置说明

### 环境变量

在 `.env` 文件中配置：
- `PUBLIC_SUPABASE_URL`: Supabase项目URL
- `PUBLIC_SUPABASE_ANON_KEY`: Supabase匿名密钥
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase服务角色密钥

### 自定义设置

可以通过修改以下文件进行自定义：
- 修改 `app.py` 中的样式定义来改变UI外观
- 调整 `db_config.py` 中的数据生成逻辑
- 在侧边栏中调整刷新频率和其他参数

## 📦 技术栈

- **前端框架**: Streamlit
- **可视化库**: Plotly, Altair
- **数据处理**: Pandas, NumPy
- **数据库**: Supabase (PostgreSQL)
- **样式**: 自定义CSS + Google Fonts

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进系统功能。

## 📄 许可证

本项目采用MIT许可证。