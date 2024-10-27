const router = require('express').Router();
const path = require('path');

router.get('/',(req,res)=>{
    res.render(path.resolve('views/SamHead.html'));
});

router.get('/SamHead',(req,res)=>{
    res.render(path.resolve('views/SamHead.html'));
});

module.exports = router;
