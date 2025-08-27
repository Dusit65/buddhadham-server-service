CREATE TRIGGER trg_UpdateChapter
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