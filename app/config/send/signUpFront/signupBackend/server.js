const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const routesURLs = require('./routes/routes');
const app = express();
const cors = require('cors');


dotenv.config();

mongoose.connect(process.env.DATABASE_ACCESS, ()=> console.log("database Connected"));

app.use(express.json());
app.use(cors());
app.use('/app', routesURLs);
app.listen(4000, ()=> console.log("server Running"));
