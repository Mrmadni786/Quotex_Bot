// Node.js admin extra security
const express = require('express');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const router = express.Router();

const SECRET_KEY = "YOUR_SECRET_KEY";

// Admin login
router.post('/login', (req, res)=>{
    const { password } = req.body;
    const hash = crypto.createHash('sha256').update(password).digest('hex');
    if(hash === "PUT_YOUR_SHA256_HASH_HERE"){
        const token = jwt.sign({role:'admin'}, SECRET_KEY, {expiresIn:'1h'});
        res.json({token});
    } else {
        res.status(401).json({error:"Invalid password"});
    }
});

module.exports = router;
