DROP TABLE IF EXISTS test.documents;
CREATE TABLE test.documents
(
	id				INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
	date_created	DATETIME NOT NULL,
	date_searched	DATETIME NOT NULL,
	url				VARCHAR(255) NOT NULL,
	title			VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS test.contents;
CREATE TABLE test.contents
(
	id			INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
	group_id	INTEGER NOT NULL,
	group_id2	INTEGER NOT NULL,
	doc_id		INTEGER NOT NULL,
	paragraph	TEXT NOT NULL,
	tag			TEXT NOT NULL
);

DROP TABLE IF EXISTS test.config;
CREATE TABLE test.config
(
	id 				INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
	date_created	DATETIME NOT NULL,
	date_searched   DATETIME NOT NULL,
	top_path		varchar(255) NOT NULL,
	user_id			VARCHAR(30) NOT NULL
)

-- REPLACE INTO test.documents ( id, group_id, group_id2, date_added, title, content ) VALUES
-- 	( 1, 1, 5, NOW(), 'test one', 'this is my test document number one. also checking search within phrases.' ),
-- 	( 2, 1, 6, NOW(), 'test two', 'this is my test document number two' ),
-- 	( 3, 2, 7, NOW(), 'another doc', 'this is another group' ),
-- 	( 4, 2, 8, NOW(), 'doc number four', 'this is to test groups' );

-- DROP TABLE IF EXISTS test.tags;
-- CREATE TABLE test.tags
-- (
-- 	docid INTEGER NOT NULL,
-- 	tagid INTEGER NOT NULL,
-- 	UNIQUE(docid,tagid)
-- );

-- INSERT INTO test.tags VALUES
-- 	(1,1), (1,3), (1,5), (1,7),
-- 	(2,6), (2,4), (2,2),
-- 	(3,15),
-- 	(4,7), (4,40);
