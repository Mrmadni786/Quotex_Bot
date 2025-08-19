const express = require('express');
const router = express.Router();

// Example: get user info (JWT auth can be added)
router.get('/:quotex_id', (req, res)=>{
    const quotex_id = req.params.quotex_id;
    res.json({quotex_id, status:"active"});
});

module.exports = router;
