/**
 * Token types for Paradox Script
 */
export type TokenType =
  | 'IDENTIFIER'
  | 'STRING'
  | 'NUMBER'
  | 'EQUALS'
  | 'LBRACE'
  | 'RBRACE'
  | 'COMMENT'
  | 'EOF';

export interface Token {
  type: TokenType;
  value: string | number;
  line: number;
  column: number;
}

/**
 * Tokenizer for Paradox Script files
 */
export class Tokenizer {
  private input: string;
  private pos: number = 0;
  private line: number = 1;
  private column: number = 1;

  constructor(input: string) {
    // Remove BOM if present
    this.input = input.replace(/^\uFEFF/, '');
  }

  /**
   * Get current character
   */
  private current(): string {
    return this.input[this.pos] || '\0';
  }

  /**
   * Peek next character
   */
  private peek(): string {
    return this.input[this.pos + 1] || '\0';
  }

  /**
   * Advance to next character
   */
  private advance(): string {
    const ch = this.current();
    this.pos++;
    if (ch === '\n') {
      this.line++;
      this.column = 1;
    } else {
      this.column++;
    }
    return ch;
  }

  /**
   * Skip whitespace
   */
  private skipWhitespace(): void {
    while (this.pos < this.input.length) {
      const ch = this.current();
      if (ch === ' ' || ch === '\t' || ch === '\r' || ch === '\n') {
        this.advance();
      } else {
        break;
      }
    }
  }

  /**
   * Read a string literal
   */
  private readString(): Token {
    const startLine = this.line;
    const startCol = this.column;
    this.advance(); // Skip opening quote
    
    let value = '';
    while (this.pos < this.input.length && this.current() !== '"') {
      if (this.current() === '\\' && this.peek() === '"') {
        this.advance();
        value += '"';
        this.advance();
      } else {
        value += this.advance();
      }
    }
    this.advance(); // Skip closing quote

    return { type: 'STRING', value, line: startLine, column: startCol };
  }

  /**
   * Read a number (integer or float)
   */
  private readNumber(): Token {
    const startLine = this.line;
    const startCol = this.column;
    let value = '';
    let hasDecimal = false;

    // Handle negative numbers
    if (this.current() === '-') {
      value += this.advance();
    }

    while (this.pos < this.input.length) {
      const ch = this.current();
      if (ch >= '0' && ch <= '9') {
        value += this.advance();
      } else if (ch === '.' && !hasDecimal) {
        hasDecimal = true;
        value += this.advance();
      } else {
        break;
      }
    }

    const numValue = hasDecimal ? parseFloat(value) : parseInt(value, 10);
    return { type: 'NUMBER', value: numValue, line: startLine, column: startCol };
  }

  /**
   * Read an identifier
   */
  private readIdentifier(): Token {
    const startLine = this.line;
    const startCol = this.column;
    let value = '';

    while (this.pos < this.input.length) {
      const ch = this.current();
      if (
        (ch >= 'a' && ch <= 'z') ||
        (ch >= 'A' && ch <= 'Z') ||
        (ch >= '0' && ch <= '9') ||
        ch === '_' ||
        ch === '-' ||
        ch === ':' ||
        ch === '.' ||
        ch === "'" ||
        ch === '@'
      ) {
        value += this.advance();
      } else {
        break;
      }
    }

    return { type: 'IDENTIFIER', value, line: startLine, column: startCol };
  }

  /**
   * Read a comment
   */
  private readComment(): Token {
    const startLine = this.line;
    const startCol = this.column;
    let value = '';
    
    this.advance(); // Skip #
    while (this.pos < this.input.length && this.current() !== '\n') {
      value += this.advance();
    }

    return { type: 'COMMENT', value: value.trim(), line: startLine, column: startCol };
  }

  /**
   * Get next token
   */
  nextToken(): Token {
    this.skipWhitespace();

    if (this.pos >= this.input.length) {
      return { type: 'EOF', value: '', line: this.line, column: this.column };
    }

    const startLine = this.line;
    const startCol = this.column;
    const ch = this.current();

    // String
    if (ch === '"') {
      return this.readString();
    }

    // Comment
    if (ch === '#') {
      return this.readComment();
    }

    // Equals
    if (ch === '=') {
      this.advance();
      return { type: 'EQUALS', value: '=', line: startLine, column: startCol };
    }

    // Left brace
    if (ch === '{') {
      this.advance();
      return { type: 'LBRACE', value: '{', line: startLine, column: startCol };
    }

    // Right brace
    if (ch === '}') {
      this.advance();
      return { type: 'RBRACE', value: '}', line: startLine, column: startCol };
    }

    // Number (including negative)
    if ((ch >= '0' && ch <= '9') || (ch === '-' && this.peek() >= '0' && this.peek() <= '9')) {
      return this.readNumber();
    }

    // Identifier
    if (
      (ch >= 'a' && ch <= 'z') ||
      (ch >= 'A' && ch <= 'Z') ||
      ch === '_' ||
      ch === '@'
    ) {
      return this.readIdentifier();
    }

    // Unknown character - skip it
    this.advance();
    return this.nextToken();
  }

  /**
   * Tokenize entire input
   */
  tokenize(): Token[] {
    const tokens: Token[] = [];
    let token: Token;
    
    while ((token = this.nextToken()).type !== 'EOF') {
      tokens.push(token);
    }
    tokens.push(token); // Add EOF
    
    return tokens;
  }
}
