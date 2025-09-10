"""
Database models for the honeypot attack map
"""

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any

DB_PATH = 'attacks.db'

class Attack:
    """Attack model for storing attack data"""
    
    def __init__(self, ip_address: str, port: int, protocol: str, 
                 country: str = 'Unknown', city: str = 'Unknown',
                 latitude: float = 0.0, longitude: float = 0.0,
                 timestamp: datetime = None, id: int = None):
        self.id = id
        self.ip_address = ip_address
        self.port = port
        self.protocol = protocol
        self.country = country
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp or datetime.now()
    
    def save(self):
        """Save attack to database"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO attacks (ip_address, port, protocol, country, city, 
                               latitude, longitude, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.ip_address, self.port, self.protocol, self.country,
              self.city, self.latitude, self.longitude, self.timestamp))
        
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()
    
    @classmethod
    def get_by_id(cls, attack_id: int) -> Optional['Attack']:
        """Get attack by ID"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM attacks WHERE id = ?', (attack_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(*row[1:], id=row[0])
        return None

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            port INTEGER NOT NULL,
            protocol TEXT NOT NULL,
            country TEXT DEFAULT 'Unknown',
            city TEXT DEFAULT 'Unknown',
            latitude REAL DEFAULT 0.0,
            longitude REAL DEFAULT 0.0,
            timestamp DATETIME NOT NULL
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ip_address ON attacks(ip_address)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON attacks(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_country ON attacks(country)')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def get_recent_attacks(limit: int = 100, country: str = None, 
                      protocol: str = None) -> List[Attack]:
    """Get recent attacks with optional filtering"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = 'SELECT * FROM attacks WHERE 1=1'
    params = []
    
    if country:
        query += ' AND country = ?'
        params.append(country)
    
    if protocol:
        query += ' AND protocol = ?'
        params.append(protocol)
    
    query += ' ORDER BY timestamp DESC LIMIT ?'
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [Attack(*row[1:], id=row[0]) for row in rows]

def get_attack_stats() -> Dict[str, Any]:
    """Get attack statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total attacks
    cursor.execute('SELECT COUNT(*) FROM attacks')
    total_attacks = cursor.fetchone()[0]
    
    # Attacks by country
    cursor.execute('''
        SELECT country, COUNT(*) as count 
        FROM attacks 
        GROUP BY country 
        ORDER BY count DESC 
        LIMIT 10
    ''')
    top_countries = cursor.fetchall()
    
    # Attacks by protocol
    cursor.execute('''
        SELECT protocol, COUNT(*) as count 
        FROM attacks 
        GROUP BY protocol 
        ORDER BY count DESC
    ''')
    protocol_stats = cursor.fetchall()
    
    # Recent attacks (last 24 hours)
    cursor.execute('''
        SELECT COUNT(*) FROM attacks 
        WHERE timestamp > datetime('now', '-1 day')
    ''')
    recent_attacks = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_attacks': total_attacks,
        'recent_attacks_24h': recent_attacks,
        'top_countries': [{'country': country, 'count': count} for country, count in top_countries],
        'protocol_stats': [{'protocol': protocol, 'count': count} for protocol, count in protocol_stats]
    }

def clear_old_attacks(days: int = 30):
    """Clear attacks older than specified days"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM attacks 
        WHERE timestamp < datetime('now', '-{} days')
    '''.format(days))
    
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"🗑️  Deleted {deleted_count} old attacks")
    return deleted_count
