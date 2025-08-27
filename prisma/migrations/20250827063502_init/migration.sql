BEGIN TRY

BEGIN TRAN;

-- CreateTable
CREATE TABLE [dbo].[user_tb] (
    [userId] INT NOT NULL IDENTITY(1,1),
    [userName] VARCHAR(100) NOT NULL,
    [userEmail] VARCHAR(50) NOT NULL,
    [userPassword] VARCHAR(50) NOT NULL,
    [createdAt] DATETIME2 NOT NULL CONSTRAINT [user_tb_createdAt_df] DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT [user_tb_pkey] PRIMARY KEY CLUSTERED ([userId])
);

-- CreateTable
CREATE TABLE [dbo].[chat_tb] (
    [chatId] INT NOT NULL IDENTITY(1,1),
    [userId] INT NOT NULL,
    [chatHeader] NVARCHAR(50) NOT NULL,
    [createdAt] DATETIME2 NOT NULL CONSTRAINT [chat_tb_createdAt_df] DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT [chat_tb_pkey] PRIMARY KEY CLUSTERED ([chatId])
);

-- CreateTable
CREATE TABLE [dbo].[qNa_tb] (
    [qNaId] INT NOT NULL IDENTITY(1,1),
    [chatId] INT NOT NULL,
    [qNaWords] NVARCHAR(max) NOT NULL,
    [qNaType] CHAR(1) NOT NULL,
    [createdAt] DATETIME2 NOT NULL CONSTRAINT [qNa_tb_createdAt_df] DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT [qNa_tb_pkey] PRIMARY KEY CLUSTERED ([qNaId])
);

-- CreateTable
CREATE TABLE [dbo].[book_tb] (
    [bookId] INT NOT NULL IDENTITY(1,1),
    [bookName] NVARCHAR(max) NOT NULL,
    [createdAt] DATETIME2 NOT NULL CONSTRAINT [book_tb_createdAt_df] DEFAULT CURRENT_TIMESTAMP,
    [updatedAt] DATETIME2 NOT NULL CONSTRAINT [book_tb_updatedAt_df] DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT [book_tb_pkey] PRIMARY KEY CLUSTERED ([bookId])
);

-- CreateTable
CREATE TABLE [dbo].[chapter_tb] (
    [chapterId] INT NOT NULL IDENTITY(1,1),
    [bookId] INT NOT NULL,
    [chapterName] NVARCHAR(50) NOT NULL,
    [chapterText] NVARCHAR(max) NOT NULL,
    [createdAt] DATETIME2 NOT NULL CONSTRAINT [chapter_tb_createdAt_df] DEFAULT CURRENT_TIMESTAMP,
    [updatedAt] DATETIME2 NOT NULL CONSTRAINT [chapter_tb_updatedAt_df] DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT [chapter_tb_pkey] PRIMARY KEY CLUSTERED ([chapterId])
);

-- CreateTable
CREATE TABLE [dbo].[embeddings_tb] (
    [id] INT NOT NULL IDENTITY(1,1),
    [embeddings] VARBINARY(max) NOT NULL,
    [metadata] VARBINARY(max) NOT NULL,
    [updatedAt] DATETIME2 NOT NULL CONSTRAINT [embeddings_tb_updatedAt_df] DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT [embeddings_tb_pkey] PRIMARY KEY CLUSTERED ([id])
);

-- CreateTable
CREATE TABLE [dbo].[log_tb] (
    [id] INT NOT NULL IDENTITY(1,1),
    [createdAt] DATETIME2 NOT NULL CONSTRAINT [log_tb_createdAt_df] DEFAULT CURRENT_TIMESTAMP,
    [message] NVARCHAR(max) NOT NULL,
    CONSTRAINT [log_tb_pkey] PRIMARY KEY CLUSTERED ([id])
);

-- AddForeignKey
ALTER TABLE [dbo].[chat_tb] ADD CONSTRAINT [chat_tb_userId_fkey] FOREIGN KEY ([userId]) REFERENCES [dbo].[user_tb]([userId]) ON DELETE NO ACTION ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE [dbo].[qNa_tb] ADD CONSTRAINT [qNa_tb_chatId_fkey] FOREIGN KEY ([chatId]) REFERENCES [dbo].[chat_tb]([chatId]) ON DELETE NO ACTION ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE [dbo].[chapter_tb] ADD CONSTRAINT [chapter_tb_bookId_fkey] FOREIGN KEY ([bookId]) REFERENCES [dbo].[book_tb]([bookId]) ON DELETE NO ACTION ON UPDATE CASCADE;

COMMIT TRAN;

END TRY
BEGIN CATCH

IF @@TRANCOUNT > 0
BEGIN
    ROLLBACK TRAN;
END;
THROW

END CATCH
