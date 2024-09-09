const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const downloadImagesFromFacebook = async (url, folderName = 'facebook_images') => {
    // Launch Puppeteer and open a new page
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    
    // Go to the Facebook page
    await page.goto(url, { waitUntil: 'networkidle2' });

    // Wait for images to be loaded
    await page.waitForSelector('img'); // Wait until at least one image is present

    // Extract image URLs
    const imgUrls = await page.evaluate(() => {
        const images = Array.from(document.querySelectorAll('img'));
        return images.map(img => img.src);
    });

    // Create folder if it doesn't exist
    if (!fs.existsSync(folderName)) {
        fs.mkdirSync(folderName);
    }

    // Download images
    for (let i = 0; i < imgUrls.length; i++) {
        const imgUrl = imgUrls[i];
        try {
            const viewSource = await page.goto(imgUrl);
            const fileName = path.join(folderName, `image_${i + 1}.jpg`);
            fs.writeFileSync(fileName, await viewSource.buffer());
            console.log(`Downloaded ${fileName}`);
        } catch (e) {
            console.error(`Could not download image ${i + 1}: ${e.message}`);
        }
    }

    // Close the browser
    await browser.close();
};

// Example usage
const fbPostUrl = 'https://www.facebook.com/share/p/1EDJs5SzFL/';
const customFolderPath = 'C:/Users/Azel/Downloads/Downloads';
downloadImagesFromFacebook(fbPostUrl, customFolderPath);
