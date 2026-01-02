/**
 * Headless browser test to capture console logs
 */

const puppeteer = require('puppeteer');

async function runTest() {
  console.log('Starting browser test...\n');
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });
  
  const page = await browser.newPage();
  
  // Collect console logs
  const consoleLogs = [];
  page.on('console', msg => {
    const text = `[${msg.type().toUpperCase()}] ${msg.text()}`;
    consoleLogs.push(text);
    console.log(text);
  });
  
  page.on('pageerror', err => {
    console.error('[PAGE ERROR]', err.message);
  });
  
  try {
    console.log('Navigating to http://localhost:5173...\n');
    await page.goto('http://localhost:5173', { waitUntil: 'networkidle0', timeout: 30000 });
    
    console.log('\n--- Page loaded ---\n');
    
    // Wait a bit for React to initialize
    await page.waitForTimeout(2000);
    
    // Check if Test Mode button exists
    const testModeBtn = await page.$('button:has-text("Test Mode")');
    if (testModeBtn) {
      console.log('Found Test Mode button, clicking...');
      await testModeBtn.click();
      await page.waitForTimeout(3000);
    } else {
      console.log('Test Mode button not found, trying alternative selector...');
      // Try clicking by visible text
      const buttons = await page.$$('button');
      for (const btn of buttons) {
        const text = await btn.evaluate(el => el.textContent);
        if (text && text.includes('Test Mode')) {
          console.log('Found button with Test Mode text, clicking...');
          await btn.click();
          await page.waitForTimeout(3000);
          break;
        }
      }
    }
    
    // Wait for potential canvas rendering
    await page.waitForTimeout(2000);
    
    // Get canvas dimensions
    const canvasInfo = await page.evaluate(() => {
      const canvas = document.querySelector('canvas');
      if (canvas) {
        return {
          width: canvas.width,
          height: canvas.height,
          found: true
        };
      }
      return { found: false };
    });
    
    console.log('\nCanvas info:', canvasInfo);
    
    // Get debug info if available
    const debugInfo = await page.evaluate(() => {
      const debugEl = document.querySelector('[class*="Debug"]');
      if (debugEl) {
        return debugEl.textContent;
      }
      return null;
    });
    
    if (debugInfo) {
      console.log('Debug info:', debugInfo);
    }
    
    // Take screenshot
    await page.screenshot({ path: '/home/user/webapp/map-ide/test-screenshot.png' });
    console.log('\nScreenshot saved to test-screenshot.png');
    
  } catch (error) {
    console.error('Error:', error.message);
  }
  
  console.log('\n--- Console Logs Summary ---');
  consoleLogs.forEach(log => console.log(log));
  
  await browser.close();
  console.log('\nTest complete.');
}

runTest().catch(console.error);
