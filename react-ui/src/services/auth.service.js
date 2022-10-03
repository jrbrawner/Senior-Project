import axios from 'axios';

class AuthDataService{

    login(data) {
        return axios.post(`/login`, data)
    }
}

export default new AuthDataService();