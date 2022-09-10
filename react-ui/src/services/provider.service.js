import axios from 'axios';

class ProviderDataService {

    getAll(){
        
        return axios.get("/provider");
    }

    get(id) {
        return axios.get(`/provider/${id}`);
    }

    create(data) {
        return axios.post("/provider/", data)
    }

    update(id, data) {
        return axios.put(`/provider/${id}`, data)
    }

    delete(id) {
        return axios.delete(`/provider/${id}`)
    }
}

export default new ProviderDataService();