const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true }));

// Main route - connects to Flask
app.post('/getbestprice', async (req, res) => {
    try {
        console.log('\n=== EXPRESS DEBUG ===');
        console.log('1. Received request body:', req.body);
        
        const productOrUrl = req.body?.productOrUrl;
        console.log('2. Extracted productOrUrl:', productOrUrl);
        
        if (!productOrUrl) {
            console.log('3. ERROR: No productOrUrl found');
            return res.status(400).json({ error: 'No product or URL provided' });
        }

        console.log('4. Forwarding to Flask backend...');
        
        // Forward to Flask
        const flaskResponse = await fetch('http://localhost:5000/bestprice', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ productOrUrl: productOrUrl })
        });

        console.log('5. Flask response status:', flaskResponse.status);
        
        const data = await flaskResponse.json();
        console.log('6. Flask response data:', data);
        
        if (!flaskResponse.ok) {
            return res.status(flaskResponse.status).json(data);
        }
        
        res.json(data);
        
    } catch (error) {
        console.log('7. Express error:', error.message);
        if (error.code === 'ECONNREFUSED') {
            return res.status(503).json({ error: 'Flask backend server is not running. Please start the Flask server on port 5000.' });
        }
        res.status(500).json({ error: 'Server error: ' + error.message });
    }
});

// Serve HTML - update the filename to match your actual HTML file
app.get('/', (req, res) => {
    // Change 'index.html' to your actual HTML filename if different
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'Express server running', port: 3000 });
});

app.listen(3000, () => {
    console.log('Express server running on http://localhost:3000');
    console.log('Ready to connect to Flask backend on port 5000');
});