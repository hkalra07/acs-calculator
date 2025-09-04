module.exports = {
  apps: [{
    name: 'acs-calculator',
    script: 'acs_server.py',
    interpreter: 'python3',
    cwd: '/home/coder',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
