const express = require('express');
const redis = require('redis');
const bodyParser = require('body-parser');
//const cookieParser = require('cookie-parser');
const utils = require('./utils.js');
const jwt = require('jsonwebtoken');

const app = express();

//app.use(cookieParser());
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
        client.set('isVIP', 'false');
        for (const key in newuser) {
            //console.log(`${key}: ${newuser[key]}`);
            const key_str = String(key);
            const val_str = String(newuser[key]);
            client.set(key_str, val_str);
        }

        await client.set(username, JSON.stringify({ 'tokens': '0' }), { EX: 60 * 30 });
        const data = { 'token': (await utils.createToken(username, client)) };
        return res.json({ "success": data });
      }
    }
    res.json({ "error": "Username is invalid." });
})

app.get('/check', async (req, res) => {
    const vip = await client.get('isVIP');
    if (vip === 'true') {
        return; // return vip page TODO
    }
    else {
        return res.json({ "permission denied": "You're not a vip member!" });
    }
})

app.get('/dashboard', async (req, res) => {
    const jwtSecretKey = "bad_key";
    const verified = jwt.verify(token, jwtSecretKey);
    if (verified) {
        return; // return dashboard page TODO
    }
    else {
        res.redirect('/');
    }
    
})

app.post('/registerTest', async (req, res)=>{
    try{

        const newuser = req.body;  // newuser is a json object
        console.log(newuser);
        client.set('username', 'bad');


        const ans = await client.get('username');
        console.log(ans);

        for (const key in newuser) {
            //console.log(`${key}: ${newuser[key]}`);
            const key_str = String(key);
            const val_str = String(newuser[key]);
            client.set(key_str, val_str);
        }
        console.log(await client.get('username'));


        // username = String(newuser.username);

        // client.HSET(username, 'name', newuser, function(err, reply) {
        //     if (err) {
        //         console.log(err);
        //     }
        //     console.log(reply);
        // });

        
        // client.HGETALL(username, function(err, obj) {
        //     console.log(obj);
        // });

        // client.set('testing', newuser);
        // console.log(client.get('testing'));

        // Set a string value
        // client.HSET('mystring', 'Hello, Redis!', (err, reply) => {
        //     if (err) throw err;
        //     console.log(reply); // Should print "OK"
        // });
        // // Get the string value
        // client.HGETALL('mystring', (err, reply) => {
        //     if (err) throw err;
        //     console.log(reply); // Should print "Hello, Redis!"
        // });


        // client.json.set(req.body.username, "$", req.body)
        // console.log(client.json.get(req.body.username, "$"))

        // client.HSET(newuser.username, newuser);
        // console.log(client.HGET(newuser.username));

        // const username = req.body.username;
        // let pass = req.body.password;
  
  
        // if (!username || !password) {
        // return res.sendStatus(400);
        // }

        // const newuser = {
        //     user: username,
        //     password: pass,
        //     isVIP: 0
        // }

  
        // client.hset(email, 
        //     'first_name', firstName,
        //     'last_name', lastName,
        //     'email', email,
        //     'password', password
        //     , function(err, reply){
        // if(err){
        //     console.log(err);
        // }
        // console.log(reply);
        // res.redirect('/register') ;
        // //res.redirect('/');
        // });
               
  
  
    } catch(e){    
        console.log(e);
        res.sendStatus(400);
    }
})