const puppeteer = require('puppeteer');
const utils = require('./utils.js')

function checkPage(path, client) {
    return new Promise(async (res, rej) => {
        const browser = await puppeteer.launch({
            executablePath: '/usr/bin/chromium',
            headless: true,
            pipe: true,
            args: ['--no-sandbox','--disable-gpu']
        });
        let ret_val;
        try {
            const page = await browser.newPage();
            const token = await utils.createToken('TARS', client);
            page.setExtraHTTPHeaders({
                'Cookie': `user=${token}`
            });
            await page.goto(`http://127.0.0.1:${process.env.SERVER_PORT}${path}`,{
                timeout: 3000
            });
            await new Promise(r => setTimeout(r, 3000));
            ret_val =  res({'success': { 'message': 'Admin checked the page.' }});
        }
        catch(e){
            ret_val =  res({'error':{'message':'Error when admin viewed your page.'}})
        } finally {
            await browser.close();
        }
        return ret_val;

    })
}

module.exports = { checkPage };