//This file is used to manage routing for service/API calls
//This file works with user_tb

//call express to use router module
const express = require("express");
const userCtrl = require("./../controllers/user.controller.js");
const router = express.Router();

//Routing is based on RESTful API principles
//GET = ค้นหา ตรวจสอบ ดึง ดู, POST = เพิ่ม, PUT = แก้ไข, DELETE = ลบ

router.post("/",userCtrl.createUser);
router.get("/:userEmail/:userPassword", userCtrl.checkLoginUser);

//export router for call to use
module.exports = router;