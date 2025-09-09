const express = require('express');
const utils = require('./utils.js');
const { MongoClient } = require('mongodb');
const cookieParser = require('cookie-parser');

const client = new MongoClient(`mongodb://${process.env.MONGO_INITDB_ROOT_USERNAME}:${process.env.MONGO_INITDB_ROOT_PASSWORD}@${process.env.MONGO_HOST}`);

const app = express()
const port = process.env.SERVER_PORT;

app.use(cookieParser())
app.use(express.json())

app.get('/', async (req, res) => {
  res.send('Hello World!')
})

app.get("/flag", utils.authMiddleware, async (req, res) => {
  console.log(req.user)
  if (req.user.username === 'admin') {
    return res.send(process.env.FLAG)
  }
  res.status(403).send('Only admin can view the flag');
})

app.post('/register', async (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  if (username && password) {
    await client.connect();
    const database = await client.db('minuteman_database');
    const user = await database.collection('users').findOne({ 'username': username });
    if (user) {
      await client.close();
      return res.redirect('/register?message=user_exists');
    }
    await database.collection('users').insertOne(
      { role: 'STUDENT', username: username, password: password }
    )
    await client.close();
    return res.redirect('/login');

  }
  return res.redirect('/register?message=failed_auth');
})

app.post('/login', async (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  if (username && password) {
    await client.connect();
    const database = await client.db('minuteman_database');
    const user = await database.collection('users').findOne({ 'username': username, 'password': password });
    if (user) {
      const token = await utils.createToken(username, database);
      res.cookie('user', token);
      await client.close();
      return res.redirect('/flag');
    }
    await client.close();
  }
  return res.redirect('/login?message=failed_auth');
})

app.listen(port, () => {
  console.log(`NoSQLi app listening on port ${port}`)
})