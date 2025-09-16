const express = require('express');
const qNaCtrl = require('../controllers/qNa.controller.js');
const router = express.Router();

// Route definitions
router.get("/:chatId", qNaCtrl.getqNaByChatId);
router.post("/ask", qNaCtrl.ask);
router.post("/answer", qNaCtrl.saveAnswer);
router.post("/cancel/:taskId", qNaCtrl.cancel);
router.post("/status/:taskId", qNaCtrl.checkStatus);
router.delete("/:qNaId", qNaCtrl.deleteqNa);

module.exports = router;