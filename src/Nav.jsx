import * as React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import PersonPinIcon from '@mui/icons-material/PersonPin';
import HomeIcon from '@mui/icons-material/Home';

export default function Nav() {
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <>
            <h1>Definitely not Financial Advice</h1>
            <div className="navbar">
                <Tabs value={value} onChange={handleChange} aria-label="icon tabs example">
                <Tab icon={<HomeIcon />} aria-label="home" />
                <Tab icon={<PersonPinIcon />} aria-label="person" />
                </Tabs>
            </div>
        </>
    );
}