import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ShowChartIcon from '@mui/icons-material/ShowChart';

export default function StockBar() {
    const stockList = ['NVIDIA', 'Apple', 'Amazon', 'Microsoft'];
    let curr = undefined;

    $(document).ready(function() {
        stockList.forEach((stock, index) => {
            const stockButton = $(`#${stock}_${index}`); 

            stockButton.hover(function() {
                stockButton.css("background-color", "#7b7b87");
            }, function() {
                if (curr && curr == stockButton) {
                    stockButton.css("background-color", "#1515bf");
                    return;
                }
                stockButton.css("background-color", "transparent");
            });

            stockButton.click(function() {
                if (curr) {
                    curr.css("background-color", "transparent");
                    if (curr == stockButton) {
                        curr = undefined;
                        return;
                    }
                }
                curr = stockButton;
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