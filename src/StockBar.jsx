import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ShowChartIcon from '@mui/icons-material/ShowChart';

export default function StockBar(props) {
    const stockList = ['NVIDIA', 'Apple', 'Amazon', 'Microsoft'];
    const [hover, updateHover] = React.useState("");

    return (
        <div className="sidebar" style={{display: (props.menu == "home") ? '' : 'none'}}>
            <List>
                {stockList.map((stock, index) => (
                    <ListItem onClick={() => props.updateDisplay((props.currentDisplay != stock) ? stock : "main")} id={`${stock}`} 
                            onMouseOver={() => updateHover(stock)}
                            onMouseLeave={() => updateHover("")}
                            key={index} disablePadding
                            style={{
                                    background: (hover == stock) ? '#7b7b87' :
                                    (props.currentDisplay == stock) ? '#1515bf' : 'transparent'
                                }}>
                        <ListItemButton>
                        <ListItemIcon>
                            <ShowChartIcon />
                        </ListItemIcon>
                        <ListItemText primary={stock} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
        </div>
    );
}