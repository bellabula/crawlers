/* create table */
CREATE TABLE sailors (
    sname VARCHAR(15) PRIMARY KEY,
    rating INT
);


CREATE TABLE boats (
    bname VARCHAR(15),
    color VARCHAR(10),
    rating INT,
    PRIMARY KEY(bname)
);


CREATE TABLE days (
    day VARCHAR(15) PRIMARY KEY
);


CREATE TABLE reservations (
    sname VARCHAR(15) NOT NULL, -- 不可以空白
    bname VARCHAR(15),
    day VARCHAR(15),
    PRIMARY Key(sname, bname, day),
    FOREIGN KEY(sname) REFERENCES sailors(sname),
    FOREIGN KEY(bname) REFERENCES boats(bname),
    FOREIGN KEY(day) REFERENCES days(day)
);



/* delet table */
DROP TABLE reservations;
DROP TABLE sailors, boats, days;


/* add data */
INSERT INTO sailors VALUES ('Brutus', 1);
INSERT INTO sailors VALUES ('Andy', 8);
INSERT INTO sailors VALUES ('Horatio', 7);
INSERT INTO sailors VALUES ('Rusty', 8);
INSERT INTO sailors VALUES ('Bob', 1);

INSERT INTO boats VALUES ('SpeedQueen', 'white', 9);
INSERT INTO boats VALUES ('Interlake', 'red', 8);
INSERT INTO boats VALUES ('Marine', 'blue', 7);
INSERT INTO boats VALUES ('Bay', 'red', 3);

INSERT INTO days VALUES ('Monday');
INSERT INTO days VALUES ('Tuesday');
INSERT INTO days VALUES ('Wednesday');
INSERT INTO days VALUES ('Thursday');
INSERT INTO days VALUES ('Friday');
INSERT INTO days VALUES ('Saturday');
INSERT INTO days VALUES ('Sunday');

INSERT INTO reservations VALUES('Andy', 'Interlake', 'Monday');
INSERT INTO reservations VALUES('Andy', 'Bay', 'Wednesday');
INSERT INTO reservations VALUES('Andy', 'Marine', 'Saturday');
INSERT INTO reservations VALUES('Rusty', 'Bay', 'Sunday');
INSERT INTO reservations VALUES('Rusty', 'Interlake', 'Wednesday');
INSERT INTO reservations VALUES('Rusty', 'Marine', 'Wednesday');
INSERT INTO reservations VALUES('Bob', 'Bay', 'Monday');


/* Query */

-- SELECT [DISTINCT只取一個] select-list
-- FROM from-list
-- WHERE qualification


SELECT * FROM sailors;

SELECT *
FROM sailors
WHERE rating >5;


SELECT COUNT(*)
FROM sailors;

SELECT COUNT(rating)
FROM sailors;

SELECT SUM(rating)
FROM boats;

-- SELECT AVG()/MAX()/MIN()

SELECT color, COUNT(*)
FROM boats
GROUP BY color;

SELECT *
FROM sailors
ORDER BY rating;

SELECT *
FROM sailors
ORDER BY rating DESC;


/* 1. 列出所有在星期三預約的傳 跟它們的顏色 */

SELECT b.bname, b.color
FROM boats b, reservations r -- 不給下面條件的話, 就是把兩個table結合 4*7=28 rows
WHERE b.bname=r.bname AND r.day='Wednesday';

/* 2. 列出最高評分的水手 */

--nested/sub query
SELECT s.sname
FROM sailors s
WHERE s.rating = (
    SELECT MAX(rating)
    FROM sailors);

/* 不用 MAX. */
SELECT s.sname
FROM sailors s
WHERE NOT EXISTS
    (SELECT s2.sname
    FROM sailors s2
    WHERE s2.rating > s.rating);


/* 3. 列出所有同一天預約船的水手名字, 避免重複 */

SELECT DISTINCT r1.sname, r2.sname
FROM reservations r1, reservations r2
WHERE r1.day = r2.day AND r1.sname != r2.sname;


/* 4. 每一天，列出那天預約紅色船的數量。
如果那天沒紅色船被預約，數字應該是0，如果那一天完全沒有出現在預約表格裡，
那天數字也應該要是0。 */

SELECT d.day, sub.num
FROM days d LEFT OUTER JOIN (
    SELECT r.day,COUNT(*) AS num 
    FROM boats b, reservations r 
    WHERE b.bname=r.bname AND b.color='red' GROUP BY r.day) AS sub
ON d.day = sub.day;

/* 5. 列出只有紅船被預約的那些天 */

