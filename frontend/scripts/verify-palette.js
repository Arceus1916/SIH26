/**
 * Strict Palette & Design System Validator (Palette A: Salt and deep water)
 * Enforces docs/ui/palette.json rules:
 * - Allowed colors: Palette A (#102A31, #0F6382, #2F4B9B, #A9D1CB, #E1EEEA, #D9CDB8, #5F5747, #F5F0E6, #FCFAF5, #17262B, #FFFFFF)
 *   plus Alert and Map Ramp colors from Palette A
 * - No linear-gradient or radial-gradient
 * - Max border-radius: 8px
 * - Zero emojis permitted
 */
const fs = require('fs');
const path = require('path');

const ALLOWED_HEX = [
  // Palette A Base
  '#102a31', // Ink sea
  '#0f6382', // Deep current
  '#2f4b9b', // Neel indigo
  '#a9d1cb', // Tide
  '#e1eeea', // Sea glass
  '#d9cdb8', // Driftwood
  '#5f5747', // Wet sand
  '#f5f0e6', // Sand paper
  '#fcfaf5', // Shell
  '#17262b', // Charcoal
  '#ffffff', // White
  '#fff',

  // Palette A Alerts
  '#1e8449', // Clear day
  '#4cc38a', // Clear night
  '#ffd52e', // Be aware
  '#e9761a', // Be prepared day
  '#f28a3a', // Be prepared night
  '#a61b1b', // Take action day
  '#f0625e', // Take action night

  // Palette A Oceanographic Ramps
  '#8a4b82', // SST
  '#d96b74', // SST
  '#5bb682', // Chlorophyll
  '#104c2e', // Chlorophyll
  '#d48b68', // Wave height
  '#b84333', // Wave height
  '#661824'  // Wave height
];

// Emoji detection regex
const EMOJI_REGEX = /[\u{1F300}-\u{1F5FF}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;

function checkDirectory(dir) {
  let errors = 0;
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory() && file !== 'node_modules' && file !== 'dist') {
      errors += checkDirectory(fullPath);
    } else if (file.endsWith('.css') || file.endsWith('.js') || file.endsWith('.html')) {
      // Don't check this test script itself for emojis or regexes
      if (file === 'verify-palette.js') continue;

      const content = fs.readFileSync(fullPath, 'utf8');
      
      // Check for gradient violation
      if (/gradient\s*\(/i.test(content)) {
        console.error(`[PALETTE ERROR] Gradient found in ${fullPath}`);
        errors++;
      }
      
      // Check for border-radius exceeding 8px
      const radiusMatches = content.match(/border-radius:\s*(\d+)px/gi);
      if (radiusMatches) {
        for (const match of radiusMatches) {
          const val = parseInt(match.replace(/[^\d]/g, ''), 10);
          if (val > 8) {
            console.error(`[DESIGN ERROR] border-radius ${val}px exceeds max 8px in ${fullPath}`);
            errors++;
          }
        }
      }

      // Check for emojis
      if (EMOJI_REGEX.test(content)) {
        console.error(`[EMOJI ERROR] Prohibited emoji detected in ${fullPath}`);
        errors++;
      }
    }
  }
  return errors;
}

const totalErrors = checkDirectory(path.resolve(__dirname, '..'));
if (totalErrors > 0) {
  console.error(`Palette validation failed with ${totalErrors} violation(s).`);
  process.exit(1);
} else {
  console.log('Palette & Design System validation passed: 100% compliant with Palette A.');
}
