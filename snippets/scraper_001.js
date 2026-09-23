const express = require('express');
const request = require('request-promise');

const app = express();
const PORT = process.env.PORT || 5000;

// const apiKey = '';
// const generateScraperUrl(api_key) = `http://api.scraperapi.com?api_key=${apiKey}&autoparse=true`;

const generateScraperUrl = (apiKey) => `http:api.scarperapi.com?api.key=${apiKey}&autoparse=true`;

app.use(express.json());

app.get('/', (req,res)=> {
    res.send('Welcome to Amazon Scraper API.');  

});
//GET Product Details
app.get('/products/:productId', async(req,res)=>{
    const{productId} = req.params;
    const{api_key} = req.query;

    try{
        const response = await request(`${generateScraperUrl(api_key)}&url=https://www.amazon.in/dp/${productId}&ultra_premium=true`);
        
        res.json(JSON.parse(response));
    }
    catch(error){
        res.json(error);
    }
});
//GET Product Reviews
app.get('/products/:productId/reviews', async(req,res)=>{
    const{productId} = req.params;
    const{api_key} = req.query;

    try{
        const response = await request(`${generateScraperUrl(api_key)}&url=https://www.amazon.in/product-reviews/${productId}&ultra_premium=true`);
        
        res.json(JSON.parse(response));
    }
    catch(error){
        res.json(error);
    }
});
//GET Product Offers
app.get('/products/:productId/offers', async(req,res)=>{
    const{productId} = req.params;
    const{api_key} = req.query;

    try{
        const response = await request(`${generateScraperUrl(api_key)}&url=https://www.amazon.in/gp/offer-listing/${productId}&ultra_premium=true`);
        
        res.json(JSON.parse(response));
    }
    catch(error){
        res.json(error);
    }
});
//GET Search Results
app.get('/search/:searchQuery', async(req,res)=>{
    const{searchQuery} = req.params;
    const{api_key} = req.query;

    try{
        const response = await request(`${generateScraperUrl(api_key)}&url=https://www.amazon.in/s?k=${searchQuery}&ultra_premium=true`);
        res.json(JSON.parse(response));
    }
    catch(error){
        res.json(error);
    }
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