SELECT DISTINCT r.day
FROM reservations r, boats b
WHERE b.color = 'red' AND b.bname = r.bname AND NOT EXISTS (
    SELECT r1.day
    FROM reservations r1, boats b1
    WHERE b1.color != 'red' AND r1.bname = b1.bname AND r1.day = r.day
);


/* 6. 列出沒有紅船預約的天。如果那天沒出現在預約表格裡，也應該是0。 */
SELECT d.day
FROM days d
WHERE NOT EXISTS (
    SELECT r.day
    FROM reservations r, boats b
    WHERE b.color = 'red' AND r.bname = b.bname AND r.day = d.day
);


/* 7. 列出全部紅船都被預約的天，如果不存在紅船，那每天都該吻合。 */ 

SELECT sub.day
FROM (
    SELECT r.day, COUNT(*) AS rcount
    FROM reservations r, boats b
    WHERE b.color = 'red' AND r.bname = b.bname
    GROUP BY r.day) sub
WHERE sub.rcount = (
    SELECT COUNT(*) AS rcount
    FROM boats
    WHERE color = 'red'
);


/* – 使用 NOT IN */
SELECT d1.day 
FROM days d1
WHERE d1.day NOT IN ( 
    SELECT d2.day
    FROM  days d2, boats b
    WHERE b.color = 'red' AND b.bname NOT IN (
            SELECT c.bname
            FROM boats c, reservations r
            WHERE r.day = d2.day AND  c.bname = r.bname
        )
);


/* 使用 NOT EXISTS */
SELECT d.day
FROM days d
WHERE NOT EXISTS (
    SELECT *
    FROM  boats b
    WHERE b.color = 'red' AND NOT EXISTS (
            SELECT *
            FROM reservations r
            WHERE r.day = d.day AND b.bname = r.bname
        )
);

/* 通過使用EXISTS，Oracle會首先檢查主查詢，然後執行子查詢直到它找到第一個匹配項，這就節省了時間。
Oracle在執行IN子查詢時，首先執行子查詢，並將獲得的結果列表存放在一個加了索引的臨時表中。
在執行子查詢之前，系統先將主查詢掛起，待子查詢執行完畢，存放在臨時表中以後再執行主查詢。
這也就是使用EXISTS比使用IN通常查詢速度快的原因 */
SELECT * 
FROM boats b WHERE EXISTS (
    select 1
    from reservations r
    where b.bname=r.bname);
-- T1資料量小而T2資料量非常大時，T1<<T2 時，1) 的查詢效率高。

/* 如果只執行括號裡的語句，是會語法錯誤，這也是使用exists需要注意的地方。
"exists（xxx）"就表示括號裡的語句能不能查出記錄，它要查的記錄是否存在。
因此"select *"這裡的 "1"其實是無關緊要的，換成"*"也沒問題
它只在乎括號裡的資料能不能查找出來，是否存在這樣的記錄
如果存在，這句的 where 條件成立。 */

/* EXISTS(包括 NOT EXISTS )子句的返回值是一個BOOL值。
EXISTS內部有一個子查詢語句(SELECT ... FROM...)， 我將其稱為EXIST的內查詢語句。
其內查詢語句返回一個結果集。 
EXISTS子句根據其內查詢語句的結果集空或者非空，返回一個布林值。 */

/* 一種通俗的可以理解為：將外查詢表的每一行，代入內查詢作為檢驗，如果內查詢返回的結果取非空值，
則EXISTS子句返回TRUE，這一行行可作為外查詢的結果行，否則不能作為結果。 */

SELECT *
FROM boats b
WHERE b.bname in (
    SELECT r.bname
    FROM reservations r
);
-- T1資料量非常大而T2資料量小時，T1>>T2 時，2) 的查詢效率高。

/* EXISTS與IN的使用效率的問題，通常情況下采用exists要比in效率高，
因為IN不走索引，但要看實際情況具體使用：
IN適合於外表大而內表小的情況；EXISTS適合於外表小而內表大的情況。 */


/* 8. 針對出現在預約表裡的天，列出那天所有水手的平均分數。
(小心重複的項目) */

SELECT sub.day, AVG(sub.rat) AS 'avg-rating'
FROM (
    SELECT DISTINCT r.day, s.sname, s.rating AS rat
    FROM reservations r, sailors s
    WHERE r.sname = s.sname) sub
GROUP BY sub.day;


/* 9. 列出最忙的一天，也就是最多預約的一天 */

SELECT sub1.day
FROM (
    SELECT day, COUNT(*) AS rcount
    FROM reservations
    GROUP BY day
    ) sub1
WHERE sub1.rcount = (
    SELECT MAX(rcount)
    FROM (
        SELECT COUNT(*) AS rcount
        FROM reservations
        GROUP BY day
        ) sub2
);