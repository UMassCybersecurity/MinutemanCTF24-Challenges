const jwt = require('jsonwebtoken');

const createToken = async (username, database) =>{
    let user = await database.collection('users').findOne({'username':username});
    delete user.password
    return jwt.sign(user,process.env.SECRET_TOKEN);
}

const authMiddleware = (req, res, next) => {
    if (req.cookies.user) {
        try {
            req.user = jwt.verify(req.cookies['user'], process.env.SECRET_TOKEN);
            return next();
        }
        catch (e) {
            console.log(e);
            return res.send("Invalid JWT, try registering a new token.");
        }
    }
    return res.send("Error when processing JWT.");
}

module.exports = {authMiddleware,createToken};