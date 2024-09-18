CREATE OR REPLACE TABLE FPG.FIXTURES (
	FIXTURE_ID          INT,
	HOME_TEAM           VARCHAR(100),
	AWAY_TEAM           VARCHAR(100),
	KICKOFF             DATETIME,
	LOCATION            VARCHAR(100),
	ROUND               INT,
	SEASON              INT,
	DERBY               BOOLEAN
);