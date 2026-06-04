CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  device_timestamp TIMESTAMPTZ,

  device_id BIGINT NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload JSONB NOT NULL,

  qos SMALLINT,
  retain BOOLEAN DEFAULT FALSE,

  CONSTRAINT fk_device
    FOREIGN KEY(device_id)
    REFERENCES devices(id)
    ON DELETE CASCADE
);