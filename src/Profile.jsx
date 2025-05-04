import * as React from 'react';
import Loading from './Loading';

export default function Profile(props) {

    const [loaded, updateLoad] = React.useState(false);

    React.useEffect(() => {
        if (props.menu == "profile") {
            
        } else if (props.menu == "home") {

        }
    }, [props.menu])

    return (
        <div className="profile" style={{display: (props.menu == "profile") ? '' : 'none'}}>
            <h1>Edit your Profile</h1>
        </div>
    );
}