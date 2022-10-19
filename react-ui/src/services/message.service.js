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

    getUserMessages(id){
        return axios.get(`/user/${id}/messages`)
    }

}

export default new MessageDataService();