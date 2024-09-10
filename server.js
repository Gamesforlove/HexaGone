const express = require('express');
const compression = require('compression');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 8000;

// Enable Brotli compression
app.use(compression({ 
    filter: shouldCompress,
    threshold: 0,
    brotli: true 
}));

function shouldCompress(req, res) {
    if (req.headers['x-no-compression']) {
        // Don't compress responses with this request header
        return false;
    }

    // Fallback to standard filter function
    return compression.filter(req, res);
}

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Serve pre-compressed Brotli files if available
app.get('*', (req, res, next) => {
    const filePath = path.join(__dirname, 'public', req.url);
    const brFilePath = filePath + '.br';

    if (fs.existsSync(brFilePath)) {
        req.url += '.br';
        res.set('Content-Encoding', 'br');
        res.set('Content-Type', 'application/javascript');
    }
    next();
});

app.listen(PORT, () => {
    console.log(`Serving at http://localhost:${PORT}`);
});
