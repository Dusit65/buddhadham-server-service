const express = require("express"); // call express module to create web server
require("dotenv").config(); // call to use .env

const cors = require("cors");
const userRoute = require("./routes/user.route"); // call to use router module
const chatRoutes = require("./routes/chat.route.js");
const qNaRoutes = require("./routes/qNa.route.js");

//++++++++++++++++++ CREATE WEB SERVER +++++++++++++++++++

const app = express(); // create web server
//Default is port 5000
const PORT = process.env.PORT || 5000;

//Use middleware to various management++++++++++++++++++++++
app.use(cors());//allow access from any domain
app.use(express.json());

//++++++++++++++++ APP USE +++++++++++++++++++++++++++++++

//use router module=================
app.use("/user", userRoute); 
app.use("/chat", chatRoutes);
app.use("/qNa", qNaRoutes);

//++++++++++++++++ test call web server +++++++++++++++++++
app.get("/", (req, res) => {
  res.json({ message: "Hello from server port " + PORT + " by prisma" }); //send message
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res
    .status(500)
    .json({ message: "Something went wrong! Please try again later." });
});

//++++++++create web server connection from client/user++++++++++++
app.listen(PORT, () => {
  console.log("Server is running on port " + PORT);
});