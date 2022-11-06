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

    loadPicture(photoUrl){
        return axios.get(`/message/load-photo/${photoUrl}`)
    }

    sendAnnouncement(id, data){
        return axios.post(`/message/announcement/${id}`, data)
    }


}

export default new MessageDataService();