DROP TABLE IF EXISTS air_data;
DROP TABLE IF EXISTS soil_data;
DROP TABLE IF EXISTS growth_snapshots;

CREATE TABLE air_data (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	air_temperature NUMERIC,
	air_humidity NUMERIC,
	timestamp DATETIME
);

CREATE TABLE soil_data (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	soil_temperature NUMERIC,
	soil_moisture NUMERIC,
	timestamp DATETIME
);

CREATE TABLE growth_snapshots (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	path INTEGER,
	timestamp DATETIME
);