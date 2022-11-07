import axios from 'axios';

class AuthDataService{

    login(data) {
        return axios.post(`/api/login`, data)
    }

    logout(){
        return axios.get('/api/logout')
    }

}

export default new AuthDataService();