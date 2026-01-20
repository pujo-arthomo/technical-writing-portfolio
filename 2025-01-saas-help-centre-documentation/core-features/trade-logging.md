# Trade Logging Explained

Trade logging is the core function of the product.

Each logged trade represents a single completed trading action.

## What Is Stored
- Instrument name
- Entry and exit values
- Trade direction
- Timestamp

## What Is Not Stored
- Broker execution details
- External market data
- Live price feeds

This design keeps the journal focused on user-entered data and reflection.
