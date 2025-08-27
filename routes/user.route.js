//ไฟล์นี้ใช้สำหรับจัดการการกำหนดเส้นทางสำหรับการเรียกใช้บริการ/API
//ไฟล์นี้ทำงานกับ user_tb

//เรียก express เพื่อใช้ router module
const express = require("express");
const userCtrl = require("./../controllers/user.controller.js");
const router = express.Router();

//Routing is based on RESTful API principles
//GET = ค้นหา ตรวจสอบ ดึง ดู, POST = เพิ่ม, PUT = แก้ไข, DELETE = ลบ

router.post("/",userCtrl.createUser);
router.post("/login", userCtrl.checkLoginUser);

//export router เพื่อเรียกใข้งาน
module.exports = router;