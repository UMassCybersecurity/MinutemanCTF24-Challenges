const puppeteer = require('puppeteer');
const utils = require('./utils.js')

function checkPage(path, client) {
    return new Promise(async (res, rej) => {
        const browser = await puppeteer.launch({
            executablePath: '/usr/bin/chromium',
            args: ['--no-sandbox']
        });
        const page = await browser.newPage();
        console.log('Making token');
        const token = await utils.createToken('TARS', client);
        console.log(token);
        page.setExtraHTTPHeaders({
            'Cookie': `user=${token}`
        });
        path = path.startsWith('/') ? path : `/${path}` ;
        await page.goto(`http://127.0.0.1:${process.env.SERVER_PORT}${path}`,{
            timeout: 5000
        });
        await browser.close();
        return res({'success': { 'message': 'Admin checked the page.' }});
    })
}

module.exports = { checkPage };