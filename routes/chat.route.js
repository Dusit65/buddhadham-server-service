const express = require('express');
const chatCtrl = require('../controllers/chat.controller.js');
const router = express.Router();

// Route definitions
router.post("/", chatCtrl.createChat);
router.put("/:chatId", chatCtrl.editChat);
router.get("/all/:userId", chatCtrl.getChatsByUserId);  // Ensure `getAllchat` is a function in the controller
router.get("/one/:chatId", chatCtrl.getChat);  // Ensure `getchat` is a function in the controller
router.get("/all", chatCtrl.getAllChats); // Ensure `getAllchat` is a function in the controller
router.delete("/:chatId", chatCtrl.deleteChat); // Ensure `deletechat` is a function in the controller

module.exports = router;