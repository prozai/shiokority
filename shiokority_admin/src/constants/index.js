// API Routes
export const ADMIN_PREFIX = '/admin';

// Other constants can be added here
export const API_ENDPOINTS = {
    LOGIN: `${ADMIN_PREFIX}/auth/login`,
    LOGOUT: `${ADMIN_PREFIX}/auth/logout`,
    IS_LOGGED_IN: `${ADMIN_PREFIX}/auth/isLoggedIn`,
    VERIFY_2FA: `${ADMIN_PREFIX}/2fa/verify`,
    GET_QR_CODE: `${ADMIN_PREFIX}/getQRcode`,
    GET_SECRET_KEY: `${ADMIN_PREFIX}/getSecretKey`
};

// Add any other constants you might need