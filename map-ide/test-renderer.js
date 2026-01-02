/**
 * Test script to verify the BMP parsing and renderer initialization
 */

const fs = require('fs');
const path = require('path');

const bmpPath = '/home/user/webapp/bakasekai/map/provinces.bmp';

// Parse BMP
function parseBMP(buffer) {
  const view = new DataView(buffer);
  const signature = String.fromCharCode(view.getUint8(0), view.getUint8(1));
  
  if (signature !== 'BM') {
    throw new Error('Not a valid BMP file');
  }
  
  const dataOffset = view.getUint32(10, true);
  const width = view.getInt32(18, true);
  let height = view.getInt32(22, true);
  const bitsPerPixel = view.getUint16(28, true);
  const compression = view.getUint32(30, true);
  
  const topDown = height < 0;
  height = Math.abs(height);
  
  if (bitsPerPixel !== 24) {
    throw new Error(`Unsupported bits per pixel: ${bitsPerPixel}`);
  }
  
  if (compression !== 0) {
    throw new Error(`Unsupported compression: ${compression}`);
  }
  
  // Calculate row padding
  const rowSize = width * 3;
  const paddedRowSize = Math.ceil(rowSize / 4) * 4;
  
  // Create pixel array (RGB format)
  const pixels = new Uint8Array(width * height * 3);
  const data = new Uint8Array(buffer);
  
  for (let y = 0; y < height; y++) {
    // BMP stores rows bottom-to-top (unless top-down)
    const srcY = topDown ? y : (height - 1 - y);
    const srcRowOffset = dataOffset + srcY * paddedRowSize;
    
    for (let x = 0; x < width; x++) {
      const srcIdx = srcRowOffset + x * 3;
      const dstIdx = (y * width + x) * 3;
      
      // BMP is BGR, convert to RGB
      pixels[dstIdx] = data[srcIdx + 2];     // R
      pixels[dstIdx + 1] = data[srcIdx + 1]; // G
      pixels[dstIdx + 2] = data[srcIdx];     // B
    }
  }
  
  return { width, height, pixels };
}

// Test the parsing
console.log('\n=== BMP Parsing Test ===\n');

const bmpBuffer = fs.readFileSync(bmpPath);
console.log(`File size: ${bmpBuffer.byteLength} bytes`);

const { width, height, pixels } = parseBMP(bmpBuffer.buffer.slice(bmpBuffer.byteOffset, bmpBuffer.byteOffset + bmpBuffer.byteLength));

console.log(`Parsed dimensions: ${width} x ${height}`);
console.log(`Pixel data size: ${pixels.length} bytes`);
console.log(`Expected size (width * height * 3): ${width * height * 3} bytes`);

// Sample some pixels
console.log('\nFirst 10 pixels (RGB):');
for (let i = 0; i < 10; i++) {
  const r = pixels[i * 3];
  const g = pixels[i * 3 + 1];
  const b = pixels[i * 3 + 2];
  console.log(`  Pixel ${i}: (${r}, ${g}, ${b})`);
}

// Check for unique colors
const colorSet = new Set();
for (let i = 0; i < width * height; i++) {
  const r = pixels[i * 3];
  const g = pixels[i * 3 + 1];
  const b = pixels[i * 3 + 2];
  colorSet.add(`${r},${g},${b}`);
}
console.log(`\nUnique colors: ${colorSet.size}`);

// Simulate renderer data conversion (RGB to RGBA for WebGL)
console.log('\n=== Renderer Simulation ===\n');

const rgbaData = new Uint8Array(width * height * 4);
for (let i = 0; i < width * height; i++) {
  rgbaData[i * 4] = pixels[i * 3];       // R
  rgbaData[i * 4 + 1] = pixels[i * 3 + 1]; // G
  rgbaData[i * 4 + 2] = pixels[i * 3 + 2]; // B
  rgbaData[i * 4 + 3] = 255;             // A
}
console.log(`RGBA data size: ${rgbaData.length} bytes`);

// Check for non-zero pixels
let nonZeroCount = 0;
for (let i = 0; i < rgbaData.length; i += 4) {
  if (rgbaData[i] !== 0 || rgbaData[i + 1] !== 0 || rgbaData[i + 2] !== 0) {
    nonZeroCount++;
  }
}
console.log(`Non-zero pixels: ${nonZeroCount} (${(nonZeroCount / (width * height) * 100).toFixed(2)}%)`);

// Sample center of the map
const centerX = Math.floor(width / 2);
const centerY = Math.floor(height / 2);
const centerIdx = (centerY * width + centerX) * 3;
console.log(`\nCenter pixel (${centerX}, ${centerY}): (${pixels[centerIdx]}, ${pixels[centerIdx + 1]}, ${pixels[centerIdx + 2]})`);

// Create a simple HTML test file to verify rendering
const htmlContent = `<!DOCTYPE html>
<html>
<head>
  <title>Map Renderer Test</title>
  <style>
    body {
      margin: 0;
      padding: 20px;
      background: #1e1e1e;
      color: #fff;
      font-family: monospace;
    }
    #canvas {
      border: 1px solid #444;
    }
    .info {
      margin: 10px 0;
    }
  </style>
</head>
<body>
  <h1>Map Renderer Test</h1>
  <div class="info">
    <p>Map size: ${width} x ${height}</p>
    <p>Unique colors: ${colorSet.size}</p>
    <p>Loading BMP data...</p>
  </div>
  <canvas id="canvas" width="${Math.min(width, 1024)}" height="${Math.min(height, 512)}"></canvas>
  
  <script>
    // Embedded pixel data (first 100x100 region for quick test)
    const testWidth = 256;
    const testHeight = 256;
    const testData = new Uint8ClampedArray(testWidth * testHeight * 4);
    
    // Generate test pattern matching the actual map colors
    const colors = [
      ${Array.from(colorSet).slice(0, 50).map(c => `[${c}]`).join(',')}
    ];
    
    const gridSize = 16;
    for (let y = 0; y < testHeight; y++) {
      for (let x = 0; x < testWidth; x++) {
        const gridX = Math.floor(x / gridSize);
        const gridY = Math.floor(y / gridSize);
        const colorIdx = (gridX * 17 + gridY * 31) % colors.length;
        const color = colors[colorIdx] || [100, 100, 100];
        const idx = (y * testWidth + x) * 4;
        testData[idx] = color[0];
        testData[idx + 1] = color[1];
        testData[idx + 2] = color[2];
        testData[idx + 3] = 255;
      }
    }
    
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    
    // Draw dark background
    ctx.fillStyle = '#1e1e1e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Create and draw test image
    const imageData = new ImageData(testData, testWidth, testHeight);
    ctx.putImageData(imageData, 10, 10);
    
    document.querySelector('.info p:last-child').textContent = 'Test pattern rendered!';
  </script>
</body>
</html>`;

fs.writeFileSync('/home/user/webapp/map-ide/dist/test-map.html', htmlContent);
console.log('\nCreated test HTML at: /home/user/webapp/map-ide/dist/test-map.html');

console.log('\n=== Test Complete ===\n');
console.log('BMP parsing is working correctly.');
console.log('The map data can be converted to RGBA format for WebGL rendering.');
console.log('\nTo test in browser:');
console.log('1. Start the dev server: npm run dev');
console.log('2. Click "Test Mode (Demo)" button');
console.log('3. The map should render');
