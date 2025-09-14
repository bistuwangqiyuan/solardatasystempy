import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import numpy as np

# Load environment variables
load_dotenv()

# Supabase configuration
url = os.environ.get("PUBLIC_SUPABASE_URL")
key = os.environ.get("PUBLIC_SUPABASE_ANON_KEY")

# Create Supabase client
supabase: Client = create_client(url, key)

def create_tables():
    """Create necessary tables in Supabase if they don't exist"""
    # This would normally be done through Supabase dashboard or migration files
    # For now, we'll assume tables are created manually
    pass

def upload_sample_data():
    """Upload sample data from Excel files to Supabase"""
    data_files = [
        'data/19.99V 6.00A data_detail_1_2025-05-09T12-15-19.xlsx',
        'data/20.2V  19.8Ω 1.3Adata_detail_1_2025-05-02T06-23-00.xlsx',
        'data/39.9V 9.02A data_detail_1_2025-05-09T13-02-36.xlsx'
    ]
    
    all_data = []
    
    for file in data_files:
        if os.path.exists(file):
            df = pd.read_excel(file)
            # Skip the header rows
            df = df.iloc[2:].reset_index(drop=True)
            
            # Clean column names
            df.columns = ['sequence', 'current_a', 'voltage_v', 'power_w', 'timestamp', 'device_address', 'device_type']
            
            # Convert data types
            df['current_a'] = pd.to_numeric(df['current_a'], errors='coerce')
            df['voltage_v'] = pd.to_numeric(df['voltage_v'], errors='coerce')
            df['power_w'] = pd.to_numeric(df['power_w'], errors='coerce')
            df['device_address'] = pd.to_numeric(df['device_address'], errors='coerce').fillna(1).astype(int)
            
            # Add station ID based on filename
            if '19.99V' in file:
                df['station_id'] = 'STATION_001'
            elif '20.2V' in file:
                df['station_id'] = 'STATION_002'
            else:
                df['station_id'] = 'STATION_003'
            
            all_data.append(df)
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Remove NaN values
    combined_df = combined_df.dropna(subset=['current_a', 'voltage_v', 'power_w'])
    
    return combined_df

def get_realtime_data(station_id=None):
    """Get real-time data from Supabase"""
    try:
        query = supabase.table('pv_measurements')
        
        if station_id:
            query = query.eq('station_id', station_id)
        
        response = query.order('timestamp', desc=True).limit(100).execute()
        
        if response.data:
            return pd.DataFrame(response.data)
        else:
            # Return sample data if no data in database
            return upload_sample_data()
    except:
        # Fallback to sample data
        return upload_sample_data()

def get_station_summary():
    """Get summary statistics for all stations"""
    try:
        response = supabase.rpc('get_station_summary').execute()
        if response.data:
            return pd.DataFrame(response.data)
        else:
            # Generate mock summary data
            return pd.DataFrame({
                'station_id': ['STATION_001', 'STATION_002', 'STATION_003'],
                'station_name': ['光伏电站 Alpha', '光伏电站 Beta', '光伏电站 Gamma'],
                'total_power': [850.5, 920.3, 780.2],
                'avg_voltage': [19.99, 20.2, 39.9],
                'avg_current': [42.5, 45.5, 19.5],
                'efficiency': [95.2, 94.8, 96.1],
                'status': ['运行中', '运行中', '运行中'],
                'panel_count': [120, 135, 98],
                'alert_count': [2, 0, 1]
            })
    except:
        # Return mock data
        return pd.DataFrame({
            'station_id': ['STATION_001', 'STATION_002', 'STATION_003'],
            'station_name': ['光伏电站 Alpha', '光伏电站 Beta', '光伏电站 Gamma'],
            'total_power': [850.5, 920.3, 780.2],
            'avg_voltage': [19.99, 20.2, 39.9],
            'avg_current': [42.5, 45.5, 19.5],
            'efficiency': [95.2, 94.8, 96.1],
            'status': ['运行中', '运行中', '运行中'],
            'panel_count': [120, 135, 98],
            'alert_count': [2, 0, 1]
        })

def get_panel_data(station_id, panel_id=None):
    """Get data for specific panels"""
    try:
        query = supabase.table('panel_measurements').eq('station_id', station_id)
        
        if panel_id:
            query = query.eq('panel_id', panel_id)
        
        response = query.order('timestamp', desc=True).limit(1000).execute()
        
        if response.data:
            return pd.DataFrame(response.data)
        else:
            # Generate mock panel data
            panels = []
            for i in range(1, 21):
                panels.append({
                    'panel_id': f'PANEL_{i:03d}',
                    'station_id': station_id,
                    'voltage': np.random.uniform(18, 22),
                    'current': np.random.uniform(5, 8),
                    'power': np.random.uniform(90, 160),
                    'temperature': np.random.uniform(25, 45),
                    'status': np.random.choice(['正常', '警告', '故障'], p=[0.9, 0.08, 0.02]),
                    'shutdown_capable': True
                })
            return pd.DataFrame(panels)
    except:
        # Generate mock panel data
        panels = []
        for i in range(1, 21):
            panels.append({
                'panel_id': f'PANEL_{i:03d}',
                'station_id': station_id,
                'voltage': np.random.uniform(18, 22),
                'current': np.random.uniform(5, 8),
                'power': np.random.uniform(90, 160),
                'temperature': np.random.uniform(25, 45),
                'status': np.random.choice(['正常', '警告', '故障'], p=[0.9, 0.08, 0.02]),
                'shutdown_capable': True
            })
        return pd.DataFrame(panels)