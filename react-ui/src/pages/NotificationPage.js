import Body from '../components/Body';
import Notifications from '../components/NotificationComponents/Notifications';

export default function NotificationPage(){
    return(
        <Body>
            <Notifications itemsPerPage={10}/>
            <div id="container"></div>
        </Body>
    );
}