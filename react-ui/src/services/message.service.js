import axios from 'axios';

class MessageDataService {

    getAll(){
        return axios.get("/message");
    }

}

export default new MessageDataService();