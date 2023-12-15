const axios = require("axios");
const express = require("express");
const router = express.Router();
const dotenv = require('dotenv');

const getResponse = async (code, clientID) => {
  dotenv.config();
  const response = await axios.post(
    "https://github.com/login/oauth/access_token",
    {
      code,
      client_id: clientID,
      client_secret: process.env.CLIENT_SECRET, 
    },
    {
      headers: {
        accept: "application/json",
      },
    }
  );

  return response;
};

router.get("/", async (req, res) => {
  let code = req.query.code;
  let clientID = req.query.clientID;
  let response = await getResponse(code, clientID);
  
  console.log(response.data.access_token);

  res.send({token: response.data.access_token});
});

module.exports = router;