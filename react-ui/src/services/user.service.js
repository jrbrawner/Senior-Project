import axios from 'axios';

class UserDataService {

    getAll(){
        return axios.get('/api/user');
    }

    get(id) {
        return axios.get(`/api/user/${id}`);
    }

    update(id, data) {
        return axios.put(`/api/user/${id}`, data);
    }

    delete(id) {
        return axios.delete(`/api/user/${id}`);
    }

    create(data) {
        return axios.post(`/api/user`, data);
    }

    getPending() {
        return axios.get(`/api/user/new`);
    }

    acceptPending(id) {
        return axios.put(`/api/user/new/accept/${id}`);
    }

    declinePending(id) {
        return axios.delete(`/api/user/new/decline/${id}`);
    }

    updateRoles(id, data){
        return axios.post(`/api/user/roles/${id}`, data);
    }


}

export default new UserDataService();