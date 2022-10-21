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

    getPending() {
        return axios.get(`/user/new`);
    }

    acceptPending(id) {
        return axios.put(`/user/new/accept/${id}`);
    }

    declinePending(id) {
        return axios.delete(`/user/new/decline/${id}`);
    }


}

export default new UserDataService();