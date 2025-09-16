const express = require("express"); // call express module to create web server
const cors = require("cors");
const http = require("http");
const { Server } = require('socket.io');

const userRoute = require("./routes/user.route"); // call to use router module
const chatRoutes = require("./routes/chat.route.js");
const qNaRoutes = require("./routes/qNa.route.js");
require("dotenv").config(); // call to use .env
//++++++++++++++++++ CREATE WEB SERVER +++++++++++++++++++

const app = express(); // create web server
const PORT = process.env.PORT || 5000; 
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:8081", // หรือ "*" ใน dev
    methods: ["GET", "POST"]
  }
});

//Middleware 
app.use(cors());
app.use(express.json());

// Routes
app.use("/user", userRoute); 
app.use("/chat", chatRoutes);
app.use("/qNa", qNaRoutes);

// Basic test route
app.get("/", (req, res) => {
  res.json({ message: "Hello from BuddhamAI_UAT server! :)" });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res
    .status(500)
    .json({ message: "Something went wrong! Please try again later TwT" });
});

io.on('connect', (socket) => {
    console.log('User connected');
    socket.on('disconnect', () => {
        console.log('User disconnected');
    });

    socket.on('message', (msg) => {
            io.emit('message', msg);
            // console.log('Message received:', msg);
    })
});

// Start server
server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT} with Socket.IO...`);
});