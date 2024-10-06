const express = require('express');
const redis = require('redis');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const utils = require('./utils.js');
const jwt = require('jsonwebtoken');
const { RedisSearchLanguages } = require('redis');

const app = express();

app.use(cookieParser());
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: false }));
console.log(process.env.REDIS_HOST);
//const client = redis.createClient({url: `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`});
const client = redis.createClient({
    url: 'redis://redis:6379'
    });

(async () => {
    client.on('error', err => console.log('Redis Client Error', err));
    await client.connect()
})();

const port = 3000;
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

app.get('/', (req,res)=>{
    res.send(`
    <h1>Register</h1>
    <form method='post' action='/register'>
    <input type='text' name='username' placeholder='Username' required />
    <input type='password' name='password' placeholder='password' required/>
    <input type='submit' />
    </form>
    <a href='/login'>Login</a>
    `)
    //res.render(views/register);
})

app.post('/register', async (req, res) => {
    const newuser = req.body;
    console.log(req.body)
    const username = newuser.username;
    if (username && typeof username == 'string' && username.match(/([a-z|A-Z|0-9])+/g)) {
      const isUserTaken = await client.exists(username);
      if (isUserTaken) {
        return res.json({ "error": "Username is taken." });
      }
      else {
        //const time = Date.now();

        await client.HSET(username, 'isVIP', 'false');
        
        await client.HSET(username, req.body);

        //console.log(await client.HGETALL(username));

        await client.HSET(username, { 'tokens': '0' });
        const data = { 'token': (await utils.createToken(username, client)) };
        // Set browser httpOnly cookies
        res.cookie("user", data['token'], {
        // secure: true,
            httpOnly: true
        });
        return res.json({ "success": data });
        //res.redirect("/dashboard");
      }
    }
    res.json({ "error": "Username is invalid." });
})

app.get('/check', utils.authMiddleware, async (req, res) => {
    const username = req.user.username;
    console.log(req.user)

    const vip = await client.HGET(username, 'isVIP');
    if (vip === 'true') {
        res.render(vip.html);
    }
    else {
        return res.json({ "permission denied": "You're not a vip member!" });
    }
})

app.get('/dashboard', utils.authMiddleware, async (req, res) => {
    res.render(dashboard.html);
})