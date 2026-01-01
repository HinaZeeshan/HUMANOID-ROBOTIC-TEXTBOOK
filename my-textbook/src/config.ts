export const getApiBaseUrl = () => {
    if (process.env.NODE_ENV === 'production') {
        return 'https://hinazeeshan-humanoid-textbook.hf.space';
    }
    return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();
