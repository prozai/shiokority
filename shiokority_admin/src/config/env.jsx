const env = {
    development: {
        API_URL: 'http://localhost:5001'
    },
    production: {
        // Production EC2 URL
        API_URL: 'https://api.shiokority.online:5001' 
    }
};

const getEnvironment = () => {
    return process.env.NODE_ENV || 'development';
};

const config = env[getEnvironment()];

export default config;