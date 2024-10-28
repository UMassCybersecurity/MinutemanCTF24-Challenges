const express = require('express')
const app = express()
const hostname = "0.0.0.0";
const port = 3000;
const nunjucks = require('nunjucks');

nunjucks.configure('views',{
    autoescape: true,
    express: app
});

app.set('views','./views');

app.use(require('./routes'));

app.use('/views', express.static('views'));

app.listen(port, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});
