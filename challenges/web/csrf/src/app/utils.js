const jwt = require('jsonwebtoken');

const parseUser = (userString) => {
    let userObj = JSON.parse(userString);
    userObj.tokens = parseFloat(userObj.tokens);
    return userObj;
}

const createToken = async (username,client) =>{
    let user = await client.get(username);
    user = parseUser(user);
    user.username = username;
    user.tokens = user.tokens.toString();
    return jwt.sign(user,process.env.SECRET_TOKEN);
}

const stringifyUser = (userObj) => {
    userObj.tokens = String(userObj.tokens);;
    return JSON.stringify({ 'tokens': userObj.tokens });
}

const authMiddleware = (req, res, next) => {
    if (req.cookies.user) {
        try {
            req.user = jwt.verify(req.cookies['user'], process.env.SECRET_TOKEN);
            req.user.tokens = parseFloat(req.user.tokens);
            return next();
        }
        catch (e) {
            console.log(e);
            return res.send("Invalid JWT, try registering a new token.");
        }
    }
    return res.send("Error when processing JWT.");
}

module.exports = {authMiddleware,createToken ,stringifyUser,parseUser};