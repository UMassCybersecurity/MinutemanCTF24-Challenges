const express = require('express');
const redis = require('redis');
const cookieParser = require('cookie-parser');
const app = express();
const port = process.env.SERVER_PORT;

const bot = require('./bot.js');
const utils = require('./utils.js')
const client = redis.createClient({
  'url': process.env.REDIS_URL
});

client.on('error', err => console.log('Redis Client Error', err));
client.connect();
client.hSet("TARS", { 'username': 'TARS', 'tokens': +Infinity });

app.use(cookieParser());
app.use(express.json());
app.use(express.static('public'))

app.set('view engine', 'ejs');

app.get("/", (req, res) => {
  res.render('index.ejs');
})

app.get('/register', (req, res) => {
  res.render('register.ejs');
})

app.post('/register', async (req, res) => {
  const username = req.body.username;
  if (username && typeof username == 'string' && username.match(/([a-z|A-Z|0-9])+/g)) {
    const isUserTaken = await client.exists(username);
    if (isUserTaken) {
      return res.json({ "error": "Username is taken." });
    }
    else {
      await client.hSet(username, {'username': username, 'tokens': 0 });
      const data = { 'token': (await utils.createToken(username, client)) };
      return res.json({ "success": data });
    }
  }
  res.json({ "error": "Username is invalid." });
})

app.post('/report', async (req, res) => {
  const path = req.body.path;
  if (path && typeof path == 'string') {
    if (WAF.some(item=>path.includes(item))) {
      return res.json({'error':'no hacking allowed >:('})
    }
    const out = await bot.checkPage(path,client);
    return res.json(out);
  }
  res.json({ 'error': 'Path is invalid.' });
})

app.get('/balance/:username', utils.authMiddleware, async (req, res) => {
  if (req.user.username != req.params.username) {
    return res.json({ 'error': 'You can only view your own balance.' });
  }
  return res.json({ 'success': { 'tokens': req.user.tokens } });
})

app.get('/dashboard', utils.authMiddleware, async (req, res) => {
  res.redirect(`/dashboard/${req.user.username}`);
})

app.get('/dashboard/:username', async (req, res) => {
  res.render('dashboard.ejs', { user: { username: req.params.username } });
})

app.get("/refresh", utils.authMiddleware, async (req,res)=>{
  const username = req.user.username;
  const data = { 'token': (await utils.createToken(username, client)) };
  return res.json({"success":data});
})

app.get('/transfer/:user/:amount', utils.authMiddleware, async (req, res) => {
  const from_user = req.user;
  const to_username = req.params.user;
  const amount = parseInt(req.params.amount);
  if (typeof to_username == 'string' && typeof amount == 'number' && from_user.tokens >= amount && from_user.tokens > 0 && await client.exists(to_username)) {
    from_user.tokens = (from_user.tokens - amount).toString();
    await client.hSet(from_user.username, from_user);
    let to_user = await client.hGetAll(to_username);
    console.log(from_user);
    console.log(to_user);
    to_user.tokens += amount;
    await client.hSet(to_username, to_user);
    return res.send("Tokens successfully transfered.");
  }
  return res.send("Please provide a valid user and/or amount you are transfering to.");
})

app.get('/flag', utils.authMiddleware, (req, res) => {
  let message = "You don't have enough tokens.";
  if (req.user.tokens >= 1000000) {
    message = `Congratulations, here is the flag: ${process.env.FLAG}`
  }
  return res.render('flag.ejs',{message});
})

app.listen(port, () => {
  console.log(`Cross Space Request Forge listening on port ${port}`);
})
