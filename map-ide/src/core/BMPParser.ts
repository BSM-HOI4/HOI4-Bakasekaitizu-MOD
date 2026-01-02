import { RGB } from '../types';

/**
 * BMP file header structure
 */
export interface BMPHeader {
  fileSize: number;
  dataOffset: number;
  headerSize: number;
  width: number;
  height: number;
  planes: number;
  bitsPerPixel: number;
  compression: number;
  imageSize: number;
  xPixelsPerMeter: number;
  yPixelsPerMeter: number;
  colorsUsed: number;
  importantColors: number;
}

/**
 * Parsed BMP data
 */
export interface BMPData {
  header: BMPHeader;
  width: number;
  height: number;
  pixels: Uint8Array; // RGB data, row by row, bottom to top in BMP
  rowPadding: number;
}

/**
 * Parse a 24-bit BMP file
 */
export function parseBMP(buffer: ArrayBuffer): BMPData {
  const view = new DataView(buffer);
  
  // Check BMP signature
  const signature = String.fromCharCode(view.getUint8(0), view.getUint8(1));
  if (signature !== 'BM') {
    throw new Error('Invalid BMP file: missing BM signature');
  }

  // Parse header
  const header: BMPHeader = {
    fileSize: view.getUint32(2, true),
    dataOffset: view.getUint32(10, true),
    headerSize: view.getUint32(14, true),
    width: view.getInt32(18, true),
    height: view.getInt32(22, true),
    planes: view.getUint16(26, true),
    bitsPerPixel: view.getUint16(28, true),
    compression: view.getUint32(30, true),
    imageSize: view.getUint32(34, true),
    xPixelsPerMeter: view.getInt32(38, true),
    yPixelsPerMeter: view.getInt32(42, true),
    colorsUsed: view.getUint32(46, true),
    importantColors: view.getUint32(50, true),
  };

  // Validate
  if (header.bitsPerPixel !== 24) {
    throw new Error(`Unsupported BMP format: ${header.bitsPerPixel} bits per pixel (only 24-bit supported)`);
  }

  if (header.compression !== 0) {
    throw new Error('Compressed BMP not supported');
  }

  const width = Math.abs(header.width);
  const height = Math.abs(header.height);
  const isTopDown = header.height < 0;

  // Calculate row padding (rows must be aligned to 4 bytes)
  const rowSize = width * 3;
  const rowPadding = (4 - (rowSize % 4)) % 4;
  const paddedRowSize = rowSize + rowPadding;

  // Extract pixel data
  const pixelData = new Uint8Array(width * height * 3);
  const rawData = new Uint8Array(buffer, header.dataOffset);

  for (let y = 0; y < height; y++) {
    // BMP stores rows bottom-to-top (unless top-down)
    const srcY = isTopDown ? y : (height - 1 - y);
    const srcOffset = srcY * paddedRowSize;
    const dstOffset = y * width * 3;

    for (let x = 0; x < width; x++) {
      const srcIdx = srcOffset + x * 3;
      const dstIdx = dstOffset + x * 3;
      
      // BMP stores as BGR, convert to RGB
      pixelData[dstIdx] = rawData[srcIdx + 2];     // R
      pixelData[dstIdx + 1] = rawData[srcIdx + 1]; // G
      pixelData[dstIdx + 2] = rawData[srcIdx];     // B
    }
  }

  return {
    header,
    width,
    height,
    pixels: pixelData,
    rowPadding,
  };
}

/**
 * Write a 24-bit BMP file
 */
export function writeBMP(width: number, height: number, pixels: Uint8Array): ArrayBuffer {
  // Calculate sizes
  const rowSize = width * 3;
  const rowPadding = (4 - (rowSize % 4)) % 4;
  const paddedRowSize = rowSize + rowPadding;
  const imageSize = paddedRowSize * height;
  const fileSize = 54 + imageSize;

  // Create buffer
  const buffer = new ArrayBuffer(fileSize);
  const view = new DataView(buffer);
  const data = new Uint8Array(buffer);

  // BMP header (14 bytes)
  view.setUint8(0, 0x42); // 'B'
  view.setUint8(1, 0x4D); // 'M'
  view.setUint32(2, fileSize, true);
  view.setUint32(6, 0, true); // Reserved
  view.setUint32(10, 54, true); // Data offset

  // DIB header (40 bytes - BITMAPINFOHEADER)
  view.setUint32(14, 40, true); // Header size
  view.setInt32(18, width, true);
  view.setInt32(22, height, true); // Positive = bottom-up
  view.setUint16(26, 1, true); // Planes
  view.setUint16(28, 24, true); // Bits per pixel
  view.setUint32(30, 0, true); // Compression (none)
  view.setUint32(34, imageSize, true);
  view.setInt32(38, 3780, true); // X pixels per meter
  view.setInt32(42, 3780, true); // Y pixels per meter
  view.setUint32(46, 0, true); // Colors used
  view.setUint32(50, 0, true); // Important colors

  // Write pixel data (bottom to top, BGR)
  for (let y = 0; y < height; y++) {
    const srcY = height - 1 - y; // Flip vertically
    const srcOffset = srcY * width * 3;
    const dstOffset = 54 + y * paddedRowSize;

    for (let x = 0; x < width; x++) {
      const srcIdx = srcOffset + x * 3;
      const dstIdx = dstOffset + x * 3;

      // Convert RGB to BGR
      data[dstIdx] = pixels[srcIdx + 2];     // B
      data[dstIdx + 1] = pixels[srcIdx + 1]; // G
      data[dstIdx + 2] = pixels[srcIdx];     // R
    }

    // Add padding
    for (let p = 0; p < rowPadding; p++) {
      data[dstOffset + rowSize + p] = 0;
    }
  }

  return buffer;
}

/**
 * Get pixel color at position
 */
export function getPixel(pixels: Uint8Array, width: number, x: number, y: number): RGB {
  const idx = (y * width + x) * 3;
  return {
    r: pixels[idx],
    g: pixels[idx + 1],
    b: pixels[idx + 2],
  };
}

/**
 * Set pixel color at position
 */
export function setPixel(pixels: Uint8Array, width: number, x: number, y: number, color: RGB): void {
  const idx = (y * width + x) * 3;
  pixels[idx] = color.r;
  pixels[idx + 1] = color.g;
  pixels[idx + 2] = color.b;
}

/**
 * Convert BMP pixels to ImageData for canvas rendering
 */
export function pixelsToImageData(pixels: Uint8Array, width: number, height: number): ImageData {
  const imageData = new ImageData(width, height);
  const data = imageData.data;

  for (let i = 0; i < width * height; i++) {
    const srcIdx = i * 3;
    const dstIdx = i * 4;
    data[dstIdx] = pixels[srcIdx];         // R
    data[dstIdx + 1] = pixels[srcIdx + 1]; // G
    data[dstIdx + 2] = pixels[srcIdx + 2]; // B
    data[dstIdx + 3] = 255;                // A
  }

  return imageData;
}

/**
 * Convert ImageData back to BMP pixels
 */
export function imageDataToPixels(imageData: ImageData): Uint8Array {
  const { width, height, data } = imageData;
  const pixels = new Uint8Array(width * height * 3);

  for (let i = 0; i < width * height; i++) {
    const srcIdx = i * 4;
    const dstIdx = i * 3;
    pixels[dstIdx] = data[srcIdx];         // R
    pixels[dstIdx + 1] = data[srcIdx + 1]; // G
    pixels[dstIdx + 2] = data[srcIdx + 2]; // B
  }

  return pixels;
}
