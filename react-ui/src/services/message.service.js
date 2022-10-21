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

    sendMessage(id, data){
        return axios.post(`/message/user/${id}`, data)
    }

}

export default new MessageDataService();