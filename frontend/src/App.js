const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve the HTML page at root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Route to handle price comparison requests
app.post('/getbestprice', async (req, res) => {
    try {
        console.log('Express: Raw request body:', req.body);
        
        // Extract productOrUrl - keeping the exact same key name
        const productOrUrl = req.body.productOrUrl;
        
        console.log('Express: Extracted productOrUrl:', productOrUrl);
        
        if (!productOrUrl) {
            console.log('Express: No productOrUrl found in request');
            return res.status(400).json({ error: 'No product or URL provided' });
        }

        console.log('Express: Forwarding to Flask backend...');
        
        // Create the exact JSON payload to send to Flask
        const flaskPayload = { productOrUrl: productOrUrl };
        console.log('Express: JSON payload being sent to Flask:', JSON.stringify(flaskPayload));

        // Forward request to Flask backend
        const flaskResponse = await fetch('http://localhost:5000/bestprice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(flaskPayload)
        });

        console.log('Express: Flask response status:', flaskResponse.status);

        if (!flaskResponse.ok) {
            const errorData = await flaskResponse.json();
            console.log('Express: Flask error response:', errorData);
            return res.status(flaskResponse.status).json(errorData);
        }

        const data = await flaskResponse.json();
        console.log('Express: Flask success response:', data);
        
        res.json(data);

    } catch (error) {
        console.error('Express: Error forwarding request to Flask:', error.message);
        
        if (error.code === 'ECONNREFUSED') {
            return res.status(503).json({ 
                error: 'Flask backend server is not running. Please start the Flask server on port 5000.' 
            });
        }
        
        res.status(500).json({ 
            error: 'Express server error: ' + error.message 
        });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'Express server is running', port: PORT });
});

app.listen(PORT, () => {
    console.log(`Express server running on http://localhost:${PORT}`);
    console.log('Make sure Flask backend is running on http://localhost:5000');
});

module.exports = app;