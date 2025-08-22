//File that writes control operations for a table in the database
//เช่น insert, update, delete, select
//This file works with user_tb
const multer = require("multer");
const path = require("path");
const fs = require("fs");

//Use prisma to co working with DB
const { PrismaClient } = require("@prisma/client"); //Models
const prisma = new PrismaClient();


//++++++++++++++++++++++++++++++ End of Require +++++++++++++++++++++++++++++++++

//+++++++++++++++++++++++++ INSERT UPDATE DELETE FUNC ++++++++++++++++++++++++++++++++++++

// Func Insert User ===============================
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



// Func Check Login User ===============================================
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
        userName,
        userEmail
      },
    });

    if (result) {
      res.status(200).json({
        message: "User login successfully OvO",
        data: result,
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


