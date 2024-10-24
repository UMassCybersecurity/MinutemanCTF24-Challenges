const express = require('express');
const { v4: uuidv4 } = require('uuid');
const path = require('path');
const cookiep = require('cookie-parser');
const bodyp = require('body-parser');

const fs = require('fs');

const redis = require('redis');
const admin = require('./admin.js');

const app = express();
const port = 3000;

const client = redis.createClient({
  'url': process.env.REDIS_URL
})
client.on('error', err => console.log('Redis Client Error', err));
client.connect();

app.use(cookiep());
app.use(bodyp.urlencoded())
app.use('/images', express.static('images'));

async function set_cache(key,val){
  return (await client.set(key,JSON.stringify(val)));
}

async function get_cache(key){
  return JSON.parse(await client.get(key));
}

app.get('/', async (req, res) => {
  let UID = req.cookies.user;
  if(!UID || !(await client.exists(UID))){
    UID = uuidv4();
    await set_cache(UID,["See you on the other side - Command", "Good Luck Dad - Cooper"]);
    res.set({'Set-Cookie':`user=${UID}`});
  }

  res.redirect(`/user/${UID}`);
})

app.get('/user/:id',async (req,res)=>{
  if(!req.params || !(await client.exists(req.params.id))){

    return res.redirect('/')
  }

  let user_note = await get_cache(req.params.id);

  res.setHeader('Content-Type', 'text/html');
  const notes = await get_cache(req.params.id);
  let htmlContent;
  fs.readFile(path.join(__dirname,'public','index.html'), (err, data) => {
      if(err) {
        res.send("Problem creating HTML");
      } else {
        htmlContent = data.toString();

        res.send(htmlContent);
      }
  });
})

app.get('/notes/:id', async (req,res)=>{
  if(!req.params){
    return res.send("Cannot find your notes!");
  }

  const notes = await get_cache(req.params.id);
  return res.send({'notes': notes});
})

app.get('/report/:id',async (req,res)=>{
  res.send("I'm reviewing your notes!");
  await admin(process.env.FLAG, req.params.id);
})

app.get('/clear',async (req,res)=>{
  if(!req.cookies || !(await client.exists(req.cookies.user))){
    return res.send("Hmm are you even a user? Go to /");
  }

  if(req.cookies.user.includes("admin") && req.ip != '::ffff:127.0.0.1'){
    return res.send("You're not an admin!")
  }

  await set_cache(req.cookies.user,[]);

  return res.redirect(`/user/${req.cookies.user}`);
})

app.post('/create',async (req,res)=>{
  if(!req.cookies || !(client.exists(req.cookies.user))){
    return res.send("Hmm are you even a user? Go to /");
  }
  if(!req.body.note){
    return res.send("Did not get a note body")
  }

  let user_note = await get_cache(req.cookies.user);

  user_note.push(req.body.note);
  await set_cache(req.cookies.user,user_note);
  return res.redirect(`/user/${req.cookies.user}`);
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
