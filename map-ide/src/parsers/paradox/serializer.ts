import { ASTNode, ASTValue } from './parser';

/**
 * Serializer options
 */
export interface SerializerOptions {
  indent?: string;
  newline?: string;
  quoteStrings?: boolean;
}

const defaultOptions: SerializerOptions = {
  indent: '\t',
  newline: '\n',
  quoteStrings: false,
};

/**
 * Check if a string needs quotes
 */
function needsQuotes(value: string): boolean {
  // Needs quotes if contains spaces, special chars, or starts with number
  if (!value) return true;
  if (/\s/.test(value)) return true;
  if (/^[0-9]/.test(value)) return true;
  if (/[={}#"']/.test(value)) return true;
  return false;
}

/**
 * Format a string value
 */
function formatString(value: string, quoteStrings: boolean): string {
  if (quoteStrings || needsQuotes(value)) {
    return `"${value.replace(/"/g, '\\"')}"`;
  }
  return value;
}

/**
 * Check if array is a simple number array
 */
function isNumberArray(arr: ASTValue[]): boolean {
  return arr.every(v => typeof v === 'number');
}

/**
 * Check if array is a simple value array (no objects)
 */
function isSimpleArray(arr: ASTValue[]): boolean {
  return arr.every(v => typeof v === 'number' || typeof v === 'string');
}

/**
 * Serialize AST value to string
 */
function serializeValue(
  value: ASTValue,
  depth: number,
  options: SerializerOptions
): string {
  const { indent, newline, quoteStrings } = options;
  const currentIndent = indent!.repeat(depth);
  const innerIndent = indent!.repeat(depth + 1);

  // Number
  if (typeof value === 'number') {
    // Format with appropriate precision
    if (Number.isInteger(value)) {
      return String(value);
    }
    return value.toFixed(3).replace(/\.?0+$/, '');
  }

  // String
  if (typeof value === 'string') {
    return formatString(value, quoteStrings!);
  }

  // Boolean (from flags)
  if (typeof value === 'boolean') {
    return value ? 'yes' : 'no';
  }

  // Array
  if (Array.isArray(value)) {
    if (value.length === 0) {
      return '{ }';
    }

    // Simple number array - inline
    if (isNumberArray(value)) {
      const numbers = value.map(v => serializeValue(v, 0, options));
      // Check if it fits on one line
      const inline = `{ ${numbers.join(' ')} }`;
      if (inline.length < 80) {
        return inline;
      }
    }

    // Simple array - inline or multiline based on length
    if (isSimpleArray(value)) {
      const items = value.map(v => serializeValue(v, 0, options));
      const inline = `{ ${items.join(' ')} }`;
      if (inline.length < 80) {
        return inline;
      }
      // Multiline
      return `{${newline}${innerIndent}${items.join(' ')}${newline}${currentIndent}}`;
    }

    // Complex array - multiline
    const items = value.map(v => {
      const serialized = serializeValue(v, depth + 1, options);
      return `${innerIndent}${serialized}`;
    });
    return `{${newline}${items.join(newline)}${newline}${currentIndent}}`;
  }

  // Object
  if (typeof value === 'object' && value !== null) {
    return serializeNode(value as ASTNode, depth, options);
  }

  return String(value);
}

/**
 * Serialize AST node to string
 */
function serializeNode(
  node: ASTNode,
  depth: number,
  options: SerializerOptions
): string {
  const { indent, newline } = options;
  const currentIndent = indent!.repeat(depth);
  const innerIndent = indent!.repeat(depth + 1);

  const entries = Object.entries(node);
  
  if (entries.length === 0) {
    return '{ }';
  }

  const lines: string[] = [];
  
  for (const [key, value] of entries) {
    const formattedKey = needsQuotes(key) ? `"${key}"` : key;
    
    // Handle arrays of duplicate keys
    if (Array.isArray(value) && !isSimpleArray(value)) {
      // Check if this is a repeated key (array of objects/blocks)
      const allObjects = value.every(v => typeof v === 'object' && !Array.isArray(v));
      if (allObjects) {
        // Serialize as repeated key=value
        for (const item of value) {
          const serializedValue = serializeValue(item, depth + 1, options);
          lines.push(`${innerIndent}${formattedKey} = ${serializedValue}`);
        }
        continue;
      }
    }

    const serializedValue = serializeValue(value, depth + 1, options);
    
    // Decide if value goes on same line or next line
    if (typeof value === 'object' && !Array.isArray(value) && Object.keys(value).length > 0) {
      // Block - put on same line
      lines.push(`${innerIndent}${formattedKey} = ${serializedValue}`);
    } else if (Array.isArray(value) && !isSimpleArray(value)) {
      lines.push(`${innerIndent}${formattedKey} = ${serializedValue}`);
    } else {
      lines.push(`${innerIndent}${formattedKey} = ${serializedValue}`);
    }
  }

  return `{${newline}${lines.join(newline)}${newline}${currentIndent}}`;
}

/**
 * Serialize AST to Paradox Script format
 */
export function serializeParadoxScript(
  ast: ASTNode,
  options: Partial<SerializerOptions> = {}
): string {
  const opts = { ...defaultOptions, ...options };
  const { newline } = opts;

  const lines: string[] = [];
  
  for (const [key, value] of Object.entries(ast)) {
    const formattedKey = needsQuotes(key) ? `"${key}"` : key;
    
    // Handle arrays of duplicate keys
    if (Array.isArray(value) && !isSimpleArray(value)) {
      const allObjects = value.every(v => typeof v === 'object' && !Array.isArray(v));
      if (allObjects) {
        for (const item of value) {
          const serializedValue = serializeValue(item, 0, opts);
          lines.push(`${formattedKey} = ${serializedValue}`);
        }
        continue;
      }
    }

    const serializedValue = serializeValue(value, 0, opts);
    lines.push(`${formattedKey} = ${serializedValue}`);
  }

  return lines.join(newline!) + newline!;
}

// Export parser types
export type { ASTNode, ASTValue };
