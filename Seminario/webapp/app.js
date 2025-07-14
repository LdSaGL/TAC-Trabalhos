const express = require("express");
const http = require("http");

const app = express();

app.get("/api", (req, res) => {
  res.send("Servidor respondeu normalmente");
});

const server = http.createServer(app);

// Limite de conexões simultâneas
server.maxConnections = 200;

server.on("connection", (socket) => {
  console.log(`Nova conexão aberta. Conexões ativas: ${server._connections}`);
});

server.listen(3000, () => {
  console.log("Servidor rodando na porta 3000");
});
