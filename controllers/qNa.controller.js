const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();
const { execFile } = require("child_process");
const path = require("path");
const axios = require("axios");

// ถาม
exports.ask = async (req, res) => {
  try {
    const { chatId, question, k, d } = req.body;

    if (!question) {
      return res.status(400).json({ message: "Question is required." });
    }

    // ส่ง request ไปที่ main.py API
    const response = await axios.post("http://58.136.35.83:8000/ask", {
      args: [question, ...(k != null ? ["-k", k.toString()] : []), ...(d != null ? ["-d", d.toString()] : [])]
    });

    const data = response.data;
    console.log("Answer:", data);
    // บันทึก Q/A ลง database
    const savedRecordQuestion = await prisma.qNa_tb.create({
      data: { chatId, qNaWords: question, qNaType: "Q" },
    });
    const savedRecordAnswer = await prisma.qNa_tb.create({
      data: { chatId, qNaWords: data.data.answer, qNaType: "A" },
    });

    return res.status(201).json({
      message: "Question and Answer saved successfully",
      data: { savedRecordQuestion, savedRecordAnswer },
      answer: data.data.answer,
      references: data.data.references,
      rejected: data.data.rejected,
      duration: data.data.duration,
    });

  } catch (error) {
    console.error("Unexpected error:", error);
    res.status(500).json({ message: "Unexpected error: " + error.message, stack: error.stack });
  }
};
exports.saveAnswer = async (req, res) => {
  try {
    const { taskId, chatId, qNaWords } = req.body;

    if (!taskId) {
      return res.status(400).json({ message: "taskId is required." });
    }

    if (!chatId) {
      return res.status(400).json({ message: "chatId is required." });
    }

    if (!qNaWords) {
      return res.status(400).json({ message: "qNaWords is required." });
    }

    // บันทึกคำตอบ AI ลง qNa_tb
    const savedAnswer = await prisma.qNa_tb.create({
      data: {
        chatId: chatId,
        taskId: taskId,
        qNaWords: qNaWords,
        qNaType: "A", // A = Answer
      },
    });

    console.log("Saved AI answer:", savedAnswer);
    return res.status(201).json({ message: "AI answer saved", data: savedAnswer });

  } catch (err) {
    console.error("Error saving AI answer:", err);
    return res.status(500).json({ message: "Internal server error", error: err.message });
  }
};

exports.cancel = async (req, res) => {
  const { taskId } = req.params;

  if (!taskId) {
    return res.status(400).json({ message: "taskId is required" });
  }

  try {
    // ส่ง request ไป main.py
    const response = await axios.post("http://" + process.env.AI_SERVER + ":" + process.env.AI_SERVER_PORT + "/cancel/" + taskId);

    // ส่งผลกลับ client
    return res.status(200).json({
      message: "Cancel request sent",
      taskId,
      response: response.data,
    });

  } catch (error) {
    console.error("Error cancelling job:", error.message);
    return res.status(500).json({
      message: "Failed to cancel job",
      error: error.message,
    });
  }
};
// ดึงข้อความแชททั้งหมด
exports.getAllqNa = async (req, res) => {
  try {
    const chats = await prisma.qNa_tb.findMany(); // ดึงข้อมูลทั้งหมดโดยไม่มีการกรอง
    res.status(200).json({ message: "All chats found", data: chats });
  } catch (error) {
    console.error("Error fetching chats: ", error);
    res.status(500).json({ message: "Error: " + error.message });
  }
};

// ดึงข้อความแชทของ user
exports.getqNaByChatId = async (req, res) => {
  try {
    const chats = await prisma.qNa_tb.findMany({
      where: {chatId: Number(req.params.chatId)
       },
      orderBy: { createdAt: "asc" },
    });
    res.status(200).json({ message: "ดึงข้อความแชทของผู้ใช้สำเร็จ", data: chats });
  } catch (error) {
    console.error("Error fetching chats by user: ", error);
    res.status(500).json({ message: "Error: " + error.message });
  }
};

// ดึงข้อความแชทเฉพาะข้อความเดียว
exports.getqNa = async (req, res) => {
  try {
    const chat = await prisma.qNa_tb.findUnique({
      where: { chatId: Number(req.params.chatId) },
      include: {
        user: {
          select: {
            userName: true,
            
          },
        },
      },
    });

    if (!chat) {
      return res.status(404).json({ message: "ข้อความแชทไม่พบ" });
    }

    res.status(200).json({
      message: "ข้อความแชทพบ",
      data: { chat, user: chat.user },
    });
  } catch (error) {
    console.error("Error fetching chat: ", error);
    res.status(500).json({ message: "Error: " + error.message });
  }
};

// ลบข้อความแชท
exports.deleteqNa = async (req, res) => {
  try {
    const chat = await prisma.qNa_tb.findUnique({
      where: { qNaId: Number(req.params.qNaId) },
    });

    if (!chat) {
      return res.status(404).json({ message: "ไม่พบ qNaID:" + req.params.qNaId });
    }

    const deletedqNa = await prisma.qNa_tb.delete({
      where: { qNaId: Number(req.params.qNaId) },
    });

    res.status(200).json({
      message: "ลบข้อความแชทสำเร็จ",
      data: deletedqNa,
    });
  } catch (error) {
    console.error("Error deleting qNa: ", error);
    res.status(500).json({ message: "Error: " + error.message });
  }
};