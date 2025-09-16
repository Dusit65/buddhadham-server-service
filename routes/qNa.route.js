const express = require('express');
const qNaCtrl = require('../controllers/qNa.controller.js');
const router = express.Router();

// Route definitions
router.get("/:chatId", qNaCtrl.getqNaByChatId);
router.post("/ask", qNaCtrl.ask);
router.post("/answer", qNaCtrl.saveAnswer);
router.delete("/:qNaId", qNaCtrl.deleteqNa);

module.exports = router;