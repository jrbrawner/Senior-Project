import axios from 'axios';

class LocationDataService {

    getAll(){
        
        return axios.get("/location");
    }

    get(id) {
        return axios.get(`/location/${id}`);
    }

    create(data) {
        return axios.post("/location/", data)
    }

    update(id, data) {
        return axios.put(`/location/${id}`, data)
    }

    delete(id) {
        return axios.delete(`/location/${id}`)
    }
}

export default new LocationDataService();