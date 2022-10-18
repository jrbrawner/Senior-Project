import axios from 'axios';

class MessageDataService {

    getAll(){
        return axios.get("/message");
    }

    getLocations(){
        return axios.get("/user/locations")
    }

    getUsers(id){
        return axios.get(`/location/${id}/users`)
    }

}

export default new MessageDataService();