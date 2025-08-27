-- ไม่ต้องเพิ่มId เพราะคุณตั้งค่า id เป็น auto-increment
INSERT INTO user_tb (userName, userEmail, userPassword)
VALUES 
('dusit65', 'dusit65@mail.com', '111'),
('user1', 'user1@mail.com', '111'),
('mew', 'mew@mail.com', '222');

INSERT INTO book_tb (bookName, createdAt, updatedAt)
VALUES (N'พุทธรรม 1', GETDATE(), GETDATE());

INSERT INTO chapter_tb (bookId, chapterName, chapterText, createdAt, updatedAt)
VALUES 
(1, N'chapter 1', N'พระพุทธเจ้าทรงตรัสรู้ใต้ต้นโพธิ์ หลังจากตรากตรำบำเพ็ญเพียรอย่างยาวนานถึง 6 ปี โดยทรงมีความตั้งใจแน่วแน่ที่จะค้นหาหนทางแห่งความดับทุกข์ พระองค์ได้ตระหนักถึงความจริงของชีวิตที่เรียกว่า ‘ทุกข์’ และทรงค้นพบคำตอบว่าการดับทุกข์นั้นเป็นไปได้จริง อริยสัจ 4 คือคำสอนที่พระพุทธเจ้าทรงแสดงหลังตรัสรู้ ซึ่งเป็นแก่นของพระพุทธศาสนา ประกอบด้วย ทุกข์ (ความทุกข์ที่มีในชีวิต) สมุทัย (สาเหตุของทุกข์) นิโรธ (การดับทุกข์) และมรรค (หนทางแห่งการดับทุกข์)', GETDATE(), GETDATE()),

(1, N'chapter 2', N'ทุกข์ หมายถึงความไม่สบายใจ ความไม่สมหวังในชีวิต ตั้งแต่ความเจ็บป่วย ความแก่ ความตาย และความพลัดพรากจากสิ่งที่รัก ทุกข์มีทั้งแบบชัดเจนและแบบแอบแฝงซึ่งเรามักไม่ทันรู้ตัว สมุทัย คือเหตุแห่งทุกข์ โดยเฉพาะอย่างยิ่งตัณหา ความอยาก ความยึดมั่นถือมั่นในสิ่งต่างๆ ซึ่งเป็นต้นเหตุที่ทำให้เกิดความทุกข์ซ้ำๆ ไม่มีที่สิ้นสุด', GETDATE(), GETDATE()),

(1, N'chapter 3', N'test', GETDATE(), GETDATE());

INSERT INTO chat_tb (userId, chatHeader, createdAt)
VALUES 
(1, N'ทุกข์', GETDATE()),
(2, N'สมุทัย', GETDATE()),
(1, N'นิโรธ', GETDATE()),
(1, N'มรรค', GETDATE());

INSERT INTO chat_tb (userId, chatHeader, createdAt)
VALUES 
(1, N'ทุกข์', GETDATE()),
(2, N'สมุทัย', GETDATE()),
(1, N'นิโรธ', GETDATE()),
(1, N'มรรค', GETDATE());

