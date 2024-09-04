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
    return jwt.sign(user,"bad_key");
}

module.exports = {createToken,parseUser};