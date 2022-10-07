import axios from 'axios';

class AuthDataService{

    login(data) {
        return axios.post(`/login`, data)
    }

    logout(){
        return axios.get('/logout')
    }

}

export default new AuthDataService();