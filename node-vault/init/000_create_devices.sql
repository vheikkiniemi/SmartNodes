CREATE TABLE devices (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    device_uid VARCHAR(50) UNIQUE NOT NULL,
    device_name VARCHAR(50) UNIQUE NOT NULL,
    ip_address INET,
    location VARCHAR(100),
    last_seen TIMESTAMPTZ
);