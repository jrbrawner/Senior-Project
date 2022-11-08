import axios from 'axios';

class MessageDataService {

    getAll(){
        return axios.get("/api/message");
    }

    getLocations(){
        return axios.get("/api/user/locations")
    }

    getUsers(id){
        return axios.get(`/api/location/${id}/users`)
    }

    getUserMessages(id){
        return axios.get(`/api/user/${id}/messages`)
    }

    sendMessage(id, locationId, data){
        return axios.post(`/api/message/user/${id}/location/${locationId}`, data)
    }

    loadPicture(photoUrl){
        return axios.get(`/api/message/load-photo/${photoUrl}`)
    }

    sendAnnouncement(id, data){
        return axios.post(`/api/message/announcement/${id}`, data)
    }


}

export default new MessageDataService();