// Entrypoint for make.fun competition 'news-summary-01' (Node 22, standard library only).
import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const targetFile = join(targetDir, 'entry.txt');

// Ensure destination directory exists and copy summary
mkdirSync(dirname(targetFile), { recursive: true });
const sourceUrl = new URL('./summary.txt', import.meta.url);
copyFileSync(sourceUrl, targetFile);

// Validate written entrypoint format and character constraints
const writtenContent = readFileSync(targetFile, 'utf8');
const charCount = [...writtenContent].length;
if (charCount < 1 || charCount > 2000) {
  throw new Error(`Invalid entry character length: ${charCount} (must be 1-2000)`);
}

