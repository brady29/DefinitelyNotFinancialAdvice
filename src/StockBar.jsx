import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ShowChartIcon from '@mui/icons-material/ShowChart';

export default function StockBar() {

    const stockList = ['NVIDIA', 'Apple', 'Amazon', 'Microsoft'];
    const states = Array(stockList.length);
    let curr = undefined;

    $(document).ready(function() {
        stockList.forEach((stock, index) => {
            states[index] = false;
            const stockButton = $(`#${stock}_${index}`); 

            stockButton.hover(function() {
                stockButton.css("background-color", "#7b7b87");
            }, function() {
                stockButton.css("background-color", "transparent");
            });
        })
    });

    return (
        <div className="sidebar">
            <List>
                {stockList.map((stock, index) => (
                    <ListItem id={`${stock}_${index}`} key={stock} disablePadding>
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