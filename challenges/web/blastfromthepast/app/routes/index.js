const router = require('express').Router();
const path = require('path')
const middleware = require('./middleware.js');
const DBHelper = require('./db.js');

//I will add my friends here once I make some 
const ALLOWED = ['admin'];
const FLAG = process.env.FLAG;

router.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../static/html/index.html'));
})

router.get('/leaderboard', async (req, res) => {
  let leaders = (await DBHelper.getAllUsers());
  let topten = leaders
    .sort((a, b) => b.diamonds - a.diamonds)
    .map(obj => ({ 'user': obj.username, 'diamonds': obj.diamonds }))
    .slice(0, 10);
  return res.json({ 'leaders': topten });
})

router.get('/buyflag/:id', middleware.authReq, async (req, res) => {
  let result = await DBHelper.getUser(req.user);
  if (result.length > 0) {
    let user = result[0];
    if (user.diamonds >= 64) {
      return res.json({ 'flag': FLAG });
    }
    return res.json({ 'error': 'not enough diamonds!' })
  }
  res.json({ 'error': 'Could not find character' });
})

router.get('/balance/:id', middleware.authReq, async (req, res) => {
  let result = await DBHelper.getUser(req.params.id);
  if (result.length > 0) {
    let user = result[0];
    if (req.params.id === req.user) {
      return res.json({ 'success': { 'balance': user.diamonds } })
    }
  }
  res.json({ 'error': 'could not find user!' })
})

/*
DISABLED FOR SECURITY!
*/
router.get('/mine/:id', middleware.authReq, async (req, res) => {
  return res.send("Login disabled for security reasons...")
})

router.get('/dashboard', middleware.authReq, (req, res) => {
  if (req.user) {
    return res.sendFile(path.join(__dirname, '../static/html/dashboard.html'));
  }
  res.redirect('/login')
})

router.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, '../static/html/login.html'));
})

router.post('/login', async (req, res) => {
  let user = req.body.user;
  let pass = req.body.pass;
  let result = await DBHelper.authUser(user, pass);
  if (result[0]) {
    let token = middleware.createToken(result[0].username);
    res.set('Set-Cookie', token);
    return res.redirect("/dashboard");
  }
  res.redirect("/login");
})

router.get('/register', async (req, res) => {
  res.sendFile(path.join(__dirname, '../static/html/register.html'));
})

/*
DISABLED FOR SECURITY!
*/
router.post('/register', async (req, res) => {
  return res.send("Login disabled for security reasons...")
})

module.exports = router;