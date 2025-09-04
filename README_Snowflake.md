# 🚀 Snowflake Ad-Hoc Connector

A secure Python connector for Snowflake that automatically handles rotating private keys through your SRE API system.

## 🔐 Security Features

- **Rotating Private Keys**: Automatically fetches new private keys every 24 hours
- **Secure Key Storage**: Private keys are stored in memory only and cleaned up automatically
- **API-Based Authentication**: Uses your SRE API for secure credential management
- **No Static Credentials**: Eliminates the need for hardcoded database credentials

## 📋 Prerequisites

- Python 3.7+
- Access to your SRE API endpoint
- Valid API key
- Snowflake ad-hoc user account

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_snowflake.txt
```

### 2. Basic Usage

```python
from snowflake_connector import SnowflakeAdHocConnector

# Initialize connector
connector = SnowflakeAdHocConnector()

# Connect to Snowflake
connector.connect(
    env='prod',  # or 'stage'
    username='TRACKING_ADHOC_SSH_USER',
    account='your_account',
    warehouse='your_warehouse',
    database='your_database',
    schema='your_schema'
)

# Execute queries
result = connector.execute_query("SELECT CURRENT_TIMESTAMP()")
print(result)

# Close connection
connector.close()
```

### 3. Using Context Manager (Recommended)

```python
with SnowflakeAdHocConnector() as connector:
    connector.connect(
        env='prod',
        username='TRACKING_ADHOC_SSH_USER',
        account='your_account',
        warehouse='your_warehouse',
        database='your_database',
        schema='your_schema'
    )
    
    # Your Snowflake operations here
    result = connector.execute_query("SHOW TABLES")
    print(result)
```

## ⚙️ Configuration

### Environment Variables (Optional)

You can set these environment variables to avoid hardcoding:

```bash
export SNOWFLAKE_API_KEY="1hjzMhVkLMhNxOu"
export SNOWFLAKE_API_URL="https://sre-snowflake-role-api.prod.joveo.com"
```

### Connection Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `env` | Environment: 'prod' or 'stage' | Yes |
| `username` | Your ad-hoc username | Yes |
| `account` | Snowflake account identifier | Yes |
| `warehouse` | Snowflake warehouse name | Yes |
| `database` | Snowflake database name | Yes |
| `schema` | Snowflake schema name | Yes |
| `role` | Snowflake role name | No |

## 🔧 API Endpoints

The connector uses your SRE API:

- **Base URL**: `https://sre-snowflake-role-api.prod.joveo.com`
- **Endpoint**: `/snowflake/private_key/{env}/{username}`
- **Method**: GET
- **Auth**: X-API-Key header

## 📊 Example Queries

### Basic Queries

```python
# Get current user info
result = connector.execute_query("SELECT CURRENT_USER(), CURRENT_ACCOUNT()")

# Show available objects
databases = connector.execute_query("SHOW DATABASES")
warehouses = connector.execute_query("SHOW WAREHOUSES")
tables = connector.execute_query("SHOW TABLES")
```

### Parameterized Queries

```python
# Query with parameters
result = connector.execute_query(
    "SELECT * FROM your_table WHERE created_date > %s LIMIT 10",
    ('2024-01-01',)
)
```

### Complex Analytics

```python
query = """
    SELECT 
        DATE_TRUNC('day', created_date) as date,
        COUNT(*) as record_count,
        SUM(amount) as total_amount
    FROM your_table 
    WHERE created_date >= DATEADD(day, -30, CURRENT_DATE())
    GROUP BY DATE_TRUNC('day', created_date)
    ORDER BY date DESC
"""

result = connector.execute_query(query)
```

## 🛡️ Security Best Practices

1. **Never hardcode credentials** in your scripts
2. **Use environment variables** for sensitive configuration
3. **Rotate API keys** regularly
4. **Monitor API usage** for unusual patterns
5. **Use least privilege** - only grant necessary permissions to ad-hoc users

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check your API key
   - Verify username and environment
   - Ensure ad-hoc user is active

2. **Connection Timeout**
   - Check network connectivity
   - Verify Snowflake account URL
   - Check firewall settings

3. **Permission Denied**
   - Verify user has access to specified warehouse/database/schema
   - Check role permissions
   - Contact your Snowflake admin

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📁 File Structure

```
├── snowflake_connector.py      # Main connector class
├── example_usage.py            # Usage examples
├── requirements_snowflake.txt  # Dependencies
└── README_Snowflake.md        # This file
```

## 🔄 Key Rotation

The connector automatically handles key rotation:

- **Cache Duration**: 23 hours (slightly less than 24-hour rotation)
- **Automatic Refresh**: Keys are fetched when expired
- **Seamless Operation**: No interruption during key rotation

## 📞 Support

For issues related to:
- **API Access**: Contact your SRE team
- **Snowflake Permissions**: Contact your Snowflake admin
- **Connector Issues**: Check the troubleshooting section above

## 📝 License

This connector is designed for internal use with your Snowflake infrastructure.

---

**⚠️ Important**: Always test connections in a staging environment before using in production!
