const express = require("express"); // call express module to create web server
require("dotenv").config(); // call to use .env

const cors = require("cors");
const userRoute = require("./routes/user.route"); // call to use router module


//++++++++++++++++++ CREATE WEB SERVER +++++++++++++++++++

const app = express(); // create web server
//Default is port 5000
const PORT = process.env.PORT || 5000;

//Use middleware to various management++++++++++++++++++++++
app.use(cors());//allow access from any domain
app.use(express.json());

//++++++++++++66++++ APP USE +++++++++++++++++++++++++++++++

//use router module=================
app.use("/user", userRoute); 



//++++++++++++++++ test call web server +++++++++++++++++++
app.get("/", (req, res) => {
  res.json({ message: "Hello from server port " + PORT + " by prisma" }); //send message
});

//++++++++create web server connection from client/user++++++++++++
app.listen(PORT, () => {
  console.log("Server is running on port " + PORT);
});