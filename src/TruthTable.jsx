import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { blue } from '@mui/material/colors';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ShowChartIcon from '@mui/icons-material/ShowChart';


export default function TruthTable(truthArg) {
    const [currentDisplay, updateDisplay] = React.useState("main");
    const stockList = ['NVIDIA', 'Apple', 'Amazon', 'Microsoft'];
    const [hover, updateHover] = React.useState("");

    // let truthArray = truthArg["truths"]["truths"];
    let date = new Date();
    const truthArray = [
        {
            "created_at" : date.toJSON(),
            "text" : "sample text",
        },
        {
            "created_at" : date.toJSON(),
            "text" : "sample text 2",
        },
        {
            "created_at" : date.toJSON(),
            "text" : "sample text 3 with lots of shit im just testing the styling and what not of this thannnggggggg i gotta keep writing shit in order to mfing fill up the damn fucking shit ass space hijo de tu chingada madre este proyecto es la verga neta weyyyy",
        },
        {
            "created_at" : date.toJSON(),
            "text" : "sample text 4",
        },
        {
            "created_at" : date.toJSON(),
            "text" : "sample text 5",
        }
    ]

    const [truths, updateTruths] = React.useState(truthArray);

    const theme = createTheme({
        palette: {
            secondary: blue,
        },
    });

    return (
        <>
        <div className="sidebar">
            <List>
                {stockList.map((stock, index) => (
                    <ListItem onClick={() => updateDisplay((currentDisplay != stock) ? stock : "main")} id={`${stock}`} 
                            onMouseOver={() => updateHover(stock)}
                            onMouseLeave={() => updateHover("")}
                            key={index} disablePadding
                            style={{
                                    background: (hover == stock) ? '#7b7b87' :
                                    (currentDisplay == stock) ? '#1515bf' : 'transparent'
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
        <div id="main" style={{display: (currentDisplay == "main") ? '' : 'none'}}>
            <h1>Trump's Truths</h1>
            <div className="truth">
                <ThemeProvider theme={theme}>
                {truths.map((truth, index) => (
                    <Card key={index} className="cards" sx={{ minWidth: 275 }}>
                        <CardContent>
                            <Typography gutterBottom sx={{ fontSize: 14 }}>
                            {Date(truth["created_at"])}
                            </Typography>
                            <Typography variant="body2">
                                {truth["text"]}
                            </Typography>
                        </CardContent>
                        <CardActions>
                            <Button color="secondary" size="small">Learn More</Button>
                        </CardActions>
                    </Card>
                ))}
                </ThemeProvider>
            </div>
        </div>
        <div id="stock" style={{display: (currentDisplay == "main") ? 'none' : ''}}>
            <h1>{currentDisplay}</h1>
            <div className="truth">
            </div>
        </div>
        </>
    );
}