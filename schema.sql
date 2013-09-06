-- Copyright 2009 FriendFeed
--
-- Licensed under the Apache License, Version 2.0 (the "License"); you may
-- not use this file except in compliance with the License. You may obtain
-- a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
-- WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
-- License for the specific language governing permissions and limitations
-- under the License.

-- To create the database:
--   CREATE DATABASE blog;
--   GRANT ALL PRIVILEGES ON blog.* TO 'blog'@'localhost' IDENTIFIED BY 'blog';
--
-- To reload the tables:
--   mysql --user=blog --password=blog --database=blog < schema.sql

SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    author_id INT NOT NULL REFERENCES authors(id),
    slug VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(512) NOT NULL,
    markdown MEDIUMTEXT NOT NULL,
    html MEDIUMTEXT NOT NULL,
    published DATETIME NOT NULL,
    updated TIMESTAMP NOT NULL,
    KEY (published)
);

DROP TABLE IF EXISTS authors;
CREATE TABLE authors (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
	password VARCHAR(18) NOT NULL,
	isadmin int
);
DROP TABLE IF EXISTS maps;
CREATE TABLE maps (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	mkey VARCHAR(20) NOT NULL UNIQUE,
	mvalue VARCHAR(20) NOT NULL
);
insert into maps (mkey,mvalue) values ("registe","on");
DROP TABLE IF EXISTS member;
CREATE TABLE member (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	weixinid VARCHAR(20) NOT NULL UNIQUE,
	employeeid VARCHAR(20) ,
	name VARCHAR(20),
	password VARCHAR(20),
	state int,
	realName VARCHAR(20)
);
DROP TABLE EXISTS content;
CREATE TABLE content (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	type int,
	sort int,
	title VARCHAR(512) ,
	description VARCHAR(512),
	picurl VARCHAR(512),
	url VARCHAR(512),
	content MEDIUMTEXT
);


