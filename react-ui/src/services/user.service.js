import axios from 'axios';

class UserDataService {

    getAll(){
        return axios.get('/user');
    }

    get(id) {
        return axios.get(`/user/${id}`);
    }

    update(id, data) {
        return axios.put(`/user/${id}`, data);
    }

    delete(id) {
        return axios.delete(`/user/${id}`);
    }

    create(data) {
        return axios.post(`/user`, data);
    }


}

export default new UserDataService();