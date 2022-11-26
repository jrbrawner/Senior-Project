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

    getProfile(){
        return axios.get(`/api/user/profile`);
    }

    changePassword(data){
        return axios.post(`/api/user/change-password`, data)
    }

    editProfile(data){
        return axios.post(`/api/user/edit-profile`, data)
    }

    getAvailableLocations(){
        return axios.get(`/api/user/create/locations`)
    }


}

export default new UserDataService();