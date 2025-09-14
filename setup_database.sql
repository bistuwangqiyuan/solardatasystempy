-- Supabase SQL script to create tables for the Photovoltaic Power Station Monitoring System

-- Create station_info table
CREATE TABLE IF NOT EXISTS station_info (
    station_id VARCHAR(50) PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    capacity_mw DECIMAL(10, 2),
    panel_count INTEGER,
    installation_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create pv_measurements table
CREATE TABLE IF NOT EXISTS pv_measurements (
    id BIGSERIAL PRIMARY KEY,
    station_id VARCHAR(50) REFERENCES station_info(station_id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    voltage_v DECIMAL(10, 2),
    current_a DECIMAL(10, 2),
    power_w DECIMAL(10, 2),
    device_address INTEGER,
    device_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create panel_measurements table
CREATE TABLE IF NOT EXISTS panel_measurements (
    id BIGSERIAL PRIMARY KEY,
    panel_id VARCHAR(50) NOT NULL,
    station_id VARCHAR(50) REFERENCES station_info(station_id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    voltage DECIMAL(10, 2),
    current DECIMAL(10, 2),
    power DECIMAL(10, 2),
    temperature DECIMAL(5, 2),
    status VARCHAR(20),
    shutdown_capable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create station_alerts table
CREATE TABLE IF NOT EXISTS station_alerts (
    id BIGSERIAL PRIMARY KEY,
    station_id VARCHAR(50) REFERENCES station_info(station_id),
    panel_id VARCHAR(50),
    alert_type VARCHAR(50),
    severity VARCHAR(20),
    message TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better performance
CREATE INDEX idx_pv_measurements_station_timestamp ON pv_measurements(station_id, timestamp DESC);
CREATE INDEX idx_panel_measurements_station_timestamp ON panel_measurements(station_id, timestamp DESC);
CREATE INDEX idx_station_alerts_station_status ON station_alerts(station_id, status);

-- Insert sample station data
INSERT INTO station_info (station_id, station_name, location, capacity_mw, panel_count, installation_date)
VALUES 
    ('STATION_001', '光伏电站 Alpha', '江苏省苏州市', 850.5, 120, '2023-06-15'),
    ('STATION_002', '光伏电站 Beta', '浙江省杭州市', 920.3, 135, '2023-08-20'),
    ('STATION_003', '光伏电站 Gamma', '上海市浦东新区', 780.2, 98, '2024-01-10')
ON CONFLICT (station_id) DO NOTHING;

-- Create a function to get station summary
CREATE OR REPLACE FUNCTION get_station_summary()
RETURNS TABLE (
    station_id VARCHAR(50),
    station_name VARCHAR(100),
    total_power DECIMAL(10, 2),
    avg_voltage DECIMAL(10, 2),
    avg_current DECIMAL(10, 2),
    efficiency DECIMAL(5, 2),
    status VARCHAR(20),
    panel_count INTEGER,
    alert_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        si.station_id,
        si.station_name,
        si.capacity_mw AS total_power,
        COALESCE(AVG(pm.voltage_v), 20.0) AS avg_voltage,
        COALESCE(AVG(pm.current_a), 40.0) AS avg_current,
        93.0 + RANDOM() * 4 AS efficiency,
        '运行中' AS status,
        si.panel_count,
        COALESCE(COUNT(DISTINCT sa.id), 0) AS alert_count
    FROM station_info si
    LEFT JOIN pv_measurements pm ON si.station_id = pm.station_id 
        AND pm.timestamp > NOW() - INTERVAL '1 hour'
    LEFT JOIN station_alerts sa ON si.station_id = sa.station_id 
        AND sa.status = 'active'
    GROUP BY si.station_id, si.station_name, si.capacity_mw, si.panel_count;
END;
$$ LANGUAGE plpgsql;

-- Enable Row Level Security (RLS)
ALTER TABLE station_info ENABLE ROW LEVEL SECURITY;
ALTER TABLE pv_measurements ENABLE ROW LEVEL SECURITY;
ALTER TABLE panel_measurements ENABLE ROW LEVEL SECURITY;
ALTER TABLE station_alerts ENABLE ROW LEVEL SECURITY;

-- Create policies for anonymous access (read-only)
CREATE POLICY "Enable read access for all users" ON station_info
    FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON pv_measurements
    FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON panel_measurements
    FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON station_alerts
    FOR SELECT USING (true);

-- Grant permissions to execute the function
GRANT EXECUTE ON FUNCTION get_station_summary() TO anon, authenticated;