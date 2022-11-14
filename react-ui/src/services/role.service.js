import axios from 'axios';

class RoleDataService {

    getAll(){
        
        return axios.get("/api/role");
    }

    get(id) {
        return axios.get(`/api/role/${id}`);
    }

    create(data) {
        return axios.post("/api/role", data)
    }

    update(id, data) {
        return axios.put(`/api/role/${id}`, data)
    }

    delete(id) {
        return axios.delete(`/api/role/${id}`)
    }

    getPermissions() {
        return axios.get(`/api/permission`)
    }

    getAvailableRoles() {
        return axios.get(`/api/user/new/roles`)
    }
}

export default new RoleDataService();