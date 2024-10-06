const jwt = require('jsonwebtoken');


const parseUser = (userString) => {
    let userObj = JSON.parse(userString);
    userObj.tokens = parseFloat(userObj.tokens);
    return userObj;
}

const createToken = async (username,client) =>{
    let user = await client.HGETALL(username);
    //user = parseUser(user);
    user.username = username;
    user.tokens = user.tokens.toString();
    return jwt.sign(user,"bad_key");
}

const authMiddleware = (req, res, next) => {
    console.log(req.cookies.user);
    if (req.cookies.user) {
        
        try {
            req.user = jwt.verify(req.cookies['user'], "bad_key");
            req.user.tokens = parseFloat(req.user.tokens);
            console.log("cookie success");
            return next();
        }
        catch (e) {
            console.log(e);
            return res.send("Invalid JWT, try registering a new token.");
        }
    }
    return res.send("Error when processing JWT.");
}

module.exports = {createToken,parseUser,authMiddleware};