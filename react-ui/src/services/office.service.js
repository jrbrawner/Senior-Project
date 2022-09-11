import axios from 'axios';

class OfficeDataService {

    getAll(){
        
        return axios.get("/office");
    }

    get(id) {
        return axios.get(`/office/${id}`);
    }

    create(data) {
        return axios.post("/office/", data)
    }

    update(id, data) {
        return axios.put(`/office/${id}`, data)
    }

    delete(id) {
        return axios.delete(`/office/${id}`)
    }
}

export default new OfficeDataService();