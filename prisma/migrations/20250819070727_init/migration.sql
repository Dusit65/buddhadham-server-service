-- CreateTable
CREATE TABLE `user_tb` (
    `userId` INTEGER NOT NULL AUTO_INCREMENT,
    `userName` VARCHAR(100) NOT NULL,
    `userEmail` VARCHAR(50) NOT NULL,
    `userPassword` VARCHAR(50) NOT NULL,
    `createAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`userId`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `chat_tb` (
    `chatId` INTEGER NOT NULL AUTO_INCREMENT,
    `userId` INTEGER NOT NULL,
    `chatHeader` VARCHAR(50) NOT NULL,
    `createAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`chatId`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `qNa_tb` (
    `qNaId` INTEGER NOT NULL AUTO_INCREMENT,
    `chatId` INTEGER NOT NULL,
    `qNaWords` TEXT NOT NULL,
    `qNaType` VARCHAR(9) NOT NULL,

    PRIMARY KEY (`qNaId`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `book_tb` (
    `bookId` INTEGER NOT NULL AUTO_INCREMENT,
    `bookName` TEXT NOT NULL,

    PRIMARY KEY (`bookId`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `chapter_tb` (
    `chapterId` INTEGER NOT NULL AUTO_INCREMENT,
    `bookId` INTEGER NOT NULL,
    `chapterName` VARCHAR(50) NOT NULL,
    `chapterText` TEXT NOT NULL,

    PRIMARY KEY (`chapterId`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `chat_tb` ADD CONSTRAINT `chat_tb_userId_fkey` FOREIGN KEY (`userId`) REFERENCES `user_tb`(`userId`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `qNa_tb` ADD CONSTRAINT `qNa_tb_chatId_fkey` FOREIGN KEY (`chatId`) REFERENCES `chat_tb`(`chatId`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `chapter_tb` ADD CONSTRAINT `chapter_tb_bookId_fkey` FOREIGN KEY (`bookId`) REFERENCES `book_tb`(`bookId`) ON DELETE RESTRICT ON UPDATE CASCADE;
