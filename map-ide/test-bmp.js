// Test script to verify BMP parsing
const fs = require('fs');
const path = require('path');

const bmpPath = '/home/user/webapp/bakasekai/map/provinces.bmp';

console.log('Reading BMP file:', bmpPath);
const buffer = fs.readFileSync(bmpPath);
console.log('File size:', buffer.length, 'bytes');

// Parse BMP header
const view = new DataView(buffer.buffer, buffer.byteOffset, buffer.byteLength);

const signature = String.fromCharCode(view.getUint8(0), view.getUint8(1));
console.log('Signature:', signature);

if (signature !== 'BM') {
  console.error('Invalid BMP file!');
  process.exit(1);
}

const fileSize = view.getUint32(2, true);
const dataOffset = view.getUint32(10, true);
const headerSize = view.getUint32(14, true);
const width = view.getInt32(18, true);
const height = view.getInt32(22, true);
const bitsPerPixel = view.getUint16(28, true);
const compression = view.getUint32(30, true);

console.log('File size:', fileSize);
console.log('Data offset:', dataOffset);
console.log('Header size:', headerSize);
console.log('Width:', Math.abs(width));
console.log('Height:', Math.abs(height));
console.log('Bits per pixel:', bitsPerPixel);
console.log('Compression:', compression);
console.log('Is top-down:', height < 0);

// Calculate row padding
const rowSize = Math.abs(width) * 3;
const rowPadding = (4 - (rowSize % 4)) % 4;
console.log('Row padding:', rowPadding);

// Read first few pixels
const absWidth = Math.abs(width);
const absHeight = Math.abs(height);
const isTopDown = height < 0;

console.log('\nFirst 5 pixels (RGB):');
for (let i = 0; i < 5; i++) {
  const srcY = isTopDown ? 0 : absHeight - 1;
  const paddedRowSize = rowSize + rowPadding;
  const srcOffset = dataOffset + srcY * paddedRowSize + i * 3;
  
  const b = buffer[srcOffset];
  const g = buffer[srcOffset + 1];
  const r = buffer[srcOffset + 2];
  
  console.log(`  Pixel ${i}: R=${r}, G=${g}, B=${b}`);
}

// Count unique colors (sample)
const colorSet = new Set();
const sampleSize = 1000000; // Sample 1M pixels
const step = Math.floor((absWidth * absHeight) / sampleSize);

for (let i = 0; i < absWidth * absHeight; i += step) {
  const y = Math.floor(i / absWidth);
  const x = i % absWidth;
  const srcY = isTopDown ? y : absHeight - 1 - y;
  const paddedRowSize = rowSize + rowPadding;
  const srcOffset = dataOffset + srcY * paddedRowSize + x * 3;
  
  const b = buffer[srcOffset];
  const g = buffer[srcOffset + 1];
  const r = buffer[srcOffset + 2];
  
  colorSet.add(`${r},${g},${b}`);
}

console.log('\nUnique colors in sample:', colorSet.size);
console.log('First 10 colors:', Array.from(colorSet).slice(0, 10));

console.log('\nBMP parsing test: SUCCESS');
