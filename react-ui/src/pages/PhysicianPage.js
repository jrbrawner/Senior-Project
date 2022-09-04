import { useParams } from 'react-router-dom';
import Body from '../components/Body';

export default function UserPage(){
    const { id } = useParams();


return(
    <Body sidebar>
        <h1>{id}</h1>
        <p>TODO</p>
    </Body>
);

}