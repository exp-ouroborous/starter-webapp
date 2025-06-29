#!/usr/bin/env node

/**
 * Frontend development helper script
 * Provides common development tasks for the React frontend
 */

import { execSync, spawn } from 'child_process';
import { existsSync, copyFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function runCommand(command, description, options = {}) {
  log(`🔄 ${description}...`, 'blue');
  try {
    const result = execSync(command, { 
      stdio: options.silent ? 'pipe' : 'inherit',
      encoding: 'utf8',
      ...options 
    });
    log(`✅ ${description} completed successfully`, 'green');
    return result;
  } catch (error) {
    log(`❌ ${description} failed`, 'red');
    if (options.silent && error.stdout) {
      console.log(error.stdout);
    }
    if (options.silent && error.stderr) {
      console.error(error.stderr);
    }
    return null;
  }
}

function setup() {
  log('🔧 Setting up frontend development environment...', 'cyan');
  
  // Install dependencies
  if (!runCommand('npm install', 'Installing dependencies')) {
    return;
  }
  
  // Create .env if it doesn't exist
  if (!existsSync('.env')) {
    if (existsSync('.env.example')) {
      copyFileSync('.env.example', '.env');
      log('✅ Created .env file from .env.example', 'green');
    } else {
      log('⚠️  .env.example not found, please create .env manually', 'yellow');
    }
  }
  
  // Type check
  if (runCommand('npm run type-check', 'Type checking')) {
    log('✅ Frontend development environment setup complete!', 'green');
    log('🚀 Run \'node dev.js server\' to start the development server', 'cyan');
  }
}

function server() {
  log('🚀 Starting development server...', 'cyan');
  log('📍 Server will be available at: http://localhost:5173', 'blue');
  log('🔄 Hot reload is enabled - server will restart on code changes', 'blue');
  log('⏹️  Press Ctrl+C to stop the server', 'blue');
  
  try {
    // Use spawn for interactive process
    const child = spawn('npm', ['run', 'dev'], { 
      stdio: 'inherit',
      shell: true 
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        log('👋 Server stopped', 'yellow');
      } else {
        log(`❌ Server exited with code ${code}`, 'red');
      }
    });
    
  } catch (error) {
    log(`❌ Server failed to start: ${error.message}`, 'red');
  }
}

function build() {
  log('🏗️  Building for production...', 'cyan');
  
  // Clean previous build
  runCommand('npm run clean', 'Cleaning previous build');
  
  // Build
  if (runCommand('npm run build:production', 'Building application')) {
    log('✅ Build completed successfully!', 'green');
    log('📦 Build files are in the dist/ directory', 'blue');
    log('🔍 Run \'node dev.js preview\' to preview the build', 'cyan');
  }
}

function preview() {
  log('👀 Starting preview server for production build...', 'cyan');
  
  if (!existsSync('dist')) {
    log('❌ No build found. Run \'node dev.js build\' first', 'red');
    return;
  }
  
  log('📍 Preview server will be available at: http://localhost:5173', 'blue');
  log('⏹️  Press Ctrl+C to stop the server', 'blue');
  
  try {
    const child = spawn('npm', ['run', 'preview'], { 
      stdio: 'inherit',
      shell: true 
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        log('👋 Preview server stopped', 'yellow');
      } else {
        log(`❌ Preview server exited with code ${code}`, 'red');
      }
    });
    
  } catch (error) {
    log(`❌ Preview server failed to start: ${error.message}`, 'red');
  }
}

function test() {
  log('🧪 Running tests...', 'cyan');
  runCommand('npm run test', 'Running tests');
}

function lint() {
  log('🔍 Running linting checks...', 'cyan');
  const lintResult = runCommand('npm run lint', 'ESLint check', { silent: true });
  const formatResult = runCommand('npm run format:check', 'Prettier format check', { silent: true });
  
  if (!lintResult || !formatResult) {
    log('💡 Run \'node dev.js fix\' to automatically fix formatting issues', 'yellow');
  }
}

function fix() {
  log('🎨 Fixing code formatting and linting issues...', 'cyan');
  runCommand('npm run lint:fix', 'Fixing ESLint issues');
  runCommand('npm run format', 'Formatting code with Prettier');
}

function clean() {
  log('🧹 Cleaning up...', 'cyan');
  runCommand('npm run clean', 'Cleaning build files and cache');
}

function analyze() {
  log('📊 Analyzing bundle size...', 'cyan');
  runCommand('npm run analyze', 'Analyzing bundle');
}

function deploy(env = 'production') {
  log(`🚀 Deploying to ${env}...`, 'cyan');
  
  const deployCommand = env === 'development' ? 'npm run deploy:dev' :
                       env === 'preview' ? 'npm run deploy:preview' :
                       'npm run deploy';
  
  if (runCommand(deployCommand, `Deploying to ${env}`)) {
    log(`✅ Deployment to ${env} completed!`, 'green');
  }
}

function wrangler(command) {
  log(`🔧 Running Wrangler command: ${command}...`, 'cyan');
  
  const wranglerCommands = {
    'login': 'npm run wrangler:login',
    'whoami': 'npm run wrangler:whoami'
  };
  
  const cmd = wranglerCommands[command];
  if (cmd) {
    runCommand(cmd, `Wrangler ${command}`);
  } else {
    log(`❌ Unknown Wrangler command: ${command}`, 'red');
    log('Available commands: login, whoami', 'yellow');
  }
}

function showHelp() {
  console.log(`
🛠️  Frontend Development Helper

Available commands:
  setup     - Set up the development environment
  server    - Start the development server with hot reload
  build     - Build for production
  preview   - Preview production build locally
  test      - Run tests
  lint      - Run linting checks
  fix       - Fix code formatting and linting issues
  clean     - Clean up build files and cache
  analyze   - Analyze bundle size
  deploy [env] - Deploy to Cloudflare (env: dev, preview, production)
  wrangler <cmd> - Run Wrangler commands (login, whoami)
  help      - Show this help message

Examples:
  node dev.js setup
  node dev.js server
  node dev.js build
  node dev.js deploy dev
  node dev.js wrangler login
`);
}

// Main command handler
function main() {
  const args = process.argv.slice(2);
  const command = args[0]?.toLowerCase();
  
  switch (command) {
    case 'setup':
      setup();
      break;
    case 'server':
    case 'dev':
      server();
      break;
    case 'build':
      build();
      break;
    case 'preview':
      preview();
      break;
    case 'test':
      test();
      break;
    case 'lint':
      lint();
      break;
    case 'fix':
      fix();
      break;
    case 'clean':
      clean();
      break;
    case 'analyze':
      analyze();
      break;
    case 'deploy':
      deploy(args[1] || 'production');
      break;
    case 'wrangler':
      wrangler(args[1]);
      break;
    case 'help':
    case undefined:
      showHelp();
      break;
    default:
      log(`❌ Unknown command: ${command}`, 'red');
      showHelp();
  }
}

main();