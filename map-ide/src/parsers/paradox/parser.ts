import { Tokenizer, Token, TokenType } from './tokenizer';

/**
 * AST Node types
 */
export type ASTValue = string | number | boolean | ASTNode | ASTValue[];

export interface ASTNode {
  [key: string]: ASTValue;
}

/**
 * Parser for Paradox Script files
 */
export class Parser {
  private tokens: Token[];
  private pos: number = 0;

  constructor(input: string) {
    const tokenizer = new Tokenizer(input);
    this.tokens = tokenizer.tokenize();
  }

  /**
   * Get current token
   */
  private current(): Token {
    return this.tokens[this.pos] || { type: 'EOF', value: '', line: 0, column: 0 };
  }

  /**
   * Peek ahead
   */
  private peek(offset: number = 1): Token {
    return this.tokens[this.pos + offset] || { type: 'EOF', value: '', line: 0, column: 0 };
  }

  /**
   * Advance to next token
   */
  private advance(): Token {
    return this.tokens[this.pos++];
  }

  /**
   * Expect a specific token type
   */
  private expect(type: TokenType): Token {
    const token = this.current();
    if (token.type !== type) {
      throw new Error(
        `Expected ${type} but got ${token.type} at line ${token.line}, column ${token.column}`
      );
    }
    return this.advance();
  }

  /**
   * Skip comments
   */
  private skipComments(): void {
    while (this.current().type === 'COMMENT') {
      this.advance();
    }
  }

  /**
   * Parse a value (number, string, array, or block)
   */
  private parseValue(): ASTValue {
    this.skipComments();
    const token = this.current();

    // String
    if (token.type === 'STRING') {
      this.advance();
      return token.value as string;
    }

    // Number
    if (token.type === 'NUMBER') {
      this.advance();
      return token.value as number;
    }

    // Identifier (treated as string)
    if (token.type === 'IDENTIFIER') {
      this.advance();
      return token.value as string;
    }

    // Block or array
    if (token.type === 'LBRACE') {
      return this.parseBlockOrArray();
    }

    throw new Error(
      `Unexpected token ${token.type} at line ${token.line}, column ${token.column}`
    );
  }

  /**
   * Parse a block { } or array { 1 2 3 }
   */
  private parseBlockOrArray(): ASTValue {
    this.expect('LBRACE');
    this.skipComments();

    // Check if this is an array (sequence of values) or a block (key=value pairs)
    // Look ahead to determine
    const firstToken = this.current();
    
    if (firstToken.type === 'RBRACE') {
      this.advance();
      return {};
    }

    // Check if next significant token after first is '=' (block) or not (array)
    const secondToken = this.peek();
    
    if (secondToken.type === 'EQUALS') {
      // This is a block with key=value pairs
      return this.parseBlock();
    } else {
      // This is an array
      return this.parseArray();
    }
  }

  /**
   * Parse a block with key=value pairs
   */
  private parseBlock(): ASTNode {
    const node: ASTNode = {};

    while (this.current().type !== 'RBRACE' && this.current().type !== 'EOF') {
      this.skipComments();
      
      if (this.current().type === 'RBRACE') break;

      // Key
      const keyToken = this.current();
      if (keyToken.type !== 'IDENTIFIER' && keyToken.type !== 'STRING' && keyToken.type !== 'NUMBER') {
        throw new Error(
          `Expected key but got ${keyToken.type} at line ${keyToken.line}, column ${keyToken.column}`
        );
      }
      this.advance();
      const key = String(keyToken.value);

      this.skipComments();

      // Check for '=' (key=value) or '{' (key { ... })
      if (this.current().type === 'EQUALS') {
        this.advance();
        this.skipComments();
        
        const value = this.parseValue();
        
        // Handle duplicate keys by converting to array
        if (key in node) {
          const existing = node[key];
          if (Array.isArray(existing) && !this.isPlainArray(existing)) {
            (existing as ASTValue[]).push(value);
          } else {
            node[key] = [existing, value];
          }
        } else {
          node[key] = value;
        }
      } else if (this.current().type === 'LBRACE') {
        // Shorthand: key { ... } without =
        const value = this.parseBlockOrArray();
        
        if (key in node) {
          const existing = node[key];
          if (Array.isArray(existing)) {
            (existing as ASTValue[]).push(value);
          } else {
            node[key] = [existing, value];
          }
        } else {
          node[key] = value;
        }
      } else {
        // Just a standalone identifier/value - treat as flag
        node[key] = true;
      }

      this.skipComments();
    }

    this.expect('RBRACE');
    return node;
  }

  /**
   * Parse an array of values
   */
  private parseArray(): ASTValue[] {
    const values: ASTValue[] = [];

    while (this.current().type !== 'RBRACE' && this.current().type !== 'EOF') {
      this.skipComments();
      
      if (this.current().type === 'RBRACE') break;

      const token = this.current();
      
      if (token.type === 'NUMBER') {
        this.advance();
        values.push(token.value as number);
      } else if (token.type === 'STRING') {
        this.advance();
        values.push(token.value as string);
      } else if (token.type === 'IDENTIFIER') {
        this.advance();
        values.push(token.value as string);
      } else if (token.type === 'LBRACE') {
        values.push(this.parseBlockOrArray());
      } else {
        break;
      }

      this.skipComments();
    }

    this.expect('RBRACE');
    return values;
  }

  /**
   * Check if value is a plain array (numbers/strings only, not objects)
   */
  private isPlainArray(value: ASTValue[]): boolean {
    return value.every(v => typeof v === 'number' || typeof v === 'string');
  }

  /**
   * Parse the entire file
   */
  parse(): ASTNode {
    const root: ASTNode = {};

    while (this.current().type !== 'EOF') {
      this.skipComments();
      
      if (this.current().type === 'EOF') break;

      // Key
      const keyToken = this.current();
      if (keyToken.type !== 'IDENTIFIER' && keyToken.type !== 'STRING' && keyToken.type !== 'NUMBER') {
        this.advance(); // Skip unexpected token
        continue;
      }
      this.advance();
      const key = String(keyToken.value);

      this.skipComments();

      // Expect '=' or '{'
      if (this.current().type === 'EQUALS') {
        this.advance();
        this.skipComments();
        
        const value = this.parseValue();
        
        // Handle duplicate keys
        if (key in root) {
          const existing = root[key];
          if (Array.isArray(existing)) {
            (existing as ASTValue[]).push(value);
          } else {
            root[key] = [existing, value];
          }
        } else {
          root[key] = value;
        }
      } else if (this.current().type === 'LBRACE') {
        const value = this.parseBlockOrArray();
        
        if (key in root) {
          const existing = root[key];
          if (Array.isArray(existing)) {
            (existing as ASTValue[]).push(value);
          } else {
            root[key] = [existing, value];
          }
        } else {
          root[key] = value;
        }
      }

      this.skipComments();
    }

    return root;
  }
}

/**
 * Parse Paradox Script content
 */
export function parseParadoxScript(content: string): ASTNode {
  const parser = new Parser(content);
  return parser.parse();
}
