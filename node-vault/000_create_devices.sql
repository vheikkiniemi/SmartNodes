-- Enable pgcrypto extension (run once per database)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE devices (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    device_uid UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    device_name VARCHAR(50) UNIQUE NOT NULL,
    api_key UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    role VARCHAR(20),
    ip_address INET,
    location VARCHAR(100),
    last_seen TIMESTAMPTZ,
    
    -- connection tracking
    is_connected BOOLEAN NOT NULL DEFAULT FALSE,
    disconnected_at TIMESTAMPTZ
);