import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { blue } from '@mui/material/colors';

export default function TruthTable(props) {
    let truthArray = props.truths;
    // let date = new Date();
    // const truthArray = [
    //     {
    //         "created_at" : date.toJSON(),
    //         "text" : "sample text",
    //     },
    //     {
    //         "created_at" : date.toJSON(),
    //         "text" : "sample text 2",
    //     },
    //     {
    //         "created_at" : date.toJSON(),
    //         "text" : "sample text 3 with lots of shit im just testing the styling and what not of this thannnggggggg i gotta keep writing shit in order to mfing fill up the damn fucking shit ass space hijo de tu chingada madre este proyecto es la verga neta weyyyy",
    //     },
    //     {
    //         "created_at" : date.toJSON(),
    //         "text" : "sample text 4",
    //     },
    //     {
    //         "created_at" : date.toJSON(),
    //         "text" : "sample text 5",
    //     }
    // ]

    const [truths, updateTruths] = React.useState(truthArray);

    const theme = createTheme({
        palette: {
            secondary: blue,
        },
    });

    return (
        <>
        <div id="main" style={{display: (props.menu == "home" && props.currentDisplay == "main") ? '' : 'none'}}>
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
        </>
    );
}