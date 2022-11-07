import axios from 'axios';

class OrganizationDataService {

    getAll(){
        return axios.get("/api/organization");
    }

    get(id) {
        return axios.get(`/api/organization/${id}`);
    }

    create(data) {
        return axios.post("/api/organization/", data)
    }

    update(id, data) {
        return axios.put(`/api/organization/${id}`, data)
    }

    delete(id) {
        return axios.delete(`/api/organization/${id}`)
    }
}

export default new OrganizationDataService();