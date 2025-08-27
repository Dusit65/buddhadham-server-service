-- =========================
-- Trigger สำหรับ book_tb
-- =========================
CREATE OR ALTER TRIGGER trg_UpdateBook
ON book_tb
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE book_tb
    SET updatedAt = GETDATE()
    FROM book_tb b
    INNER JOIN inserted i ON b.bookId = i.bookId;
END;
GO

-- =========================
-- Trigger สำหรับ chapter_tb
-- =========================
CREATE OR ALTER TRIGGER trg_UpdateChapter
ON chapter_tb
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE chapter_tb
    SET updatedAt = GETDATE()
    FROM chapter_tb c
    INNER JOIN inserted i ON c.chapterId = i.chapterId;
END;
GO