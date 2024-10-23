const express = require('express');
const redis = require('redis');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const utils = require('./utils.js');
const jwt = require('jsonwebtoken');

const app = express();

app.use(cookieParser());
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static('public'))

console.log(process.env.REDIS_HOST);
const client = redis.createClient({url: `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`});

(async () => {
    client.on('error', err => console.log('Redis Client Error', err));
    await client.connect()
})();

const port = 3000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

app.get('/', (req,res)=>{
    return res.render('register.ejs');
})

app.post('/register', async (req, res) => {
    const newuser = req.body;
    const username = newuser.username;
    if (username && typeof username == 'string' && username.match(/([a-z|A-Z|0-9])+/g)) {
      const isUserTaken = await client.exists(username);
      if (isUserTaken) {
        return res.json({ "error": "Username is taken." });
      }
      else {
        await client.HSET(username, 'isVIP', 'false');
        await client.HSET(username, req.body);
        await client.HSET(username, { 'tokens': '0' });
        const data = { 'token': (await utils.createToken(username, client)) };
        res.cookie("user", data['token'], {
            httpOnly: true
        });
        return res.redirect('/dashboard');
      }
    }
    return res.json({ "error": "Username is invalid." });
})

app.get('/check', utils.authMiddleware, async (req, res) => {
    const username = req.user.username;

    const vip = await client.HGET(username, 'isVIP');
    if (vip === 'true') {
        let flag = process.env.FLAG;
        return res.render("vip.ejs", {flag});
    }
    else {
        return res.json({ "Permission Denied": "Only vip members get to watch this movie!" });
    }
})

app.get('/dashboard', utils.authMiddleware, async (req, res) => {
    return res.render('dashboard.ejs');
})