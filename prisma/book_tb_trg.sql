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