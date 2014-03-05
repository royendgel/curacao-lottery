-- Royendgel Silberie @ 2014-03-04 [YYYY-MM-DD]
-- DATABASE : Lottery skeleton 
-- SOURCE   : SQLITE 3


-- Drawings number table
DROP TABLE IF EXISTS [Drawing];
CREATE TABLE [Drawing]
(      [DrawingID] INTEGER PRIMARY KEY AUTOINCREMENT,
       [Date] varchar(10),
       [Position] INTEGER,
       [Drawing] varchar(4)
);