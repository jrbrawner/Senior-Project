import Cookies from 'js-cookie';
import React from 'react';
import AuthDataService from '../services/auth.service';

export default function Logout(){

    const [status, setStatus] = React.useState(null)

    React.useEffect(() => {
        AuthDataService.logout().then((response) =>
        {
            if (response.status === 200){
                setStatus("You logged out.")
                Cookies.remove('name');
                Cookies.remove('roles');
                window.location.href = '/';
            }
            else{
                setStatus("You didnt log out?")
            }
        }
    )});

    return (
        <div>
            <p>{status}</p>
        </div>
    )
}