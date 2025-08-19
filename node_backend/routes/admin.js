const express = require('express');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const router = express.Router();

const SECRET_KEY = "YOUR_SECRET_KEY"; // JWT secret

// Login admin
router.post('/login', (req, res) => {
    const { password } = req.body;
    const hash = crypto.createHash('sha256').update(password).digest('hex');
    if(hash === "PUT_YOUR_SHA256_HASH_HERE"){
        const token = jwt.sign({role: 'admin'}, SECRET_KEY, {expiresIn: '1h'});
        res.json({token});
    } else {
        res.status(401).json({error: "Invalid password"});
    }
});

// Middleware
function verifyAdmin(req, res, next){
    const token = req.headers['authorization'];
    if(!token) return res.status(403).send("No token");
    jwt.verify(token, SECRET_KEY, (err, decoded) => {
        if(err) return res.status(401).send("Invalid token");
        next();
    });
}

// Example: broadcast message
router.post('/broadcast', verifyAdmin, (req, res)=>{
    const { message } = req.body;
    console.log("Broadcast to all users:", message);
    res.json({status:"Message sent"});
});

module.exports = router;
