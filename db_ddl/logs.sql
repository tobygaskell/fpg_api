CREATE OR REPLACE TABLE FPG.LOGS (
	TIME_ADDED            DATETIME,
	ROUND                 INT,
	RESULTS_PULLED        BOOLEAN,
	SCORES_UPDATED        BOOLEAN,
	NEXT_ROUND_INIT       BOOLEAN
);