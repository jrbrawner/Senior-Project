import axios from 'axios';

class LocationDataService {

    getAll(){
        
        return axios.get("/api/location");
    }

    get(id) {
        return axios.get(`/api/location/${id}`);
    }

    create(data) {
        return axios.post("/api/location", data)
    }

    update(id, data) {
        return axios.put(`/api/location/${id}`, data)
    }

    delete(id) {
        return axios.delete(`/api/location/${id}`)
    }
}

export default new LocationDataService();