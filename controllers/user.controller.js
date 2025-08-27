
// ไฟล์ที่เขียนการดำเนินการควบคุมสำหรับตารางในฐานข้อมูล
//เช่น insert, update, delete, select
//ไฟล์นี้ทำงานกับ user_tb
const multer = require("multer");
const path = require("path");
const fs = require("fs");

//ใช้ Prisma เพื่อทำงานร่วมกับ DB
const { PrismaClient } = require("@prisma/client"); //Models
const prisma = new PrismaClient();

// สร้างผู้ใช้งานใหม่ 
exports.createUser = async (req, res) => {
  try {
    const result = await prisma.user_tb.create({
      data: {

        userName: req.body.userName,
        userEmail: req.body.userEmail,
        userPassword: req.body.userPassword,
      },
    });
    res.status(201).json({
      message: "User created successfully",
      data: result,
    });
  } catch (error) {
    res.status(500).json({
      message: error.message,
    });
  }
};

// ตรวจสอบการเข้าสู่ระบบ 
exports.checkLoginUser = async (req, res) => {
  try {
    const { userEmail, userPassword } = req.body;

    // ตรวจสอบว่าข้อมูลครบไหม
    if (!userEmail || !userPassword) {
      return res.status(400).json({
        message: "userEmail and userPassword are required.",
      });
    }

    // ค้นหาผู้ใช้
    const result = await prisma.user_tb.findFirst({
      where: {
        userEmail,
        userPassword
      },
    });

    if (result) {
      res.status(200).json({
        message: "User login successfully OvO",
        data: {
          userId: result.userId,
          userName: result.userName,
          userEmail: result.userEmail
        }
      });
    } else {
      res.status(404).json({
        message: "User login failed TwT",
      });
    }
  } catch (error) {
    res.status(500).json({
      message: error.message,
    });
  }
};


