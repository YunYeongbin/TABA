const express = require("express");
const app = express();

const cors = require("cors");
app.use(cors());

const githubLogin = require("./routes/githubLogin");

app.use("/githubLogin", githubLogin);

app.listen(3002, () =>
  console.log("Node.js Server is running on port 3002...")
);