import axios from 'axios';

class OrganizationDataService {

    getAll(){
        return axios.get("/organization");
    }

    get(id) {
        return axios.get(`/organization/${id}`);
    }

    create(data) {
        return axios.post("/organization/", data)
    }

    update(id, data) {
        return axios.put(`/organization/${id}`, data)
    }

    delete(id) {
        return axios.delete(`/organization/${id}`)
    }
}

export default new OrganizationDataService();