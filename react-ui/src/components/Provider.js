import Stack from 'react-bootstrap/Stack';
import Image from 'react-bootstrap/Image';
import { Link } from 'react-router-dom';

export default function Provider({ provider }) {
    return (
    <>
        
            <div>
                {provider.name}
            </div>
        
    </>
    )
}