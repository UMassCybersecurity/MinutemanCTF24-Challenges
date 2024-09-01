const puppeteer = require('puppeteer');
const utils = require('./utils.js')

function checkPage(path,client) {
    return new Promise(async (res, rej) => {
        console.log(path)
        const browser = await puppeteer.launch({
            executablePath: '/usr/bin/chromium',
            args: ['--no-sandbox']
        });
        const page = await browser.newPage();
        page.setExtraHTTPHeaders({
            'Cookie': `user=${(await utils.createToken('TARS', client))}`
        });
        await page.goto(`http://127.0.0.1:${process.env.SERVER_PORT}/${path}`);
        return res(await browser.close());
    })
}

module.exports = { checkPage };